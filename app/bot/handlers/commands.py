from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram_dialog import DialogManager, StartMode, ShowMode


from app.bot.dialogs import MailMessagesSG


commands_router = Router()


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message, dialog_manager: DialogManager, bot: Bot
):
    await dialog_manager.start(
        state=MailMessagesSG.menu,
        mode=StartMode.RESET_STACK,
    )


@commands_router.message(Command("help"))
async def process_help_command(message: Message, dialog_manager: DialogManager):
    await message.answer(
        text="Бот, демонстрирующий работу рассылки сообщений по чатам/группам/каналам"
    )
    await dialog_manager.switch_to(state=MailMessagesSG.menu, show_mode=ShowMode.SEND)
