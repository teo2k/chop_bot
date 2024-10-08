import apscheduler.jobstores.base
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query, ReplyKeyboardRemove
import app.keyboards as kb
import app.questions_and_text as q_t
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.bitrix import create_test_lead
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()
router = Router()


async def send_reminder_30_min(message, n, t):
    a = ''
    if n == 1:
        a = 'ов.'
    elif n == 2:
        a = 'а.'
    elif n == 3:
        a = 'а.'
    elif n == 4:
        a = 'а.'
    elif n == 5:
        a = '.'
    n = 5 - n + 1
    if t == 'e':
        await message.answer(q_t.text_30min_edit)
    elif t == 's':
        await message.answer(q_t.text_30min_send)
    else:
        await message.answer(
            f'С момента последней вашей активности прошло более 30 минут. Вам осталось ответить всего лишь на {n} вопрос{a}')


async def send_reminder_5_hours(message, n, t):
    a = ''
    if n == 1:
        a = 'ов.'
    elif n == 2:
        a = 'а.'
    elif n == 3:
        a = 'а.'
    elif n == 4:
        a = 'а.'
    elif n == 5:
        a = '.'
    n = 5 - n + 1
    if t == 'e':
        await message.answer(q_t.text_5hours_edit)
    elif t == 's':
        await message.answer(q_t.text_5hours_send)
    else:
        await message.answer(
            f'С момента вашей последней активности прошло более 5 часов. Вам осталось ответить всего лишь на {n} вопрос{a}')


async def send_reminder_19_hours(message, n, t):
    a = ''
    if n == 1:
        a = 'ов.'
    elif n == 2:
        a = 'а.'
    elif n == 3:
        a = 'а.'
    elif n == 4:
        a = 'а.'
    elif n == 5:
        a = '.'
    n = 5 - n + 1
    if t == 'e':
        await message.answer(q_t.text_19hours_edit)
    elif t == 's':
        await message.answer(q_t.text_19hours_send)
    else:
        await message.answer(
            f'С момента вашей последней активности прошли сутки. Вам осталось ответить всего лишь на {n} вопрос{a}')


def schedule_reminders(message, user_id, n, t):
    # cancel_reminders(user_id)
    scheduler.add_job(send_reminder_30_min, 'date', run_date=datetime.now() + timedelta(seconds=10),
                      args=[message, n, t],
                      id=f'reminder_30_min_{user_id}')
    scheduler.add_job(send_reminder_5_hours, 'date', run_date=datetime.now() + timedelta(seconds=20),
                      args=[message, n, t],
                      id=f'reminder_5_hours_{user_id}')
    scheduler.add_job(send_reminder_19_hours, 'date', run_date=datetime.now() + timedelta(seconds=30),
                      args=[message, n, t],
                      id=f'reminder_19_hours_{user_id}')
    scheduler.start()


def cancel_reminders(user_id):
    for reminder_type in ['30_min', '5_hours', '19_hours']:
        job_id = f'reminder_{reminder_type}_{user_id}'
        try:
            scheduler.remove_job(job_id=job_id)
        except apscheduler.jobstores.base.JobLookupError:
            print(f'Job {job_id} does not exist.')

def num_check(n):
    return any(char.isdigit() for char in n)

def alf_check(n):
    alf_ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alf_en = 'abcdefghijklmnopqrstuvwxyz'
    return any(char.lower() in alf_ru or char.lower() in alf_en for char in n)

def age_check(n):
    if alf_check(n):
       return 'Введен некорректный ответ'
    else:
        n = int(n)
        if not(n >= 18 and n < 100):
            return 'Введеный возраст не удовлетворяет нашим требованиям'
        else:
            return False


class Reg(StatesGroup):
    name = State()
    surname = State()
    city = State()
    age = State()
    phone = State()
    check = State()
    confirm = State()
    b4questions = State()
    questions = State()
    already_send = []


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in Reg.already_send:
        await message.answer(q_t.try_again)
    else:
        await message.answer(q_t.greetings, reply_markup=kb.confirm_start)

@router.callback_query(F.data == 'confirm')
async def confirmed(callback: callback_query, state=FSMContext):
    await callback.answer(q_t.confirm_start, show_alert=True)
    await state.set_state(Reg.name)
    await callback.message.edit_text(q_t.name)
    schedule_reminders(message=callback.message, user_id=callback.message.chat.id, n=1, t='')


@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    text = num_check(message.text)
    if not text:
        await state.update_data(name=message.text)
        temp = await state.get_data()
        if 'edit' not in temp:
            await state.set_state(Reg.surname)
            await message.answer(q_t.surname)
            schedule_reminders(message=message, user_id=message.from_user.id, n=2, t='')
        else:
            await process_check_stage(message, state)
            await state.set_state(Reg.check)
            schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    else:
        await message.answer('Вы ввели некорректное имя')
        await state.set_state(Reg.name)
        await message.answer(q_t.name)
        schedule_reminders(message=message, user_id=message.from_user.id, n=1, t='')

