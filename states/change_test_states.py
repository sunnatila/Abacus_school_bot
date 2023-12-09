from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeTestStateGroup(StatesGroup):
    free_premium = State()
    tests = State()
    test = State()


class ActiveTestStates(StatesGroup):
    free_premium = State()
    tests = State()
    test = State()


class DeActiveTestStates(StatesGroup):
    free_premium = State()
    tests = State()
    test = State()
