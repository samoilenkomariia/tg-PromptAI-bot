from groq import AsyncGroq

from app.config import GROQ_API_KEY, GROQ_MODEL


async def ask_ai(prompt: str) -> str:
    async with AsyncGroq(
        api_key=GROQ_API_KEY,
        timeout=40.0,
        max_retries=0,
    ) as client:
        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ти навчальний помічник студента. "
                        "Відповідай українською, зрозуміло й стисло. "
                        "За потреби додавай короткі приклади."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_completion_tokens=2048,
        )

    answer = response.choices[0].message.content

    if not answer or not answer.strip():
        return "The AI ​​did not return any text. Try rephrasing your request."

    return answer.strip()