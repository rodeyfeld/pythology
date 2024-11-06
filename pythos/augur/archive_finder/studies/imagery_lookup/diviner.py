from augury.mystics.diviner import Diviner
from core.models import Sensor
from provider.models import Collection, Provider
from archive_finder.studies.imagery_lookup.models import ImageryLookupResult, ImageryLookupStudy


class ImageryLookupDiviner(Diviner):

    def divine(self):
        self.transform_study_results()

    def transform_study_results(self):
        imagery_lookups = ImageryLookupStudy.objects.filter(archive_finder=self.study.archive_finder)
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
                imagery_lookup_study=self,
                external_id=archive_item.external_id,
                collection=collection,
                start_date=archive_item.start_date,
                end_date=archive_item.end_date,
                sensor=sensor,
                geometry=archive_item.geometry,
                thumbnail=archive_item.thumbnail,
            )