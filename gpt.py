import logging

import requests
from transformers import AutoTokenizer

from config import GPT_URL, LOGS_PATH, MAX_MODEL_TOKENS, MODEL_NAME, IAM_TOKEN, FOLDER_ID

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w"
)


# Функция для подсчета токенов в истории сообщений. На вход обязательно принимает список словарей, а не строку!
def count_tokens_in_dialogue(messages: list) -> int:
    token, folder_id = IAM_TOKEN, FOLDER_ID
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "maxTokens": MAX_MODEL_TOKENS,
        "messages": []
    }

    for row in messages:  # Меняет ключ "content" на "text" в словарях списка для корректного запроса
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["content"]
            }
        )

    return len(
        requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion",
            json=data,
            headers=headers
        ).json()["tokens"]
    )


def get_system_content(subject, level):  # Собирает строку для system_content
    return f"Ты учитель по предмету {subject}. Формулируй ответы уровня {level}"


def ask_gpt_helper(messages: list) -> str:
    """
    Отправляет запрос к модели GPT с задачей и предыдущим ответом
    для получения ответа или следующего шага
    """
    temperature = 1

    response = requests.post(
        GPT_URL,
        headers={"Content-Type": "application/json"},
        json={
            "messages": messages,
            "temperature": temperature,
            "max_tokens": MAX_MODEL_TOKENS,
        },
    )
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        logging.info(f"Ответ нейросети: {result}")
        return result
    else:
        logging.error(f"Случилась ошибка. {response.text}")
