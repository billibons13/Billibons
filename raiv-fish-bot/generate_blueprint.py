import json, re
CONN = 11456488  # RAIV_Fish Telegram Bot
GROUP = "-1004438320479"  # канал RAIVFISH
HOOK = 3818482  # v2 webhook (рабочий)
cats = [
 ("a","🐟 Икра вяленая (100 г)",[("Икра толстолоба","6",1),("Икра кеты","8.5",1),("Икра форели","8.5",1),("Икра судака","6.5",0),("Икра щуки","7",1),("Икра плотвы","7",0),("Икра минтая","6.5",0)]),
 ("b","🐠 Рыба вяленая (кг)",[("Плотва с икрой","35",1),("Чищенные тушки плотвы без головы (100% икра)","49",1),("Вобла с икрой (80% икра)","30",1),("Верховодка","35",1),("Лещ с икрой","35",1),("Лещ без икры","20",0),("Карась с икрой","23",1),("Щука потрошеная","25",1),("Форель вяленая потрошеная","35",1),("Судак потрошеный","30",1),("Чехонь","25",1),("Чехонь крупная с икрой 90%","35",1),("Бычок","34",1),("Корюшка с икрой (премиум)","60",0),("Окунь с икрой","34",1),("Юкола лосося","67",1)]),
 ("c","🍢 Рыбные снеки (100 г)",[("Филе горбуши (соломка)","6",1),("Кальмар + лосось (соломка)","4.9",1),("Корюшка сушеная потрошеная","5.5",1),("Соломка леща","3.5",1),("Джерки лосося","6",1),("Ириска из лосося","6",1),("Стейк щуки","4.5",1)]),
 ("d","🦑 Снеки к пиву (кг)",[("Пятачки осьминога","40",1),("Паутинка кальмара «сладкий чили»","40",1),("Кальмар по-шанхайски","40",1),("Стружка кальмара","40",1),("Палочки патасу","40",1),("Филе голубого марлина","40",1),("Кальмар по-перуански","40",1),("Полосатик","40",1),("Стружка краба","40",1),("Анчоус","40",1),("Крабовые палочки","40",1)]),
 ("e","🥫 Консервы",[("Снеток в томате","5",1),("Лещ в томате","5",1)]),
]
UNIT = {"a":"g","b":"k","c":"g","d":"k","e":"p"}
ULBL = {"a":"€ / 100 г","b":"€ / кг","c":"€ / 100 г","d":"€ / кг","e":"€ / шт."}
QTY = {"a":["100","200","300","500"],"b":["0.5","1","1.5","2"],"c":["100","200","300","500"],"d":["0.2","0.3","0.5","1"],"e":["1","2","3","5"]}
QL = {"g":"г","k":"кг","p":"шт."}
HINT = {"g":"в граммах, например 250","k":"в кг, например 0,7","p":"в штуках, например 4"}
DS = 203268  # data store «RAIV_Fish — корзины покупателей»
CUST = 203277   # клиенты: база, бонусы, история
ORD = 203280    # все заказы
PROMO = 203278  # промокоды (/promo) и КАТАЛОГ: записи cat_<код> — цена, наличие (владелец: /price, /stock)
CATALOG_API = "https://hook.eu1.make.com/hzm5bgeixv8k4652x3ofaaxw378nwyhu"  # сценарий 7708101: цены и наличие для витрины
STATS = 203279  # продажи по дням (для ежедневного отчёта)
OWNER_ID = "6883357001"  # владелец магазина: команды /admin /promo /send /report
BONUS_PCT = 5   # начисление бонусов, % от суммы к оплате
BONUS_CAP = 20  # бонусами можно оплатить не больше этого % заказа
TZ = "Europe/Berlin"
MIN_ORDER = 20   # минимальная сумма заказа, €
MAX_KG, MAX_G, MAX_PCS = 10, 5000, 50   # лимиты «Своего веса»: кг, граммы, штуки
PROMO_MAX = 50                       # /promo: скидка не больше 50 %
STRIPE_PUBLIC = False                # тестовый ключ Stripe — кнопку оплаты видит только владелец
REF_BONUS = 3    # «приведи друга»: бонус другу сразу и пригласившему после первого заказа друга
BOT_USER = "RAIV_FISH_bot"
WEBAPP = "https://billibons13.github.io/Billibons/?v=9"  # ?v= — сброс кэша Telegram Desktop  # Mini App витрина: ветка gh-pages (собирается из miniapp/, generate_miniapp.py)
WEBAPP_V = "2"  # поднять, чтобы заново выдать кнопку витрины всем клиентам
STRIPE_CONN = 11458868  # Stripe (test) — онлайн-оплата (Pro)
BOT_URL = "https%3A%2F%2Ft.me%2FRAIV_FISH_bot"
items = {}
for c,_,lst in cats:
    for i,(n,p,s) in enumerate(lst,1): items[f"{c}{i}"]=(n,p,s)

# ==== v9.6: языки клиента ru / de / es / uk ====
# Язык хранится в записи клиента (data store CUST, поле lang). Пока поля нет — определяется по
# language_code из Telegram (de/es/uk, иначе ru). Выбор: кнопка «🌐 Язык» и /language (callback lg → ln|<код>).
# Всё, что видит клиент, — через T()/S(): switch(lang; "de"; …; "es"; …; "uk"; …; "<ru>").
# Владельцу (карточка заказа, канал, команды, отчёты) — только русский.
LANGS = ("ru","de","es","uk")
LANG_NAMES = {"ru":"Русский","de":"Deutsch","es":"Español","uk":"Українська"}
DETECT = ('switch(substring(lower(ifempty(1.callback_query.from.language_code; ifempty(1.message.from.language_code; "ru"))); 0; 2); '
          '"de"; "de"; "es"; "es"; "uk"; "uk"; "ru")')
LANG0 = "ifempty(95.lang; " + DETECT + ")"   # для модуля 2 (сам на себя ссылаться не может)
LG = "2.lang"                                 # во всех маршрутах после модуля 2
TR_LOG = {}                                   # ru → (ru, de, es, uk) — для таблицы переводов
def _chk(x):
    assert '"' not in x and "{{" not in x and "}}" not in x and ";" not in x and "\n" not in x, repr(x)
def _log(vals):
    TR_LOG.setdefault(vals[0], tuple(vals))
def S(ru, de, es, uk, lang=LG, log=True):
    """Формула (без {{ }}) — строка на языке клиента."""
    vals = (ru, de, es, uk)
    for x in vals: _chk(x)
    if log: _log(vals)
    br = [f'"{L}"; "{v}"' for L, v in zip(LANGS[1:], vals[1:]) if v != ru]
    return f'"{ru}"' if not br else f'switch({lang}; ' + "; ".join(br) + f'; "{ru}")'
_FRM = re.compile(r"(\{\{.*?\}\})", re.S)
def T(ru, de, es, uk, lang=LG):
    """Шаблон с {{формулами}}: формулы одинаковы во всех языках и в том же порядке, переводится текст между ними
    (построчно, число строк одинаковое)."""
    toks = [_FRM.split(x) for x in (ru, de, es, uk)]
    assert len({len(t) for t in toks}) == 1, ("разное число формул", ru, de)
    _log(tuple(_FRM.sub("{…}", x) for x in (ru, de, es, uk)))
    out = []
    for i in range(len(toks[0])):
        if i % 2:
            assert len({t[i] for t in toks}) == 1, ("формулы различаются", [t[i] for t in toks]); out.append(toks[0][i]); continue
        parts = [t[i].split("\n") for t in toks]
        assert len({len(p) for p in parts}) == 1, ("разное число строк", [t[i] for t in toks])
        pcs = []
        for j in range(len(parts[0])):
            vals = [p[j] for p in parts]
            pcs.append(vals[0] if len(set(vals)) == 1 else "{{" + S(*vals, lang=lang, log=False) + "}}")
        out.append("\n".join(pcs))
    return "".join(out)
def TT(tr, lang=LG): return T(*tr, lang=lang)   # tr = (ru, de, es, uk)
def SS(tr, lang=LG): return S(*tr, lang=lang)
# названия разделов (как в cats) и товаров по коду: (de, es, uk); ru — из каталога (data store)
CAT_TR = {
 "a":("🐟 Getrockneter Fischrogen (100 g)","🐟 Huevas secas (100 g)","🐟 Ікра в’ялена (100 г)"),
 "b":("🐠 Getrockneter Fisch (kg)","🐠 Pescado seco (kg)","🐠 Риба в’ялена (кг)"),
 "c":("🍢 Fischsnacks (100 g)","🍢 Snacks de pescado (100 g)","🍢 Рибні снеки (100 г)"),
 "d":("🦑 Snacks zum Bier (kg)","🦑 Snacks para cerveza (kg)","🦑 Снеки до пива (кг)"),
 "e":("🥫 Konserven","🥫 Conservas","🥫 Консерви")}
NAMES = {
 "a1":("Silberkarpfen-Rogen","Huevas de carpa plateada","Ікра товстолоба"),
 "a2":("Ketalachs-Rogen","Huevas de salmón keta","Ікра кети"),
 "a3":("Forellenrogen","Huevas de trucha","Ікра форелі"),
 "a4":("Zanderrogen","Huevas de lucioperca","Ікра судака"),
 "a5":("Hechtrogen","Huevas de lucio","Ікра щуки"),
 "a6":("Rotaugenrogen","Huevas de rutilo","Ікра плітки"),
 "a7":("Alaska-Seelachs-Rogen","Huevas de abadejo de Alaska","Ікра минтаю"),
 "b1":("Rotauge mit Rogen","Rutilo con huevas","Плітка з ікрою"),
 "b2":("Rotauge geputzt, ohne Kopf (100 % Rogen)","Rutilo limpio sin cabeza (100 % huevas)","Чищені тушки плітки без голови (100% ікра)"),
 "b3":("Wobla mit Rogen (80 % Rogen)","Vobla con huevas (80 % huevas)","Вобла з ікрою (80% ікра)"),
 "b4":("Ukelei","Alburno","Верховодка"),
 "b5":("Brachse mit Rogen","Brema con huevas","Лящ з ікрою"),
 "b6":("Brachse ohne Rogen","Brema sin huevas","Лящ без ікри"),
 "b7":("Karausche mit Rogen","Carpín con huevas","Карась з ікрою"),
 "b8":("Hecht, ausgenommen","Lucio eviscerado","Щука потрошена"),
 "b9":("Forelle getrocknet, ausgenommen","Trucha seca eviscerada","Форель в’ялена потрошена"),
 "b10":("Zander, ausgenommen","Lucioperca eviscerada","Судак потрошений"),
 "b11":("Sichling","Chejon","Чехоня"),
 "b12":("Sichling groß, mit Rogen 90 %","Chejon grande con huevas 90 %","Чехоня велика з ікрою 90%"),
 "b13":("Grundel","Gobio","Бичок"),
 "b14":("Stint mit Rogen (Premium)","Eperlano con huevas (premium)","Корюшка з ікрою (преміум)"),
 "b15":("Barsch mit Rogen","Perca con huevas","Окунь з ікрою"),
 "b16":("Lachs-Jukola","Yukola de salmón","Юкола лосося"),
 "c1":("Buckellachsfilet (Streifen)","Filete de salmón rosado (tiras)","Філе горбуші (соломка)"),
 "c2":("Tintenfisch + Lachs (Streifen)","Calamar + salmón (tiras)","Кальмар + лосось (соломка)"),
 "c3":("Stint getrocknet, ausgenommen","Eperlano seco eviscerado","Корюшка сушена потрошена"),
 "c4":("Brachsen-Streifen","Tiras de brema","Соломка ляща"),
 "c5":("Lachs-Jerky","Jerky de salmón","Джерки лосося"),
 "c6":("Lachs-Toffee","Toffee de salmón","Іриска з лосося"),
 "c7":("Hechtsteak","Steak de lucio","Стейк щуки"),
 "d1":("Oktopus-Scheiben","Rodajas de pulpo","П’ятачки восьминога"),
 "d2":("Tintenfisch-Netz „Sweet Chili“","Red de calamar «chili dulce»","Павутинка кальмара «солодкий чилі»"),
 "d3":("Tintenfisch nach Shanghai-Art","Calamar al estilo Shanghái","Кальмар по-шанхайськи"),
 "d4":("Tintenfisch-Raspeln","Virutas de calamar","Стружка кальмара"),
 "d5":("Patasu-Sticks","Palitos de patasu","Палички патасу"),
 "d6":("Blauer-Marlin-Filet","Filete de marlín azul","Філе блакитного марліна"),
 "d7":("Tintenfisch nach peruanischer Art","Calamar al estilo peruano","Кальмар по-перуанськи"),
 "d8":("Polosatik","Polosatik","Полосатик"),
 "d9":("Krabben-Raspeln","Virutas de cangrejo","Стружка краба"),
 "d10":("Sardellen","Anchoas","Анчоус"),
 "d11":("Surimi-Sticks","Palitos de cangrejo","Крабові палички"),
 "e1":("Stint in Tomatensoße","Eperlano en tomate","Снеток у томаті"),
 "e2":("Brachse in Tomatensoße","Brema en tomate","Лящ у томаті")}
assert set(NAMES) == set(items), set(items) ^ set(NAMES)
for _k, _v in NAMES.items():
    for _x in _v: _chk(_x)
def NAMEX(code, ru, lang=LG):
    """Название товара по коду на языке клиента; нет перевода — русское название из каталога (ru)."""
    br = []
    for i, L in enumerate(LANGS[1:]):
        pairs = [f'"{k}"; "{NAMES[k][i]}"' for k in items if NAMES[k][i] != items[k][0]]
        if pairs: br.append(f'"{L}"; switch({code}; ' + "; ".join(pairs) + f"; {ru})")
    return f"switch({lang}; " + "; ".join(br) + f"; {ru})"
def CATT(c, lang=LG):
    t = next(t for k, t, _ in cats if k == c); return T(t, *CAT_TR[c], lang=lang)
def CATS(c, lang=LG):
    t = next(t for k, t, _ in cats if k == c); return S(t, *CAT_TR[c], lang=lang)
# единицы
U_G   = ("г","g","g","г")
U_KG  = ("кг","kg","kg","кг")
U_PCS = ("шт.","Stk.","ud.","шт.")
UL_G  = ("€ / 100 г","€ / 100 g","€ / 100 g","€ / 100 г")
UL_KG = ("€ / кг","€ / kg","€ / kg","€ / кг")
UL_PCS= ("€ / шт.","€ / Stk.","€ / ud.","€ / шт.")
def UNIT_L(cat, lang=LG):  return f'switch({cat}; "a"; {S(*U_G,lang=lang)}; "c"; {S(*U_G,lang=lang)}; "e"; {S(*U_PCS,lang=lang)}; {S(*U_KG,lang=lang)})'
def ULBL_L(cat, lang=LG):  return f'switch({cat}; "a"; {S(*UL_G,lang=lang)}; "c"; {S(*UL_G,lang=lang)}; "e"; {S(*UL_PCS,lang=lang)}; {S(*UL_KG,lang=lang)})'
QL_L = {"g":U_G, "k":U_KG, "p":U_PCS}
HINT_L = {"g":("в граммах, например 250","in Gramm, z. B. 250","en gramos, por ejemplo 250","у грамах, наприклад 250"),
          "k":("в кг, например 0,7","in kg, z. B. 0,7","en kg, por ejemplo 0,7","у кг, наприклад 0,7"),
          "p":("в штуках, например 4","in Stück, z. B. 4","en unidades, por ejemplo 4","у штуках, наприклад 4")}
