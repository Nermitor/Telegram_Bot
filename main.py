from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Command, ContentTypeFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery, ContentType, Message
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from math import *
from decimal import Decimal

from graph_to_send import save_picture
from sudoku import solve_sudoku
from config import Config
from translate import Translator
from translate.exceptions import InvalidProviderError

print('OK')


class Common(StatesGroup):
    weath = State()
    calc = State()
    sudoku = State()
    connect_to_admin = State()


class TranslatorState(StatesGroup):
    text = State()
    lang = State()


class GraphikState(StatesGroup):
    function = State()
    get_range = State()


class Weather:
    def __init__(self, place):
        self.observation = mgr.weather_at_place(place)
        self.w = self.observation.weather

    def get_status(self):
        return self.w.detailed_status

    def get_temp(self):
        return self.w.temperature('celsius')['temp']

    def get_speed(self):
        return self.w.wind()['speed']


bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

mgr = OWM(Config.OWM_TOKEN).weather_manager()
config_dict = get_default_config()
config_dict['language'] = Config.LANGUAGE
print("OK")


@dp.message_handler(Command("start"), state='*')
async def process_start_command(message: Message, state: FSMContext):
    greet = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("/help"))
    await message.reply(Config.MESSAGES['start'], reply_markup=greet)
    await state.finish()


@dp.message_handler(text="Связаться с разработчиком🆘", state='*')
async def dev_call(message: Message):
    await message.reply("Что бы вы хотели сообщить разработчику, постарайтесь подробно описать проблему:", reply=False)
    await Common.connect_to_admin.set()


@dp.message_handler(Command("help"), state='*')
async def process_help_command(message: Message, state: FSMContext):
    greet = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    [greet.insert(i) for i in Config.OPTIONS]
    if message.from_user.id != Config.ADMIN_ID:
        greet.add(KeyboardButton("Связаться с разработчиком🆘"))
    await message.reply(Config.MESSAGES['help'], reply_markup=greet)
    await state.finish()


@dp.message_handler(text="Узнать погоду🌅", state='*')
async def w(message: Message):
    await message.reply(Config.MESSAGES['weather'], reply=False)
    await Common.weath.set()


@dp.message_handler(text="Продвинутый калькулятор🔢", state='*')
async def c(message: Message):
    z = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Узнать список всех операторов", callback_data="operators"))
    await message.reply(Config.MESSAGES['calc'], reply=False, reply_markup=z)
    await Common.calc.set()


@dp.message_handler(text="Решить судоку📝", state='*')
async def s(message: Message):
    await message.reply(Config.MESSAGES[message.text], reply=False)
    await Common.sudoku.set()


@dp.message_handler(text='График📈', state='*')
async def graph_state(message: Message, state: FSMContext):
    await message.reply(Config.MESSAGES[message.text], reply=False)
    await GraphikState.get_range.set()


@dp.message_handler(text="Перевести текст㊙", state='*')
async def translate_state(message: Message, state: FSMContext):
    await message.reply(Config.MESSAGES[message.text], reply=False)
    await TranslatorState.lang.set()


@dp.callback_query_handler(text='change_dia', state=GraphikState.function)
async def change_dia(callback: CallbackQuery):
    await callback.message.answer("Введите новый диапазон")
    await GraphikState.get_range.set()


@dp.callback_query_handler(text="operators", state='*')
async def info_operators(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='x**y - Возведение x в степень y.\n\n'
                                       'x // y - Деление нацело x на y.\n\n'
                                       'ceil(x) - Округление x вверх.\n\n'
                                       'abs(x) - Модуль x.\n\n'
                                       'factorial(x) - Факториал x.\n\n'
                                       'floor(x) - округление x вниз.\n\n'
                                       'x % y - остаток от деления x на y.\n\n'
                                       'trunc(x) - отсекает дробную часть x.\n\n'
                                       'exp(x) - Постоянная Эйлера в степени x.\n\n'
                                       'log(x, base) - Логарифм от x по основанию base, если base не указан, '
                                       'считается натуральный логарифм.\n\n '
                                       'log10(x) - Логарифм от х по основанию 10.\n\n'
                                       'log2(x) - Логарифм от x по основанию 2.\n\n'
                                       'sqrt(x, base) - корень из x по основанию base, ели base не указан, считается '
                                       'квадратный корень.\n\n '
                                       'acos(x) - аркосинус x в радианах.\n\n'
                                       'asin(x) - арксинус x в радианах.\n\n'
                                       'atan(x) - арктангенс х в радианах.\n\n'
                                       'cos(x) - косинус х.\n\n'
                                       'sin(x) - синус х.\n\n'
                                       'gcd() - Наибольший общий делитель для любого количества чисел\n\n'
                                       'lcm() - Наименьшее общее кратное для любого количества чисел\n\n'
                                       'tan(x) - тангенс х.\n\n'
                                       'hypot(x, y) - вычисляет гипотенузус с катетами x и y.\n\n'
                                       'degrees(x) - преобразует радианы в градусы.\n\n'
                                       'radians(x) - преобразует градусы в радианы.\n\n'
                                       'cosh(X) - вычисляет гиперболический косинус.\n\n'
                                       'sinh(X) - вычисляет гиперболический синус.\n\n'
                                       'tanh(X) - вычисляет гиперболический тангенс.\n\n'
                                       'int(x, base) - преобразует число х из системы счисления base в десятичную.\n\n'
                                       'bin(x) - преобразует х в двоичную систему счисления.\n\n'
                                       'oct(x) - преобразует x в восьмеричную систему счисления.\n\n'
                                       'hex(x) - преобразует х в шестнадцетиричную систему счисления.\n\n'
                                       'acosh(X) - вычисляет обратный гиперболический косинус.\n\n'
                                       'asinh(X) - вычисляет обратный гиперболический синус.\n\n'
                                       'perm(x, y) - Количество перестановок x элементов по y\n\n'
                                       'comb(x, y) - Количество комбинаций из x элементов по y\n\n'
                                       'atanh(x) - вычисляет обратный гиперболический тангенс.\n\n'
                                       'Примечание: тригонометрические функции вычисляются в радианах\n\n'
                                       'Константы:\n\n'
                                       'pi - число π.\n\n'
                                       'e - Постоянная Эйлера.'
                                  )


