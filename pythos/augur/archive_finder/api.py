import json
from typing import List
from ninja import Router
from archive_finder.utils import geojson_to_geosgeom
from augury.schema import DreamStatusResponseSchema
from core.models import User
from archive_finder.models import ArchiveFinder, ArchiveStudy
from archive_finder.schema import (
    ArchiveFinderCreateRequestSchema,   
    ArchiveFinderCreateResponseSchema,  
    ArchiveFinderSchema,    
    ArchiveStudyResponseSchema
)

router = Router(tags=["archive search"])

@router.get('/finders', response=List[ArchiveFinderSchema])
def archive_finders(request):
    queryset = ArchiveFinder.objects.all()
    return list(queryset)

@router.get('/finders/id/{archive_finder_id}', response=ArchiveFinderSchema)
def archive_finder_by_id(request, archive_finder_id):
    queryset = ArchiveFinder.objects.get(id=archive_finder_id)
    return queryset

@router.post('/finders/create',  response=ArchiveFinderCreateResponseSchema)
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

@router.post('/finders/execute',  response=DreamStatusResponseSchema)
def finder_execute(request,  archive_study: ArchiveStudyResponseSchema):

    archive_finder_id = archive_study.archive_finder_id
    archive_finder = ArchiveFinder.objects.get(id=archive_finder_id)

    name = archive_study.name
    study = ArchiveStudy.objects.create(archive_finder=archive_finder, name=name)
    seeker = study.seeker
    dream = seeker.seek(study)
    
    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

@router.get('/finders/study/{archive_finder_id}',  response=DreamStatusResponseSchema)
def finder_status(request, archive_finder_id):
    archive_finder = ArchiveFinder.objects.get(id=archive_finder_id)
    
    study = ArchiveStudy.objects.filter(archive_finder=archive_finder).latest()
    seeker = study.seeker
    dream = seeker.poll(study)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

@router.get('/finders/study/{archive_finder_id}/{name}',  response=DreamStatusResponseSchema)
def finder_study_status(request, archive_finder_id, name):
    archive_finder = ArchiveFinder.objects.get(id=archive_finder_id)
    
    study = ArchiveStudy.objects.filter(archive_finder=archive_finder, name=name).latest()
    seeker = study.seeker
    dream = seeker.poll(study)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

@router.post('/finders/study/process',  response=DreamStatusResponseSchema)
def finder_study_process(request, archive_study: ArchiveStudyResponseSchema):
    archive_finder_id = archive_study.archive_finder_id
    archive_finder = ArchiveFinder.objects.get(id=archive_finder_id)

    name = archive_study.name
    study = ArchiveStudy.objects.filter(archive_finder=archive_finder, name=name).latest()
    diviner = study.diviner
    dream = diviner.divine(study)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response