# частые подписи кнопок и фраз
B_TOSHOP = ("📋 К покупкам","📋 Zum Einkaufen","📋 Ir a la tienda","📋 До покупок")
B_CHOOSE = ("📋 Выбрать товары","📋 Artikel auswählen","📋 Elegir productos","📋 Обрати товари")
B_ORDER  = ("🧾 Оформить заказ","🧾 Bestellung aufgeben","🧾 Hacer el pedido","🧾 Оформити замовлення")
B_MORE   = ("➕ Добавить ещё","➕ Weitere Artikel","➕ Añadir más","➕ Додати ще")
B_CLEAR  = ("🗑 Очистить корзину","🗑 Warenkorb leeren","🗑 Vaciar el carrito","🗑 Очистити кошик")
B_CART   = ("🧺 Корзина / оформить","🧺 Warenkorb / bestellen","🧺 Carrito / pedir","🧺 Кошик / оформити")
B_ALLCAT = ("⬅️ Все разделы","⬅️ Alle Kategorien","⬅️ Todas las secciones","⬅️ Усі розділи")
B_WEIGHT = ("✏️ Свой вес","✏️ Eigene Menge","✏️ Otra cantidad","✏️ Своя вага")
B_SELLER = ("💬 Написать продавцу","💬 Verkäufer schreiben","💬 Escribir al vendedor","💬 Написати продавцю")
B_LANG   = ("🌐 Язык","🌐 Sprache","🌐 Idioma","🌐 Мова")
P_CHOOSE_CAT = ("Выберите раздел 👇","Bitte wählen Sie eine Kategorie 👇","Elija una sección 👇","Оберіть розділ 👇")
P_TOTAL  = ("💶 Итого:","💶 Summe:","💶 Total:","💶 Разом:")
P_YOURCART = ("🧺 Ваша корзина:","🧺 Ihr Warenkorb:","🧺 Su carrito:","🧺 Ваш кошик:")
# метки, по которым бот узнаёт ответ клиента (force_reply) — по всем языкам
H_ORDER = ("🧾 Ваш заказ","🧾 Ihre Bestellung","🧾 Su pedido","🧾 Ваше замовлення")
H_ADDR  = ("Адрес доставки:","Lieferadresse:","Dirección de entrega:","Адреса доставки:")
H_PROMO = ("🎟 Промокод","🎟 Gutscheincode","🎟 Código promocional","🎟 Промокод")
H_CODE  = ("код:","Code:","código:","код:")

# ---- module 90: unify callback / custom-weight reply into one "d" string + chat id
RT = 'ifempty(1.message.reply_to_message.text; "")'
# v9.6: подсказка «✏️ …» на любом языке; код товара — после последнего «:» («код: b5», «Code: b5», …)
IS_W = f'contains({RT}; "✏️")'
W_CODE = f'trim(last(split({RT}; ":")))'
W_TXT = 'lower(trim(ifempty(1.message.text; "")))'
# единицы и латиницей: kg, g, stk, uds/ud
W_NUM = 'parseNumber(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace('+W_TXT+'; "кг"; ""); "kg"; ""); "шт"; ""); "stk"; ""); "uds"; ""); "ud"; ""); "г"; ""); "g"; ""); " "; ""); ","; "."); ".")'
W_UNIT = 'if(contains('+W_TXT+'; "кг"); "k"; if(contains('+W_TXT+'; "kg"); "k"; if(contains('+W_TXT+'; "г"); "g"; if(contains('+W_TXT+'; "g"); "g"; ""))))'
W_CAT = 'substring('+W_CODE+'; 0; 1)'
# «700 г» в разделе «кг» → 0,7 кг; «1 кг» в разделе «100 г» → 1000 г
W_QTY = ('switch('+W_CAT+'; "b"; if('+W_UNIT+' = "g"; '+W_NUM+' / 1000; '+W_NUM+'); "d"; if('+W_UNIT+' = "g"; '+W_NUM+' / 1000; '+W_NUM+'); '
         '"a"; if('+W_UNIT+' = "k"; '+W_NUM+' * 1000; '+W_NUM+'); "c"; if('+W_UNIT+' = "k"; '+W_NUM+' * 1000; '+W_NUM+'); '+W_NUM+')')
d_val = ("{{1.callback_query.data}}"
         + "{{if(" + IS_W + '; "q|"; "")}}'
         + "{{if(" + IS_W + "; " + W_CODE + '; "")}}'
         + "{{if(" + IS_W + '; "|"; "")}}'
         + "{{if(" + IS_W + "; " + W_QTY + '; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/orders"; "h"; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/invite"; "rf"; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/contacts"; "cn"; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/language"; "lg"; "")}}')
unify = [{"name":"d","value":d_val},
         {"name":"chat","value":"{{1.callback_query.message.chat.id}}{{1.message.chat.id}}"}]

def D(n): return f'get(split(90.d; "|"); {n})'
pref = f'substring(ifempty({D(2)}; "x"); 0; 1)'
IN_STOCK = '{{if(99.stock; "1"; "0")}}'
sw_name = "switch(" + D(2) + "; " + "; ".join(f'"{k}"; "{v[0]}"' for k,v in items.items()) + '; "")'
sw_price = "switch(" + D(2) + "; " + "; ".join(f'"{k}"; "{v[1]}"' for k,v in items.items()) + '; "0")'
div = f'switch({pref}; "a"; 100; "c"; 100; 1)'
qunit = f'switch({pref}; "a"; "г"; "c"; "г"; "e"; "шт."; "кг")'
Q2 = f'parseNumber(ifempty({D(3)}; "0"); ".")'
LIM = f'switch({pref}; "a"; {MAX_G}; "c"; {MAX_G}; "e"; {MAX_PCS}; {MAX_KG})'  # больше лимита → «Не понял количество»
_HG, _HK, _HP = (S(*HINT_L[u], lang=LANG0) for u in "gkp")
variables = [
 {"name":"lang","value":"{{"+LANG0+"}}"},
 {"name":"name","value":"{{99.name}}"},                                   # русское — для корзины владельцу, заказов
 {"name":"lname","value":"{{"+NAMEX(D(2), "99.name", LANG0)+"}}"},     # на языке клиента
 {"name":"price","value":"{{ifempty(99.price; 0)}}"},
 {"name":"ulabel","value":"{{"+ULBL_L(pref, LANG0)+"}}"},
 {"name":"qlabel","value":"{{"+f'replace(ifempty({D(3)}; ""); "."; ",")'+"}} {{"+qunit+"}}"},
 {"name":"lqlabel","value":"{{"+f'replace(ifempty({D(3)}; ""); "."; ",")'+"}} {{"+UNIT_L(pref, LANG0)+"}}"},
 {"name":"total","value":"{{"+f'ifempty(99.price; 0) * {Q2} / {div} * if({Q2} > {LIM}; 0; 1)'+"}}"},
 {"name":"kg","value":"{{"+f'switch({pref}; "a"; {Q2} / 1000; "c"; {Q2} / 1000; "e"; 0; {Q2})'+"}}"},
 {"name":"pcs","value":"{{"+f'if({pref} = "e"; {Q2}; 0)'+"}}"},
 {"name":"hint","value":"{{"+f'switch({pref}; "a"; {_HG}; "c"; {_HG}; "e"; {_HP}; {_HK})'+"}}"},
]
# ---- main menu text
SELLER = "@esusnob"  # продавец бота
OFFER_BTN = [{"text":"💼 Хочу такой бот для своего бизнеса","callback_data":"p"}]
offer = """💼 Такой бот — для вашего магазина

Этот бот принимает заказы сам: каталог с наличием, корзина, свой вес, расчёт суммы, адрес и телефон. Готовый заказ с маршрутом приходит в ваш Telegram-канал. Работает 24/7.

📦 ПАКЕТЫ
• Start — 350 €
каталог, корзина, доставка, заказ в канал, учёт остатков
• Business — 800 € ⭐
+ база клиентов, рассылки, акции, промокоды, бонусы, ежедневный отчёт
• Pro — 1 500 €
+ AI-помощник по продажам и остаткам, подключение внешних сервисов

🛠 ОБСЛУЖИВАНИЕ
• Базовое — 25 €/мес (250 €/год)
• Полное — 39 €/мес (390 €/год)
🎁 Start + 6 мес. обслуживания — 440 € вместо 500 €

➕ Онлайн-оплата (Apple Pay, Google Pay, карты, PayPal) — 150 €

Запуск Start за 1–2 дня: ваше название, логотип, цены и города. 50% предоплата, остальное после тестового заказа.

Попробуйте сами: соберите корзину и оформите пробный заказ.
Вопросы и заказ бота: @esusnob 👇"""
menu = """📋 ВЕСЬ ПРАЙС RAIV FISH
То, что отмечено ❌, — сейчас нет в наличии.

"""
for c,title,lst in cats:
    menu += title.upper() if c!="e" else "🥫 КОНСЕРВЫ"
    menu += "\n"
    for n,p,s in lst:
        menu += f"• {n} — {p.replace('.',',')} {ULBL[c]}" + ("❌" if not s else "") + "\n"
    menu += "\n"
menu += "Выберите раздел 👇"
start_text = ("🐟 RAIV FISH — вяленая рыба, икра и снеки к пиву\n\n"
 "🕐 Сегодня или завтра — днём или вечером\n"
 "💳 Онлайн или наличными · 💎 "+str(BONUS_PCT)+"% бонусами с каждого заказа\n\n"
 "Выберите раздел 👇")
# v9.6: переводы стартового экрана, меню и предложения
OFFER_BTN_TR = ("💼 Хочу такой бот для своего бизнеса","💼 Ich möchte so einen Bot für mein Geschäft","💼 Quiero un bot así para mi negocio","💼 Хочу такий бот для свого бізнесу")
OFFER_TR = (offer, """💼 So ein Bot für Ihren Shop

Dieser Bot nimmt Bestellungen selbstständig an: Katalog mit Verfügbarkeit, Warenkorb, eigene Menge, Summenberechnung, Adresse und Telefon. Die fertige Bestellung mit Route kommt in Ihren Telegram-Kanal. Rund um die Uhr (24/7).

📦 PAKETE
• Start — 350 €
Katalog, Warenkorb, Lieferung, Bestellung in den Kanal, Bestandsführung
• Business — 800 € ⭐
+ Kundendatenbank, Rundschreiben, Aktionen, Gutscheincodes, Bonus, täglicher Bericht
• Pro — 1 500 €
+ KI-Assistent für Verkauf und Bestand, Anbindung externer Dienste

🛠 WARTUNG
• Basis — 25 €/Monat (250 €/Jahr)
• Komplett — 39 €/Monat (390 €/Jahr)
🎁 Start + 6 Monate Wartung — 440 € statt 500 €

➕ Online-Zahlung (Apple Pay, Google Pay, Karten, PayPal) — 150 €

Start ist in 1–2 Tagen einsatzbereit: Ihr Name, Logo, Preise und Städte. 50 % Vorauszahlung, der Rest nach der Testbestellung.

Probieren Sie es selbst: Legen Sie Artikel in den Warenkorb und geben Sie eine Probebestellung auf.
Fragen und Bot-Bestellung: @esusnob 👇""", """💼 Un bot así para su tienda

Este bot recibe pedidos por sí solo: catálogo con disponibilidad, carrito, cantidad a elegir, cálculo del total, dirección y teléfono. El pedido listo, con la ruta, llega a su canal de Telegram. Funciona 24/7.

📦 PAQUETES
• Start — 350 €
catálogo, carrito, entrega, pedido al canal, control de stock
• Business — 800 € ⭐
+ base de clientes, envíos masivos, promociones, códigos promocionales, bonos, informe diario
• Pro — 1 500 €
+ asistente de IA para ventas y stock, conexión de servicios externos

🛠 MANTENIMIENTO
• Básico — 25 €/mes (250 €/año)
• Completo — 39 €/mes (390 €/año)
🎁 Start + 6 meses de mantenimiento — 440 € en lugar de 500 €

➕ Pago en línea (Apple Pay, Google Pay, tarjetas, PayPal) — 150 €

Puesta en marcha de Start en 1–2 días: su nombre, logotipo, precios y ciudades. 50 % por adelantado, el resto tras el pedido de prueba.

Pruébelo usted mismo: llene el carrito y haga un pedido de prueba.
Preguntas y pedido del bot: @esusnob 👇""", """💼 Такий бот — для вашого магазину

Цей бот приймає замовлення сам: каталог із наявністю, кошик, своя вага, розрахунок суми, адреса й телефон. Готове замовлення з маршрутом приходить у ваш Telegram-канал. Працює 24/7.

📦 ПАКЕТИ
• Start — 350 €
каталог, кошик, доставка, замовлення в канал, облік залишків
• Business — 800 € ⭐
+ база клієнтів, розсилки, акції, промокоди, бонуси, щоденний звіт
• Pro — 1 500 €
+ AI-помічник із продажів і залишків, підключення зовнішніх сервісів

🛠 ОБСЛУГОВУВАННЯ
• Базове — 25 €/міс (250 €/рік)
• Повне — 39 €/міс (390 €/рік)
🎁 Start + 6 міс. обслуговування — 440 € замість 500 €

➕ Онлайн-оплата (Apple Pay, Google Pay, картки, PayPal) — 150 €

Запуск Start за 1–2 дні: ваша назва, логотип, ціни та міста. 50% передоплата, решта після тестового замовлення.

Спробуйте самі: зберіть кошик і оформіть пробне замовлення.
Питання та замовлення бота: @esusnob 👇""")
START_TR = (start_text,
 "🐟 RAIV FISH — getrockneter Fisch, Fischrogen und Snacks zum Bier\n\n"
 "🕐 Heute oder morgen — tagsüber oder abends\n"
 "💳 Online oder bar · 💎 "+str(BONUS_PCT)+" % Bonus auf jede Bestellung\n\n"
 "Bitte wählen Sie eine Kategorie 👇",
 "🐟 RAIV FISH — pescado seco, huevas y snacks para cerveza\n\n"
 "🕐 Hoy o mañana — de día o por la tarde\n"
 "💳 En línea o en efectivo · 💎 "+str(BONUS_PCT)+" % en bonos por cada pedido\n\n"
 "Elija una sección 👇",
 "🐟 RAIV FISH — в’ялена риба, ікра та снеки до пива\n\n"
 "🕐 Сьогодні або завтра — вдень або ввечері\n"
 "💳 Онлайн або готівкою · 💎 "+str(BONUS_PCT)+"% бонусами з кожного замовлення\n\n"
 "Оберіть розділ 👇")
B_PRICE  = ("📋 Весь прайс","📋 Preisliste","📋 Lista de precios","📋 Весь прайс")
B_REPEAT = ("🔁 Повторить заказ","🔁 Bestellung wiederholen","🔁 Repetir pedido","🔁 Повторити замовлення")
B_MYORD  = ("📜 Мои заказы","📜 Meine Bestellungen","📜 Mis pedidos","📜 Мої замовлення")
B_PROMO  = H_PROMO
B_REF    = ("🎁 Приведи друга — 3 € обоим","🎁 Freunde einladen — 3 € für beide","🎁 Invita a un amigo — 3 € para ambos","🎁 Приведи друга — 3 € обом")
B_CONT   = ("📇 Контакты","📇 Kontakt","📇 Contactos","📇 Контакти")
def SERVICE_ROWS(lang=LG):
    return [[{"text":T(*B_PRICE,lang=lang),"callback_data":"pl"},{"text":T(*B_REPEAT,lang=lang),"callback_data":"r"}],
            [{"text":T(*B_MYORD,lang=lang),"callback_data":"h"},{"text":T(*B_PROMO,lang=lang),"callback_data":"pr"}],
            [{"text":T(*B_REF,lang=lang),"callback_data":"rf"},{"text":T(*B_CONT,lang=lang),"callback_data":"cn"}],
            [{"text":T(*B_LANG,lang=lang),"callback_data":"lg"}]]
