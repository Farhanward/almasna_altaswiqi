# Changelog — almasna-altaswiqi

## 1.0.0 — 2026-07-05 (الترقية المؤسسية)

- **خدمة HTTP محلية**: `python -m almasna_altaswiqi.cli serve` — نقاط `/api/health` (مفتوحة) و`/api/version` و`/api/metrics` + نقاط النطاق.
- **Config مركزي عبر البيئة**: `almasna_altaswiqi/config.py` (متغيرات `ALMASNA_*`).
- **Observability**: `almasna_altaswiqi/observability.py` — سجلات JSON بتدوير تلقائي + عدادات وp50/p95/p99.
- **مصادقة وحدود**: `X-API-Key` بمقارنة constant-time عند ضبط `ALMASNA_API_KEY`، وحد حجم الطلب (413) مع تفريغ آمن للجسم.
- **تغليف**: `pyproject.toml` كامل مع entry point وأمر `version`.
- **توثيق تشغيل**: `docs/OPERATIONS.md`.
- **اختبارات enterprise**: config/metrics/auth/الخدمة عبر HTTP حقيقي على منفذ ephemeral.

## 0.1.0 — 2026-07-04

- المنتج الأولي + تحسين الجودة الإنتاجية الموثق في MASTER_REFERENCE.
