from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import exit_from_inline
from loader import dp
from states import Mailing


@dp.callback_query_handler(exit_from_inline.filter(where='mailing'), state='*')
async def exit_(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await Mailing.Start.set()