import json
from archive_finder.studies.imagery_lookup.schema import ImageryLookupResultSchema, ImageryLookupStudyResultDataSchema
from core.models import Sensor
from provider.models import Collection, Provider
from archive_finder.studies.imagery_lookup.models import ImageryLookupResult, ImageryLookupStudy


class ImageryLookupDiviner:

    def divine(self, dream):
        study = dream.study
        self.transform_study_results(study)
        return dream
     
    def interpret(self, study_id):
        study = ImageryLookupStudy.objects.get(pk=study_id)
        archive_finder = study.archive_finder
        results = []
        imagery_lookup_results = ImageryLookupResult.objects.filter(study=study)
        for imagery_lookup_result in imagery_lookup_results:
            geometry = json.loads(imagery_lookup_result.geometry.geojson)
            result = ImageryLookupResultSchema(
                external_id=imagery_lookup_result.external_id,
                collection=imagery_lookup_result.collection.name,
                start_date=imagery_lookup_result.start_date,
                end_date=imagery_lookup_result.end_date,
                sensor=imagery_lookup_result.sensor,
                geometry=geometry,
                thumbnail=imagery_lookup_result.thumbnail,
                metadata=imagery_lookup_result.metadata,
            )
            results.append(result)
        geometry = json.loads(archive_finder.geometry.geojson)
        data = ImageryLookupStudyResultDataSchema(
            archive_finder_id=archive_finder.pk,
            archive_finder_geometry=geometry,
            results=results,
        )
        return data

    def transform_study_results(self, study):
        imagery_lookups = study.imagerylookupitem_set.all()
        for imagery_lookup in imagery_lookups:
            archive_item = imagery_lookup.archive_item
            provider, _ = Provider.objects.get_or_create(
                            name=archive_item.provider
            )
            collection, _ = Collection.objects.get_or_create(
                name=archive_item.collection,
                provider=provider
            )
            sensor, _ = Sensor.objects.get_or_create(
                name=archive_item.sensor
            )
            _ = ImageryLookupResult.objects.create(
                study=study,
                external_id=archive_item.external_id,
                collection=collection,
                start_date=archive_item.start_date,
                end_date=archive_item.end_date,
                sensor=sensor,
                geometry=archive_item.geometry,
                thumbnail=archive_item.thumbnail,
            )

