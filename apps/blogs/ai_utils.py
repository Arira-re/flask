from transformers import pipeline

MODEL_NAME = "Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime"
sentiment_analyzer = pipeline("text-classification", model=MODEL_NAME)

def get_sentiment_score(text):
    results = sentiment_analyzer(text)
    pos_labels = {"喜び", "期待", "信頼"}
    neg_labels = {"悲しみ", "怒り", "恐れ", "嫌悪"}
    score = 0
    total = 0
    for r in results:
        total += r["score"]
        if r["label"] in pos_labels:
            score += r["score"]
        elif r["label"] in neg_labels:
            score -= r["score"]
    score_normalized = score / total if total != 0 else 0  # -1～1に正規化
    return score_normalized