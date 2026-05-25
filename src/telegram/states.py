from aiogram.fsm.state import StatesGroup, State


class EnterNum(StatesGroup):
    ch_num = State()


class EnterPath(StatesGroup):
    ch_path = State()