def OFFER_BTN_L(lang=LG): return [{"text":T(*OFFER_BTN_TR,lang=lang),"callback_data":"p"}]
cat_kb = lambda mode, lang=LG: {"inline_keyboard":[[{"text":CATT(c,lang),"callback_data":f"k|{c}|{mode}"}] for c,t,_ in cats]+(SERVICE_ROWS(lang)+[OFFER_BTN_L(lang)] if mode=="s" else [])}
PH = {}
def ph(expr):
    k=f"@@{len(PH)}@@"; PH[k]=expr; return k
def body(obj):
    s=json.dumps(obj,ensure_ascii=False)
    for k,v in PH.items():
        s=s.replace(f'"{k}"',v).replace(k,v)
    return s
def meta(x,y): return {"designer":{"x":x,"y":y}}
def resp(mid, x, y, name, conds, obj):
    m={"id":mid,"mapper":{"body":body(obj),"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(x,y),"parameters":{}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
SAFE_SEND={103,104,143,175,184,193,194,195,196}
def api(mid, x, y, method, spec, name=None, conds=None, onerror=False):
    m={"id":mid,"mapper":{"method":"POST","bodyType":"assembled_body","body_spec":[{"key":k,"value":v} for k,v in spec],"urlMethod":method},
       "module":"telegram:UniversalAPICall","version":1,"metadata":meta(x,y),"parameters":{"__IMTCONN__":CONN}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    if mid in SAFE_SEND: onerror=True  # клиент мог заблокировать бота — не роняем сценарий
    if onerror: m["onerror"]=[{"id":mid+500,"mapper":None,"module":"builtin:Ignore","version":1,"metadata":meta(x,y+300)}]
    return m
def ds(mid, x, y, module, mapper, name=None, conds=None, store=None):
    m={"id":mid,"mapper":mapper,"module":f"datastore:{module}","version":1,"metadata":meta(x,y),"parameters":{"datastore":store or DS}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
def sv(mid, x, y, pairs): return {"id":mid,"mapper":{"variables":[{"name":k,"value":v} for k,v in pairs],"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(x,y),"parameters":{}}
def search(mid, x, y, store, flt, name=None, conds=None, limit=1000):
    m={"id":mid,"mapper":{"filter":flt,"sort":[]},"module":"datastore:SearchRecord","version":1,"metadata":meta(x,y),"parameters":{"datastore":store,"continueWhenNoRes":True,"limit":limit}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
def router(mid, x, y, routes): return {"id":mid,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":meta(x,y),"routes":[{"flow":r} for r in routes]}
def eq(a,b): return {"a":"{{"+a+"}}","b":b,"o":"text:equal"}
# кавычки внутри формул {{...}} не экранируем — иначе Make получит \".\" вместо "."
FIXF = lambda s: re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"', '"'), s)
KB = lambda rows: re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"', '"'), json.dumps({"inline_keyboard":rows},ensure_ascii=False))
CHAT="{{90.chat}}"; MID="{{1.callback_query.message.message_id}}"
routes=[]
chat=ph("{{1.message.chat.id}}")
CMDS = ["/admin","/promo","/send","/report","/stop","/orders","/help","/invite","/price","/stock","/catalog","/sklad","/contacts","/language"]
REFC = '{{replace(trim(1.message.text); "/start ref_"; "")}}'
IS_TEXT = [{"a":"{{1.message.text}}","o":"exist"},{"a":"{{1.message.reply_to_message.message_id}}","o":"notexist"}]
FMT = lambda e: "{{formatNumber("+e+'; 2; ","; ".")}}'
RET = "ifempty(101.orders; 0) > 0"
greet = ph('{{if('+RET+'; '+S("👋 С возвращением! Ваши бонусы: 💎 ","👋 Willkommen zurück! Ihr Bonus: 💎 ","👋 ¡Bienvenido de nuevo! Sus bonos: 💎 ","👋 З поверненням! Ваші бонуси: 💎 ")+'; "")}}{{if('+RET+'; formatNumber(ifempty(101.bonus; 0); 2; ","; "."); "")}}{{if('+RET+'; " €\\n\\n"; "")}}')
routes.append([
 ds(100,900,-1100,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"name":"{{1.message.from.first_name}}","username":"{{1.message.from.username}}","last_seen":"{{now}}","lang":"{{"+LG+"}}"}},"Меню",
    [IS_TEXT+[{"a":"{{1.message.text}}","b":c,"o":"text:notstartwith"} for c in CMDS+["/start c_"]]],store=CUST),
 ds(101,1200,-1100,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 resp(4,1500,-1100,None,None,{"method":"sendMessage","chat_id":chat,"text":greet+TT(START_TR),"reply_markup":cat_kb("s")}),
 router(108,1800,-1100,[[
 ds(102,2100,-1100,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"ref":REFC,"bonus":"{{ifempty(101.bonus; 0) + "+str(REF_BONUS)+"}}"}},"Новый по приглашению",
    [[{"a":"{{1.message.text}}","b":"/start ref_","o":"text:startwith"},{"a":"{{ifempty(101.orders; 0)}}","b":"0","o":"number:equal"},{"a":"{{101.ref}}","o":"notexist"},{"a":REFC,"b":CHAT,"o":"text:notequal"}]],store=CUST),
 api(103,2100,-1100,"sendMessage",[("chat_id",CHAT),("text",T("🎁 Вам начислено "+str(REF_BONUS)+" € бонусами по приглашению друга! Они спишутся при первом заказе.",
   "🎁 Sie haben über die Einladung eines Freundes "+str(REF_BONUS)+" € Bonus erhalten! Er wird bei Ihrer ersten Bestellung verrechnet.",
   "🎁 ¡Ha recibido "+str(REF_BONUS)+" € en bonos por la invitación de un amigo! Se descontarán en su primer pedido.",
   "🎁 Вам нараховано "+str(REF_BONUS)+" € бонусами за запрошенням друга! Вони спишуться під час першого замовлення."))]),
 ds(268,2250,-1100,"GetRecord",{"key":REFC,"returnWrapped":False},store=CUST),   # v9.6: язык пригласившего
 api(104,2400,-1100,"sendMessage",[("chat_id",REFC),("text",T("👋 По вашей ссылке пришёл новый покупатель. Когда он сделает первый заказ, вам начислится "+str(REF_BONUS)+" € бонусами.",
   "👋 Über Ihren Link ist ein neuer Kunde gekommen. Sobald er seine erste Bestellung aufgibt, erhalten Sie "+str(REF_BONUS)+" € Bonus.",
   "👋 Un nuevo cliente ha llegado a través de su enlace. Cuando haga su primer pedido, recibirá "+str(REF_BONUS)+" € en bonos.",
   "👋 За вашим посиланням прийшов новий покупець. Коли він зробить перше замовлення, вам нарахується "+str(REF_BONUS)+" € бонусами.",lang="268.lang"))],onerror=True)],
 [api(109,2100,-800,"sendMessage",[("chat_id",CHAT),("text",T("🛍 Новинка: витрина с фото! Кнопка «🛍 Витрина» теперь всегда внизу чата — выбирайте товары по фото, корзина соберётся сама.",
   "🛍 Neu: Schaufenster mit Fotos! Die Schaltfläche „🛍 Schaufenster“ ist jetzt immer unten im Chat — wählen Sie Artikel nach Foto, der Warenkorb füllt sich von selbst.",
   "🛍 Novedad: ¡escaparate con fotos! El botón «🛍 Escaparate» está ahora siempre abajo en el chat: elija productos por foto y el carrito se llenará solo.",
   "🛍 Новинка: вітрина з фото! Кнопка «🛍 Вітрина» тепер завжди внизу чату — обирайте товари за фото, кошик збереться сам.")),
   ("reply_markup",FIXF(json.dumps({"keyboard":[[{"text":T("🛍 Витрина","🛍 Schaufenster","🛍 Escaparate","🛍 Вітрина"),"web_app":{"url":WEBAPP},"style":"primary"}]],"resize_keyboard":True,"is_persistent":True},ensure_ascii=False)))],
   "Кнопка витрины ещё не выдана",[[{"a":"{{101.kb}}","b":WEBAPP_V,"o":"text:notequal"}]],onerror=True),
  ds(98,2400,-800,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"kb":WEBAPP_V}},store=CUST)]])])
TOUCH_CUST = lambda mid,x,y,name,conds: ds(mid,x,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"last_seen":"{{now}}"}},name,conds,store=CUST)
cbchat=ph("{{1.callback_query.message.chat.id}}"); cbmid=ph(MID)
routes.append([resp(5,900,-700,"Разделы",[[eq(D(1),"m")]],
  {"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":TT(P_CHOOSE_CAT),"reply_markup":cat_kb("e")})])
routes.append([resp(30,900,-600,"Предложение",[[eq(D(1),"p")]],
  {"method":"sendMessage","chat_id":cbchat,"text":TT(OFFER_TR),"reply_markup":{"inline_keyboard":[
    [{"text":TT(B_SELLER),"url":"https://t.me/esusnob"}],
    [{"text":T("🛒 Попробовать заказ","🛒 Bestellung ausprobieren","🛒 Probar un pedido","🛒 Спробувати замовлення"),"callback_data":"m"}]]}})])
# весь прайс
PL_LINE = ('{{switch(213.data.cat; "a"; "🐟"; "b"; "🐠"; "c"; "🍢"; "d"; "🦑"; "🥫")}} {{'+NAMEX("213.data.item","213.data.name")+'}} — {{replace(toString(213.data.price); "."; ",")}} {{'
  +ULBL_L("213.data.cat")+'}}{{if(213.data.stock; ""; " ❌")}}')
routes.append([search(213,900,-2400,PROMO,[[{"a":"item","o":"exist"}]],"Весь прайс",[[eq(D(1),"pl")]],limit=100),
  {"id":214,"mapper":{"line":PL_LINE},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,-2400),"parameters":{"feeder":213},
   "filter":{"name":"Товар","conditions":[[{"a":"{{213.data.item}}","o":"exist"}]]}},
  api(105,1500,-2400,"sendMessage",[("chat_id",CHAT),("text",T("📋 ВЕСЬ ПРАЙС RAIV FISH\n❌ — сейчас нет в наличии\n\n{{join(map(214.array; \"line\"); \"\n\")}}\n\nВыберите раздел 👇",
   "📋 PREISLISTE RAIV FISH\n❌ — derzeit nicht vorrätig\n\n{{join(map(214.array; \"line\"); \"\n\")}}\n\nBitte wählen Sie eine Kategorie 👇",
   "📋 LISTA DE PRECIOS RAIV FISH\n❌ — no disponible ahora\n\n{{join(map(214.array; \"line\"); \"\n\")}}\n\nElija una sección 👇",
   "📋 ВЕСЬ ПРАЙС RAIV FISH\n❌ — зараз немає в наявності\n\n{{join(map(214.array; \"line\"); \"\n\")}}\n\nОберіть розділ 👇")),("reply_markup",KB(cat_kb("s")["inline_keyboard"][:len(cats)]))])])
# приведи друга
REFLINK = "https://t.me/"+BOT_USER+"?start=ref_{{90.chat}}"
RB = str(REF_BONUS)
routes.append([api(106,900,-2300,"sendMessage",[("chat_id",CHAT),("text",T("🎁 Приведи друга — получите оба по "+RB+" €\n\nВаша личная ссылка:\n"+REFLINK+"\n\nДруг получает "+RB+" € бонусами сразу, вы — после его первого заказа.",
   "🎁 Freunde einladen — Sie beide erhalten je "+RB+" €\n\nIhr persönlicher Link:\n"+REFLINK+"\n\nIhr Freund erhält "+RB+" € Bonus sofort, Sie — nach seiner ersten Bestellung.",
   "🎁 Invita a un amigo — ambos reciben "+RB+" €\n\nSu enlace personal:\n"+REFLINK+"\n\nSu amigo recibe "+RB+" € en bonos al instante, y usted, tras su primer pedido.",
   "🎁 Приведи друга — отримайте обидва по "+RB+" €\n\nВаше особисте посилання:\n"+REFLINK+"\n\nДруг отримує "+RB+" € бонусами одразу, ви — після його першого замовлення.")),
   ("reply_markup",'{"inline_keyboard":[[{"text":"'+T("📤 Отправить другу","📤 An Freund senden","📤 Enviar a un amigo","📤 Надіслати другу")+'","url":"https://t.me/share/url?url={{encodeURL(\"https://t.me/'+BOT_USER+'?start=ref_\")}}{{90.chat}}&text={{encodeURL('
     +S("Вяленая рыба и снеки с доставкой — держи 3 € на первый заказ 🐟","Getrockneter Fisch und Snacks mit Lieferung — hier sind 3 € für deine erste Bestellung 🐟","Pescado seco y snacks con entrega — aquí tienes 3 € para tu primer pedido 🐟","В’ялена риба та снеки з доставкою — тримай 3 € на перше замовлення 🐟")
     +')}}"}],[{"text":"'+TT(B_TOSHOP)+'","callback_data":"m"}]]}')],"Приведи друга",[[eq(D(1),"rf")]])])
# контакты и медиа (новые ссылки — строкой в CONTACT_LINKS: подпись, url)
CONTACT_LINKS = [   # v9.6: подпись — (ru, de, es, uk)
  (("🎵 TikTok — видео","🎵 TikTok — Videos","🎵 TikTok — vídeos","🎵 TikTok — відео"), "https://www.tiktok.com/@vasya_raivfish"),
  (("📸 Instagram — фото","📸 Instagram — Fotos","📸 Instagram — fotos","📸 Instagram — фото"), "https://www.instagram.com/vasya_ivanchuk_/"),
  (("👍 Facebook",)*4, "https://www.facebook.com/share/1K6wTjKZx9/"),
  (("📣 Telegram-канал @raiv_fish1","📣 Telegram-Kanal @raiv_fish1","📣 Canal de Telegram @raiv_fish1","📣 Telegram-канал @raiv_fish1"), "https://t.me/raiv_fish1"),
  (("🐟 Поставщик — Василий","🐟 Lieferant — Wassili","🐟 Proveedor — Vasili","🐟 Постачальник — Василь"), "https://t.me/vasyaivancuk"),
  (B_SELLER, "https://t.me/"+SELLER.lstrip("@")),
]
CONTACT_TEXT = ("📇 Контакты RAIV FISH\n\n"
 "🐟 Рыба и икра — от поставщика из Эстонии: @vasyaivancuk\n"
 "🎬 Видео, фото и новинки — TikTok, Instagram, Facebook и канал @raiv_fish1\n"
 "💬 Вопросы по заказу — "+SELLER)
CONTACT_TR = (CONTACT_TEXT,
 "📇 Kontakt RAIV FISH\n\n🐟 Fisch und Rogen — vom Lieferanten aus Estland: @vasyaivancuk\n🎬 Videos, Fotos und Neuheiten — TikTok, Instagram, Facebook und Kanal @raiv_fish1\n💬 Fragen zur Bestellung — "+SELLER,
 "📇 Contactos RAIV FISH\n\n🐟 Pescado y huevas — del proveedor de Estonia: @vasyaivancuk\n🎬 Vídeos, fotos y novedades — TikTok, Instagram, Facebook y el canal @raiv_fish1\n💬 Preguntas sobre el pedido — "+SELLER,
 "📇 Контакти RAIV FISH\n\n🐟 Риба та ікра — від постачальника з Естонії: @vasyaivancuk\n🎬 Відео, фото й новинки — TikTok, Instagram, Facebook і канал @raiv_fish1\n💬 Питання щодо замовлення — "+SELLER)
routes.append([api(266,900,-2250,"sendMessage",[("chat_id",CHAT),("text",TT(CONTACT_TR)),
   ("reply_markup",KB([[{"text":TT(t),"url":u}] for t,u in CONTACT_LINKS]+[[{"text":TT(B_TOSHOP),"callback_data":"m"}]]))],"Контакты",[[eq(D(1),"cn")]])])
