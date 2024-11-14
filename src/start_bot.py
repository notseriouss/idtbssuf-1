#import logging
import config as cfg
import asyncio
import kbs
import nim
from time import sleep
from loguru import logger


from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder



#logging.basicConfig(level=logging.INFO);
dp = Dispatcher();
GAME: nim.nim = nim.nim();
IS_PLAYING: bool = False;


def build_string(lst: list) -> str:
    output: str = "";
    for index, i in enumerate(lst):
        output += f"{index+1}. {i}\n";
    return output;


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    logger.info(f"{message.chat.full_name} - {message.chat.id} => {message.text}")
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kbs.kb_start,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    );

    await message.answer(text="Выберите действие", reply_markup=keyboard);


@dp.message()
async def msgs(message: types.Message) -> None:
    global IS_PLAYING;
    logger.info(f"{message.chat.full_name} - {message.chat.id} => {message.text}")
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kbs.kb_start,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    );

    if (message.text == "Начать игру"):
        if (not IS_PLAYING):
            IS_PLAYING = True;
            GAME.reset();
        else:
            await message.answer(text="Игра уже идет");
            return;

        await message.answer(text=f"Выберите кучу (номер кучи - кол-во камней)\n\n{build_string(lst=GAME.get_bunches())}", reply_markup=kbs.build_kb(GAME=GAME).as_markup(resize_keyboard=True));

    elif (message.text[0].isdigit() and len(message.text) < 7 and IS_PLAYING):
        try:
            data: list = list(map(int, message.text.split(" - ")));
            if (data[0]-1 not in [i for i in range(len(GAME.get_bunches()))]):
                await message.answer(text="Такой кучи нет, попробуйте снова");
                return;
            elif (data[1] == 0):
                await message.answer(text="Умно, но нет.\nВсе еще ваш ход");
                return;
            elif (GAME.get_bunches()[data[0]-1] < data[1]):
                await message.answer(text="Вы пытаетесь взять больше камней чем их есть в куче, попробуйте снова");
                return;
            elif (GAME.get_bunches()[data[0]-1] == 0):
                await message.answer(text="Куча уже пустая, попробуйте снова");
                return;
        
            GAME.player_move(pile=data[0], stones=data[1]); 

            if (GAME.check_winner()):
                await message.answer(text=f"Вы выиграли!\n\n{build_string(lst=GAME.get_bunches())}", reply_markup=keyboard);
                IS_PLAYING = False;
                return;
            else:
                data = GAME.pc_move();
                if (GAME.check_winner()):
                    await message.answer(text=f"Вы проиграли!\n\n{build_string(lst=GAME.get_bunches())}", reply_markup=keyboard);
                    IS_PLAYING = False;
                    return;


                await message.answer(text=f"Компьютер взял {data[1]} из {data[0]}\n\n{build_string(lst=GAME.get_bunches())}\n\nТеперь ваш ход!", reply_markup=kbs.build_kb(GAME=GAME).as_markup(resize_keyboard=True));
                
    
            #await message.answer(text="Выберите кучу (номер кучи - кол-во камней)", reply_markup=builder.as_markup(resize_keyboard=True));
        except ValueError: await message.answer(text="Не понял");
        except Exception as e:
            await message.answer(text="Не понял");
            raise e;

    elif (message.text == "Стоп"):
        if (not IS_PLAYING):
            await message.answer(text="Нечего останавливать :/");

        else:
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kbs.kb_start,
                resize_keyboard=True,
                input_field_placeholder="Выберите действие"
            );

            IS_PLAYING = False;
            GAME.reset();
            await message.answer(text="Игра остановлена, вы можете начать новую", reply_markup=keyboard);


    else:
        await message.answer(text="Не понял");






async def main() -> None:
    bot = Bot(token=cfg.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML));

    await dp.start_polling(bot);

if __name__ == "__main__":
    asyncio.run(main());
