import json
from typing import List
from ninja import Router
from archive_finder.utils import geojson_to_geosgeom
from core.models import User
from archive_finder.models import ArchiveFinder
from archive_finder.schema import (
    ArchiveFinderCreateRequestSchema,   
    ArchiveFinderCreateResponseSchema,  
    ArchiveFinderSchema,    
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
