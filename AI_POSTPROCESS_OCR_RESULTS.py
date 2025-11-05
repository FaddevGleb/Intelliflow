from SETUP_MODELS_LLM import general_llm_20b, POSTPROCESSING_PROMPT_TEMPLATE


def PROCESS_OCR_RESULT(ocr_result):
    compiled_prompt = POSTPROCESSING_PROMPT_TEMPLATE.format_messages(text=ocr_result)
    processed_text = general_llm_20b.invoke(compiled_prompt)
    return processed_text.content