# v9.6: выбор языка — кнопка «🌐 Язык» (lg) и /language; ln|<код> — сохранить и показать меню на новом языке
LANG_KB = KB([[{"text":LANG_NAMES["ru"],"callback_data":"ln|ru"},{"text":LANG_NAMES["de"],"callback_data":"ln|de"}],
              [{"text":LANG_NAMES["es"],"callback_data":"ln|es"},{"text":LANG_NAMES["uk"],"callback_data":"ln|uk"}]])
routes.append([api(271,900,-2900,"sendMessage",[("chat_id",CHAT),("text","🌐 Выберите язык · Sprache wählen · Elija el idioma · Оберіть мову"),("reply_markup",LANG_KB)],"Язык — выбор",[[eq(D(1),"lg")]],onerror=True)])
NL = D(2)
routes.append([ds(269,900,-2750,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"lang":"{{"+NL+"}}","last_seen":"{{now}}"}},"Язык — сохранить",
   [[eq(D(1),"ln"),eq(NL,L)] for L in LANGS],store=CUST),
  api(270,1200,-2750,"editMessageText",[("chat_id",CHAT),("message_id",MID),
   ("text",T("✅ Язык: Русский\n\n","✅ Sprache: Deutsch\n\n","✅ Idioma: español\n\n","✅ Мова: українська\n\n",lang=NL)+T(*START_TR,lang=NL)),
   ("reply_markup",KB(cat_kb("s",NL)["inline_keyboard"]))],onerror=True)])
# помощь
routes.append([resp(107,900,-2200,"/help",[[IS_TEXT[1],{"a":"{{1.message.text}}","b":"/help","o":"text:startwith"}]],{"method":"sendMessage","chat_id":chat,
  "text":T("ℹ️ Как заказать\n1. /start → раздел → товар → вес (или «✏️ Свой вес»)\n2. «🧺 Корзина / оформить» → город → время → адрес → телефон\n3. Оплатите онлайн по кнопке или наличными курьеру\n\nС каждого заказа — "+str(BONUS_PCT)+"% бонусами.\n\n/orders — мои заказы и бонусы\n/invite — приведи друга\n/contacts — контакты, канал и медиа\n/language — сменить язык\n/stop — не получать рассылки\nВопросы: "+SELLER,
  "ℹ️ So bestellen Sie\n1. /start → Kategorie → Artikel → Menge (oder „✏️ Eigene Menge“)\n2. „🧺 Warenkorb / bestellen“ → Stadt → Zeit → Adresse → Telefon\n3. Bezahlen Sie online per Schaltfläche oder bar beim Kurier\n\nAuf jede Bestellung — "+str(BONUS_PCT)+" % Bonus.\n\n/orders — meine Bestellungen und Bonus\n/invite — Freunde einladen\n/contacts — Kontakt, Kanal und Medien\n/language — Sprache ändern\n/stop — keine Rundschreiben mehr erhalten\nFragen: "+SELLER,
  "ℹ️ Cómo hacer un pedido\n1. /start → sección → producto → cantidad (o «✏️ Otra cantidad»)\n2. «🧺 Carrito / pedir» → ciudad → hora → dirección → teléfono\n3. Pague en línea con el botón o en efectivo al repartidor\n\nPor cada pedido, un "+str(BONUS_PCT)+" % en bonos.\n\n/orders — mis pedidos y bonos\n/invite — invitar a un amigo\n/contacts — contactos, canal y redes\n/language — cambiar el idioma\n/stop — no recibir envíos masivos\nPreguntas: "+SELLER,
  "ℹ️ Як замовити\n1. /start → розділ → товар → вага (або «✏️ Своя вага»)\n2. «🧺 Кошик / оформити» → місто → час → адреса → телефон\n3. Оплатіть онлайн кнопкою або готівкою кур’єру\n\nЗ кожного замовлення — "+str(BONUS_PCT)+"% бонусами.\n\n/orders — мої замовлення та бонуси\n/invite — приведи друга\n/contacts — контакти, канал і медіа\n/language — змінити мову\n/stop — не отримувати розсилки\nПитання: "+SELLER)})])
# повторить прошлый заказ
routes.append([TOUCH_CUST(110,900,-2000,"Повторить заказ",[[eq(D(1),"r")]]),
 ds(111,1200,-2000,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 router(112,1500,-2000,[
  [ds(113,1800,-2000,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"text":"{{111.last_text}}","ltext":"{{ifempty(111.last_ltext; 111.last_text)}}","total":"{{111.last_total}}","count":"{{111.last_count}}","kg":"{{ifempty(111.last_kg; 0)}}","pcs":"{{ifempty(111.last_pcs; 0)}}"}},"Есть прошлый заказ",[[{"a":"{{ifempty(111.last_count; 0)}}","b":"0","o":"number:greater"}]]),
   api(114,2100,-2000,"sendMessage",[("chat_id",CHAT),("text",T("🔁 Корзина как в прошлый раз:\n{{ifempty(111.last_ltext; 111.last_text)}}💶 Итого: "+FMT("111.last_total")+" €\n\nМожно добавить ещё товары или сразу оформить.",
   "🔁 Warenkorb wie beim letzten Mal:\n{{ifempty(111.last_ltext; 111.last_text)}}💶 Summe: "+FMT("111.last_total")+" €\n\nSie können weitere Artikel hinzufügen oder gleich bestellen.",
   "🔁 Carrito como la última vez:\n{{ifempty(111.last_ltext; 111.last_text)}}💶 Total: "+FMT("111.last_total")+" €\n\nPuede añadir más productos o hacer el pedido ya.",
   "🔁 Кошик як минулого разу:\n{{ifempty(111.last_ltext; 111.last_text)}}💶 Разом: "+FMT("111.last_total")+" €\n\nМожна додати ще товари або одразу оформити.")),("reply_markup","@@CARTBTNS@@")])],
  [api(115,1800,-1800,"sendMessage",[("chat_id",CHAT),("text",T("Прошлых заказов пока нет. Выберите товары 👇","Noch keine früheren Bestellungen. Bitte wählen Sie Artikel 👇","Aún no hay pedidos anteriores. Elija productos 👇","Минулих замовлень поки немає. Оберіть товари 👇")),("reply_markup","@@EMPTYKB@@")],"Нет заказов",[[{"a":"{{ifempty(111.last_count; 0)}}","b":"0","o":"number:lessorequal"}]])]])])
# мои заказы и бонусы
routes.append([TOUCH_CUST(116,900,-1700,"Мои заказы",[[eq(D(1),"h")]]),
 ds(117,1200,-1700,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 api(118,1500,-1700,"sendMessage",[("chat_id",CHAT),("text",
   T("📜 Ваши заказы\n\n{{ifempty(117.history; @H)}}\n\n💎 Бонусы: "+FMT("ifempty(117.bonus; 0)")+" €\nЗа каждый заказ начисляем "+str(BONUS_PCT)+"% бонусами. При оформлении они списываются автоматически — до "+str(BONUS_CAP)+"% суммы заказа.",
     "📜 Ihre Bestellungen\n\n{{ifempty(117.history; @H)}}\n\n💎 Bonus: "+FMT("ifempty(117.bonus; 0)")+" €\nFür jede Bestellung schreiben wir Ihnen "+str(BONUS_PCT)+" % Bonus gut. Bei der Bestellung wird er automatisch verrechnet — bis zu "+str(BONUS_CAP)+" % des Bestellwerts.",
     "📜 Sus pedidos\n\n{{ifempty(117.history; @H)}}\n\n💎 Bonos: "+FMT("ifempty(117.bonus; 0)")+" €\nPor cada pedido abonamos un "+str(BONUS_PCT)+" % en bonos. Al hacer el pedido se descuentan automáticamente, hasta el "+str(BONUS_CAP)+" % del importe.",
     "📜 Ваші замовлення\n\n{{ifempty(117.history; @H)}}\n\n💎 Бонуси: "+FMT("ifempty(117.bonus; 0)")+" €\nЗа кожне замовлення нараховуємо "+str(BONUS_PCT)+"% бонусами. Під час оформлення вони списуються автоматично — до "+str(BONUS_CAP)+"% суми замовлення.").replace("@H",S("Пока заказов нет.","Noch keine Bestellungen.","Aún no hay pedidos.","Поки що замовлень немає."))),
   ("reply_markup",KB([[{"text":T("🔁 Повторить прошлый заказ","🔁 Letzte Bestellung wiederholen","🔁 Repetir el último pedido","🔁 Повторити минуле замовлення"),"callback_data":"r"}],[{"text":TT(B_TOSHOP),"callback_data":"m"}]]))])])
# промокод: вопрос
routes.append([resp(119,900,-1500,"Промокод — вопрос",[[eq(D(1),"pr")]],
  {"method":"sendMessage","chat_id":cbchat,"text":T("🎟 Промокод\n\nОтветьте на это сообщение: напишите промокод.","🎟 Gutscheincode\n\nAntworten Sie auf diese Nachricht: Geben Sie den Gutscheincode ein.","🎟 Código promocional\n\nResponda a este mensaje: escriba el código promocional.","🎟 Промокод\n\nДайте відповідь на це повідомлення: напишіть промокод."),
   "reply_markup":{"force_reply":True,"input_field_placeholder":T("Например FISH10","z. B. FISH10","Por ejemplo FISH10","Наприклад FISH10")}})])
# промокод: ответ
PCODE = "{{upper(trim(1.message.text))}}"
routes.append([search(160,900,-1300,PROMO,[[{"a":"code","o":"text:equal","b":PCODE}]],"Промокод — ответ",[[{"a":"{{1.message.reply_to_message.text}}","b":h,"o":"text:contain"}] for h in dict.fromkeys(H_PROMO)],limit=1),
 router(161,1200,-1300,[
  [ds(162,1500,-1300,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"promo":"{{160.data.percent}}","pcode":PCODE}},"Действует",[[{"a":"{{ifempty(160.data.percent; 0)}}","b":"0","o":"number:greater"}]]),
   api(163,1800,-1300,"sendMessage",[("chat_id",CHAT),("text",T("✅ Промокод "+PCODE+" принят: скидка {{160.data.percent}}% на этот заказ.\nСкидка появится при оформлении.",
     "✅ Gutscheincode "+PCODE+" angenommen: {{160.data.percent}} % Rabatt auf diese Bestellung.\nDer Rabatt wird bei der Bestellung angezeigt.",
     "✅ Código "+PCODE+" aceptado: {{160.data.percent}} % de descuento en este pedido.\nEl descuento aparecerá al hacer el pedido.",
     "✅ Промокод "+PCODE+" прийнято: знижка {{160.data.percent}}% на це замовлення.\nЗнижка з’явиться під час оформлення.")),("reply_markup",KB([[{"text":TT(B_CHOOSE),"callback_data":"m"}],[{"text":TT(B_ORDER),"callback_data":"o"}]]))])],
  [api(164,1500,-1100,"sendMessage",[("chat_id",CHAT),("text",T("❌ Промокод «{{trim(1.message.text)}}» не найден или уже не действует.","❌ Gutscheincode „{{trim(1.message.text)}}“ nicht gefunden oder nicht mehr gültig.","❌ El código «{{trim(1.message.text)}}» no existe o ya no es válido.","❌ Промокод «{{trim(1.message.text)}}» не знайдено або він уже не діє.")),
     ("reply_markup",KB([[{"text":T("🎟 Ввести другой","🎟 Anderen Code eingeben","🎟 Introducir otro","🎟 Ввести інший"),"callback_data":"pr"}],[{"text":TT(B_TOSHOP),"callback_data":"m"}]]))],"Нет такого",[[{"a":"{{ifempty(160.data.percent; 0)}}","b":"0","o":"number:lessorequal"}]])]])])
y=-500
CAT_TITLE = "switch("+D(2)+"; "+"; ".join(f'"{c}"; {CATS(c)}' for c,t,_ in cats)+'; '+S("Каталог","Katalog","Catálogo","Каталог")+')'
catbtn = '[{"text":"{{'+NAMEX("210.data.item","210.data.name")+'}} — {{replace(toString(210.data.price); "."; ",")}} {{'+ULBL_L("210.data.cat")+'}}","callback_data":"f|{{210.data.item}}"}]'
cat_body = ('{"method":"{{if('+D(3)+' = "e"; "editMessageText"; "sendMessage")}}","chat_id":{{1.callback_query.message.chat.id}},'
  '"message_id":{{1.callback_query.message.message_id}},"text":"{{'+CAT_TITLE+'}}\\n\\n{{'+S("Выберите товар 👇","Bitte wählen Sie einen Artikel 👇","Elija un producto 👇","Оберіть товар 👇")+'}}",'
  '"reply_markup":{"inline_keyboard":[{{join(map(211.array; "btn"); ",")}}{{if(length(211.array) > 0; ","; "")}}'
  '[{"text":"{{'+SS(B_CART)+'}}","callback_data":"o"}],[{"text":"{{'+SS(B_ALLCAT)+'}}","callback_data":"m"}]]}}')
