from __future__ import annotations

import json
import statistics
import time
import tracemalloc
from pathlib import Path

from .core import content_brief


def _p(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round((pct / 100) * (len(ordered) - 1))))]


def evaluate(path: str | Path, *, repeat: int = 1, brand: str = "CarbonFlow") -> dict:
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = complete = 0
    scores = []
    channels: dict[str, int] = {}
    latencies = []
    started = time.perf_counter()
    tracemalloc.start()
    for _ in range(repeat):
        for row in rows:
            t0 = time.perf_counter()
            try:
                brief = content_brief(str(row.get("text") or ""), brand=brand)
                ok = bool(brief["title"] and brief["meta_description"] and brief["outline"])
                complete += 1 if ok else 0
                scores.append(float(brief["quality_score"]))
                channels[brief["channel"]] = channels.get(brief["channel"], 0) + 1
            except Exception:
                errors += 1
            latencies.append((time.perf_counter() - t0) * 1000)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    processed = len(rows) * repeat
    return {
        "input": str(Path(path).resolve()),
        "records": len(rows),
        "repeat": repeat,
        "processed": processed,
        "complete": complete,
        "errors": errors,
        "quality_mean": statistics.fmean(scores) if scores else 0.0,
        "channels": channels,
        "latency_ms": {"mean": statistics.fmean(latencies) if latencies else 0.0, "p99": _p(latencies, 99), "max": max(latencies) if latencies else 0.0},
        "memory_mb": {"current": current / 1_000_000, "peak": peak / 1_000_000},
        "elapsed_seconds": time.perf_counter() - started,
        "collapse_check": {"passed": errors == 0, "criteria": "errors == 0"},
    }

