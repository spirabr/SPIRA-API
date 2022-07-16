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
    """subscribes the listener service to a channel in the message service

    Args:
        message_service_port (MessageServicePort) : message service port
        central_channel (str) : channel to subscribe in

    Returns:
        None

    Raises:
        exception, if there was an error subscribing

    """
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
    """waits for a message to arrive at central channel in message service
        and updates the database with the received data

    Args:
        simple_storage_port (SimpleStoragePort) : simple storage port
        message_service_port (MessageServicePort) : message service port
        database_port (DatabasePort) : database port
        central_channel (str) : subscribed channel

    Returns:
        None

    Raises:
        exception, if there was an error waiting for messages
        exception, if there was an error while updating the database

    """
    try:
        result_update = await message_service_port.wait_for_message(central_channel)

        _update_database(database_port, result_update)

        simple_storage_port.remove_inference_directory(result_update.inference_id)

    except LogicException:
        raise
    except:
        raise LogicException("an error occurred while waiting for the messages")


def _update_database(database_port: DatabasePort, result_update: ResultUpdate):
    """updates the database with the result update

    Args:
        database_port (DatabasePort) : database port
        result_update (ResultUpdate) : result update form

    Returns:
        None

    Raises:
        exception, if there was an error while updating the database

    """
    try:
        database_port.update_result(result_update)
        database_port.update_inference_status(
            result_update.inference_id, Status.completed_status
        )
    except:
        raise LogicException("cound not update inference result")
