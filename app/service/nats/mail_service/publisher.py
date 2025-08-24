import logging

from nats.js.client import JetStreamContext


logger = logging.getLogger(__name__)


async def send_mailing_message(
    js: JetStreamContext,
    subject: str,
    chat_ids: list[int],
    text: str,
    photo_id: str | None,
):
    chat_ids = " ".join(list(map(str, chat_ids)))
    headers = {"Chat-Ids": chat_ids}
    if photo_id:
        headers["Photo-Id"] = photo_id
    if text:
        payload = text.encode(encoding="utf-8")
        result = await js.publish(subject, payload=payload, headers=headers)
    else:
        result = await js.publish(subject, headers=headers)
    logger.debug(result)
    logger.info(f"Message: '{text}' sent to subject: '{subject}'")
    return result
