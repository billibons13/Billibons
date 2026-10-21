"""Бренд сборки (T-20261021-0044, переход RAIV FISH → FishDeck).

Выбор: переменная окружения BRAND_PROFILE = raiv (по умолчанию, сборка как раньше) | fishdeck.
  BRAND_PROFILE=fishdeck FD_BOT_USER=<username без @> FD_CONN=<ID подключения Make> python3 generate_blueprint.py out.json
Тексты пишутся с «RAIV FISH»; apply() меняет бренд в готовом JSON/HTML одной заменой.
Ключи localStorage витрины (raiv_cart, raiv_best) и ID хранилищ/сценариев НЕ меняются — иначе пропадут корзины и данные.
"""
import os

PROFILE = os.environ.get("BRAND_PROFILE", "raiv").lower()
FISHDECK = PROFILE == "fishdeck"

OLD_BRAND, OLD_BOT = "RAIV FISH", "RAIV_FISH_bot"
BRAND = "FishDeck" if FISHDECK else OLD_BRAND
# новый бот (решение владельца 21.10: вариант B) — username и подключение Make появятся после BotFather
BOT_USER = os.environ.get("FD_BOT_USER", "Fish_Deck_bot") if FISHDECK else OLD_BOT
CONN = int(os.environ.get("FD_CONN", "12180688")) if FISHDECK else None   # None — оставить подключение генератора
INSTAGRAM = "https://www.instagram.com/fish.deck_/" if FISHDECK else None
GROUP = "-1004468791786" if FISHDECK else None   # канал заказов «Fish_Deck» (бот — админ, проверено getUpdates 21.10)

REPLACE = [(OLD_BRAND, BRAND), (OLD_BOT, BOT_USER), ("RAIV_Fish", "FishDeck")] if FISHDECK else []


def apply(s):
    """Бренд в готовом тексте (JSON блюпринта, HTML витрины)."""
    for a, b in REPLACE:
        s = s.replace(a, b)
    return s


def check(s):
    """Предупреждения сборки FishDeck: что ещё не задано владельцем."""
    if not FISHDECK:
        return []
    w = []
    if "TBD" in BOT_USER:
        w.append("FD_BOT_USER не задан — username нового бота (BotFather)")
    if not CONN:
        w.append("FD_CONN не задан — подключение Make к новому боту")
    left = [x for x in ("RAIV FISH", "RAIV_FISH_bot") if x in s]
    if left:
        w.append("остался старый бренд: " + ", ".join(left))
    return w
