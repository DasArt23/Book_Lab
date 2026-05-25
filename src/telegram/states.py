from aiogram.fsm.state import StatesGroup, State


class EnterNum(StatesGroup):
    ch_num = State()


class EnterPath(StatesGroup):
    ch_path = State()


class EnterHandler(StatesGroup):
    ch_type = State()
    ch_rec_id = State()
    ch_threshold = State()
    ch_mode = State()
