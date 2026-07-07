from __future__ import annotations

import json
from pathlib import Path


def convert_tweet_eval(input_path: str | Path, out_path: str | Path, *, limit: int = 0) -> dict:
    source = Path(input_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = 0
    labels: dict[str, int] = {}
    with source.open("r", encoding="utf-8") as handle, out.open("w", encoding="utf-8") as output:
        for line in handle:
            if limit and rows >= limit:
                break
            if not line.strip():
                continue
            record = json.loads(line)
            label = str(record.get("label", ""))
            item = {"text": record.get("text") or "", "label": label, "success": bool(record.get("success")), "source": "tweet_eval"}
            output.write(json.dumps(item, ensure_ascii=False) + "\n")
            labels[label] = labels.get(label, 0) + 1
            rows += 1
    return {"source": str(source.resolve()), "out": str(out.resolve()), "rows": rows, "labels": labels}

