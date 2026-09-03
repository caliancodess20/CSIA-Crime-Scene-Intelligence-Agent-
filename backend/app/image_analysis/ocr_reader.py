import easyocr
reader = easyocr.Reader(['en'], gpu=False)
def extract_text(image_path: str):
    results = reader.readtext(image_path)
    extracted = []
    for (bbox, text, prob) in results:
        extracted.append({
            "text": text,
            "confidence": round(float(prob), 2)
        })
    return extracted
