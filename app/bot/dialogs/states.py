from aiogram.fsm.state import StatesGroup, State


class MailMessagesSG(StatesGroup):
    menu = State()
    mail_text = State()
