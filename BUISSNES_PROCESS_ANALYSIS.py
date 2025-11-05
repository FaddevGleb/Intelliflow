import autogen
from typing import List, Dict, Any
import json


class BusinessProcessAnalyzer:
    def __init__(self, config_list: List[Dict[str, str]]):
        """
        Инициализация системы агентов для анализа бизнес-процессов
        
        Args:
            config_list: Список конфигураций для LLM (OpenAI, Azure и т.д.)
        """
        self.config_list = config_list
        self.setup_agents()
    
    def setup_agents(self):
        """Настройка агентов системы"""
        
        # Агент-аналитик документов
        self.document_analyzer = autogen.AssistantAgent(
            name="Document_Analyzer",
            system_message="""Ты - эксперт по анализу документов и извлечению информации о бизнес-процессах.
            
            Твоя задача:
            1. Анализировать предоставленные документы
            2. Извлекать информацию о процессах, ролях, действиях
            3. Определять последовательность операций
            4. Выявлять входные и выходные данные процессов
            Начни свой анализ с объявления своей роли.
            Отвечай структурированно и подробно.""",
            llm_config={"config_list": self.config_list},

        )
        
        # Агент-процессный архитектор
        self.process_architect = autogen.AssistantAgent(
            name="Process_Architect", 
            system_message="""Ты - архитектор бизнес-процессов, специализирующийся на создании BPMN диаграмм.
            
            Твоя задача:
            1. Структурировать извлеченную информацию в логические блоки
            2. Определять участников процесса (роли, системы)
            3. Выделять основные этапы и подпроцессы
            4. Определять точки принятия решений и условия
            5. Формировать описание для BPMN диаграммы
            Начни свой анализ с объявления своей роли.
            Используй стандартную BPMN нотацию.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Агент-валидатор
        self.process_validator = autogen.AssistantAgent(
            name="Process_Validator",
            system_message="""Ты - валидатор бизнес-процессов, проверяющий корректность и полноту описания.
            
            Твоя задача:
            1. Проверять логическую последовательность этапов
            2. Убеждаться в наличии всех необходимых элементов
            3. Проверять соответствие BPMN стандартам
            4. Предлагать улучшения и исправления
            Начни свой анализ с объявления своей роли.
            Будь критичным и внимательным к деталям.
            Если выполненен необходимый анализ процесса и ты с ним согласен выведи TERMINATE""",
            llm_config={"config_list": self.config_list}
        )
        
        # Пользователь-прокси для взаимодействия
        self.user_proxy = autogen.UserProxyAgent(
            name="User_Proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
            code_execution_config=False
        )
    
    def analyze_business_process(self, prompt: str, documents: List[str]) -> Dict[str, Any]:
        """
        Основная функция анализа бизнес-процесса
        
        Args:
            prompt: Промпт с описанием задачи
            documents: Список текстов документов для анализа
            
        Returns:
            Словарь с результатами анализа
        """
        
        # Подготовка контекста
        context = f"""
        ЗАДАЧА: {prompt}
        
        ДОКУМЕНТЫ ДЛЯ АНАЛИЗА:
        {chr(10).join([f"Документ {i+1}: {doc}" for i, doc in enumerate(documents)])}
        
        ТРЕБУЕТСЯ:
        1. Проанализировать документы и извлечь информацию о бизнес-процессах
        2. Структурировать процесс в логические блоки
        3. Подготовить описание для создания BPMN диаграммы в Camunda
        4. Валидировать результат
        """
        
        # Создание группового чата
        groupchat = autogen.GroupChat(
            agents=[self.document_analyzer, self.process_architect, self.process_validator],
            messages=[],
            max_round=6,
            speaker_selection_method="round_robin"
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": self.config_list}
        )
        
        # Запуск анализа
        self.chat_result = self.user_proxy.initiate_chat(
            manager,
            message=context,
            summary_method="reflection_with_llm"
        )

        
        # Извлечение результатов из последних сообщений
        messages = groupchat.messages
        analysis_result = self._extract_analysis_result(messages)

        return self.chat_result
    
    def _extract_analysis_result(self, messages: List[Dict]) -> Dict[str, Any]:
        """Извлечение структурированного результата из сообщений агентов"""
        
        # Поиск финального результата от Process_Architect
        final_result = None
        for msg in reversed(messages):
            if msg.get("name") == "Process_Architect" and "BPMN" in msg.get("content", ""):
                final_result = msg.get("content", "")
                break
        
        if not final_result:
            # Если не найден структурированный результат, используем последнее сообщение
            final_result = messages[-1].get("content", "") if messages else "Анализ не завершен"
        
        return {
            "raw_analysis": final_result,
            "process_elements": self._parse_process_elements(final_result),
            "bpmn_ready": "BPMN" in final_result.upper(),
            "status": "completed" if final_result else "failed"
        }
    
    def _parse_process_elements(self, analysis_text: str) -> Dict[str, List[str]]:
        """Парсинг элементов процесса из текста анализа"""

        elements = {
            "participants": [],
            "activities": [],
            "decisions": [],
            "start_events": [],
            "end_events": []
        }

        # Простой парсинг ключевых слов (можно улучшить)
        text_lower = analysis_text.lower()
        return  text_lower
        # Поиск участников
        if "участник" in text_lower or "роль" in text_lower:
            # Здесь можно добавить более сложную логику парсинга
            pass

        # Поиск активностей
        if "процесс" in text_lower or "этап" in text_lower:
            # Здесь можно добавить более сложную логику парсинга
            pass

        return elements

def create_business_process_analysis_system(api_key: str, base_url: str = None) -> BusinessProcessAnalyzer:
    """
    Создание системы анализа бизнес-процессов
    
    Args:
        api_key: API ключ для LLM
        base_url: Базовый URL (опционально)
    
    Returns:
        Настроенная система анализа
    """
    
    config_list = [
        {
            "model": "openai/gpt-oss-20b:free",
            "api_key": api_key,
            "base_url": base_url or "https://openrouter.ai/api/v1"
        }
    ]
    
    return BusinessProcessAnalyzer(config_list)


# Пример использования
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Создание системы
    analyzer = create_business_process_analysis_system(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # Пример анализа
    prompt = "Проанализируй процесс обработки заказов в интернет-магазине"
    documents = [
        "Документ 1: Описание процесса приема заказов...",
        "Документ 2: Инструкция по обработке платежей...",
        "Документ 3: Процедура отгрузки товаров..."
    ]
    
    result = analyzer.analyze_business_process(prompt, documents)
    print(result)
