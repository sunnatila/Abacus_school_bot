from aiogram.dispatcher.filters.state import State, StatesGroup


class NewTestStateGroup(StatesGroup):
    science = State()
    class_number = State()
    question = State()
    quantity = State()
    responses = State()
    time = State()
    premium = State()
    amount = State()
    access = State()
    confirm = State()
