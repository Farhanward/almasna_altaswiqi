from __future__ import annotations

import re
from collections import Counter


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_#'-]{2,}|[\u0600-\u06ff]{2,}", re.I)
STOPWORDS = {"the", "and", "for", "with", "you", "your", "this", "that", "from", "about", "into", "what", "how", "why", "في", "من", "على", "عن", "هذا", "هذه", "كيف"}
PAIN = {"problem", "fail", "slow", "expensive", "angry", "bad", "مشكلة", "بطيء", "غالي"}
VALUE = {"easy", "fast", "save", "new", "free", "simple", "proven", "سهل", "سريع", "وفر", "جديد"}


def tokens(text: str) -> list[str]:
    return [tok for tok in (m.group(0).casefold() for m in TOKEN_RE.finditer(text)) if tok not in STOPWORDS]


def analyze_text(text: str, *, brand: str = "CarbonFlow") -> dict:
    ts = tokens(text)
    counts = Counter(ts)
    keywords = [word for word, _ in counts.most_common(8)]
    low = text.casefold()
    pain = sum(1 for word in PAIN if word in low)
    value = sum(1 for word in VALUE if word in low)
    angle = "حل مشكلة" if pain > value else "قيمة/توفير" if value else "توعية"
    primary = keywords[0] if keywords else "automation"
    title = f"{brand}: {primary} بدون تعقيد"
    meta = f"دليل عملي عن {primary} مع خطوات واضحة ونتيجة قابلة للقياس."
    channel = "blog" if len(text) > 120 else "social"
    return {
        "brand": brand,
        "angle": angle,
        "keywords": keywords,
        "title": title[:70],
        "meta_description": meta[:155],
        "channel": channel,
        "cta": "احجز مراجعة مجانية" if angle == "حل مشكلة" else "ابدأ بخطوة صغيرة اليوم",
        "quality_score": min(100, 35 + 8 * len(keywords) + 12 * value + 10 * pain),
    }


def content_brief(text: str, *, brand: str = "CarbonFlow") -> dict:
    analysis = analyze_text(text, brand=brand)
    outline = [
        f"المشكلة أو الفرصة: {analysis['angle']}",
        f"الكلمات المستهدفة: {', '.join(analysis['keywords'][:5])}",
        "برهان أو مثال محلي",
        f"دعوة إجراء: {analysis['cta']}",
    ]
    return {**analysis, "outline": outline}

