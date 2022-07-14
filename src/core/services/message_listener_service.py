from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort
from core.ports.simple_storage_port import SimpleStoragePort
from core.services.result_service import update_inference_result
from core.model.constants import Status


async def subscribe_to_channel(
    message_service_port: MessageServicePort,
    central_channel: str,
):
    await message_service_port.subscribe(central_channel)


async def listen_for_messages_and_update(
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
    database_port: DatabasePort,
    central_channel: str,
):
    try:
        result_update = await message_service_port.wait_for_message(central_channel)
        database_port.update_result(result_update)
        database_port.update_inference_status(
            result_update.inference_id, Status.completed_status
        )
        simple_storage_port.remove_inference_directory(result_update.inference_id)
    except Exception as e:
        print(e, flush=True)
