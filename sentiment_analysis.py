import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import glob



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINBERT_PATH = os.path.join(BASE_DIR, "models", "finbert")

if not os.path.exists(FINBERT_PATH):
    raise FileNotFoundError(f"FinBERT folder not found at: {FINBERT_PATH}")

tokenizer = AutoTokenizer.from_pretrained(FINBERT_PATH)
model = AutoModelForSequenceClassification.from_pretrained(FINBERT_PATH)

finbert = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    top_k=None,   
    truncation=True,
)



def split_text(text: str, max_chars: int = 400) -> list[str]:

    text = text.strip()
    if not text:
        return []
    chunks = []
    for i in range(0, len(text), max_chars):
        chunk = text[i:i + max_chars].strip()
        if chunk:
            chunks.append(chunk)
    return chunks



def analyze_market_sentiment_en(text: str):

    text = text.strip()
    if not text:
        return 0.0, 0.0, 0.0

    chunks = split_text(text)
    if not chunks:
        return 0.0, 0.0, 0.0

    totals = {"positive": 0.0, "neutral": 0.0, "negative": 0.0}
    count = 0

    for ch in chunks:
        scores = finbert(ch)[0] 

        for s in scores:
            raw_label = s["label"].lower()
            score = s["score"]

            # Map flexible labels to positive/neutral/negative
            if "pos" in raw_label:
                totals["positive"] += score
            elif "neu" in raw_label:
                totals["neutral"] += score
            elif "neg" in raw_label:
                totals["negative"] += score
            elif raw_label in totals:
                totals[raw_label] += score

        count += 1

    if count == 0:
        return 0.0, 0.0, 0.0

    for k in totals:
        totals[k] /= count

    bullish = round(totals["positive"] * 100, 2)
    neutral = round(totals["neutral"] * 100, 2)
    bearish = round(totals["negative"] * 100, 2)

    return bullish, neutral, bearish



def analyze_file(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Check if the text is empty
    if not text.strip():
        print("The file is empty!")
        return 0.0, 0.0, 0.0

    # Analyze sentiment of the extracted text
    bullish, neutral, bearish = analyze_market_sentiment_en(text)


    return {"file": path, "data":{"bullish":bullish, "neutral": neutral, "bearish":bearish}}

