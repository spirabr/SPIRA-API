from core.model.exception import LogicException
from core.model.result import ResultUpdate
from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort
from core.ports.simple_storage_port import SimpleStoragePort
from core.services.result_service import update_inference_result
from core.model.constants import Status


async def subscribe_to_channel(
    message_service_port: MessageServicePort,
    central_channel: str,
):
    try:
        await message_service_port.subscribe(central_channel)
    except:
        raise LogicException("cound not subscribe to channel")


async def listen_for_messages_and_update(
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
    database_port: DatabasePort,
    central_channel: str,
):
    try:
        result_update = await message_service_port.wait_for_message(central_channel)

        _update_database(database_port, result_update)

        simple_storage_port.remove_inference_directory(result_update.inference_id)

    except LogicException:
        raise
    except:
        raise LogicException("cound not create new inference")


def _update_database(database_port: DatabasePort, result_update: ResultUpdate):
    try:
        database_port.update_result(result_update)
        database_port.update_inference_status(
            result_update.inference_id, Status.completed_status
        )
    except:
        raise LogicException("cound not update database")
