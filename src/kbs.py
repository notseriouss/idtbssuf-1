from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import nim


kb_start: list = [
    [
        types.KeyboardButton(text="Начать игру")
    ],
];


def build_kb(GAME: nim.nim):
    builder = ReplyKeyboardBuilder();
    for i in range(len(GAME.get_bunches())):
        builder.row(
            types.KeyboardButton(text=f"{i+1}. {str(GAME.get_bunches()[i])}")
        );

    return builder;