@router.message(Reg.surname)
async def two(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    text = num_check(message.text)
    if not text:
        await state.update_data(surname=message.text)
        temp = await state.get_data()
        if 'edit' not in temp:
            await state.set_state(Reg.city)
            await message.answer(q_t.city)
            schedule_reminders(message=message, user_id=message.from_user.id, n=3, t='')
        else:
            await process_check_stage(message, state)
            await state.set_state(Reg.check)
            schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    else:
        await message.answer('Вы ввели некорректную фамилию')
        await state.set_state(Reg.surname)
        await message.answer(q_t.surname)
        schedule_reminders(message=message, user_id=message.from_user.id, n=2, t='')


@router.message(Reg.city)
async def two_three(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    text = num_check(message.text)
    if not text:
        await state.update_data(city=message.text)
        temp = await state.get_data()
        if 'edit' not in temp:
            await state.set_state(Reg.age)
            await message.answer(q_t.age)
            schedule_reminders(message=message, user_id=message.from_user.id, n=4, t='')
        else:
            await process_check_stage(message, state)
            await state.set_state(Reg.check)
            schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    else:
        await message.answer('Вы ввели некорректный город')
        await state.set_state(Reg.city)
        await message.answer(q_t.city)
        schedule_reminders(message=message, user_id=message.from_user.id, n=3, t='')

@router.message(Reg.age)
async def three_four(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    text = age_check(message.text)
    if not text:
        await state.update_data(age=message.text)
        temp = await state.get_data()
        if 'edit' not in temp:
            await state.set_state(Reg.phone)
            await message.answer(q_t.phone)
            schedule_reminders(message=message, user_id=message.from_user.id, n=5, t='')
        else:
            await process_check_stage(message, state)
            await state.set_state(Reg.check)
            schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    else:
        await message.answer(text)
        await state.set_state(Reg.age)
        await message.answer(q_t.age)
        schedule_reminders(message=message, user_id=message.from_user.id, n=4, t='')
@router.message(Reg.phone)
async def four_five(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    text = alf_check(message.text)
    if not text:
        await state.update_data(phone=message.text)
        await state.set_state(Reg.check)
        await process_check_stage(message, state)
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='s')
    else:
        await message.answer('Вы ввели некорректный номер телефона')
        await state.set_state(Reg.phone)
        await message.answer(q_t.phone)
        schedule_reminders(message=message, user_id=message.from_user.id, n=5, t='')

async def process_check_stage(message: Message, state: FSMContext):
    data = await state.get_data()
    data_ans = list(data.values())
    t = 'Проверьте правильно ли введены ваши данные'
    questions = [q_t.name, q_t.surname, q_t.city, q_t.age, q_t.phone]
    for i, ans in enumerate(data_ans[:5]):
        t += f'\n\n{questions[i]}\nВаш ответ:\n{ans}'
    await message.answer(t, reply_markup=kb.q_check)


@router.message(Reg.check)
async def five_six(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    await state.update_data(edit=message.text)
    choice = await state.get_data()
    print(choice)
    pick = choice['edit'][0]
    if pick == '6':
        await state.set_state(Reg.b4questions)
        await message.answer(q_t.confirm, reply_markup=kb.confirm_ans)
        schedule_reminders(message=message, user_id=message.from_user.id, n=777, t='s')
        print('asdf')
    elif pick == '1':
        await state.set_state(Reg.name)
        await message.answer(q_t.name, reply_markup=ReplyKeyboardRemove())
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    elif pick == '2':
        await state.set_state(Reg.surname)
        await message.answer(q_t.surname, reply_markup=ReplyKeyboardRemove())
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    elif pick == '3':
        await state.set_state(Reg.city)
        await message.answer(q_t.city, reply_markup=ReplyKeyboardRemove())
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    elif pick == '4':
        await state.set_state(Reg.age)
        await message.answer(q_t.age, reply_markup=ReplyKeyboardRemove())
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    elif pick == '5':
        await state.set_state(Reg.phone)
        await message.answer(q_t.phone, reply_markup=ReplyKeyboardRemove())
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')
    else:
        await state.set_state(Reg.check)
        await message.answer(q_t.wrong_edit_pick)
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')


@router.message(Reg.b4questions)
async def six_seven(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    await state.update_data(b4questions=message.text)
    temp = await state.get_data()
    print(temp)
    if temp['b4questions'] == 'Подтверждаю данные':
        name = temp['name']
        surname = temp['surname']
        phone = temp['phone']
        city = temp['city']
        age = temp['age']
        create_test_lead(name, surname, phone, city, age)
        Reg.already_send.append(message.from_user.id)
        await state.set_state(Reg.questions)
        await message.answer(q_t.questions, reply_markup=ReplyKeyboardRemove())
    elif temp['b4questions'] == 'Изменить данные':
        await process_check_stage(message, state)
        await state.set_state(Reg.check)
        schedule_reminders(message=message, user_id=message.from_user.id, n=999, t='e')


@router.message(Reg.questions)
async def seven_eight(message: Message, state: FSMContext):
    cancel_reminders(message.from_user.id)
    await state.update_data(questions=message.text)
    data = await state.get_data()
    question = data['questions']
    print(question)
    pass
