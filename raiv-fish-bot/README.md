# RAIV_Fish Bot — заказы (Make)

Telegram-бот заказов по образцу «Rybka Bot — Заказы» (Rybka Eddelak), с ассортиментом RAIV FISH.

- Сценарий Make: `RAIV_Fish Bot — Заказы` (id 7706268)
- Вебхук: https://hook.eu1.make.com/xykao4wf3fux8knvlu4y2vuva6mhtz82

## Как изменить цены / наличие
Отредактируйте список `cats` в `generate_blueprint.py` (третье значение: 1 — в наличии, 0 — нет ❌),
запустите `python3 generate_blueprint.py` и загрузите `bp.json` в сценарий.

## Шаги диалога
Меню (весь прайс) → раздел → товар → вес/кол-во → город → оплата → адрес → телефон → заказ в группу.
