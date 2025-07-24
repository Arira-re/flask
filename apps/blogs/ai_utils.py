from transformers import pipeline

MODEL_NAME = "Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime"
sentiment_analyzer = pipeline("text-classification", model=MODEL_NAME)

LABEL_MAP = {
    "LABEL_0": "喜び",
    "LABEL_1": "期待",
    "LABEL_2": "信頼",
    "LABEL_3": "怒り",
    "LABEL_4": "嫌悪",
    "LABEL_5": "恐れ",
    "LABEL_6": "悲しみ",
    "LABEL_7": "驚き"
}

POSITIVE_LABELS = {"喜び", "期待", "信頼"}
NEGATIVE_LABELS = {"怒り", "嫌悪", "恐れ", "悲しみ"}

def get_sentiment_score(text):
    results = sentiment_analyzer(text)
    print("モデル返却:", results)
    if not results:
        return 0.0

    top = max(results, key=lambda x: x["score"])
    label_name = LABEL_MAP.get(top["label"], None)
    print("topラベル:", top["label"], "->", label_name)

    if label_name in POSITIVE_LABELS:
        return top["score"]
    elif label_name in NEGATIVE_LABELS:
        return -top["score"]
    else:
        return 0.0