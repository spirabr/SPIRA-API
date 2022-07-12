from fastapi import File, Form, UploadFile
from core.model.inference import InferenceCreationForm, InferenceFiles


async def get_inference_form_model(age=Form(), sex=Form(), model_id=Form()):
    return InferenceCreationForm(age=age, sex=sex, model_id=model_id)


async def get_inference_form_files(
    vogal_sustentada: UploadFile = File(),
    parlenda_ritmada: UploadFile = File(),
    frase: UploadFile = File(),
):
    return InferenceFiles(
        vogal_sustentada=vogal_sustentada,
        parlenda_ritmada=parlenda_ritmada,
        frase=frase,
    )
