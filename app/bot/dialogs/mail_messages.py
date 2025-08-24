from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager, Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.input import MessageInput

from config.config import settings
from app.bot.dialogs import MailMessagesSG
from app.service.nats.mail_service import send_mailing_message


async def message_input_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    data = await dialog_manager.load_data()
    js = data.get("middleware_data").get("js")
    if message.photo:
        photo_id = message.photo[-1].file_id
        text = message.caption
    else:
        photo_id = None
        text = message.text
    mailing_result = await send_mailing_message(
        js=js,
        subject=settings.nats.subject,
        chat_ids=settings.chat_ids,
        text=text,
        photo_id=photo_id,
    )
    if mailing_result:
        await message.answer(text="Рассылка прошла успешно")
    await dialog_manager.switch_to(
        state=MailMessagesSG.menu, show_mode=ShowMode.DELETE_AND_SEND
    )


dialog = Dialog(
    Window(
        Const("Меню"),
        Next(text=Const(text="Сделать рассылку")),
        state=MailMessagesSG.menu,
    ),
    Window(
        Const(
            text="Введите текст рассылки\n*поддерживается только: текст, изображения"
        ),
        MessageInput(func=message_input_handler, content_types=ContentType.ANY),
        state=MailMessagesSG.mail_text,
    ),
)
