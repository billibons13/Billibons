"""CLI агента.

  python3 -m hunter prepare candidates.json [--amazon-tag meintag-21] > payloads.json
      candidates.json: [{"product": {...}, "signals": {"demand":0.7,"competition":0.4,"video_fit":0.9}}, ...]
      Выдаёт {"ready": [...], "rejected": [...]} — ready можно отправлять в Make.
  python3 -m hunter match scripts.txt
      Подбор типов товаров под недельные скрипты Klaus.
  python3 -m hunter link https://www.amazon.de/dp/ASIN
      Партнёрская ссылка по config.json (только ваши аккаунты, только официальный формат сети).
  python3 -m hunter learn records.json
      Фактическая статистика по категориям из выгрузки Make data store.
"""
import argparse
import json
import os
import sys

from .links import build
from .learning import category_stats, real_rates
from .matching import match_week
from .pipeline import prepare


def _config():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="hunter")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("prepare")
    pr.add_argument("file")
    pr.add_argument("--amazon-tag", default=os.environ.get("AMAZON_PARTNER_TAG") or _config().get("amazon_partner_tag"))
    pr.add_argument("--stats", help="выгрузка data store: EPM по факту вместо допущений, где данных достаточно")
    mt = sub.add_parser("match")
    mt.add_argument("file")
    lk = sub.add_parser("link")
    lk.add_argument("url")
    ln = sub.add_parser("learn")
    ln.add_argument("file")
    a = ap.parse_args(argv)

    if a.cmd == "prepare":
        items = json.load(open(a.file, encoding="utf-8"))
        stats = category_stats(json.load(open(a.stats, encoding="utf-8"))) if a.stats else {}
        ready, rejected = [], []
        for it in items:
            prod = it.get("product", it)
            payload, rep = prepare(prod, it.get("signals"), amazon_tag=a.amazon_tag,
                                   real_rates=real_rates(stats, prod.get("category")))
            (ready if payload else rejected).append(payload or rep)
            print(f"{rep.get('product_id')}: {rep.get('priority', 'ERROR')} "
                  f"{rep.get('score', '')} {'; '.join(rep['errors'] + rep['warnings'])}", file=sys.stderr)
        json.dump({"ready": ready, "rejected": rejected}, sys.stdout, ensure_ascii=False, indent=1)
    elif a.cmd == "link":
        url, net, status, cookie = build(a.url, _config())
        json.dump({"affiliate_url": url, "affiliate_network": net, "affiliate_status": status,
                   "cookie_duration_days": cookie}, sys.stdout, ensure_ascii=False)
    elif a.cmd == "learn":
        json.dump(category_stats(json.load(open(a.file, encoding="utf-8"))), sys.stdout, ensure_ascii=False, indent=1)
    else:
        json.dump(match_week(open(a.file, encoding="utf-8").read()), sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
