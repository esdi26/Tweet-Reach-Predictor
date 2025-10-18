from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from textblob import TextBlob
import re

app = FastAPI()

@app.post("/api/score")
async def score(request: Request):
    data = await request.json()
    tweet = data.get("tweet", "").strip()
    tweet_lower = tweet.lower()

    sentiment = TextBlob(tweet).sentiment.polarity
    score = 0
    reasons = []
    suggestions = []

    # === Elon Musk ===
    if "elon" in tweet_lower:
        if sentiment >= 0:
            score += 100
            reasons.append("+ Mentioned Elon positively")
        else:
            score -= 100
            reasons.append("- Spoke negatively about Elon")
            suggestions.append("Try keeping Elon mentions positive.")
    
    # === Tesla ===
    if "tesla" in tweet_lower:
        if sentiment >= 0:
            score += 100
            reasons.append("+ Mentioned Tesla positively")
        else:
            score -= 100
            reasons.append("- Spoke negatively about Tesla")
            suggestions.append("Keep Tesla mentions optimistic.")
    
    # === Emojis ===
    emojis = ["🚀", "💫", "🚘", "❤️", "🤖", "🌞", "🌍", "🥳"]
    emoji_count = sum(tweet.count(e) for e in emojis)
    if emoji_count > 0:
        score += 10 * emoji_count
        reasons.append(f"+ Used {emoji_count} Elon-style emoji(s)")
    else:
        suggestions.append("Add emojis like 🚀💫❤️ to boost engagement.")
    
    # === Sentiment impact ===
    if sentiment >= 0.5:
        score -= 30
        reasons.append("- Too positive, not edgy enough")
        suggestions.append("Be slightly controversial or humorous.")
    elif sentiment <= -0.5:
        score += 50
        reasons.append("+ Negative/controversial tone (viral)")
    
    # === Thread ===
    if "🧵" in tweet or "thread" in tweet_lower:
        score += 50
        reasons.append("+ Thread detected")
    
    # === Confidence words ===
    confident_words = ["definitely", "always", "never", "must", "only"]
    conf_count = sum(tweet_lower.count(w) for w in confident_words)
    if conf_count > 0:
        score += 20 * conf_count
        reasons.append(f"+ {conf_count} confident phrase(s)")
    else:
        suggestions.append("Use strong words like 'always', 'never', 'must'.")
    
    # === Questions ===
    if "?" in tweet:
        score -= 25
        reasons.append("- Question detected (reduces confidence)")
        suggestions.append("Avoid using too many questions.")
    
    # === Exclamations ===
    exclamations = len(re.findall(r"!", tweet))
    if exclamations > 0:
        score += 5 * exclamations
        reasons.append(f"+ {exclamations} exclamation(s)")
    
    # === All caps / lowercase ===
    if tweet.isupper():
        score += 60
        reasons.append("+ ALL CAPS = Big energy")
    elif tweet.islower():
        score += 40
        reasons.append("+ All lowercase = Nihilistic energy")
    
    # === Score bounds ===
    score = max(-100, min(score, 100))
    tone = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"

    response = {
        "score": score,
        "sentiment": round(sentiment, 2),
        "tone": tone,
        "reasons": reasons,
        "suggestions": suggestions
    }

    return JSONResponse(response)
