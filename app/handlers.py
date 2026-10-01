import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from groq import APIError, RateLimitError

from app.config import (
    CONTACT_EMAIL,
    CONTACT_PHONE,
    STUDENT_GROUP,
    STUDENT_NAME,
)
from app.keyboards import (
    CONTACTS,
    PROMPT_AI,
    STUDENT,
    TECHNOLOGIES,
    main_menu,
)
from app.services.ai_service import ask_ai

router = Router()
logger = logging.getLogger(__name__)


class AIForm(StatesGroup):
    waiting_for_prompt = State()


@router.message(CommandStart())
@router.message(Command("cancel"))
async def show_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Вітаю! Це бот для лабораторної роботи №3.\n"
        "Обери потрібний пункт меню.",
        reply_markup=main_menu,
    )


@router.message(F.text == STUDENT)
async def show_student(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Студент: {STUDENT_NAME}\n"
        f"Група: {STUDENT_GROUP}",
        reply_markup=main_menu,
    )


@router.message(F.text == TECHNOLOGIES)
async def show_technologies(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "IT-технології:\n\n"
        "• HTML — структура вебсторінки.\n"
        "• CSS — оформлення вебсторінки.\n"
        "• JavaScript — інтерактивність у браузері.\n"
        "• Python — серверна логіка та автоматизація.\n"
        "• API — обмін даними між програмами.\n"
        "• AI — створення відповідей на запити користувача.",
        reply_markup=main_menu,
    )


@router.message(F.text == CONTACTS)
async def show_contacts(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Телефон: {CONTACT_PHONE}\n"
        f"E-mail: {CONTACT_EMAIL}",
        reply_markup=main_menu,
    )


@router.message(F.text == PROMPT_AI)
async def start_ai(message: Message, state: FSMContext):
    await state.set_state(AIForm.waiting_for_prompt)
    await message.answer(
        "Напиши запит до AI одним повідомленням.\n"
        "Наприклад: «Поясни різницю між HTML і CSS».\n\n"
        "Текст запиту буде передано сервісу Groq.",
        reply_markup=main_menu,
    )


@router.message(AIForm.waiting_for_prompt, F.text)
async def process_prompt(message: Message, state: FSMContext):
    prompt = message.text.strip()

    if not prompt:
        await message.answer("Enter text.")
        return

    if len(prompt) > 3000:
        await message.answer(
            "Request is too long, shorten it up to 3000 characters."
        )
        return

    # Один запит на одне натискання Prompt AI.
    await state.clear()
    await message.answer("Обробляю запит…")

    try:
        answer = await ask_ai(prompt)
    except RateLimitError:
        answer = (
            "Reached AI-service limit. "
            "Try again later."
        )
    except APIError as error:
        logger.warning("Groq error: %s", type(error).__name__)
        answer = (
            "Failed to get AI response "
            "Check the key, model availability and connection."
        )
    except Exception as error:
        logger.error("Unexpected AI error: %s", type(error).__name__)
        answer = "An error occured. Try again later."

    # Надсилаємо довгу відповідь частинами.
    for position in range(0, len(answer), 2000):
        await message.answer(
            answer[position:position + 2000],
            reply_markup=main_menu,
        )


@router.message(AIForm.waiting_for_prompt)
async def require_text(message: Message):
    await message.answer(
        "Для запиту до AI надішли текст"
    )


@router.message()
async def fallback(message: Message):
    await message.answer(
        "Обери пункт меню. Для запиту до AI натисни Prompt AI.",
        reply_markup=main_menu,
    )