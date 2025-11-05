from paddleocr import PaddleOCR
import autogen
import os

ocr_ru = PaddleOCR(
    use_textline_orientation=True,  # вместо use_angle_cls
    lang="ru",
)

ocr_en = PaddleOCR(
    use_textline_orientation=True,  # вместо use_angle_cls
    lang="en",
)
OCR_languages = {"ru": ocr_ru, "en": ocr_en}
