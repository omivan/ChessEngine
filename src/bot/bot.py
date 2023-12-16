import asyncio
import logging
import random
import sys
import os
import aiogram.filters
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import FSInputFile
import config
from image_generator import ChessBoardGenerator
import chess
import time
import chess.svg
import chess.pgn

from src.game_process.engine import ChessEngine

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config.TOKEN

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
chess_game = None
generator = None
bot_color = 1  # 1 - White, 2 - Black
engine = ChessEngine()


class GameStates(StatesGroup):
    not_in_game = State()
    in_game = State()
    in_bot_game = State()


game_state = None


class StyleStates(StatesGroup):
    board_style_setting = State()
    pieces_style_setting = State()
    not_style_setting = State()
    accept_style = State()
    color_setting = State()


new_style = {'board': None, 'pieces': None}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


# @dp.message(aiogram.filters.Command('get_position'))
# async def echo_handler(message: types.Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")

async def send_current_position(message: types.Message):
    generator.set_styles_from_dictionary(new_style)
    generator.set_fen_pos(chess_game.board_fen())
    path_to_image = str(message.from_user.id)
    pos_name = 'position.png'
    if not os.path.exists(path_to_image):
        os.mkdir(path_to_image)

    path_to_pos = os.path.join(os.path.join(path_to_image, pos_name))
    generator.generate_picture(save_to=path_to_pos)
    pos = FSInputFile(path_to_pos)
    # print('done?')
    await message.answer_photo(pos)


