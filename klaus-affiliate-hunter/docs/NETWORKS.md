# Партнёрские сети для рынка Германии — аудит (01.10.2026)

Статус колонки «Проверено»: ✅ — подтверждено официальным источником; ⚠️ — из вторичных источников
(агрегаторы, блоги), сверить в кабинете сети перед использованием. Комиссии меняются — агент берёт их
только из кабинета/условий программы на дату проверки, а не из этой таблицы.

| Сеть | Регистрация и требования | Категории Klaus | Комиссия | Cookie | Deeplink | API / экспорт | Соцсети | Проверено |
|---|---|---|---|---|---|---|---|---|
| **Amazon PartnerNet DE** | partnernet.amazon.de; нужно указать каждый соцканал (полный URL профиля); 3 квалифицированные продажи за первые 180 дней, иначе аккаунт закрывается | все | Baumarkt, Haushalt, Küche, Garten, Elektro-/Handwerkzeuge: 7 % (8 % при > 40 000 € в мес.), косвенные продажи 1,5 % | 24 ч | да: `amazon.de/dp/ASIN?tag=…-21` | **PA-API 5 отключён (403 с 15.05.2026)**, замена — **Creators API** (OAuth 2.0, ключи в Associates Central) | TikTok, Instagram, YouTube, Facebook разрешены при указании в аккаунте; обязательна фраза «Als Amazon-Partner verdiene ich an qualifizierten Verkäufen» | ⚠️ ставки — по вторичным источникам; ✅ PA-API → Creators API |
| **Awin** | ui.awin.com; одобрение каждой программы отдельно | OBI, toom и др. DIY/Haushalt | OBI: 2 % стандарт / 7 % контент; toom: 4–8 % | по программе | да: Link Builder / `awin1.com/cread.php?awinmid=…&awinaffid=…&ued=…` | Publisher API: programmes (`membershipStatus` joined/pending/…; `deeplinkEnabled`), transactions, product feeds, Link Builder API | по условиям каждой программы | ✅ API; ⚠️ ставки OBI/toom |
| **Adcell** | adcell.com (DE), одобрение по программам | DIY, Haushalt, Garten | по программе | по программе | да | Publisher API (статистика, промо) | по программе | ⚠️ |
| **Belboon** | belboon.com, одобрение по программам | Haushalt, Garten | по программе | по программе | да | API статистики | по программе | ⚠️ |
| **TradeTracker DE** | tradetracker.com | частично | по программе | по программе | да | API (SOAP/REST) | по программе | ⚠️ |
| **CJ / Impact** | международные, одобрение брендом | бренды техники/Smart Home | по программе | по программе | да | API | по программе | ⚠️ |
| **Digistore24** | в основном цифровые продукты/курсы | слабо подходит (не физические товары) | высокая, но не наш профиль | — | да | API | — | ⚠️, низкий приоритет |
| **Программы производителей** | Kärcher, Bosch, tado, Eve и др. — чаще через Awin/CJ | инструменты, Smart Home | по программе | по программе | да | зависит | по программе | ⚠️ |

## Вывод для архитектуры
1. **Amazon.de** — самый широкий ассортимент для Klaus, но cookie 24 ч и низкая ставка; ссылку строим сами
   по официальному формату (нужен только ваш tag). Данные товара — через **Creators API** (нужны ключи из
   Associates Central) или с открытой страницы товара. PA-API 5 больше не работает — интеграции на нём не строим.
2. **Awin** — главный источник для Baumarkt-ретейлеров (OBI, toom): длиннее cookie, официальный API
   с проверкой статуса программы (`joined`) и Link Builder. API-токен подключается в Make как ключ —
   не в чат и не в репозиторий.
3. Остальные сети — по мере одобрения программ; агент еженедельно ищет новые программы и предлагает владельцу.

## Источники
- [Amazon PartnerNet: Provision](https://partnernet.amazon.de/help/operating/schedule)
- [Amazon Partnerprogramm 2026 (rabattfuchs)](https://rabattfuchs.blog/posts/amazon-partnerprogramm-erfahrung.html)
- [PA-API 5 deprecation → Creators API](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation)
- [PA-API retirement (dev.to)](https://dev.to/th3nate/amazon-pa-api-v5-is-shutting-down-april-30-2026-here-is-what-changes-at-the-auth-layer-22ek)
- [Awin API introduction](https://help.awin.com/apidocs/introduction-1), [Publisher API: GET programmes](https://success.awin.com/s/article/Publisher-API-GET-Programmes?language=en_US), [Link Builder](https://success.awin.com/articles/en_US/Knowledge/How-can-I-use-Link-Builder-to-create-Deep-Links)
- [OBI bei Awin (100partnerprogramme)](https://www.100partnerprogramme.de/p/obi-de-10223/), [toom bei Awin](https://www.100partnerprogramme.de/p/toom-baumarkt-de/)
- [Amazon Associates DE – Hilfe](https://partnernet.amazon.de/help/node/topic/GPXFHVYZMTGPUMPE), [Amazon-Links in Social Media](https://geniuslink.com/blog/amazon-affiliate-links-on-social-media/)
