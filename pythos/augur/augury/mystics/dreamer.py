from enum import StrEnum
import uuid
import requests
from augur.augury.mystics.diviner import Diviner
from augur.augury.mystics.seeker import Seeker
from augury.models import Dream
from requests.auth import HTTPBasicAuth
from archive_finder.studies.imagery_lookup.seeker import ImageryLookupSeeker
from archive_finder.studies.imagery_lookup.diviner import ImageryLookupDiviner
DREAMFLOW_URL = "http://localhost:8080/api/v1"

class Dreamer:

    class StudyDAGName(StrEnum):
        IMAGERY_FINDER = "imagery_finder"

    @property
    def seeker(self) -> Seeker:
        return self.study.DREAM_CHART[self.study.name]["seeker"]()

    @property
    def diviner(self) -> Diviner:
        return self.study.DREAM_CHART[self.study.name]["diviner"]()
    
    @property
    def dag_name(self) -> str:
        return self.DREAM_CHART[self.study.name]["dag_name"]

    DREAM_CHART = {
        StudyDAGName.IMAGERY_FINDER: {
            "seeker": ImageryLookupSeeker,
            "diviner": ImageryLookupDiviner
        }
    }

    def __init__(self, study_name) -> None:
        self.study_name = study_name

    def get_auth(self):    
        auth = HTTPBasicAuth("admin", "uGTgxN78bzBadxNq")
        return auth

    def execute(self, study, conf):
        dream = Dream.objects.create(study=study)
        dreamflow_dag_id = study.DREAM_CHART[study.name]["dag_name"]
        response = self.execute_study(dag_id=dreamflow_dag_id, conf=conf)
        if response.status_code != 200:
            dream.status = Dream.Status.ANOMALOUS
            dream.save()
            return dream
        dream.status = Dream.Status.INITIALIZED
        dream.save()
        return dream

    def poll(self, dream: Dream):
        dreamflow_dag_details_response = self.get_dag_details()
        dreamflow_state = dreamflow_dag_details_response.json()["state"]
        if dreamflow_state:
            status = Dream.DREAMFLOW_STATUS_MAP[dreamflow_state]
            dream = status
            dream.save()
            return dream
        dream = Dream.Status.ANOMALOUS
        dream.save()
        return dream
    
    def get_dag_details(self, dag_id, dag_run_id):
        endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}"
        response = requests.get(url=f"{DREAMFLOW_URL}/{endpoint}", auth=self.get_auth())
        return response

    def execute_dag(self, dag_id, payload=dict):        
        endpoint = f"dags/{dag_id}/dagRuns"
        response = requests.post(url=f"{DREAMFLOW_URL}/{endpoint}", auth=self.get_auth(), json=payload)
        return response
    
    def execute_study(self, dag_id, conf=dict):
        dag_run_id = uuid.uuid4().hex
        payload = {"conf": conf, "dag_run_id": dag_run_id}
        response = self.execute_dag(dag_id=dag_id, payload=payload)
        return response