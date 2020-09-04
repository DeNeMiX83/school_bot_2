from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def teacher_panel(classroom=False):
    panel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Рассылка')
            ]
        ],
        resize_keyboard=True
    )

    if classroom:
        panel.keyboard[0].append(KeyboardButton(text='Ученики'))
        panel.add(KeyboardButton(text='Главный по столовой'))
    return panel
