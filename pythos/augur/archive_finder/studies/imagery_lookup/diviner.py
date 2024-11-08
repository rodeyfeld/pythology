from core.models import Sensor
from provider.models import Collection, Provider
from archive_finder.studies.imagery_lookup.models import ImageryLookupResult, ImageryLookupStudy


class ImageryLookupDiviner():

    def divine(self, dream):
        study = dream.study
        self.transform_study_results(study)
        return dream

    def transform_study_results(self, study):
        imagery_lookups = study.imagerylookupitem_set.all()
        print(imagery_lookups)
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
                imagery_lookup_study=study,
                external_id=archive_item.external_id,
                collection=collection,
                start_date=archive_item.start_date,
                end_date=archive_item.end_date,
                sensor=sensor,
                geometry=archive_item.geometry,
                thumbnail=archive_item.thumbnail,
            )

