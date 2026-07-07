from __future__ import annotations

import argparse
import json
from pathlib import Path

from .batch import evaluate
from .core import content_brief
from .datasets import convert_tweet_eval
from .reports import markdown


def _write_json(path: str | Path, data: dict) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="almasna-altaswiqi", description="المصنع التسويقي: SEO ورادار فرص محلي.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("--text", required=True)
    analyze.add_argument("--brand", default="CarbonFlow")
    convert = sub.add_parser("convert-tweets")
    convert.add_argument("--input", default="C:/Projects/alnabd/data/external/tweet_eval_sentiment_12000.jsonl")
    convert.add_argument("--out", default="data/benchmarks/almasna_tweet_eval_marketing.jsonl")
    convert.add_argument("--limit", type=int, default=12000)
    batch = sub.add_parser("batch")
    batch.add_argument("--input", default="data/benchmarks/almasna_tweet_eval_marketing.jsonl")
    batch.add_argument("--brand", default="CarbonFlow")
    batch.add_argument("--json-out", default="reports/almasna_benchmark.json")
    batch.add_argument("--report", default="reports/almasna_benchmark.md")
    stress = sub.add_parser("stress")
    stress.add_argument("--input", default="data/benchmarks/almasna_tweet_eval_marketing.jsonl")
    stress.add_argument("--brand", default="CarbonFlow")
    stress.add_argument("--repeat", type=int, default=3)
    stress.add_argument("--json-out", default="reports/almasna_stress.json")
    stress.add_argument("--report", default="reports/almasna_stress.md")
    serve = sub.add_parser("serve")
    serve.add_argument("--host")
    serve.add_argument("--port", type=int)
    sub.add_parser("version")
    args = parser.parse_args(argv)
    if args.cmd == "serve":
        from .service import run_server

        run_server(host=args.host, port=args.port)
        return 0
    if args.cmd == "version":
        from .version import __version__

        print(json.dumps({"service": "almasna-altaswiqi", "version": __version__}, ensure_ascii=False))
        return 0
    if args.cmd == "analyze":
        print(json.dumps(content_brief(args.text, brand=args.brand), ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "convert-tweets":
        print(json.dumps(convert_tweet_eval(args.input, args.out, limit=args.limit), ensure_ascii=False, indent=2))
        return 0
    if args.cmd in {"batch", "stress"}:
        summary = evaluate(args.input, repeat=getattr(args, "repeat", 1), brand=args.brand)
        _write_json(args.json_out, summary)
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(markdown(summary, "تقرير ضغط المصنع التسويقي" if args.cmd == "stress" else "تقرير المصنع التسويقي"), encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if summary["collapse_check"]["passed"] else 2
    raise ValueError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())

