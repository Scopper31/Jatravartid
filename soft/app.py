from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
load_dotenv()
# from .code.solve import *
# from utilities import *
# from config import *
# from correction import *


   


# Инициализация бота и диспетчера
bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

# Класс состояний для создания нового проекта
class NewProject(StatesGroup):
    description = State() # Состояние для получения описания проекта

# Класс состояний для редактирования старого проекта
class EditProject(StatesGroup):
    file = State() # Состояние для получения файла проекта
    correction = State() # Состояние для получения описания изменений

# Кнопки для выбора действия
start_keyboard = types.InlineKeyboardMarkup(row_width=2)
start_keyboard.add(types.InlineKeyboardButton('Создать новый проект', callback_data='new_project'),
                  types.InlineKeyboardButton('Изменить старый проект', callback_data='edit_project'))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Добро пожаловать! Что вы хотите сделать?", reply_markup=start_keyboard)

# Обработчик нажатия на кнопку "Создать новый проект"
@dp.callback_query_handler(lambda c: c.data == 'new_project')
async def new_project_start(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Введите описание вашего проекта:")
    await NewProject.description.set()
    await callback_query.answer()

# Обработчик состояния описания проекта
@dp.message_handler(state=NewProject.description)
async def new_project_description(message: types.Message, state: FSMContext):
    project_description = message.text
    await state.update_data(description=project_description)

    await message.reply("Подождите пару минут...")

    # Имитация обработки проекта (замените на вашу логику)
    #await asyncio.sleep(5) 

    set_folder_name(generate_alias(project_description))
    print("Folder name: ", folder_obj.folder_name)
    file_work(project_description)
    solve_task(project_description)

    # Отправка папки с файлами (замените на отправку файлов)
    await message.reply("Проект готов! Вот ссылка на папку с файлами:")
    #await message.reply_document(open('path/to/your/folder.zip', 'rb'))

    await state.finish()

# Обработчик нажатия на кнопку "Изменить старый проект"
@dp.callback_query_handler(lambda c: c.data == 'edit_project')
async def edit_project_start(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Загрузите файл с проектом:")
    await EditProject.file.set()
    await callback_query.answer()

# Обработчик состояния загрузки файла
@dp.message_handler(content_types=['document'], state=EditProject.file)
async def edit_project_file(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document.file_id)
    await message.reply("Введите, что нужно исправить:")
    await EditProject.correction.set()

# Обработчик состояния описания изменений
@dp.message_handler(state=EditProject.correction)
async def edit_project_correction(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = data.get('file')
    correction = message.text

    await message.reply("Подождите пару минут...")

    # Имитация обработки изменений (замените на вашу логику)
    #await asyncio.sleep(5) 

    # Отправка папки с файлами (замените на отправку файлов)
    await message.reply("Проект изменен! Вот ссылка на папку с файлами:")
    #await message.reply_document(open('path/to/your/folder.zip', 'rb'))

    await state.finish()

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)