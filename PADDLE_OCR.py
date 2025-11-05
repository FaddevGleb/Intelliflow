from SETUP_MODELS_OCR import OCR_languages


def extract_text_from_paddleocr_result(result):
    """
    Извлекает текст из результата PaddleOCR, обрабатывая сложную структуру,
    которая может возвращаться при обработке PDF-файлов.

    Args:
        result: Результат, возвращаемый ocr.ocr() или ocr.predict() для PDF.
                Это может быть список словарей или список списков (страниц).

    Returns:
        str: Объединённый текст со всех страниц и блоков.
    """
    all_text_lines = []

    if not result:
        print("Предупреждение: Результат OCR пустой.")
        return ""

    # print(f"Отладка: Тип result[0]: {type(result[0])}") # Для отладки
    # print(f"Отладка: Структура первого элемента:\n{json.dumps(result[0], indent=2, ensure_ascii=False)}") # Для отладки

    for page_data in result:
        # page_data может быть словарём (если это результат обработки PDF с предобработкой)
        # или списком (если это "чистый" результат OCR для изображения/страницы)

        page_text_lines = []

        if isinstance(page_data, dict):
            # Структура, как в вашем первом примере (PDF с предобработкой)
            # Ищем ключи, содержащие результаты OCR
            ocr_results = page_data.get('rec_texts')  # Это список текстов
            if ocr_results:
                page_text_lines.extend(ocr_results)
            else:
                # Если 'rec_texts' нет, пробуем стандартную структуру внутри словаря
                # Иногда результаты OCR могут быть в 'dt_polys' и 'rec_texts' внутри 'doc_preprocessor_res'
                # или в корне словаря под ключом, например, 'dt_polys' и 'rec_texts' уже находятся на верхнем уровне
                # Проверим стандартный список блоков в словаре, если он есть
                # Этот путь менее вероятен для сложной структуры PDF, но на всякий случай
                standard_blocks = page_data.get('standard_blocks')  # НЕТ стандартного ключа в такой структуре
                # Нужно искать конкретно 'rec_texts' как делали выше

        elif isinstance(page_data, list):
            # Стандартная структура: [page1_blocks, page2_blocks, ...]
            # page_data (page1_blocks) - это список блоков [block1, block2, ...]
            # block выглядит как [[x1, y1], [x2, y2], [x3, y2], [x4, y1], (text, confidence)]
            for block in page_data:
                if isinstance(block, (list, tuple)) and len(block) >= 5:
                    text_info = block[4]  # или block[-1] - последний элемент
                    if isinstance(text_info, tuple) and len(text_info) >= 2:
                        text_content = text_info[0]
                        if text_content and str(text_content).strip():  # Проверяем, что текст не пустой
                            page_text_lines.append(str(text_content))
        else:
            print(f"Предупреждение: Неизвестный формат данных страницы: {type(page_data)}")
            continue

        # Фильтруем пустые строки на уровне страницы
        page_text_lines = [line for line in page_text_lines if line.strip()]
        all_text_lines.extend(page_text_lines)

    # Фильтруем пустые строки на общем уровне
    all_text_lines = [line for line in all_text_lines if line.strip()]

    # Объединяем все строки текста
    # Можно использовать "\n" для сохранения структуры строк
    # Или " " для простого объединения в один абзац
    final_text = "\n".join(all_text_lines)
    return final_text


def OCR(filepath, language="ru"):
    """
    Выполняет OCR на файле и возвращает извлечённый текст.

    Args:
        filepath (str): Путь к файлу (изображение или PDF).
        language (str): Язык ("ru" для русского, "en" для английского).

    Returns:
        str: Извлечённый текст.
    """
    ocr = OCR_languages[language]
    # Используем ocr.ocr() для получения результата в стандартном формате
    result = ocr.predict(filepath)  # cls=True включает классификацию ориентации, если use_textline_orientation не сработает
    # print(json.dumps(result, indent=2, ensure_ascii=False))  # Для отладки - можно раскомментировать, чтобы посмотреть структуру

    extracted_text = extract_text_from_paddleocr_result(result)
    return extracted_text


# Пример использования
"""file_path = "C:/Users/User/Documents/Экономическая модернизация в конце XIX – начале XX века.pdf"
try:
    extracted_text = OCR(file_path, language="ru")
    print("Извлечённый текст:")
    print(extracted_text)
except Exception as e:
    print(f"Произошла ошибка: {e}")"""