routes.append([
  search(210,900,y,PROMO,[[{"a":"item","o":"exist"},{"a":"cat","o":"text:equal","b":"{{"+D(2)+"}}"}]],"Раздел (каталог)",[[eq(D(1),"k")]],limit=50),
  {"id":211,"mapper":{"btn":catbtn},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,y),"parameters":{"feeder":210},
   "filter":{"name":"Товар есть в наличии","conditions":[[{"a":"{{210.data.item}}","o":"exist"},{"a":'{{if(210.data.stock; "1"; "0")}}',"b":"1","o":"text:equal"}]]}},
  {"id":212,"mapper":{"body":cat_body,"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(1500,y),"parameters":{}}])
y+=200
# product chosen -> qty (one route per category: quantities differ)
PH["@@CODE@@"]="{{"+D(2)+"}}"; PH["@@CAT@@"]="{{"+pref+"}}"
mid=20
for c in UNIT:
    u=UNIT[c]; qs=QTY[c]
    QU = "{{"+S(*QL_L[u])+"}}"
    qk=[[{"text":f"{q.replace('.',',')} "+QU,"callback_data":f"q|@@CODE@@|{q}"} for q in qs[:2]],
        [{"text":f"{q.replace('.',',')} "+QU,"callback_data":f"q|@@CODE@@|{q}"} for q in qs[2:]],
        [{"text":TT(B_WEIGHT),"callback_data":"w|@@CODE@@"}],
        [{"text":T("⬅️ Назад","⬅️ Zurück","⬅️ Atrás","⬅️ Назад"),"callback_data":"k|@@CAT@@|e"}]]
    obj={"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"🐟 {{2.lname}} — {{replace(2.price; \".\"; \",\")}} {{2.ulabel}}\n\n"+T("Сколько добавить в корзину?","Wie viel möchten Sie in den Warenkorb legen?","¿Cuánto desea añadir al carrito?","Скільки додати в кошик?"),"reply_markup":{"inline_keyboard":qk}}
    routes.append([resp(mid,900,y,f"Товар ({c})",[[eq(D(1),"f"),{"a":"{{"+pref+"}}","b":c,"o":"text:equal"},{"a":IN_STOCK,"b":"1","o":"text:equal"}]],obj)])
    mid+=1; y+=200
# custom weight prompt
routes.append([resp(26,900,y,"Свой вес — вопрос",[[eq(D(1),"w")]],
  {"method":"sendMessage","chat_id":cbchat,"text":TT(B_WEIGHT)+"\n🐟 {{2.lname}} — {{replace(2.price; \".\"; \",\")}} {{2.ulabel}}\n\n"
     +T("Ответьте на это сообщение: сколько взять {{2.hint}}.","Antworten Sie auf diese Nachricht: gewünschte Menge {{2.hint}}.","Responda a este mensaje: cuánto desea, {{2.hint}}.","Дайте відповідь на це повідомлення: скільки взяти {{2.hint}}.")
     +"\n"+TT(H_CODE)+" {{"+D(2)+"}}",
   "reply_markup":{"force_reply":True,"input_field_placeholder":T("Например 0,7","z. B. 0,7","Por ejemplo 0,7","Наприклад 0,7")}})]); y+=200
routes.append([resp(25,900,y,"Нет в наличии",[[eq(D(1),"f"),{"a":IN_STOCK,"b":"1","o":"text:notequal"}]],
  {"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"❌ {{ifempty(2.lname; "+S("Этот товар","Dieser Artikel","Este producto","Цей товар")+")}}"+T(" — сейчас нет в наличии.\nВыберите другой товар 👇"," — derzeit nicht vorrätig.\nBitte wählen Sie einen anderen Artikel 👇"," — no disponible ahora.\nElija otro producto 👇"," — зараз немає в наявності.\nОберіть інший товар 👇"),"reply_markup":{"inline_keyboard":[[{"text":TT(B_ALLCAT),"callback_data":"m"}]]}})]); y+=200
# ---- add to cart
SUM='{{formatNumber(2.total; 2; ","; ".")}}'
CART_BTNS=KB([[{"text":TT(B_MORE),"callback_data":"m"}],[{"text":TT(B_ORDER),"callback_data":"o"}],[{"text":TT(B_CLEAR),"callback_data":"x"}]])
# v9.6: в корзине две строки — text (русская: заказ, канал, история, отчёты) и ltext (на языке клиента: показ клиенту)
NEWTEXT='{{51.text}}• {{2.name}} — {{2.qlabel}} — '+SUM+' €\n'
NEWLTEXT='{{ifempty(51.ltext; 51.text)}}• {{2.lname}} — {{2.lqlabel}} — '+SUM+' €\n'
NEWTOTAL='{{ifempty(51.total; 0) + 2.total}}'
_NT = "{{formatNumber(ifempty(51.total; 0) + 2.total; 2; \",\"; \".\")}}"
view=T("✅ Добавлено: {{2.lname}} — {{2.lqlabel}} — "+SUM+" €\n\n🧺 Ваша корзина:\n"+NEWLTEXT+"💶 Итого: "+_NT+" €",
       "✅ Hinzugefügt: {{2.lname}} — {{2.lqlabel}} — "+SUM+" €\n\n🧺 Ihr Warenkorb:\n"+NEWLTEXT+"💶 Summe: "+_NT+" €",
       "✅ Añadido: {{2.lname}} — {{2.lqlabel}} — "+SUM+" €\n\n🧺 Su carrito:\n"+NEWLTEXT+"💶 Total: "+_NT+" €",
       "✅ Додано: {{2.lname}} — {{2.lqlabel}} — "+SUM+" €\n\n🧺 Ваш кошик:\n"+NEWLTEXT+"💶 Разом: "+_NT+" €")
add_flow=[
 ds(50,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Добавить в корзину",
    [[eq(D(1),"q"),{"a":"{{2.total}}","b":"0","o":"number:greater"},{"a":IN_STOCK,"b":"1","o":"text:equal"}]]),
 ds(51,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 ds(52,1500,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"text":NEWTEXT,"ltext":NEWLTEXT,"total":NEWTOTAL,"count":"{{ifempty(51.count; 0) + 1}}","kg":"{{ifempty(51.kg; 0) + 2.kg}}","pcs":"{{ifempty(51.pcs; 0) + 2.pcs}}"}}),
 router(53,1800,y,[
   [api(54,2100,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",view),("reply_markup",CART_BTNS)],"Кнопка",[[{"a":"{{1.callback_query.id}}","o":"exist"}]])],
   [api(55,2100,y+200,"sendMessage",[("chat_id",CHAT),("text",view),("reply_markup",CART_BTNS)],"Свой вес",[[{"a":"{{1.callback_query.id}}","o":"notexist"}]])],
 ])]
routes.append(add_flow); y+=400
routes.append([api(56,900,y,"sendMessage",[("chat_id",CHAT),("text",T("🤔 Не понял количество. Нажмите «✏️ Свой вес» ещё раз и напишите число, например 0,7 или 250.",
     "🤔 Menge nicht erkannt. Tippen Sie erneut auf „✏️ Eigene Menge“ und schreiben Sie eine Zahl, z. B. 0,7 oder 250.",
     "🤔 No he entendido la cantidad. Pulse «✏️ Otra cantidad» de nuevo y escriba un número, por ejemplo 0,7 o 250.",
     "🤔 Не зрозумів кількість. Натисніть «✏️ Своя вага» ще раз і напишіть число, наприклад 0,7 або 250."))],
   "Неверный вес",[[eq(D(1),"q"),{"a":"{{2.total}}","b":"0","o":"number:lessorequal"}]])]); y+=200
# ---- checkout: city choice
cities=["Эдделак","Марне","Брунсбюттель","Хайде","Другое место"]
CITIES_TR=[("Эдделак","Eddelak","Eddelak","Еддельак"),("Марне","Marne","Marne","Марне"),("Брунсбюттель","Brunsbüttel","Brunsbüttel","Брунсбюттель"),
           ("Хайде","Heide","Heide","Гайде"),("Другое место","Anderer Ort","Otro lugar","Інше місце")]
CITY_KB=KB([[{"text":TT(CITIES_TR[0]),"callback_data":"c|1"},{"text":TT(CITIES_TR[1]),"callback_data":"c|2"}],[{"text":TT(CITIES_TR[2]),"callback_data":"c|3"},{"text":TT(CITIES_TR[3]),"callback_data":"c|4"}],[{"text":TT(CITIES_TR[4]),"callback_data":"c|5"}],[{"text":TT(B_MORE),"callback_data":"m"}]])
EMPTY_KB=KB([[{"text":TT(B_CHOOSE),"callback_data":"m"}]])
LT61 = "{{ifempty(61.ltext; 61.text)}}"
_T61 = "{{formatNumber(61.total; 2; \",\"; \".\")}}"
routes.append([
 ds(60,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Оформить",[[eq(D(1),"o")]]),
 ds(61,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 router(62,1500,y,[
  [api(63,1800,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",T("🧺 Ваша корзина:\n"+LT61+"💶 Итого: "+_T61+" €\n\n📍 Куда доставить? Доставка бесплатно.",
     "🧺 Ihr Warenkorb:\n"+LT61+"💶 Summe: "+_T61+" €\n\n📍 Wohin sollen wir liefern? Die Lieferung ist kostenlos.",
     "🧺 Su carrito:\n"+LT61+"💶 Total: "+_T61+" €\n\n📍 ¿Adónde lo entregamos? La entrega es gratuita.",
     "🧺 Ваш кошик:\n"+LT61+"💶 Разом: "+_T61+" €\n\n📍 Куди доставити? Доставка безкоштовна.")),("reply_markup",CITY_KB)],"Есть товары",[[{"a":"{{61.count}}","b":"0","o":"number:greater"},{"a":"{{61.total}}","b":str(MIN_ORDER),"o":"number:greaterorequal"}]],onerror=True)],
  [api(65,1800,y+400,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",T("🧺 Ваша корзина:\n"+LT61+"💶 Итого: "+_T61+" €\n\nМинимальный заказ — "+str(MIN_ORDER)+" €. Добавьте ещё на {{formatNumber("+str(MIN_ORDER)+" - 61.total; 2; \",\"; \".\")}} € 👇",
     "🧺 Ihr Warenkorb:\n"+LT61+"💶 Summe: "+_T61+" €\n\nMindestbestellwert — "+str(MIN_ORDER)+" €. Bitte fügen Sie noch Artikel für {{formatNumber("+str(MIN_ORDER)+" - 61.total; 2; \",\"; \".\")}} € hinzu 👇",
     "🧺 Su carrito:\n"+LT61+"💶 Total: "+_T61+" €\n\nPedido mínimo: "+str(MIN_ORDER)+" €. Añada productos por {{formatNumber("+str(MIN_ORDER)+" - 61.total; 2; \",\"; \".\")}} € más 👇",
     "🧺 Ваш кошик:\n"+LT61+"💶 Разом: "+_T61+" €\n\nМінімальне замовлення — "+str(MIN_ORDER)+" €. Додайте ще на {{formatNumber("+str(MIN_ORDER)+" - 61.total; 2; \",\"; \".\")}} € 👇")),("reply_markup",KB([[{"text":TT(B_MORE),"callback_data":"m"}]]))],"Меньше минимума",[[{"a":"{{61.count}}","b":"0","o":"number:greater"},{"a":"{{61.total}}","b":str(MIN_ORDER),"o":"number:less"}]],onerror=True)],
  [api(64,1800,y+200,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",T("🧺 Корзина пуста.","🧺 Der Warenkorb ist leer.","🧺 El carrito está vacío.","🧺 Кошик порожній.")),("reply_markup",EMPTY_KB)],"Пусто",[[{"a":"{{ifempty(61.count; 0)}}","b":"0","o":"number:lessorequal"}]],onerror=True)],
 ])]); y+=400
DISC = "floor(ifempty(71.total; 0) * ifempty(71.promo; 0)) / 100"
AFTER = "(ifempty(71.total; 0) - "+DISC+")"
BUSED = "floor(min(ifempty(77.bonus; 0); "+AFTER+" * "+str(BONUS_CAP/100)+") * 100) / 100"
CITY='{{switch('+D(2)+'; "1"; "Эдделак"; "2"; "Марне"; "3"; "Брунсбюттель"; "4"; "Хайде"; "Другое место")}}'
SLOTS=["Сегодня 12–16","Сегодня 17–21","Завтра 12–16","Завтра 17–21"]
SLOT='{{switch('+D(3)+'; "1"; "'+SLOTS[0]+'"; "2"; "'+SLOTS[1]+'"; "3"; "'+SLOTS[2]+'"; "'+SLOTS[3]+'")}}'
# v9.6: город и время в data store — по-русски (для владельца); клиенту — на его языке
SLOTS_TR=[(SLOTS[0],"Heute 12–16","Hoy 12–16","Сьогодні 12–16"),(SLOTS[1],"Heute 17–21","Hoy 17–21","Сьогодні 17–21"),
          (SLOTS[2],"Morgen 12–16","Mañana 12–16","Завтра 12–16"),(SLOTS[3],"Morgen 17–21","Mañana 17–21","Завтра 17–21")]
CITY_L='{{switch('+D(2)+'; "1"; '+SS(CITIES_TR[0])+'; "2"; '+SS(CITIES_TR[1])+'; "3"; '+SS(CITIES_TR[2])+'; "4"; '+SS(CITIES_TR[3])+'; '+SS(CITIES_TR[4])+')}}'
SLOT_L='{{switch('+D(3)+'; "1"; '+SS(SLOTS_TR[0])+'; "2"; '+SS(SLOTS_TR[1])+'; "3"; '+SS(SLOTS_TR[2])+'; '+SS(SLOTS_TR[3])+')}}'
SLOT_KB=KB([[{"text":TT(SLOTS_TR[0]),"callback_data":"t|{{"+D(2)+"}}|1"},{"text":TT(SLOTS_TR[1]),"callback_data":"t|{{"+D(2)+"}}|2"}],
            [{"text":TT(SLOTS_TR[2]),"callback_data":"t|{{"+D(2)+"}}|3"},{"text":TT(SLOTS_TR[3]),"callback_data":"t|{{"+D(2)+"}}|4"}],
            [{"text":T("⬅️ Другой город","⬅️ Andere Stadt","⬅️ Otra ciudad","⬅️ Інше місто"),"callback_data":"o"}]])
routes.append([api(66,900,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","📍 "+CITY_L+"\n"+T("🕐 Когда удобно получить заказ?","🕐 Wann möchten Sie die Bestellung erhalten?","🕐 ¿Cuándo le viene bien recibir el pedido?","🕐 Коли зручно отримати замовлення?")),("reply_markup",SLOT_KB)],"Выбран город",[[eq(D(1),"c")]],onerror=True)]); y+=200
routes.append([
 ds(70,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Выбрано время",[[eq(D(1),"t")]]),
 ds(71,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 TOUCH_CUST(76,1350,y,None,None),
 ds(77,1500,y,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 sv(78,1650,y,[("disc","{{"+DISC+"}}"),("bused","{{"+BUSED+"}}"),("final","{{"+AFTER+" - "+BUSED+"}}")]),
 sv(79,1800,y,[("pline",T("🎟 Промокод {{71.pcode}} (−{{71.promo}}%): −"+FMT("78.disc")+" €\n","🎟 Gutscheincode {{71.pcode}} (−{{71.promo}}%): −"+FMT("78.disc")+" €\n","🎟 Código promocional {{71.pcode}} (−{{71.promo}}%): −"+FMT("78.disc")+" €\n","🎟 Промокод {{71.pcode}} (−{{71.promo}}%): −"+FMT("78.disc")+" €\n")),
               ("bline",T("💎 Бонусами: −"+FMT("78.bused")+" €\n","💎 Mit Bonus: −"+FMT("78.bused")+" €\n","💎 Con bonos: −"+FMT("78.bused")+" €\n","💎 Бонусами: −"+FMT("78.bused")+" €\n"))]),
 ds(75,1950,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"disc":"{{78.disc}}","bused":"{{78.bused}}","final":"{{78.final}}","city":CITY,"slot":SLOT}}),
 router(72,2100,y,[
  [api(73,2400,y,"sendMessage",[("chat_id",CHAT),("text",T(*[h+"\n{{ifempty(71.ltext; 71.text)}}📍 "+CITY_L+"\n🕐 "+SLOT_L+"\n"+pay+"\n"+goods+" "+FMT("71.total")+" €\n{{if(78.disc > 0; 79.pline; \"\")}}{{if(78.bused > 0; 79.bline; \"\")}}"+topay+" "+FMT("78.final")+" €\n\n"+ask
     for h,pay,goods,topay,ask in zip(H_ORDER,
       ("💳 Оплата: онлайн или наличными при получении","💳 Zahlung: online oder bar bei Erhalt","💳 Pago: en línea o en efectivo al recibirlo","💳 Оплата: онлайн або готівкою під час отримання"),
       ("🧺 Товары:","🧺 Artikel:","🧺 Productos:","🧺 Товари:"),
       ("💶 К оплате:","💶 Zu zahlen:","💶 A pagar:","💶 До сплати:"),
       ("✍️ Ответьте на это сообщение: напишите адрес доставки — улица, дом, город","✍️ Antworten Sie auf diese Nachricht: Lieferadresse — Straße, Hausnummer, Stadt",
        "✍️ Responda a este mensaje: escriba la dirección de entrega — calle, número, ciudad","✍️ Дайте відповідь на це повідомлення: напишіть адресу доставки — вулиця, будинок, місто"))])),
     ("reply_markup",FIXF(json.dumps({"force_reply":True,"input_field_placeholder":T("Улица, дом, город","Straße, Hausnr., Stadt","Calle, número, ciudad","Вулиця, будинок, місто")},ensure_ascii=False)))],"Есть товары",[[{"a":"{{71.count}}","b":"0","o":"number:greater"}]])],
  [api(74,2400,y+200,"sendMessage",[("chat_id",CHAT),("text",T("🧺 Корзина пуста. Нажмите /start, чтобы выбрать товары.","🧺 Der Warenkorb ist leer. Tippen Sie auf /start, um Artikel auszuwählen.","🧺 El carrito está vacío. Pulse /start para elegir productos.","🧺 Кошик порожній. Натисніть /start, щоб обрати товари."))],"Пусто",[[{"a":"{{ifempty(71.count; 0)}}","b":"0","o":"number:lessorequal"}]])],
 ])]); y+=400
EMPTY_REC={"text":"","ltext":"","total":0,"count":0,"kg":0,"pcs":0}
routes.append([
 ds(80,900,y,"AddRecord",{"key":CHAT,"overwrite":True,"data":EMPTY_REC},"Очистить",[[eq(D(1),"x")]]),
 api(81,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",T("🗑 Корзина очищена.","🗑 Warenkorb geleert.","🗑 Carrito vaciado.","🗑 Кошик очищено.")),("reply_markup",EMPTY_KB)],onerror=True)]); y+=200
H_ORDER_W = ("Ваш заказ","Ihre Bestellung","Su pedido","Ваше замовлення")   # как в v9.5: «Ваш заказ» без эмодзи
addr=api(40,900,y,"sendMessage",[("chat_id","{{1.message.chat.id}}"),("text",T(*["{{trim(first(split(1.message.reply_to_message.text; \"✍️\")))}}\n🏠 "+a+" {{1.message.text}}\n\n"+p for a,p in zip(H_ADDR,
     ("📞 Ответьте на это сообщение: напишите ваш номер телефона","📞 Antworten Sie auf diese Nachricht: Ihre Telefonnummer","📞 Responda a este mensaje: escriba su número de teléfono","📞 Дайте відповідь на це повідомлення: напишіть ваш номер телефону"))])),
   ("reply_markup",FIXF(json.dumps({"force_reply":True,"input_field_placeholder":T("Номер телефона","Telefonnummer","Número de teléfono","Номер телефону")},ensure_ascii=False)))],
   "Получен адрес",[[{"a":"{{1.message.reply_to_message.text}}","b":h,"o":"text:contain"}]+[{"a":"{{1.message.reply_to_message.text}}","b":a,"o":"text:notcontain"} for a in dict.fromkeys(H_ADDR)] for h in H_ORDER_W])
y+=200
EARN = "floor(ifempty(120.final; 120.total) * "+str(BONUS_PCT)+") / 100"
DAY = '{{formatDate(now; "YYYY-MM-DD"; "'+TZ+'")}}'
MONTH = '{{formatDate(now; "YYYY-MM"; "'+TZ+'")}}'
ph_flow=[
 ds(121,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Получен телефон",[[{"a":"{{1.message.reply_to_message.text}}","b":a,"o":"text:contain"}] for a in dict.fromkeys(H_ADDR)]),
 ds(120,1050,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 ds(122,1200,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"name":"{{1.message.from.first_name}} {{1.message.from.last_name}}","username":"{{1.message.from.username}}","phone":"{{1.message.text}}","last_seen":"{{now}}","lang":"{{"+LG+"}}"}},"Корзина не пуста",[[{"a":"{{ifempty(120.count; 0)}}","b":"0","o":"number:greater"}]],store=CUST),
 ds(123,1350,y,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 sv(124,1500,y,[("earn","{{"+EARN+"}}"),("nb","{{ifempty(123.bonus; 0) - ifempty(120.bused; 0)}}"),("n","{{ifempty(123.orders; 0) + 1}}"),("day",DAY),
   ("okey","{{90.chat}}-{{formatDate(now; \"X\")}}"),("ono",'{{formatDate(now; "DDMM-HHmm"; "'+TZ+'")}}'),
   ("hist",'{{formatDate(now; "DD.MM.YY"; "'+TZ+'")}} — {{120.count}} {{'+S("поз.","Pos.","art.","поз.")+'}} — '+FMT("ifempty(120.final; 120.total)")+" €")]),
 {"id":42,"mapper":{"body":'{"method":"sendMessage","chat_id":{{1.message.chat.id}},"text":'+json.dumps(T(
   "✅ Спасибо! Заказ №{{124.ono}} принят.\nМы свяжемся с вами, чтобы договориться о времени доставки.\n\n💎 После доставки начислим "+FMT("124.earn")+" € бонусами.\nВаш баланс: "+FMT("124.nb")+" €\n\nНовый заказ: /start",
   "✅ Vielen Dank! Bestellung Nr. {{124.ono}} ist eingegangen.\nWir melden uns bei Ihnen, um die Lieferzeit abzustimmen.\n\n💎 Nach der Lieferung schreiben wir Ihnen "+FMT("124.earn")+" € Bonus gut.\nIhr Guthaben: "+FMT("124.nb")+" €\n\nNeue Bestellung: /start",
   "✅ ¡Gracias! Pedido n.º {{124.ono}} recibido.\nNos pondremos en contacto con usted para acordar la hora de entrega.\n\n💎 Tras la entrega le abonaremos "+FMT("124.earn")+" € en bonos.\nSu saldo: "+FMT("124.nb")+" €\n\nNuevo pedido: /start",
   "✅ Дякуємо! Замовлення №{{124.ono}} прийнято.\nМи зв’яжемося з вами, щоб домовитися про час доставки.\n\n💎 Після доставки нарахуємо "+FMT("124.earn")+" € бонусами.\nВаш баланс: "+FMT("124.nb")+" €\n\nНове замовлення: /start"),ensure_ascii=False)+'}',"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(1650,y),"parameters":{}},
 ds(125,1800,y,"AddRecord",{"key":"{{124.okey}}","overwrite":True,"data":{"chat":CHAT,"name":"{{1.message.from.first_name}} {{1.message.from.last_name}}","phone":"{{1.message.text}}","items":"{{120.text}}","total":"{{120.total}}","disc":"{{ifempty(120.disc; 0)}}","bused":"{{ifempty(120.bused; 0)}}","final":"{{ifempty(120.final; 120.total)}}","pcode":"{{120.pcode}}","city":"{{120.city}}","slot":"{{120.slot}}","no":"{{124.ono}}","status":"принят","day":"{{124.day}}","created":"{{now}}",
   "kg":"{{ifempty(120.kg; 0)}}","pcs":"{{ifempty(120.pcs; 0)}}","earn":"{{124.earn}}","ref":"{{123.ref}}","first":"{{ifempty(123.orders; 0) = 0}}","bonus_done":False}},store=ORD),
 ds(126,1950,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"orders":"{{124.n}}","spent":"{{ifempty(123.spent; 0) + ifempty(120.final; 120.total)}}","bonus":"{{124.nb}}",
   "history":"{{124.hist}}\n{{substring(ifempty(123.history; \"\"); 0; 600)}}","last_text":"{{120.text}}","last_ltext":"{{ifempty(120.ltext; 120.text)}}","last_total":"{{120.total}}","last_count":"{{120.count}}","last_kg":"{{ifempty(120.kg; 0)}}","last_pcs":"{{ifempty(120.pcs; 0)}}"}},store=CUST),
 ds(127,2100,y,"UpdateRecord",{"key":"{{124.day}}","upsert":True,"overwriteArrays":False,"data":{"day":"{{124.day}}"}},store=STATS),
 ds(128,2250,y,"GetRecord",{"key":"{{124.day}}","returnWrapped":False},store=STATS),
 ds(129,2400,y,"UpdateRecord",{"key":"{{124.day}}","upsert":True,"overwriteArrays":False,"data":{"orders":"{{ifempty(128.orders; 0) + 1}}","revenue":"{{ifempty(128.revenue; 0) + ifempty(120.final; 120.total)}}",
   "newcust":"{{ifempty(128.newcust; 0) + if(ifempty(123.orders; 0) > 0; 0; 1)}}","disc":"{{ifempty(128.disc; 0) + ifempty(120.disc; 0)}}","bused":"{{ifempty(128.bused; 0) + ifempty(120.bused; 0)}}","kg":"{{ifempty(128.kg; 0) + ifempty(120.kg; 0)}}","pcs":"{{ifempty(128.pcs; 0) + ifempty(120.pcs; 0)}}",
   "lines":'{{ifempty(128.lines; "")}}• {{formatDate(now; "HH:mm"; "'+TZ+'")}} {{1.message.from.first_name}}, {{120.city}} — '+FMT("ifempty(120.final; 120.total)")+" €\n"}},store=STATS),
 ds(260,2400,y+150,"UpdateRecord",{"key":MONTH,"upsert":True,"overwriteArrays":False,"data":{"day":MONTH}},store=STATS),
 ds(261,2450,y+150,"GetRecord",{"key":MONTH,"returnWrapped":False},store=STATS),
 ds(262,2500,y+150,"UpdateRecord",{"key":MONTH,"upsert":True,"overwriteArrays":False,"data":{"orders":"{{ifempty(261.orders; 0) + 1}}","revenue":"{{ifempty(261.revenue; 0) + ifempty(120.final; 120.total)}}",
   "kg":"{{ifempty(261.kg; 0) + ifempty(120.kg; 0)}}","pcs":"{{ifempty(261.pcs; 0) + ifempty(120.pcs; 0)}}"}},store=STATS),
]
g_clear=ds(45,2550,y,"AddRecord",{"key":CHAT,"overwrite":True,"data":EMPTY_REC})
# v9.6: карточка владельцу — всегда по-русски: собирается из корзины (120), а не из сообщения клиента (оно на его языке).
# Для русского клиента текст тот же, что в v9.5 (сводка «🧾 Ваш заказ …» + адрес).
_ADDR_SRC = 'first(split(get(split(1.message.reply_to_message.text; "🏠"); 2); "📞"))'
for _a in dict.fromkeys(H_ADDR): _ADDR_SRC = f'replace({_ADDR_SRC}; "{_a}"; "")'
ADDR = "trim(" + _ADDR_SRC + ")"
_DC = "ifempty(120.disc; 0) > 0"; _BC = "ifempty(120.bused; 0) > 0"
CARD_ORDER = ("🧾 Ваш заказ\n{{120.text}}📍 {{120.city}}\n🕐 {{120.slot}}\n💳 Оплата: онлайн или наличными при получении\n🧺 Товары: "+FMT("120.total")+" €\n"
  '{{if('+_DC+'; "🎟 Промокод "; "")}}{{if('+_DC+'; 120.pcode; "")}}{{if('+_DC+'; " (−"; "")}}{{if('+_DC+'; 120.promo; "")}}{{if('+_DC+'; "%): −"; "")}}'
  '{{if('+_DC+'; formatNumber(120.disc; 2; ","; "."); "")}}{{if('+_DC+'; " €\n"; "")}}'
  '{{if('+_BC+'; "💎 Бонусами: −"; "")}}{{if('+_BC+'; formatNumber(120.bused; 2; ","; "."); "")}}{{if('+_BC+'; " €\n"; "")}}'
  "💶 К оплате: "+FMT("ifempty(120.final; 120.total)")+" €\n🏠 Адрес доставки: {{"+ADDR+"}}")
g1=api(41,2700,y,"sendMessage",[("chat_id",GROUP),("text","🆕 НОВЫЙ ЗАКАЗ №{{124.ono}} — RAIV FISH\n{{if(ifempty(123.orders; 0) > 0; \"🔁 Постоянный клиент, заказ №\"; \"🆕 Новый клиент\")}}{{if(ifempty(123.orders; 0) > 0; 124.n; \"\")}} · ⚖️ {{formatNumber(ifempty(120.kg; 0); 2; \",\"; \".\")}} кг · 💎 после доставки +"+FMT("124.earn")+" €\n\n"+CARD_ORDER+"\n📞 Телефон: {{1.message.text}}\n👤 Клиент: {{1.message.from.first_name}} {{1.message.from.last_name}} @{{1.message.from.username}}\n\n🗺 Маршрут: https://www.google.com/maps/search/?api=1&query={{encodeURL("+ADDR+")}}%2C%20Deutschland"),("reply_markup",'{"inline_keyboard":[[{"text":"🚚 В пути","callback_data":"s|{{124.okey}}|1"},{"text":"✅ Доставлен","callback_data":"s|{{124.okey}}|2"}]]}')])
g3=api(43,2850,y,"sendMessage",[("chat_id",GROUP),("text","💬 Связаться с клиентом в Telegram 👇"),("reply_to_message_id","{{41.body.result.message_id}}"),("reply_markup","{\"inline_keyboard\":[[{\"text\":\"💬 Написать клиенту\",\"url\":\"tg://user?id={{1.message.from.id}}\"}]]}")],onerror=True)
OWN = {"a":"{{1.message.from.id}}","b":OWNER_ID,"o":"text:equal"}
NOREPLY = {"a":"{{1.message.reply_to_message.message_id}}","o":"notexist"}
ARG = lambda n: 'get(split(trim(1.message.text); " "); '+str(n)+')'
admin_help = ("🛠 Команды владельца\n\n"
 "/report — продажи за сегодня\n"
 "/promo КОД 10 — создать промокод на 10% (КОД 0 — выключить)\n"
 "/send текст — рассылка всем клиентам бота\n"
 "/catalog — коды товаров, цены и наличие\n"
 "/price b5 37 — новая цена (подтверждение кнопкой)\n"
 "/stock b5 0 — нет в наличии, /stock b5 1 — снова есть\n"
 "В канале под заказом: 🚚 В пути / ✅ Доставлен — клиент получит уведомление и оценит заказ\n\n"
 "Каждый вечер в 21:00 отчёт приходит в канал заказов.\n"
 "Бонусы: "+str(BONUS_PCT)+"% с заказа, списание до "+str(BONUS_CAP)+"% суммы.")
y+=600
own=[]
ORDK = "{{"+D(2)+"}}"
STAR = '{{switch('+D(3)+'; "1"; "⭐"; "2"; "⭐⭐"; "3"; "⭐⭐⭐"; "4"; "⭐⭐⭐⭐"; "⭐⭐⭐⭐⭐")}}'
own.append([ds(190,900,y,"UpdateRecord",{"key":ORDK,"upsert":False,"overwriteArrays":False,"data":{"status":'{{if('+D(3)+' = "1"; "в пути"; "доставлен")}}',"status_at":"{{now}}"}},"Статус заказа",[[eq(D(1),"s")]],store=ORD),
  ds(191,1200,y,"GetRecord",{"key":ORDK,"returnWrapped":False},store=ORD),
  ds(267,1350,y,"GetRecord",{"key":"{{191.chat}}","returnWrapped":False},store=CUST),   # v9.6: язык клиента для уведомлений
  router(192,1500,y,[
   [api(193,1800,y,"sendMessage",[("chat_id","{{191.chat}}"),("text",T("🚚 Ваш заказ №{{191.no}} уже в пути! Скоро будем.","🚚 Ihre Bestellung Nr. {{191.no}} ist unterwegs! Wir sind bald da.","🚚 ¡Su pedido n.º {{191.no}} ya está en camino! Llegamos pronto.","🚚 Ваше замовлення №{{191.no}} уже в дорозі! Скоро будемо.",lang="267.lang"))],"В пути",[[eq(D(3),"1")]],onerror=True),
    api(194,2100,y,"editMessageReplyMarkup",[("chat_id",CHAT),("message_id",MID),("reply_markup",'{"inline_keyboard":[[{"text":"🚚 В пути ✓","callback_data":"z"},{"text":"✅ Доставлен","callback_data":"s|'+ORDK+'|2"}]]}')],onerror=True)],
   [router(264,1800,y+250,[
    [api(195,1800,y+250,"sendMessage",[("chat_id","{{191.chat}}"),("text",T("✅ Заказ №{{191.no}} доставлен. Приятного аппетита! 🐟\n\nОцените, пожалуйста, заказ:","✅ Bestellung Nr. {{191.no}} wurde geliefert. Guten Appetit! 🐟\n\nBitte bewerten Sie die Bestellung:",
     "✅ Pedido n.º {{191.no}} entregado. ¡Buen provecho! 🐟\n\nPor favor, valore el pedido:","✅ Замовлення №{{191.no}} доставлено. Смачного! 🐟\n\nОцініть, будь ласка, замовлення:",lang="267.lang")),
     ("reply_markup",'{"inline_keyboard":[['+",".join('{"text":"'+"⭐"*i+'","callback_data":"rt|'+ORDK+'|'+str(i)+'"}' for i in (1,2,3))+'],['+",".join('{"text":"'+"⭐"*i+'","callback_data":"rt|'+ORDK+'|'+str(i)+'"}' for i in (4,5))+']]}')],"Доставлен",[[eq(D(3),"2")]],onerror=True),
    api(196,2100,y+250,"editMessageReplyMarkup",[("chat_id",CHAT),("message_id",MID),("reply_markup",'{"inline_keyboard":[[{"text":"✅ Доставлен","callback_data":"z"}]]}')],onerror=True)],
    [ds(250,2400,y+250,"GetRecord",{"key":"{{191.chat}}","returnWrapped":False},"Доставлен, бонусы ещё не начислены",[[{"a":"{{191.bonus_done}}","b":"true","o":"text:notequal"},eq(D(3),"2")]],store=CUST),
    ds(251,2700,y+250,"UpdateRecord",{"key":"{{191.chat}}","upsert":False,"overwriteArrays":False,"data":{"bonus":"{{ifempty(250.bonus; 0) + ifempty(191.earn; 0)}}"}},store=CUST),
    ds(252,3000,y+250,"UpdateRecord",{"key":ORDK,"upsert":False,"overwriteArrays":False,"data":{"bonus_done":True}},store=ORD),
    api(259,3300,y+250,"sendMessage",[("chat_id","{{191.chat}}"),("text",T(*[a+FMT("ifempty(191.earn; 0)")+b+"{{191.no}}"+c+FMT("ifempty(250.bonus; 0) + ifempty(191.earn; 0)")+" €" for a,b,c in (
     ("💎 Начислено "," € бонусами за заказ №",". Баланс: "),("💎 Ihnen wurden "," € Bonus für Bestellung Nr. ",". Guthaben: "),
     ("💎 Se le han abonado "," € en bonos por el pedido n.º ",". Saldo: "),("💎 Нараховано "," € бонусами за замовлення №",". Баланс: "))],lang="267.lang"))],onerror=True)],
    [ds(253,3600,y+250,"GetRecord",{"key":"{{191.ref}}","returnWrapped":False},"Доставлен, первый заказ друга",[[eq(D(3),"2"),{"a":"{{191.first}}","b":"true","o":"text:equal"},{"a":"{{191.ref}}","o":"exist"}]],store=CUST),
    ds(254,3900,y+250,"UpdateRecord",{"key":"{{191.ref}}","upsert":False,"overwriteArrays":False,"data":{"bonus":"{{ifempty(253.bonus; 0) + "+str(REF_BONUS)+"}}"}},"Пригласивший есть в базе",[[{"a":"{{253.chat}}","o":"exist"}]],store=CUST),
    api(255,4200,y+250,"sendMessage",[("chat_id","{{191.ref}}"),("text",T("🎁 Ваш друг получил первый заказ — вам +"+str(REF_BONUS)+" € бонусами! Спасибо, что советуете RAIV FISH.",
     "🎁 Ihr Freund hat seine erste Bestellung erhalten — Sie bekommen +"+str(REF_BONUS)+" € Bonus! Danke, dass Sie RAIV FISH weiterempfehlen.",
     "🎁 Su amigo ha recibido su primer pedido: ¡+"+str(REF_BONUS)+" € en bonos para usted! Gracias por recomendar RAIV FISH.",
     "🎁 Ваш друг отримав перше замовлення — вам +"+str(REF_BONUS)+" € бонусами! Дякуємо, що радите RAIV FISH.",lang="253.lang"))],onerror=True)]])]]) ]); y+=500
own.append([ds(197,900,y,"UpdateRecord",{"key":ORDK,"upsert":False,"overwriteArrays":False,"data":{"rating":"{{"+D(3)+"}}"}},"Оценка",[[eq(D(1),"rt")]],store=ORD),
  ds(198,1200,y,"GetRecord",{"key":ORDK,"returnWrapped":False},store=ORD),
  api(199,1500,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",T("Спасибо за оценку "+STAR+"!\nБудем рады видеть вас снова 🐟","Danke für Ihre Bewertung "+STAR+"!\nWir freuen uns, Sie wiederzusehen 🐟","¡Gracias por su valoración "+STAR+"!\nSerá un placer volver a atenderle 🐟","Дякуємо за оцінку "+STAR+"!\nБудемо раді бачити вас знову 🐟")),
     ("reply_markup",KB([[{"text":T("🛒 Новый заказ","🛒 Neue Bestellung","🛒 Nuevo pedido","🛒 Нове замовлення"),"callback_data":"m"}]]))],onerror=True),
  api(184,1800,y,"sendMessage",[("chat_id",GROUP),("text",STAR+" Оценка заказа №{{198.no}} — {{198.name}}{{if(parseNumber("+D(3)+"; \".\") < 4; \"\\n⚠️ Низкая оценка — напишите клиенту\"; \"\")}}")],onerror=True),
  ds(185,2100,y,"UpdateRecord",{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"day":DAY}},store=STATS),
  ds(186,2400,y,"GetRecord",{"key":DAY,"returnWrapped":False},store=STATS),
  ds(187,2700,y,"UpdateRecord",{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"rsum":"{{ifempty(186.rsum; 0) + parseNumber("+D(3)+"; \".\")}}","rcount":"{{ifempty(186.rcount; 0) + 1}}"}},store=STATS)]); y+=300
own.append([resp(170,900,y,"/admin",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/admin","o":"text:startwith"}]],{"method":"sendMessage","chat_id":chat,"text":admin_help})]); y+=200
PCT = "parseNumber(ifempty("+ARG(3)+"; \"0\"); \".\")"
own.append([api(256,900,y,"sendMessage",[("chat_id",CHAT),("text","⚠️ Скидка по промокоду — от 1 до "+str(PROMO_MAX)+" %. Пример: /promo FISH10 10\n/promo FISH10 0 — выключить.")],"/promo вне 0–"+str(PROMO_MAX),
   [[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/promo ","o":"text:startwith"},{"a":"{{"+PCT+"}}","b":str(PROMO_MAX),"o":"number:greater"}],[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/promo ","o":"text:startwith"},{"a":"{{"+PCT+"}}","b":"0","o":"number:less"}]])]); y+=200
own.append([ds(171,900,y,"AddRecord",{"key":"{{upper("+ARG(2)+")}}","overwrite":True,"data":{"code":"{{upper("+ARG(2)+")}}","percent":"{{parseNumber(ifempty("+ARG(3)+"; \"0\"); \".\")}}","active":"{{parseNumber(ifempty("+ARG(3)+"; \"0\"); \".\") > 0}}","uses":0}},"/promo",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/promo ","o":"text:startwith"},{"a":"{{"+PCT+"}}","b":str(PROMO_MAX),"o":"number:lessorequal"},{"a":"{{"+PCT+"}}","b":"0","o":"number:greaterorequal"}]],store=PROMO),
  resp(172,1200,y,None,None,{"method":"sendMessage","chat_id":chat,"text":ph('"🎟 Промокод {{upper('+ARG(2)+')}}: {{if(parseNumber(ifempty('+ARG(3)+'; "0"); ".") > 0; "скидка "; "выключен")}}{{if(parseNumber(ifempty('+ARG(3)+'; "0"); ".") > 0; '+ARG(3)+'; "")}}{{if(parseNumber(ifempty('+ARG(3)+'; "0"); ".") > 0; "%"; "")}}.\\nКлиенты вводят его кнопкой «🎟 Промокод»."')})]); y+=200
own.append([resp(173,900,y,"/send",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/send ","o":"text:startwith"}]],{"method":"sendMessage","chat_id":chat,"text":"📣 Рассылка отправляется всем клиентам бота. Копия придёт и вам."}),
  search(174,1200,y,CUST,[[{"a":"chat","o":"exist"},{"a":"blocked","o":"notexist"}],[{"a":"chat","o":"exist"},{"a":"blocked","o":"boolean:isfalse"}]]),
  api(175,1500,y,"sendMessage",[("chat_id","{{174.data.chat}}"),("text",'{{substring(trim(1.message.text); 6; 4000)}}\n\n'+T("/start — каталог · /stop — отписаться от рассылок","/start — Katalog · /stop — Rundschreiben abbestellen","/start — catálogo · /stop — darse de baja de los envíos","/start — каталог · /stop — відписатися від розсилок",lang="174.data.lang")),
     ("reply_markup",KB([[{"text":T("🛒 К покупкам","🛒 Zum Einkaufen","🛒 Ir a la tienda","🛒 До покупок",lang="174.data.lang"),"callback_data":"m"}]]))],"Есть клиент",[[{"a":"{{174.data.chat}}","o":"exist"}]],onerror=True)]); y+=200
own.append([TOUCH_CUST(176,900,y,"/stop",[[NOREPLY,{"a":"{{1.message.text}}","b":"/stop","o":"text:startwith"}]]),
  ds(177,1200,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"blocked":True}},store=CUST),
  resp(178,1500,y,None,None,{"method":"sendMessage","chat_id":chat,"text":T("Вы отписались от рассылок. Заказы и бонусы сохранены.\n/start — открыть каталог","Sie haben die Rundschreiben abbestellt. Bestellungen und Bonus bleiben erhalten.\n/start — Katalog öffnen","Se ha dado de baja de los envíos. Sus pedidos y bonos se conservan.\n/start — abrir el catálogo","Ви відписалися від розсилок. Замовлення та бонуси збережено.\n/start — відкрити каталог")})]); y+=200
CODEK = 'cat_{{lower('+ARG(2)+')}}'
NEWP = 'parseNumber(replace(ifempty('+ARG(3)+'; "0"); ","; "."); ".")'
CB_OWN = {"a":"{{1.callback_query.from.id}}","b":OWNER_ID,"o":"text:equal"}
CONFIRM = lambda code, cbv: KB([[{"text":"✅ Подтвердить","callback_data":code+"|{{lower("+ARG(2)+")}}|"+cbv,"style":"success"},{"text":"Отмена","callback_data":"zx"}]])
# /price b5 37
own.append([ds(220,900,y,"GetRecord",{"key":CODEK,"returnWrapped":False},"/price",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/price ","o":"text:startwith"}]],store=PROMO),
  router(221,1200,y,[
   [api(222,1500,y,"sendMessage",[("chat_id",CHAT),("text","💶 {{220.name}}: {{replace(toString(220.price); \".\"; \",\")}} € → {{replace(toString("+NEWP+"); \".\"; \",\")}} €\nПодтвердить новую цену?"),
     ("reply_markup",CONFIRM("cp","{{"+NEWP+"}}"))],"Товар есть и цена > 0",[[{"a":"{{220.item}}","o":"exist"},{"a":"{{"+NEWP+"}}","b":"0","o":"number:greater"}]])],
   [api(223,1500,y+200,"sendMessage",[("chat_id",CHAT),("text","🤔 Не понял. Пример: /price b5 37\nКоды товаров: /catalog")],"Ошибка",
     [[{"a":"{{220.item}}","o":"notexist"}],[{"a":"{{"+NEWP+"}}","b":"0","o":"number:lessorequal"}]])]])]); y+=400
# /stock b5 0|1
own.append([ds(224,900,y,"GetRecord",{"key":CODEK,"returnWrapped":False},"/stock",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/stock ","o":"text:startwith"}]],store=PROMO),
  router(225,1200,y,[
   [api(226,1500,y,"sendMessage",[("chat_id",CHAT),("text","📦 {{224.name}}: {{if(224.stock; \"есть\"; \"нет\")}} → {{if("+ARG(3)+" = \"1\"; \"есть в наличии\"; \"нет в наличии\")}}\nПодтвердить?"),
     ("reply_markup",CONFIRM("cs","{{if("+ARG(3)+" = \"1\"; \"1\"; \"0\")}}"))],"Товар есть",[[{"a":"{{224.item}}","o":"exist"}]])],
   [api(227,1500,y+200,"sendMessage",[("chat_id",CHAT),("text","🤔 Не понял. Пример: /stock b5 0 — нет в наличии, /stock b5 1 — есть\nКоды товаров: /catalog")],"Нет товара",[[{"a":"{{224.item}}","o":"notexist"}]])]])]); y+=400
# подтверждение кнопкой (только владелец)
own.append([ds(228,900,y,"UpdateRecord",{"key":"cat_{{"+D(2)+"}}","upsert":False,"overwriteArrays":False,"data":{"price":"{{parseNumber("+D(3)+"; \".\")}}","updated":"{{now}}"}},"Подтверждена цена",[[eq(D(1),"cp"),CB_OWN]],store=PROMO),
  api(229,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","✅ Цена обновлена: {{99.name}} — было {{replace(toString(99.price); \".\"; \",\")}} €, стало {{replace("+D(3)+"; \".\"; \",\")}} €.\nБот и витрина уже показывают новую цену.")],onerror=True)]); y+=200
own.append([ds(230,900,y,"UpdateRecord",{"key":"cat_{{"+D(2)+"}}","upsert":False,"overwriteArrays":False,"data":{"stock":"{{"+D(3)+" = \"1\"}}","updated":"{{now}}"}},"Подтверждено наличие",[[eq(D(1),"cs"),CB_OWN]],store=PROMO),
  api(231,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","✅ {{99.name}}: {{if("+D(3)+" = \"1\"; \"снова в наличии\"; \"нет в наличии — скрыт из каталога и витрины\")}}.")],onerror=True)]); y+=200
own.append([api(232,900,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","Отменено.")],"Отмена",[[eq(D(1),"zx")]],onerror=True)]); y+=200
# /catalog
own.append([search(233,900,y,PROMO,[[{"a":"item","o":"exist"}]],"/catalog",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/catalog","o":"text:startwith"}]],limit=100),
  {"id":234,"mapper":{"line":"{{233.data.item}} · {{233.data.name}} — {{replace(toString(233.data.price); \".\"; \",\")}} € {{if(233.data.stock; \"✅\"; \"❌\")}}"},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,y),"parameters":{"feeder":233},
   "filter":{"name":"Товар","conditions":[[{"a":"{{233.data.item}}","o":"exist"}]]}},
  api(235,1500,y,"sendMessage",[("chat_id",CHAT),("text","🗂 Каталог (код · товар — цена · наличие)\n\n{{join(map(234.array; \"line\"); \"\n\")}}\n\nИзменить: /price b5 37 · /stock b5 0")])]); y+=200
# 📦 Склад: владелец переключает наличие кнопками (sk|b — раздел, ct|b5|0 — переключить, sm//sklad — разделы)
SKC = 'substring('+D(2)+'; 0; 1)'
SK_TITLE = "switch("+SKC+"; "+"; ".join(f'"{c}"; "{t}"' for c,t,_ in cats)+'; "Склад")'
sk_btn = '[{"text":"{{if(237.data.stock; "✅"; "❌")}} {{237.data.name}}","callback_data":"ct|{{237.data.item}}|{{if(237.data.stock; "0"; "1")}}"}]'
sk_body = ('{"method":"editMessageText","chat_id":{{1.callback_query.message.chat.id}},"message_id":{{1.callback_query.message.message_id}},'
  '"text":"📦 Склад · {{'+SK_TITLE+'}}\\nНажмите на товар, чтобы переключить: ✅ есть → ❌ нет и обратно.\\nИзменения сразу видны в боте и витрине.",'
  '"reply_markup":{"inline_keyboard":[{{join(map(238.array; "btn"); ",")}}{{if(length(238.array) > 0; ","; "")}}[{"text":"⬅️ Разделы склада","callback_data":"sm"}]]}}')
SK_MENU = KB([[{"text":t,"callback_data":"sk|"+c}] for c,t,_ in cats])
SK_CB_OWN = [eq(D(1),"sk"),CB_OWN]
own.append([ds(236,900,y,"UpdateRecord",{"key":"cat_{{"+D(2)+"}}","upsert":False,"overwriteArrays":False,"data":{"stock":"{{"+D(3)+" = \"1\"}}","updated":"{{now}}"}},"Склад: переключить",[[eq(D(1),"ct"),CB_OWN]],store=PROMO)]); y+=200
own.append([search(237,900,y,PROMO,[[{"a":"item","o":"exist"},{"a":"cat","o":"text:equal","b":"{{"+SKC+"}}"}]],"Склад: раздел",[[eq(D(1),"sk"),CB_OWN],[eq(D(1),"ct"),CB_OWN]],limit=50),
  {"id":238,"mapper":{"btn":sk_btn},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,y),"parameters":{"feeder":237},
   "filter":{"name":"Товар","conditions":[[{"a":"{{237.data.item}}","o":"exist"}]]}},
  {"id":239,"mapper":{"body":sk_body,"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(1500,y),"parameters":{}}]); y+=200
own.append([api(240,900,y,"sendMessage",[("chat_id",CHAT),("text","📦 Склад — выберите раздел. Нажатие на товар переключает наличие."),("reply_markup",SK_MENU)],"/sklad",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/sklad","o":"text:startwith"}]])]); y+=200
own.append([api(241,900,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","📦 Склад — выберите раздел. Нажатие на товар переключает наличие."),("reply_markup",SK_MENU)],"Склад: разделы",[[eq(D(1),"sm"),CB_OWN]],onerror=True)]); y+=200
REPORT_TXT = ("📊 Продажи за {{formatDate(now; \"DD.MM.YYYY\"; \""+TZ+"\")}}\n\n"
 "🧾 Заказов: {{ifempty(@S.orders; 0)}}\n💶 Выручка: "+FMT("ifempty(@S.revenue; 0)")+" €\n"
 "🧮 Средний чек: "+FMT("if(ifempty(@S.orders; 0) > 0; @S.revenue / @S.orders; 0)")+" €\n"
 "🆕 Новых клиентов: {{ifempty(@S.newcust; 0)}}\n🎟 Скидки по промокодам: "+FMT("ifempty(@S.disc; 0)")+" €\n💎 Оплачено бонусами: "+FMT("ifempty(@S.bused; 0)")+" €\n"
 "⭐ Средняя оценка: {{if(ifempty(@S.rcount; 0) > 0; formatNumber(@S.rsum / @S.rcount; 1; \",\"; \".\"); \"—\")}} ({{ifempty(@S.rcount; 0)}})\n"
 "⚖️ Продано: {{formatNumber(ifempty(@S.kg; 0); 2; \",\"; \".\")}} кг · {{ifempty(@S.pcs; 0)}} шт\n"
 "🧺 Напомнили о брошенной корзине: {{ifempty(@S.abandoned; 0)}}\n\n{{ifempty(@S.lines; \"Заказов пока нет.\")}}")
MONTH_TXT = ("\n\n📅 С начала месяца: {{ifempty(@M.orders; 0)}} зак. · "+FMT("ifempty(@M.revenue; 0)")+" € · ⚖️ {{formatNumber(ifempty(@M.kg; 0); 2; \",\"; \".\")}} кг · {{ifempty(@M.pcs; 0)}} шт")
own.append([ds(179,900,y,"UpdateRecord",{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"day":DAY}},"/report",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/report","o":"text:startwith"}]],store=STATS),
  ds(180,1200,y,"GetRecord",{"key":DAY,"returnWrapped":False},store=STATS),
  ds(265,1300,y,"UpdateRecord",{"key":MONTH,"upsert":True,"overwriteArrays":False,"data":{"day":MONTH}},store=STATS),
  ds(263,1350,y,"GetRecord",{"key":MONTH,"returnWrapped":False},store=STATS),
  api(181,1500,y,"sendMessage",[("chat_id",CHAT),("text",REPORT_TXT.replace("@S","180")+MONTH_TXT.replace("@M","263"))])])
AMOUNT = "{{round(ifempty(120.final; 120.total) * 100)}}"
pay_body = ("mode=payment&success_url="+BOT_URL+"&cancel_url="+BOT_URL+"&client_reference_id={{124.okey}}"
 "&metadata[chat]={{90.chat}}&metadata[order]={{124.okey}}&metadata[no]={{124.ono}}&metadata[name]={{encodeURL(1.message.from.first_name)}}"
 "&line_items[0][quantity]=1&line_items[0][price_data][currency]=eur&line_items[0][price_data][unit_amount]="+AMOUNT+
 "&line_items[0][price_data][product_data][name]={{encodeURL(\"RAIV FISH — заказ\")}}"
 "&line_items[0][price_data][product_data][description]={{encodeURL(substring(120.text; 0; 300))}}")
pay = {"id":130,"module":"stripe:makeAnApiCall","version":1,"metadata":meta(2700,y+250),"parameters":{"__IMTCONN__":STRIPE_CONN},
  "mapper":{"url":"/v1/checkout/sessions","method":"POST","headers":[{"key":"Content-Type","value":"application/x-www-form-urlencoded"}],"qs":[],"body":pay_body},
  "filter":{"name":"Сумма от 0,50 €","conditions":[[{"a":"{{ifempty(120.final; 120.total)}}","b":"0.5","o":"number:greaterorequal"}]+([] if STRIPE_PUBLIC else [{"a":"{{90.chat}}","b":OWNER_ID,"o":"text:equal"}])]},
  "onerror":[{"id":630,"mapper":None,"module":"builtin:Ignore","version":1,"metadata":meta(2700,y+550)}]}
pay_msg = api(131,3000,y+250,"sendMessage",[("chat_id",CHAT),("text",T("💳 Можно оплатить заказ онлайн — "+FMT("ifempty(120.final; 120.total)")+" €\nApple Pay, Google Pay или карта, безопасно через Stripe.\nИли наличными при получении — как удобно.",
   "💳 Sie können die Bestellung online bezahlen — "+FMT("ifempty(120.final; 120.total)")+" €\nApple Pay, Google Pay oder Karte, sicher über Stripe.\nOder bar bei Erhalt — wie es Ihnen passt.",
   "💳 Puede pagar el pedido en línea — "+FMT("ifempty(120.final; 120.total)")+" €\nApple Pay, Google Pay o tarjeta, de forma segura con Stripe.\nO en efectivo al recibirlo, como prefiera.",
   "💳 Можна оплатити замовлення онлайн — "+FMT("ifempty(120.final; 120.total)")+" €\nApple Pay, Google Pay або картка, безпечно через Stripe.\nАбо готівкою під час отримання — як зручно.")),
  ("reply_markup",KB([[{"text":T("💳 Оплатить онлайн","💳 Online bezahlen","💳 Pagar en línea","💳 Оплатити онлайн"),"url":"{{130.body.url}}"}]]))],"Ссылка есть",[[{"a":"{{130.body.url}}","o":"exist"}]],onerror=True)
# корзина из витрины: sendData ("b5:1,a2:0.3") или ссылка /start c_b5-1_a2-0p3 (кнопка меню / браузер)
DEEP = "/start c_"
WA_SRC = ('ifempty(1.message.web_app_data.data; replace(replace(replace(replace(ifempty(1.message.text; ""); "'+DEEP+'"; ""); "_"; ","); "-"; ":"); "p"; "."))')
IT='first(split(201.value; ":"))'
IQ='last(split(201.value; ":"))'
ipref=f'substring({IT}; 0; 1)'
iname="205.name"
istock='if(205.stock; "1"; "0")'
itot=f'ifempty(205.price; 0) * parseNumber({IQ}; ".") / switch({ipref}; "a"; 100; "c"; 100; 1)'
iunit=f'switch({ipref}; "a"; "г"; "c"; "г"; "e"; "шт."; "кг")'
ikg=f'switch({ipref}; "a"; parseNumber({IQ}; ".") / 1000; "c"; parseNumber({IQ}; ".") / 1000; "e"; 0; parseNumber({IQ}; "."))'
ipcs=f'if({ipref} = "e"; parseNumber({IQ}; "."); 0)'
ilim=f'switch({ipref}; "a"; {MAX_G}; "c"; {MAX_G}; "e"; {MAX_PCS}; {MAX_KG})'
WA_TEXT='{{join(map(202.array; "line"); "")}}'
WA_LTEXT='{{join(map(202.array; "lline"); "")}}'
WA_TOTAL='sum(map(202.array; "total"))'
routes.append([
 {"id":201,"mapper":{"array":'{{split('+WA_SRC+'; ",")}}'},"module":"builtin:BasicFeeder","version":1,"metadata":meta(900,-2600),"parameters":{},
  "filter":{"name":"Корзина из витрины","conditions":[[{"a":"{{1.message.web_app_data.data}}","o":"exist"}],[{"a":"{{1.message.text}}","b":DEEP,"o":"text:startwith"}]]}},
 ds(205,1050,-2600,"GetRecord",{"key":"cat_{{"+IT+"}}","returnWrapped":False},store=PROMO),
 {"id":202,"mapper":{"line":"• {{"+iname+"}} — {{replace("+IQ+'; "."; ",")}} {{'+iunit+"}} — {{formatNumber("+itot+'; 2; ","; ".")}} €\n',"lline":"• {{"+NAMEX(IT,iname)+"}} — {{replace("+IQ+'; "."; ",")}} {{'+UNIT_L(ipref)+"}} — {{formatNumber("+itot+'; 2; ","; ".")}} €\n',"total":"{{"+itot+"}}","kg":"{{"+ikg+"}}","pcs":"{{"+ipcs+"}}"},
  "module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,-2600),"parameters":{"feeder":201},
  "filter":{"name":"Есть в наличии","conditions":[[{"a":"{{"+istock+"}}","b":"1","o":"text:equal"},{"a":"{{"+itot+"}}","b":"0","o":"number:greater"},{"a":"{{parseNumber("+IQ+"; \".\")}}","b":"{{"+ilim+"}}","o":"number:lessorequal"}]]}},
 ds(203,1500,-2600,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"text":WA_TEXT,"ltext":WA_LTEXT,"total":"{{"+WA_TOTAL+"}}","count":"{{length(202.array)}}","kg":"{{sum(map(202.array; \"kg\"))}}","pcs":"{{sum(map(202.array; \"pcs\"))}}","seen":"{{now}}"}},
    "Корзина не пустая",[[{"a":"{{length(202.array)}}","b":"0","o":"number:greater"}]]),
 api(204,1800,-2600,"sendMessage",[("chat_id",CHAT),("text",T(*[h+"\n"+WA_LTEXT+t+" {{formatNumber("+WA_TOTAL+'; 2; ","; ".")}} €\n\n' for h,t in zip(
     ("🛍 Корзина из витрины:","🛍 Warenkorb aus dem Schaufenster:","🛍 Carrito del escaparate:","🛍 Кошик із вітрини:"),P_TOTAL)])
   +'{{if('+WA_TOTAL+" >= "+str(MIN_ORDER)+'; '+S("🚗 Доставка бесплатно. Оформим?","🚗 Die Lieferung ist kostenlos. Bestellung aufgeben?","🚗 La entrega es gratuita. ¿Hacemos el pedido?","🚗 Доставка безкоштовна. Оформлюємо?")
   +'; '+S("Минимальный заказ "+str(MIN_ORDER)+" € — добавьте ещё товаров.","Mindestbestellwert "+str(MIN_ORDER)+" € — bitte fügen Sie weitere Artikel hinzu.","Pedido mínimo: "+str(MIN_ORDER)+" €. Añada más productos.","Мінімальне замовлення "+str(MIN_ORDER)+" € — додайте ще товарів.")+')}}'),("reply_markup",CART_BTNS)])])
dup_msg=api(258,1200,y+300,"sendMessage",[("chat_id",CHAT),("text",T("✅ Этот заказ уже оформлен и передан продавцу.\nНовый заказ: /start","✅ Diese Bestellung wurde bereits aufgegeben und an den Verkäufer übermittelt.\nNeue Bestellung: /start","✅ Este pedido ya está hecho y se ha enviado al vendedor.\nNuevo pedido: /start","✅ Це замовлення вже оформлено й передано продавцю.\nНове замовлення: /start"))],"Корзина пуста",[[{"a":"{{ifempty(120.count; 0)}}","b":"0","o":"number:lessorequal"}]],onerror=True)
rts=[{"flow":r} for r in routes]+[{"flow":[addr]},{"flow":ph_flow[:2]+[router(257,1150,y,[ph_flow[2:]+[g_clear,router(140,2650,y,[[g1,g3],[pay,pay_msg]])],[dup_msg]])]}]+[{"flow":r} for r in own]
bp={"name":"RAIV_Fish Bot — Заказы","metadata":{"instant":True,"version":1},"flow":[
 {"id":1,"mapper":{},"module":"gateway:CustomWebHook","version":1,"metadata":meta(0,0),"parameters":{"hook":HOOK,"maxResults":1}},
 {"id":90,"mapper":{"variables":unify,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(150,0),"parameters":{}},
 {"id":99,"mapper":{"key":"cat_{{"+D(2)+"}}","returnWrapped":False},"module":"datastore:GetRecord","version":1,"metadata":meta(225,0),"parameters":{"datastore":PROMO}},
 {"id":95,"mapper":{"key":"{{90.chat}}","returnWrapped":False},"module":"datastore:GetRecord","version":1,"metadata":meta(262,0),"parameters":{"datastore":CUST}},  # v9.6: язык клиента (поле lang)
 {"id":2,"mapper":{"variables":variables,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(300,0),"parameters":{}},
 {"id":3,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":meta(600,0),"routes":rts}]}
import re, sys
_s=json.dumps(bp,ensure_ascii=False)
_s=_s.replace("@@CARTBTNS@@",json.dumps(CART_BTNS,ensure_ascii=False)[1:-1]).replace("@@EMPTYKB@@",json.dumps(EMPTY_KB,ensure_ascii=False)[1:-1])
bp=json.loads(_s)
def fix(s): return re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"','"'), s)
def walk(flow):
    for m in flow:
        if m["module"]=="gateway:WebhookRespond":
            m["mapper"]["body"]=fix(m["mapper"]["body"])
            json.loads(re.sub(r"\{\{.*?\}\}","1",m["mapper"]["body"].replace("}}{{if(length(211.array) > 0; \",\"; \"\")}}","}},").replace("}}{{if(length(238.array) > 0; \",\"; \"\")}}","}},")))
        for r in m.get("routes",[]): walk(r["flow"])
walk(bp["flow"])
# цветные кнопки (Bot API 9.4): главное действие зелёное, удаление красное, статусы заказа в канале
_t=json.dumps(bp,ensure_ascii=False)
STYLE={"o":"success","x":"danger"}
# v9.6: подпись кнопки — формула switch(…; "<ru>")}}, ищем по русскому варианту в её конце
_t=re.sub(r'((?:🧾 Оформить заказ|🧺 Корзина / оформить|🗑 Очистить корзину)\\"\)\}\}\\",\s?\\"callback_data\\":\s?\\"(o|x)\\")', lambda m: m.group(1)+', \\"style\\": \\"'+STYLE[m.group(2)]+'\\"', _t)
_t=re.sub(r'(\\"callback_data\\":\s?\\"s\|[^"\\]*\|([12])\\")', lambda m: m.group(1)+', \\"style\\": \\"'+("primary" if m.group(2)=="1" else "success")+'\\"', _t)
bp=json.loads(_t)
s=json.dumps(bp,ensure_ascii=False)
assert "@@" not in s, s[s.find("@@")-80:s.find("@@")+40]
ids=[]
def collect(flow):
    for m in flow:
        ids.append(m["id"]); [ids.append(e["id"]) for e in m.get("onerror",[])]
        for r in m.get("routes",[]): collect(r["flow"])
collect(bp["flow"]); assert len(ids)==len(set(ids)), sorted(ids)
out = sys.argv[1] if len(sys.argv)>1 else "bp.json"
json.dump(bp,open(out,"w"),ensure_ascii=False)
print("ok", len(s), "modules", len(ids))
