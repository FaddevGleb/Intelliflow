from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatMessagePromptTemplate
import os
import dotenv

dotenv.load_dotenv()
general_llm_20b = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1")

llm_text_postprocessing_prompt = """Ты - эксперт по постобработке текста после OCR. Твоя задача - исправить артефакты, ошибки распознавания и улучшить качество текста.

ИНСТРУКЦИИ:
1. Исправь все ошибки OCR (замененные символы, пропущенные буквы, лишние символы)
2. Восстанови правильную пунктуацию и форматирование
3. Исправь опечатки и грамматические ошибки
4. Сохрани оригинальную структуру текста (абзацы, списки, заголовки)
5. Если текст содержит числа, даты, адреса - проверь их корректность
6. Сохрани специальные символы и форматирование где это уместно

ВАЖНО: 
- Выводи ТОЛЬКО исправленный текст
- НЕ добавляй комментарии, объяснения или метки
- НЕ изменяй смысл текста
- НЕ добавляй лишние пробелы или переносы строк

Исходный текст для исправления:
{text}

Исправленный текст:"""

POSTPROCESSING_PROMPT_TEMPLATE = ChatMessagePromptTemplate.from_template(
    role="system",
    template=llm_text_postprocessing_prompt
)

config_list = [{
    "model": "openai/gpt-oss-20b:free",
    "api_type": "together",
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "base_url": "https://openrouter.ai/api/v1",
    "max_tokens": 2048,
    "temperature": 0.7
}]
LLM_CONFIG = {"config_list": config_list}