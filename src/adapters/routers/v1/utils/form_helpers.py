from fastapi import File, Form, UploadFile
from core.model.inference import InferenceCreationForm, InferenceFiles, UploadAudio


async def get_inference_form_model(age=Form(-1), sex=Form(""), model_id=Form("")):
    return InferenceCreationForm(age=age, sex=sex, model_id=model_id)


async def get_inference_form_files(
    vogal_sustentada: UploadFile = File(None),
    parlenda_ritmada: UploadFile = File(None),
    frase: UploadFile = File(None),
):
    return InferenceFiles(
        vogal_sustentada=UploadAudio(
            content=vogal_sustentada.file.read(), filename=vogal_sustentada.filename
        ),
        parlenda_ritmada=UploadAudio(
            content=parlenda_ritmada.file.read(), filename=parlenda_ritmada.filename
        ),
        frase=UploadAudio(content=frase.file.read(), filename=frase.filename),
    )
