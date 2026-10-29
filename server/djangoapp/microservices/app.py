import json
import os

import nltk
from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer

# The VADER lexicon ships in ./sentiment/vader_lexicon.zip; let NLTK find it
nltk.data.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask("Sentiment Analyzer")

sia = SentimentIntensityAnalyzer()


@app.get('/')
def home():
    return "Welcome to the Sentiment Analyzer. \
    Use /analyze/text to get the sentiment"


@app.get('/analyze/<input_txt>')
def analyze_sentiment(input_txt):

    scores = sia.polarity_scores(input_txt)
    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])
    res = "positive"
    if (neg > pos and neg > neu):
        res = "negative"
    elif (neu > neg and neu > pos):
        res = "neutral"
    return app.response_class(
        json.dumps({"sentiment": res}), mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
