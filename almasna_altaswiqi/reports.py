from __future__ import annotations


def markdown(summary: dict, title: str = "تقرير المصنع التسويقي") -> str:
    return "\n".join(
        [
            f"# {title}",
            "",
            f"- المعالجة: `{summary.get('processed', 0)}`",
            f"- اكتمال المخرجات: `{summary.get('complete', 0)}`",
            f"- الأخطاء: `{summary.get('errors', 0)}`",
            f"- متوسط الجودة: `{summary.get('quality_mean', 0):.2f}`",
            f"- القنوات: `{summary.get('channels', {})}`",
            f"- p99: `{summary.get('latency_ms', {}).get('p99', 0):.4f}ms`",
            f"- peak memory: `{summary.get('memory_mb', {}).get('peak', 0):.2f}MB`",
            "",
        ]
    )

