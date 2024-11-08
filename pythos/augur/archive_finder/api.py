import json
from typing import List
from ninja import Router
from archive_finder.utils import geojson_to_geosgeom
from archive_finder.studies.scholar import Scholar
from augury.schema import DreamStatusResponseSchema
from core.models import User
from archive_finder.models import ArchiveFinder
from archive_finder.schema import (
    ArchiveFinderCreateRequestSchema,   
    ArchiveFinderCreateResponseSchema,  
    ArchiveFinderSchema,
    StudyExecuteRequestSchema
)

router = Router(tags=["archive search"])

@router.get('/finder', response=List[ArchiveFinderSchema])
def archive_finders(request):
    queryset = ArchiveFinder.objects.all()
    return list(queryset)

@router.get('/finder/id/{archive_finder_id}', response=ArchiveFinderSchema)
def archive_finder_by_id(request, archive_finder_id):
    queryset = ArchiveFinder.objects.get(id=archive_finder_id)
    return queryset

@router.post('/finder/create',  response=ArchiveFinderCreateResponseSchema)
def create_finder(request, archive_finder_create_schema: ArchiveFinderCreateRequestSchema):
    user = User.objects.all().first()
    geometry = geojson_to_geosgeom(archive_finder_create_schema.geometry)

    archive_finder = ArchiveFinder.objects.create(
        name=archive_finder_create_schema.name,
        geometry=geometry.wkt,
        start_date = archive_finder_create_schema.start_date,
        end_date = archive_finder_create_schema.end_date,
    )
    response = ArchiveFinderCreateResponseSchema(
        name=archive_finder.name,
        archive_finder_id=archive_finder.id,
        start_date=archive_finder.start_date,
        end_date=archive_finder.end_date,
        geometry=json.loads(archive_finder.geometry.geojson)
    )
    return response

@router.post('/study/execute',  response=DreamStatusResponseSchema)
def execute_study(request, study_execute_schema: StudyExecuteRequestSchema):

    study_name = study_execute_schema.name

    seeker_class = Scholar.studies[study_name]["seeker"]

    seeker = seeker_class()
    dream = seeker.seek(archive_finder_id=study_execute_schema.archive_finder_id)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