def result_of_game(board: chess.Board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1
        else:
            return 1
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0
    else:
        return 2


async def send_style_example(message: types.Message, style_sample):
    path_to_image = str(message.from_user.id)
    pos_name = 'example.png'
    if not os.path.exists(path_to_image):
        os.mkdir(path_to_image)

    path_to_pos = os.path.join(os.path.join(path_to_image, pos_name))
    generator.get_style_sample(figure_style=style_sample['pieces'],
                               board_style=style_sample['board'],
                               save_to=path_to_pos)
    pos = FSInputFile(path_to_pos)
    # print('done?')
    await message.answer_photo(pos)


async def bot_make_move(message: types.Message, board: chess.Board):
    best_move1, best_eval1 = engine.get_best_move(board, depth=4)
    board.push(best_move1)
    await message.answer('Я походив, чекай позицію')


@dp.message(aiogram.filters.Command('get_position'))
async def get_current_position(message: types.Message):
    await send_current_position(message)


@dp.message(aiogram.filters.Command('get_style'))
async def get_current_style(message: types.Message):
    style = generator.get_this_style()
    await message.answer(f'Styles of the chess:\n'
                         f'Board style is {style["board"]}\n'
                         f'Figures style is {style["figures"]}')


@dp.message(aiogram.filters.Command('start_game'))
async def start_chess_game(message: types.Message, state: FSMContext):
    global chess_game, generator, make_move_now
    chess_game = chess.Board()
    generator = ChessBoardGenerator(chess_game.board_fen())
    await state.set_state(GameStates.in_game)
    await send_current_position(message)


@dp.message(aiogram.filters.Command('start_bot_game'))
async def start_bot_game_color_setting(message: types.Message, state: FSMContext):
    await state.set_state(StyleStates.color_setting)
    await message.answer(f'Ти певен? Ну добре, я зіграю з тобою, шкіряний мішок {hbold(message.from_user.full_name)}'
                         f'\nТільки потім не плач **бугагага**')
    await message.answer(f'Ну добре, даю тобі фору, обирай колір за який гратимеш:\n'
                         f'1) білі\n'
                         f'2) чорні\n'
                         f'3) випадковий\n'
                         f'Відповідь 1, або 2, або 3')


@dp.message(StyleStates.color_setting)
async def start_bot_game(message: types.Message, state: FSMContext):
    global chess_game, generator, bot_color

    if message.text == '1':
        bot_color = 1
        await message.answer(f'Пхаха, відчув, що слабше, думаєш білий колір допоможе, я - машина, я - краще, '
                             f'твій вибір тільки відсроче кінцівку')
    elif message.text == '2':
        bot_color = 2
        await message.answer(f'Хм, ну добре, хочеш швидше програти, це твій вибір')
    elif message.text == '3':
        await message.answer(f'Ох, ти настільки облінився, що й сам не можеш обрати колір, ну добре, ...')
        bot_color = random.Random().randint(1, 2)
        await message.answer(f"Напрягши всі свої резистори обрав тобі колір, і це "
                             f"**{'білий' if bot_color == 1 else 'чорний'}**")
    else:
        await message.answer(f'Ти що, не можеш навіть нормально написати просто одну цифру, капець, ну я сьогодні '
                             f'добрий, спробуй ще')
        return

    chess_game = chess.Board()
    generator = ChessBoardGenerator(chess_game.board_fen())
    await state.set_state(GameStates.in_bot_game)

    await send_current_position(message)
    if bot_color == 2:
        await bot_make_move(message, chess_game)
        await send_current_position(message)


@dp.message(GameStates.in_game)
async def get_move(message: types.Message, state: FSMContext):
    try:
        move_text = message.text.lower()[-4:]
        move = chess.Move.from_uci(move_text)
        if move in chess_game.legal_moves:
            chess_game.push(chess.Move.from_uci(move_text))
        else:
            await message.answer('Хід є неможливим, спробуйте інший')
    except chess.InvalidMoveError as e:
        await message.answer('Хід написано неправильно, спробуйте ще раз\nформат: {Назва (однією літерою)}{Звідки}{'
                             'Куди}')
    except ValueError as e:
        await message.answer(e.message)
    await send_current_position(message)


@dp.message(GameStates.in_bot_game)
async def get_move(message: types.Message, state: FSMContext):
    global chess_game
    try:
        move_text = message.text.lower()[-4:]
        move = chess.Move.from_uci(move_text)
        if move in chess_game.legal_moves:
            chess_game.push(chess.Move.from_uci(move_text))
        else:
            await message.answer('Хід є неможливим, спробуйте інший')
            return
    except chess.InvalidMoveError as e:
        await message.answer('Хід написано неправильно, спробуйте ще раз\nформат: {Назва (однією літерою)}{Звідки}{'
                             'Куди}')
    except ValueError as e:
        await message.answer(e.message)

    await send_current_position(message)
    if chess_game.is_game_over():
        result = result_of_game(chess_game)
        print(result)
        if result == -1:
            await message.answer('Чорні виграли!')
        elif result == 0:
            await message.answer('Нічия')
        elif result == 1:
            await message.answer('Білі виграли!')
        await state.set_state()

    await bot_make_move(message, chess_game)
    await send_current_position(message)
    if chess_game.is_game_over():
        result = result_of_game(chess_game)
        if result == -1:
            await message.answer('Чорні виграли!')
        elif result == 0:
            await message.answer('Нічия')
        elif result == 1:
            await message.answer('Білі виграли!')
        await state.set_state()

@dp.message(aiogram.filters.Command('set_board_style'))
async def get_board_styles(message: types.Message, state: FSMContext):
    global game_state
    await state.set_state(StyleStates.board_style_setting)
    await message.answer(', '.join(generator.get_all_board_styles()))


@dp.message(StyleStates.board_style_setting)
async def get_board_example(message: types.Message, state: FSMContext):
    global chess_game, generator
    new_style['board'] = message.text
    await state.set_state(StyleStates.not_style_setting)
    if chess_game is None:
        chess_game = chess.Board()
    if generator is None:
        generator = ChessBoardGenerator(chess_game.board_fen())
    await send_current_position(message)


@dp.message(aiogram.filters.Command('set_pieces_style'))
async def get_pieces_styles(message: types.Message, state: FSMContext):
    global game_state
    await state.set_state(StyleStates.pieces_style_setting)
    await message.answer(', '.join(generator.get_all_figures_styles()))


@dp.message(StyleStates.pieces_style_setting)
async def get_pieces_example(message: types.Message, state: FSMContext):
    global chess_game, generator
    new_style['pieces'] = message.text
    await state.set_state(StyleStates.not_style_setting)
    if chess_game is None:
        chess_game = chess.Board()
    if generator is None:
        generator = ChessBoardGenerator(chess_game.board_fen())
    await send_current_position(message)


async def main() -> None:
    global generator
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    generator = ChessBoardGenerator()
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