@dp.message_handler(state=TranslatorState.lang)
async def commit_text(message: Message, state: FSMContext):
    try:
        translator = Translator(*message.text.split('-')[::-1])
    except InvalidProviderError:
        await message.reply(
            "Невозможно настроить переводчик на данную пару, возможно вы неправильно ввели один из языков", reply=False)
    else:
        await state.update_data(
            {"translator": translator}
        )
        await message.reply("Введите текст, который надо перевести")
        await TranslatorState.text.set()


@dp.callback_query_handler(text="switch_lang", state=TranslatorState.text)
async def switch_lang(call: CallbackQuery):
    await call.answer(cache_time=60)
    await bot.send_message(call.from_user.id, text="Введите новую языковую пару")
    await TranslatorState.lang.set()


@dp.message_handler(state=TranslatorState.text)
async def set_language(message: Message, state: FSMContext):
    data = await state.get_data()
    translator = data.get("translator")
    button = InlineKeyboardMarkup().add(InlineKeyboardButton("Поменять язык", callback_data="switch_lang"))
    try:
        await message.reply("Переведённый текст:\n\n" + translator.translate(message.text), reply=False,
                            reply_markup=button)
    except:
        await message.reply("Невозможно перевести введённый текст, возможно таких слов не существует", reply=False,
                            reply_markup=button)


@dp.message_handler(state=GraphikState.get_range)
async def get_function(message: Message, state: FSMContext):
    try:
        start, stop, n = map(int, message.text.split('/'))
    except:
        await message.reply("Вы где-то ошиблись, попробуйте ещё раз")
    else:
        await state.update_data(
            {'values': [start, stop, n]}
        )
        z = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="Узнать список всех операторов", callback_data="operators"))
        await message.reply("А теперь введите значение функции f(x), например, (x - 2)**2", reply_markup=z)
        await GraphikState.function.set()


@dp.message_handler(state=GraphikState.function)
async def art(message: types.Message, state: FSMContext):
    try:
        func = lambda x: eval(message.text)
    except:
        await message.reply("Вы где-то ошиблись")
    else:
        data = await state.get_data()
        try:
            save_picture(*data.get("values"), func, f"График функции f(x) = {message.text}")
        except:
            await message.reply("Невозможно начертить график для данной функции")
        else:
            z = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text="Изменить диапазон", callback_data="change_dia"))
            with open("to_send.png", 'rb') as im:
                await bot.send_photo(message.from_user.id, photo=im, reply_markup=z)


@dp.message_handler(state=Common.connect_to_admin)
async def back_call(message: Message, state: FSMContext):
    await bot.send_message(Config.ADMIN_ID, "Сообщение от пользователя:\n" + message.text)
    await state.finish()
    await message.reply("Сообщение доставлено📪", reply=False)


@dp.message_handler(state=Common.calc)
async def calculating(message: Message):
    try:
        ans = Decimal(eval(message.text))
    except NameError:
        await message.reply("Невозможно выполнить данную команду⚠", reply=False)
    except ZeroDivisionError:
        await message.reply("Нельзя делить на ноль⚠", reply=False)
    except TypeError:
        await message.reply("Вы хотите сделать что-то незаконное⛔", reply=False)
    except SyntaxError:
        await message.reply("Вы хотите сделать что-то незаконное⛔", reply=False)
    else:
        await message.reply(f"🆗Ответ:\n{ans}")


@dp.message_handler(state=Common.weath)
async def get_weather(message: Message):
    await message.reply('Секунду...🔍', reply=False)
    city = message.text.title()
    try:
        ans = Weather(city)
    except NotFoundError:
        await message.reply("Не могу найти указанный город🛑")
    else:
        await message.reply(f"Сейчас в {city} {ans.get_status()}.\n"
                            f"Температура на улице составляет {ans.get_temp()} градусов.\n"
                            f"Скорость ветра достигает {ans.get_speed()} м/с.")


@dp.message_handler(state=Common.sudoku)
async def sudoku(message: Message):
    k = message.text.split('\n')
    if len(k) == 9 and len(k[0]) == 9:
        await message.reply(
            'Ответ:' + '\n' + '\n'.join([' '.join(map(str, i)) for i in solve_sudoku(message.text.strip())]))
    else:
        await message.reply('Вы ввели неправильный формат судоку⚠'
                            'Введите поле 9 на 9, незаполненные клетки отметьте нулями.')


@dp.message_handler(ContentTypeFilter(content_types=[ContentType.ANY]), state='*')
async def info(message: Message):
    await message.reply("Такой команды я не знаю, попробуйте использовать /help, чтобы узнать список доступных команд")


if __name__ == '__main__':
    executor.start_polling(dp)
