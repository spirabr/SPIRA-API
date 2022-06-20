from core.ports.database_port import DatabasePort
from core.ports.message_service_port import MessageServicePort
from core.services.result_service import update_inference_result


async def listen_for_messages_and_update(
    message_service_port: MessageServicePort,
    database_port: DatabasePort,
    central_channel: str,
):
    result_update = await message_service_port.receive_message(central_channel)
    update_inference_result(database_port, result_update)
