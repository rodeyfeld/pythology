import json
from typing import List
from geojson_pydantic import Polygon
from ninja import Router
from archive_finder.utils import geojson_to_geosgeom
from core.models import User
from archive_finder.factories import ArchiveFinderFactory
from archive_finder.models import ArchiveFinder, ArchiveResult
from archive_finder.schema import (
    ArchiveFinderCreateRequestSchema,   
    ArchiveFinderCreateResponseSchema,  
    ArchiveFinderSeekerRequestSchema,   
    ArchiveFinderSchema,    
    ArchiveFinderSeekerStatusResponseSchema,    
    ArchiveResultSchema,
)
from archive_finder.seekers.internal.seeker import Seeker

router = Router(tags=["archive search"])

@router.get('/finders', response=List[ArchiveFinderSchema])
def get_all_archive_finders(request):
    queryset = ArchiveFinder.objects.all()
    return list(queryset)

@router.get('/finders/id/{archive_finder_id}', response=ArchiveFinderSchema)
def get_archive_finder_by_id(request, archive_finder_id):
    queryset = ArchiveFinder.objects.get(id=archive_finder_id)
    return queryset

@router.post('/finders/create',  response=ArchiveFinderCreateResponseSchema)
def post_create_finder(request, archive_finder_create_schema: ArchiveFinderCreateRequestSchema):
    user = User.objects.all().first()


    # if is_valid_geometry_type(archive_finder_create_schema.geometry):
    geometry = geojson_to_geosgeom(archive_finder_create_schema.geometry)

    archive_finder = ArchiveFinderFactory.create(
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

@router.post('/finders/execute',  response=ArchiveFinderSeekerStatusResponseSchema)
def post_finder_execute(request, archive_finder_create_schema: ArchiveFinderSeekerRequestSchema):

    archive_finder_id = archive_finder_create_schema.archive_finder_id
    archive_finder = ArchiveFinder.objects.get(id=archive_finder_id)

    seeker = Seeker(archive_finder)
    seeker.seek()
    
    response = ArchiveFinderSeekerStatusResponseSchema(
        status=archive_finder.status
    )
    return response

@router.get('/finders/status/{archive_finder_id}',  response=ArchiveFinderSeekerStatusResponseSchema)
def get_finder_status(request, archive_finder_id):
    archive_finder = ArchiveFinder.objects.get(id=archive_finder_id)

    response = ArchiveFinderSeekerStatusResponseSchema(
        status=archive_finder.status
    )
    return response

@router.get('/results', response=List[ArchiveResultSchema])
def get_all_archive_results(request):
    queryset = ArchiveResult.objects.all()
    return list(queryset)

@router.get('/results/id/result/{archive_result_id}', response=ArchiveResultSchema)
def get_archive_result_by_id(request, archive_result_id):
    queryset = ArchiveResult.objects.get(id=archive_result_id)
    return queryset

@router.get('/results/id/finder/{archive_finder_id}', response=List[ArchiveResultSchema])
def get_archive_results_by_archive_finder_id(request, archive_finder_id):
    queryset = ArchiveResult.objects.filter(archive_finder__id=archive_finder_id)
    return list(queryset)
