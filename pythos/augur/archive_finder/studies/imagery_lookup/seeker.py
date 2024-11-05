from augury.models import Dream
from augury.mystics.dreamer import Dreamer
from augury.mystics.seeker import Seeker


class ImageryLookupSeeker(Seeker):

    def seek(self, study):
        dreamer = Dreamer()
        conf = {"archive_finder_pk": study.archive_finder.pk}
        dream = dreamer.execute(study, conf)
        return dream
    
    def poll(self, study):
        dream = Dream.objects.filter(study=study).latest()
        dreamer = Dreamer()
        dream = dreamer.poll(dream)
        return dream.status