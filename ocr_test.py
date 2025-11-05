from PADDLE_OCR import OCR
from AI_POSTPROCESS_OCR_RESULTS import PROCESS_OCR_RESULT

text = OCR("C:/Users/User/Documents/Экономическая модернизация в конце XIX – начале XX века.pdf")
corrected = PROCESS_OCR_RESULT(text)
print(corrected)