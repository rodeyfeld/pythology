from typing import List
from ninja import Router

from augury.mystics.dreamer import Dreamer
from augury.models import Dream
from augury.schema import DreamCreateSchema, DreamDetailsResponseSchema, DreamRequestSchema, DreamStatusResponseSchema

router = Router(tags=["augury"])

@router.get('/dream/details/',  response=List[DreamStatusResponseSchema])
def dream_details(request):

    dreams = Dream.objects.all()
    responses = []
    for dream in dreams:
        study = dream.study
        response = DreamDetailsResponseSchema(
            study_name=study.name,
            study_id=study.id,
            study_status=study.status,
            dream_status=dream.status,
        )
        responses.append(response)
    return responses

@router.get('/dream/details/{dream_id}',  response=DreamStatusResponseSchema)
def dream_details_id(request, dream_id):

    dream = Dream.objects.get(pk=dream_id)
    study = dream.study

    response = DreamDetailsResponseSchema(
        study_name=study.name,
        study_id=study.id,
        study_status=study.status,
        dream_status=dream.status,
    )
    return response

@router.get('/dream/status/{dream_id}',  response=DreamStatusResponseSchema)
def dreamer_execute(request, dream_id):

    dream = Dream.objects.get(id=dream_id)
    study = dream.study
    seeker = study.seeker
    dream = seeker.poll(study)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

@router.post('/divine',  response=DreamStatusResponseSchema)
def diviner_process(request, dream: DreamRequestSchema):

    dream = Dream.objects.get(dream.dream_id)
    study = dream.study
    diviner = study.diviner
    dream = diviner.divine(dream)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response
