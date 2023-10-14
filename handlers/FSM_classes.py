from aiogram.filters.state import State, StatesGroup, StateFilter


class FSMSubscription(StatesGroup):
    subscribe = State()
    unsubscribe = State()
