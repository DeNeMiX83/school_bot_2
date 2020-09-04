from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import exit_from_inline
from loader import dp


@dp.callback_query_handler(exit_from_inline.filter(where='all'), state=['*', None])
async def exit_(call: CallbackQuery, state: FSMContext):
    print(f'{call.from_user.full_name} нажал выйти через инлайн кнопку')
    await call.answer(cache_time=5)
    await call.message.delete()
    await state.finish()