from enum import StrEnum
from archive_finder.studies.imagery_lookup.models import ImageryLookupStudy
from archive_finder.studies.imagery_lookup.diviner import ImageryLookupDiviner
from archive_finder.studies.imagery_lookup.seeker import ImageryLookupSeeker


class Scholar:
    
    class StudyNames(StrEnum):
        BASE_STUDY = "base_study"
        IMAGERY_FINDER = "imagery_finder"

    studies = {
        StudyNames.IMAGERY_FINDER: {
            "study": ImageryLookupStudy,
            "seeker": ImageryLookupSeeker,
            "diviner":  ImageryLookupDiviner,
        },
    }