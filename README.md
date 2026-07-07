# المصنع التسويقي AlMasna AlTaswiqi

المصنع التسويقي أداة محلية لاستخراج فرص محتوى/SEO من نصوص كثيرة: يستخرج كلمات، يحدد زاوية المحتوى، يولد عنواناً ووصفاً وخطة نشر مختصرة.

## آلية العمل

1. `analyze` يحلل نصاً واحداً ويولد brief.
2. `convert-tweets` يحول بيانات tweet_eval إلى مدخلات تسويقية.
3. `batch/stress` يقيسان اكتمال المخرجات والانهيار.

## تشغيل سريع

```powershell
python -m almasna_altaswiqi.cli analyze --text "fast automation saves time"
python -m almasna_altaswiqi.cli convert-tweets
python -m almasna_altaswiqi.cli batch
```

## بيانات الاختبار

المصدر: Hugging Face `cardiffnlp/tweet_eval` المحفوظ داخل `C:\Projects\alnabd` بعدد 12,000 منشور.

## آخر نتائج

- الاختبارات الذاتية: 2/2 ناجحة.
- بيانات الإنترنت: 12,000 منشور tweet_eval (4,680 إيجابي، 5,452 محايد، 1,868 سلبي).
- Benchmark: 12,000 معالجة، complete=12,000، errors=0، quality_mean=98.15، p99=0.168ms.
- Stress: 36,000 معالجة، errors=0، p99=0.162ms، peak memory=2.40MB.
- توزيع القنوات في batch: social=7,995، blog=4,005.

## تحسينات إنتاجية 2026-07-04

- كل brief يحتوي عنواناً، meta description، channel، CTA، outline، وquality_score.
- يتم فصل زاوية المحتوى إلى `حل مشكلة/قيمة/توعية` حسب إشارات الألم والقيمة.
- batch/stress يقيسان اكتمال المخرجات وليس مجرد عدم حدوث أخطاء.

## التشغيل المؤسسي (Enterprise) — v1.0.0

- **خدمة briefs عبر HTTP**: `python -m almasna_altaswiqi.cli serve` → `POST /api/brief {"text","brand"}` يعيد brief كامل بschema ثابت.
- **نقاط فحص**: `/api/health` (مفتوح) · `/api/version` · `/api/metrics`.
- **تهيئة عبر البيئة**: متغيرات `ALMASNA_*` — انظر `docs/OPERATIONS.md`.
- **مصادقة**: `ALMASNA_API_KEY` → ترويسة `X-API-Key`. **سجلات JSON**: `logs\almasna-altaswiqi.service.jsonl`.
