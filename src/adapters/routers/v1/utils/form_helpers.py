from calendar import c
from fastapi import File, Form, UploadFile
from core.model.inference import InferenceCreationForm, InferenceFiles, UploadAudio


async def get_inference_form_model(
    age=Form(0),
    gender=Form(""),
    model_id=Form(""),
    rgh=Form(""),
    covid_status=Form(""),
    mask_type=Form(None),
    local=Form(""),
    cid=Form(None),
    bpm=Form(None),
    respiratory_frequency=Form(None),
    respiratory_insufficiency_status=Form(None),
    location=Form(None),
    last_positive_diagnose_date=Form(None),
    hospitalized=Form(None),
    hospitalization_start=Form(None),
    hospitalization_end=Form(None),
    spo2=Form(None),
):
    return InferenceCreationForm(
        age=int(age),
        gender=gender,
        model_id=model_id,
        rgh=rgh,
        covid_status=covid_status,
        mask_type=mask_type,
        local=local,
        cid=cid,
        bpm=bpm,
        respiratory_frequency=respiratory_frequency,
        respiratory_insufficiency_status=respiratory_insufficiency_status,
        location=location,
        last_positive_diagnose_date=last_positive_diagnose_date,
        hospitalized=hospitalized,
        hospitalization_start=hospitalization_start,
        hospitalization_end=hospitalization_end,
        spo2=spo2,
    )


async def get_inference_form_files(
    aceite: UploadFile = File(None),
    sustentada: UploadFile = File(None),
    parlenda: UploadFile = File(None),
    frase: UploadFile = File(None),
):
    return InferenceFiles(
        aceite=UploadAudio(content=aceite.file.read(), filename=aceite.filename),
        sustentada=UploadAudio(
            content=sustentada.file.read(), filename=sustentada.filename
        ),
        parlenda=UploadAudio(content=parlenda.file.read(), filename=parlenda.filename),
        frase=UploadAudio(content=frase.file.read(), filename=frase.filename),
    )
