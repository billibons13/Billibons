# T-0013 · Переводы бота RAIV FISH: ru | de | es | uk (для проверки владельцем)

Подготовил: 🌐 Локализатор, 06.10.2026. Статус: **подготовлено, не выкачено** (бот 7707233 работает на v9.5).
Источник: `generate_blueprint.py` (v9.6) — таблица собрана из тех же строк, что попали в `backup/v9_6_lang_blueprint.json`.

Как читать:
- `{…}` — подставляемое значение (номер заказа, сумма, название товара, ссылка и т.п.); цены, суммы, промокоды не переводятся.
- `<br>` — перенос строки.
- Немецкий — на «Sie», испанский — на «usted», украинский — на «ви». Исключение: текст, который клиент **сам пересылает другу**
  (кнопка «📤 Отправить другу»), — на «ты/du/tú», как в русском оригинале («держи 3 €»).
- Новых обещаний нет: «Доставка бесплатно» и бонусы — только там, где они уже есть в русском тексте v9.5.
- Владельцу (карточка заказа в канале, команды /admin /promo /price /stock /sklad /report, отчёты) — всё по-русски, в таблицу не входит.
- Выбор языка: сообщение «🌐 Выберите язык · Sprache wählen · Elija el idioma · Оберіть мову» с кнопками
  «Русский · Deutsch · Español · Українська» показывается одинаково на всех языках.

## На что обратить внимание владельцу (лучше проверить носителем языка)
1. Названия рыбы на испанском и украинском — перевод по смыслу; **транслитерация** там, где точного названия нет:
   «Polosatik» (d8 «Полосатик», de/es), «Chejon» (чехонь, es), «Patasu» (палочки патасу), «Lachs-Jukola / Yukola».
2. Немецкие названия: «Sichling» (чехонь), «Ukelei» (верховодка), «Wobla» (вобла), «Brachse» (лещ), «Rotauge» (плотва).
3. Названия городов: de/es — немецкое написание (Eddelak, Brunsbüttel, Heide), uk — «Еддельак, Марне, Брунсбюттель, Гайде».
4. Если в каталоге появится новый товар (новый код), он будет показан **по-русски** на всех языках, пока перевод
   не добавят в `NAMES` генератора.

## 1. Разделы каталога
| Раздел | ru | de | es | uk |
|---|---|---|---|---|
| a | 🐟 Икра вяленая (100 г) | 🐟 Getrockneter Fischrogen (100 g) | 🐟 Huevas secas (100 g) | 🐟 Ікра в’ялена (100 г) |
| b | 🐠 Рыба вяленая (кг) | 🐠 Getrockneter Fisch (kg) | 🐠 Pescado seco (kg) | 🐠 Риба в’ялена (кг) |
| c | 🍢 Рыбные снеки (100 г) | 🍢 Fischsnacks (100 g) | 🍢 Snacks de pescado (100 g) | 🍢 Рибні снеки (100 г) |
| d | 🦑 Снеки к пиву (кг) | 🦑 Snacks zum Bier (kg) | 🦑 Snacks para cerveza (kg) | 🦑 Снеки до пива (кг) |
| e | 🥫 Консервы | 🥫 Konserven | 🥫 Conservas | 🥫 Консерви |

## 2. Товары (по коду товара)

| Код | ru (каталог) | de | es | uk |
|---|---|---|---|---|
| a1 | Икра толстолоба | Silberkarpfen-Rogen | Huevas de carpa plateada | Ікра товстолоба |
| a2 | Икра кеты | Ketalachs-Rogen | Huevas de salmón keta | Ікра кети |
| a3 | Икра форели | Forellenrogen | Huevas de trucha | Ікра форелі |
| a4 | Икра судака | Zanderrogen | Huevas de lucioperca | Ікра судака |
| a5 | Икра щуки | Hechtrogen | Huevas de lucio | Ікра щуки |
| a6 | Икра плотвы | Rotaugenrogen | Huevas de rutilo | Ікра плітки |
| a7 | Икра минтая | Alaska-Seelachs-Rogen | Huevas de abadejo de Alaska | Ікра минтаю |
| b1 | Плотва с икрой | Rotauge mit Rogen | Rutilo con huevas | Плітка з ікрою |
| b2 | Чищенные тушки плотвы без головы (100% икра) | Rotauge geputzt, ohne Kopf (100 % Rogen) | Rutilo limpio sin cabeza (100 % huevas) | Чищені тушки плітки без голови (100% ікра) |
| b3 | Вобла с икрой (80% икра) | Wobla mit Rogen (80 % Rogen) | Vobla con huevas (80 % huevas) | Вобла з ікрою (80% ікра) |
| b4 | Верховодка | Ukelei | Alburno | Верховодка |
| b5 | Лещ с икрой | Brachse mit Rogen | Brema con huevas | Лящ з ікрою |
| b6 | Лещ без икры | Brachse ohne Rogen | Brema sin huevas | Лящ без ікри |
| b7 | Карась с икрой | Karausche mit Rogen | Carpín con huevas | Карась з ікрою |
| b8 | Щука потрошеная | Hecht, ausgenommen | Lucio eviscerado | Щука потрошена |
| b9 | Форель вяленая потрошеная | Forelle getrocknet, ausgenommen | Trucha seca eviscerada | Форель в’ялена потрошена |
| b10 | Судак потрошеный | Zander, ausgenommen | Lucioperca eviscerada | Судак потрошений |
| b11 | Чехонь | Sichling | Chejon | Чехоня |
| b12 | Чехонь крупная с икрой 90% | Sichling groß, mit Rogen 90 % | Chejon grande con huevas 90 % | Чехоня велика з ікрою 90% |
| b13 | Бычок | Grundel | Gobio | Бичок |
| b14 | Корюшка с икрой (премиум) | Stint mit Rogen (Premium) | Eperlano con huevas (premium) | Корюшка з ікрою (преміум) |
| b15 | Окунь с икрой | Barsch mit Rogen | Perca con huevas | Окунь з ікрою |
| b16 | Юкола лосося | Lachs-Jukola | Yukola de salmón | Юкола лосося |
| c1 | Филе горбуши (соломка) | Buckellachsfilet (Streifen) | Filete de salmón rosado (tiras) | Філе горбуші (соломка) |
| c2 | Кальмар + лосось (соломка) | Tintenfisch + Lachs (Streifen) | Calamar + salmón (tiras) | Кальмар + лосось (соломка) |
| c3 | Корюшка сушеная потрошеная | Stint getrocknet, ausgenommen | Eperlano seco eviscerado | Корюшка сушена потрошена |
| c4 | Соломка леща | Brachsen-Streifen | Tiras de brema | Соломка ляща |
| c5 | Джерки лосося | Lachs-Jerky | Jerky de salmón | Джерки лосося |
| c6 | Ириска из лосося | Lachs-Toffee | Toffee de salmón | Іриска з лосося |
| c7 | Стейк щуки | Hechtsteak | Steak de lucio | Стейк щуки |
| d1 | Пятачки осьминога | Oktopus-Scheiben | Rodajas de pulpo | П’ятачки восьминога |
| d2 | Паутинка кальмара «сладкий чили» | Tintenfisch-Netz „Sweet Chili“ | Red de calamar «chili dulce» | Павутинка кальмара «солодкий чилі» |
| d3 | Кальмар по-шанхайски | Tintenfisch nach Shanghai-Art | Calamar al estilo Shanghái | Кальмар по-шанхайськи |
| d4 | Стружка кальмара | Tintenfisch-Raspeln | Virutas de calamar | Стружка кальмара |
| d5 | Палочки патасу | Patasu-Sticks | Palitos de patasu | Палички патасу |
| d6 | Филе голубого марлина | Blauer-Marlin-Filet | Filete de marlín azul | Філе блакитного марліна |
| d7 | Кальмар по-перуански | Tintenfisch nach peruanischer Art | Calamar al estilo peruano | Кальмар по-перуанськи |
| d8 | Полосатик | Polosatik | Polosatik | Полосатик |
| d9 | Стружка краба | Krabben-Raspeln | Virutas de cangrejo | Стружка краба |
| d10 | Анчоус | Sardellen | Anchoas | Анчоус |
| d11 | Крабовые палочки | Surimi-Sticks | Palitos de cangrejo | Крабові палички |
| e1 | Снеток в томате | Stint in Tomatensoße | Eperlano en tomate | Снеток у томаті |
| e2 | Лещ в томате | Brachse in Tomatensoße | Brema en tomate | Лящ у томаті |

## 3. Сообщения и кнопки (все строки, которые видит клиент)

| # | ru | de | es | uk |
|---|---|---|---|---|
| 1 | в граммах, например 250 | in Gramm, z. B. 250 | en gramos, por ejemplo 250 | у грамах, наприклад 250 |
| 2 | в кг, например 0,7 | in kg, z. B. 0,7 | en kg, por ejemplo 0,7 | у кг, наприклад 0,7 |
| 3 | в штуках, например 4 | in Stück, z. B. 4 | en unidades, por ejemplo 4 | у штуках, наприклад 4 |
| 4 | € / 100 г | € / 100 g | € / 100 g | € / 100 г |
| 5 | € / шт. | € / Stk. | € / ud. | € / шт. |
| 6 | € / кг | € / kg | € / kg | € / кг |
| 7 | г | g | g | г |
| 8 | шт. | Stk. | ud. | шт. |
| 9 | кг | kg | kg | кг |
| 10 | 👋 С возвращением! Ваши бонусы: 💎  | 👋 Willkommen zurück! Ihr Bonus: 💎  | 👋 ¡Bienvenido de nuevo! Sus bonos: 💎  | 👋 З поверненням! Ваші бонуси: 💎  |
| 11 | 🐟 RAIV FISH — вяленая рыба, икра и снеки к пиву<br><br>🕐 Сегодня или завтра — днём или вечером<br>💳 Онлайн или наличными · 💎 5% бонусами с каждого заказа<br><br>Выберите раздел 👇 | 🐟 RAIV FISH — getrockneter Fisch, Fischrogen und Snacks zum Bier<br><br>🕐 Heute oder morgen — tagsüber oder abends<br>💳 Online oder bar · 💎 5 % Bonus auf jede Bestellung<br><br>Bitte wählen Sie eine Kategorie 👇 | 🐟 RAIV FISH — pescado seco, huevas y snacks para cerveza<br><br>🕐 Hoy o mañana — de día o por la tarde<br>💳 En línea o en efectivo · 💎 5 % en bonos por cada pedido<br><br>Elija una sección 👇 | 🐟 RAIV FISH — в’ялена риба, ікра та снеки до пива<br><br>🕐 Сьогодні або завтра — вдень або ввечері<br>💳 Онлайн або готівкою · 💎 5% бонусами з кожного замовлення<br><br>Оберіть розділ 👇 |
| 12 | 🐟 Икра вяленая (100 г) | 🐟 Getrockneter Fischrogen (100 g) | 🐟 Huevas secas (100 g) | 🐟 Ікра в’ялена (100 г) |
| 13 | 🐠 Рыба вяленая (кг) | 🐠 Getrockneter Fisch (kg) | 🐠 Pescado seco (kg) | 🐠 Риба в’ялена (кг) |
| 14 | 🍢 Рыбные снеки (100 г) | 🍢 Fischsnacks (100 g) | 🍢 Snacks de pescado (100 g) | 🍢 Рибні снеки (100 г) |
| 15 | 🦑 Снеки к пиву (кг) | 🦑 Snacks zum Bier (kg) | 🦑 Snacks para cerveza (kg) | 🦑 Снеки до пива (кг) |
| 16 | 🥫 Консервы | 🥫 Konserven | 🥫 Conservas | 🥫 Консерви |
| 17 | 📋 Весь прайс | 📋 Preisliste | 📋 Lista de precios | 📋 Весь прайс |
| 18 | 🔁 Повторить заказ | 🔁 Bestellung wiederholen | 🔁 Repetir pedido | 🔁 Повторити замовлення |
| 19 | 📜 Мои заказы | 📜 Meine Bestellungen | 📜 Mis pedidos | 📜 Мої замовлення |
| 20 | 🎟 Промокод | 🎟 Gutscheincode | 🎟 Código promocional | 🎟 Промокод |
| 21 | 🎁 Приведи друга — 3 € обоим | 🎁 Freunde einladen — 3 € für beide | 🎁 Invita a un amigo — 3 € para ambos | 🎁 Приведи друга — 3 € обом |
| 22 | 📇 Контакты | 📇 Kontakt | 📇 Contactos | 📇 Контакти |
| 23 | 🌐 Язык | 🌐 Sprache | 🌐 Idioma | 🌐 Мова |
| 24 | 💼 Хочу такой бот для своего бизнеса | 💼 Ich möchte so einen Bot für mein Geschäft | 💼 Quiero un bot así para mi negocio | 💼 Хочу такий бот для свого бізнесу |
| 25 | 🎁 Вам начислено 3 € бонусами по приглашению друга! Они спишутся при первом заказе. | 🎁 Sie haben über die Einladung eines Freundes 3 € Bonus erhalten! Er wird bei Ihrer ersten Bestellung verrechnet. | 🎁 ¡Ha recibido 3 € en bonos por la invitación de un amigo! Se descontarán en su primer pedido. | 🎁 Вам нараховано 3 € бонусами за запрошенням друга! Вони спишуться під час першого замовлення. |
| 26 | 👋 По вашей ссылке пришёл новый покупатель. Когда он сделает первый заказ, вам начислится 3 € бонусами. | 👋 Über Ihren Link ist ein neuer Kunde gekommen. Sobald er seine erste Bestellung aufgibt, erhalten Sie 3 € Bonus. | 👋 Un nuevo cliente ha llegado a través de su enlace. Cuando haga su primer pedido, recibirá 3 € en bonos. | 👋 За вашим посиланням прийшов новий покупець. Коли він зробить перше замовлення, вам нарахується 3 € бонусами. |
| 27 | 🛍 Новинка: витрина с фото! Кнопка «🛍 Витрина» теперь всегда внизу чата — выбирайте товары по фото, корзина соберётся сама. | 🛍 Neu: Schaufenster mit Fotos! Die Schaltfläche „🛍 Schaufenster“ ist jetzt immer unten im Chat — wählen Sie Artikel nach Foto, der Warenkorb füllt sich von selbst. | 🛍 Novedad: ¡escaparate con fotos! El botón «🛍 Escaparate» está ahora siempre abajo en el chat: elija productos por foto y el carrito se llenará solo. | 🛍 Новинка: вітрина з фото! Кнопка «🛍 Вітрина» тепер завжди внизу чату — обирайте товари за фото, кошик збереться сам. |
| 28 | 🛍 Витрина | 🛍 Schaufenster | 🛍 Escaparate | 🛍 Вітрина |
| 29 | Выберите раздел 👇 | Bitte wählen Sie eine Kategorie 👇 | Elija una sección 👇 | Оберіть розділ 👇 |
| 30 | 💼 Такой бот — для вашего магазина<br><br>Этот бот принимает заказы сам: каталог с наличием, корзина, свой вес, расчёт суммы, адрес и телефон. Готовый заказ с маршрутом приходит в ваш Telegram-канал. Работает 24/7.<br><br>📦 ПАКЕТЫ<br>• Start — 350 €<br>каталог, корзина, доставка, заказ в канал, учёт остатков<br>• Business — 800 € ⭐<br>+ база клиентов, рассылки, акции, промокоды, бонусы, ежедневный отчёт<br>• Pro — 1 500 €<br>+ AI-помощник по продажам и остаткам, подключение внешних сервисов<br><br>🛠 ОБСЛУЖИВАНИЕ<br>• Базовое — 25 €/мес (250 €/год)<br>• Полное — 39 €/мес (390 €/год)<br>🎁 Start + 6 мес. обслуживания — 440 € вместо 500 €<br><br>➕ Онлайн-оплата (Apple Pay, Google Pay, карты, PayPal) — 150 €<br><br>Запуск Start за 1–2 дня: ваше название, логотип, цены и города. 50% предоплата, остальное после тестового заказа.<br><br>Попробуйте сами: соберите корзину и оформите пробный заказ.<br>Вопросы и заказ бота: @esusnob 👇 | 💼 So ein Bot für Ihren Shop<br><br>Dieser Bot nimmt Bestellungen selbstständig an: Katalog mit Verfügbarkeit, Warenkorb, eigene Menge, Summenberechnung, Adresse und Telefon. Die fertige Bestellung mit Route kommt in Ihren Telegram-Kanal. Rund um die Uhr (24/7).<br><br>📦 PAKETE<br>• Start — 350 €<br>Katalog, Warenkorb, Lieferung, Bestellung in den Kanal, Bestandsführung<br>• Business — 800 € ⭐<br>+ Kundendatenbank, Rundschreiben, Aktionen, Gutscheincodes, Bonus, täglicher Bericht<br>• Pro — 1 500 €<br>+ KI-Assistent für Verkauf und Bestand, Anbindung externer Dienste<br><br>🛠 WARTUNG<br>• Basis — 25 €/Monat (250 €/Jahr)<br>• Komplett — 39 €/Monat (390 €/Jahr)<br>🎁 Start + 6 Monate Wartung — 440 € statt 500 €<br><br>➕ Online-Zahlung (Apple Pay, Google Pay, Karten, PayPal) — 150 €<br><br>Start ist in 1–2 Tagen einsatzbereit: Ihr Name, Logo, Preise und Städte. 50 % Vorauszahlung, der Rest nach der Testbestellung.<br><br>Probieren Sie es selbst: Legen Sie Artikel in den Warenkorb und geben Sie eine Probebestellung auf.<br>Fragen und Bot-Bestellung: @esusnob 👇 | 💼 Un bot así para su tienda<br><br>Este bot recibe pedidos por sí solo: catálogo con disponibilidad, carrito, cantidad a elegir, cálculo del total, dirección y teléfono. El pedido listo, con la ruta, llega a su canal de Telegram. Funciona 24/7.<br><br>📦 PAQUETES<br>• Start — 350 €<br>catálogo, carrito, entrega, pedido al canal, control de stock<br>• Business — 800 € ⭐<br>+ base de clientes, envíos masivos, promociones, códigos promocionales, bonos, informe diario<br>• Pro — 1 500 €<br>+ asistente de IA para ventas y stock, conexión de servicios externos<br><br>🛠 MANTENIMIENTO<br>• Básico — 25 €/mes (250 €/año)<br>• Completo — 39 €/mes (390 €/año)<br>🎁 Start + 6 meses de mantenimiento — 440 € en lugar de 500 €<br><br>➕ Pago en línea (Apple Pay, Google Pay, tarjetas, PayPal) — 150 €<br><br>Puesta en marcha de Start en 1–2 días: su nombre, logotipo, precios y ciudades. 50 % por adelantado, el resto tras el pedido de prueba.<br><br>Pruébelo usted mismo: llene el carrito y haga un pedido de prueba.<br>Preguntas y pedido del bot: @esusnob 👇 | 💼 Такий бот — для вашого магазину<br><br>Цей бот приймає замовлення сам: каталог із наявністю, кошик, своя вага, розрахунок суми, адреса й телефон. Готове замовлення з маршрутом приходить у ваш Telegram-канал. Працює 24/7.<br><br>📦 ПАКЕТИ<br>• Start — 350 €<br>каталог, кошик, доставка, замовлення в канал, облік залишків<br>• Business — 800 € ⭐<br>+ база клієнтів, розсилки, акції, промокоди, бонуси, щоденний звіт<br>• Pro — 1 500 €<br>+ AI-помічник із продажів і залишків, підключення зовнішніх сервісів<br><br>🛠 ОБСЛУГОВУВАННЯ<br>• Базове — 25 €/міс (250 €/рік)<br>• Повне — 39 €/міс (390 €/рік)<br>🎁 Start + 6 міс. обслуговування — 440 € замість 500 €<br><br>➕ Онлайн-оплата (Apple Pay, Google Pay, картки, PayPal) — 150 €<br><br>Запуск Start за 1–2 дні: ваша назва, логотип, ціни та міста. 50% передоплата, решта після тестового замовлення.<br><br>Спробуйте самі: зберіть кошик і оформіть пробне замовлення.<br>Питання та замовлення бота: @esusnob 👇 |
| 31 | 💬 Написать продавцу | 💬 Verkäufer schreiben | 💬 Escribir al vendedor | 💬 Написати продавцю |
| 32 | 🛒 Попробовать заказ | 🛒 Bestellung ausprobieren | 🛒 Probar un pedido | 🛒 Спробувати замовлення |
| 33 | 📋 ВЕСЬ ПРАЙС RAIV FISH<br>❌ — сейчас нет в наличии<br><br>{…}<br><br>Выберите раздел 👇 | 📋 PREISLISTE RAIV FISH<br>❌ — derzeit nicht vorrätig<br><br>{…}<br><br>Bitte wählen Sie eine Kategorie 👇 | 📋 LISTA DE PRECIOS RAIV FISH<br>❌ — no disponible ahora<br><br>{…}<br><br>Elija una sección 👇 | 📋 ВЕСЬ ПРАЙС RAIV FISH<br>❌ — зараз немає в наявності<br><br>{…}<br><br>Оберіть розділ 👇 |
| 34 | 🎁 Приведи друга — получите оба по 3 €<br><br>Ваша личная ссылка:<br>https://t.me/RAIV_FISH_bot?start=ref_{…}<br><br>Друг получает 3 € бонусами сразу, вы — после его первого заказа. | 🎁 Freunde einladen — Sie beide erhalten je 3 €<br><br>Ihr persönlicher Link:<br>https://t.me/RAIV_FISH_bot?start=ref_{…}<br><br>Ihr Freund erhält 3 € Bonus sofort, Sie — nach seiner ersten Bestellung. | 🎁 Invita a un amigo — ambos reciben 3 €<br><br>Su enlace personal:<br>https://t.me/RAIV_FISH_bot?start=ref_{…}<br><br>Su amigo recibe 3 € en bonos al instante, y usted, tras su primer pedido. | 🎁 Приведи друга — отримайте обидва по 3 €<br><br>Ваше особисте посилання:<br>https://t.me/RAIV_FISH_bot?start=ref_{…}<br><br>Друг отримує 3 € бонусами одразу, ви — після його першого замовлення. |
| 35 | 📤 Отправить другу | 📤 An Freund senden | 📤 Enviar a un amigo | 📤 Надіслати другу |
| 36 | Вяленая рыба и снеки с доставкой — держи 3 € на первый заказ 🐟 | Getrockneter Fisch und Snacks mit Lieferung — hier sind 3 € für deine erste Bestellung 🐟 | Pescado seco y snacks con entrega — aquí tienes 3 € para tu primer pedido 🐟 | В’ялена риба та снеки з доставкою — тримай 3 € на перше замовлення 🐟 |
| 37 | 📋 К покупкам | 📋 Zum Einkaufen | 📋 Ir a la tienda | 📋 До покупок |
| 38 | 📇 Контакты RAIV FISH<br><br>🐟 Рыба и икра — от поставщика из Эстонии: @vasyaivancuk<br>🎬 Видео, фото и новинки — TikTok, Instagram, Facebook и канал @raiv_fish1<br>💬 Вопросы по заказу — @esusnob | 📇 Kontakt RAIV FISH<br><br>🐟 Fisch und Rogen — vom Lieferanten aus Estland: @vasyaivancuk<br>🎬 Videos, Fotos und Neuheiten — TikTok, Instagram, Facebook und Kanal @raiv_fish1<br>💬 Fragen zur Bestellung — @esusnob | 📇 Contactos RAIV FISH<br><br>🐟 Pescado y huevas — del proveedor de Estonia: @vasyaivancuk<br>🎬 Vídeos, fotos y novedades — TikTok, Instagram, Facebook y el canal @raiv_fish1<br>💬 Preguntas sobre el pedido — @esusnob | 📇 Контакти RAIV FISH<br><br>🐟 Риба та ікра — від постачальника з Естонії: @vasyaivancuk<br>🎬 Відео, фото й новинки — TikTok, Instagram, Facebook і канал @raiv_fish1<br>💬 Питання щодо замовлення — @esusnob |
| 39 | 🎵 TikTok — видео | 🎵 TikTok — Videos | 🎵 TikTok — vídeos | 🎵 TikTok — відео |
| 40 | 📸 Instagram — фото | 📸 Instagram — Fotos | 📸 Instagram — fotos | 📸 Instagram — фото |
| 41 | 👍 Facebook | 👍 Facebook | 👍 Facebook | 👍 Facebook |
| 42 | 📣 Telegram-канал @raiv_fish1 | 📣 Telegram-Kanal @raiv_fish1 | 📣 Canal de Telegram @raiv_fish1 | 📣 Telegram-канал @raiv_fish1 |
| 43 | 🐟 Поставщик — Василий | 🐟 Lieferant — Wassili | 🐟 Proveedor — Vasili | 🐟 Постачальник — Василь |
| 44 | ✅ Язык: Русский<br><br> | ✅ Sprache: Deutsch<br><br> | ✅ Idioma: español<br><br> | ✅ Мова: українська<br><br> |
| 45 | ℹ️ Как заказать<br>1. /start → раздел → товар → вес (или «✏️ Свой вес»)<br>2. «🧺 Корзина / оформить» → город → время → адрес → телефон<br>3. Оплатите онлайн по кнопке или наличными курьеру<br><br>С каждого заказа — 5% бонусами.<br><br>/orders — мои заказы и бонусы<br>/invite — приведи друга<br>/contacts — контакты, канал и медиа<br>/language — сменить язык<br>/stop — не получать рассылки<br>Вопросы: @esusnob | ℹ️ So bestellen Sie<br>1. /start → Kategorie → Artikel → Menge (oder „✏️ Eigene Menge“)<br>2. „🧺 Warenkorb / bestellen“ → Stadt → Zeit → Adresse → Telefon<br>3. Bezahlen Sie online per Schaltfläche oder bar beim Kurier<br><br>Auf jede Bestellung — 5 % Bonus.<br><br>/orders — meine Bestellungen und Bonus<br>/invite — Freunde einladen<br>/contacts — Kontakt, Kanal und Medien<br>/language — Sprache ändern<br>/stop — keine Rundschreiben mehr erhalten<br>Fragen: @esusnob | ℹ️ Cómo hacer un pedido<br>1. /start → sección → producto → cantidad (o «✏️ Otra cantidad»)<br>2. «🧺 Carrito / pedir» → ciudad → hora → dirección → teléfono<br>3. Pague en línea con el botón o en efectivo al repartidor<br><br>Por cada pedido, un 5 % en bonos.<br><br>/orders — mis pedidos y bonos<br>/invite — invitar a un amigo<br>/contacts — contactos, canal y redes<br>/language — cambiar el idioma<br>/stop — no recibir envíos masivos<br>Preguntas: @esusnob | ℹ️ Як замовити<br>1. /start → розділ → товар → вага (або «✏️ Своя вага»)<br>2. «🧺 Кошик / оформити» → місто → час → адреса → телефон<br>3. Оплатіть онлайн кнопкою або готівкою кур’єру<br><br>З кожного замовлення — 5% бонусами.<br><br>/orders — мої замовлення та бонуси<br>/invite — приведи друга<br>/contacts — контакти, канал і медіа<br>/language — змінити мову<br>/stop — не отримувати розсилки<br>Питання: @esusnob |
| 46 | 🔁 Корзина как в прошлый раз:<br>{…}💶 Итого: {…} €<br><br>Можно добавить ещё товары или сразу оформить. | 🔁 Warenkorb wie beim letzten Mal:<br>{…}💶 Summe: {…} €<br><br>Sie können weitere Artikel hinzufügen oder gleich bestellen. | 🔁 Carrito como la última vez:<br>{…}💶 Total: {…} €<br><br>Puede añadir más productos o hacer el pedido ya. | 🔁 Кошик як минулого разу:<br>{…}💶 Разом: {…} €<br><br>Можна додати ще товари або одразу оформити. |
| 47 | Прошлых заказов пока нет. Выберите товары 👇 | Noch keine früheren Bestellungen. Bitte wählen Sie Artikel 👇 | Aún no hay pedidos anteriores. Elija productos 👇 | Минулих замовлень поки немає. Оберіть товари 👇 |
| 48 | 📜 Ваши заказы<br><br>{…}<br><br>💎 Бонусы: {…} €<br>За каждый заказ начисляем 5% бонусами. При оформлении они списываются автоматически — до 20% суммы заказа. | 📜 Ihre Bestellungen<br><br>{…}<br><br>💎 Bonus: {…} €<br>Für jede Bestellung schreiben wir Ihnen 5 % Bonus gut. Bei der Bestellung wird er automatisch verrechnet — bis zu 20 % des Bestellwerts. | 📜 Sus pedidos<br><br>{…}<br><br>💎 Bonos: {…} €<br>Por cada pedido abonamos un 5 % en bonos. Al hacer el pedido se descuentan automáticamente, hasta el 20 % del importe. | 📜 Ваші замовлення<br><br>{…}<br><br>💎 Бонуси: {…} €<br>За кожне замовлення нараховуємо 5% бонусами. Під час оформлення вони списуються автоматично — до 20% суми замовлення. |
| 49 | Пока заказов нет. | Noch keine Bestellungen. | Aún no hay pedidos. | Поки що замовлень немає. |
| 50 | 🔁 Повторить прошлый заказ | 🔁 Letzte Bestellung wiederholen | 🔁 Repetir el último pedido | 🔁 Повторити минуле замовлення |
| 51 | 🎟 Промокод<br><br>Ответьте на это сообщение: напишите промокод. | 🎟 Gutscheincode<br><br>Antworten Sie auf diese Nachricht: Geben Sie den Gutscheincode ein. | 🎟 Código promocional<br><br>Responda a este mensaje: escriba el código promocional. | 🎟 Промокод<br><br>Дайте відповідь на це повідомлення: напишіть промокод. |
| 52 | Например FISH10 | z. B. FISH10 | Por ejemplo FISH10 | Наприклад FISH10 |
| 53 | ✅ Промокод {…} принят: скидка {…}% на этот заказ.<br>Скидка появится при оформлении. | ✅ Gutscheincode {…} angenommen: {…} % Rabatt auf diese Bestellung.<br>Der Rabatt wird bei der Bestellung angezeigt. | ✅ Código {…} aceptado: {…} % de descuento en este pedido.<br>El descuento aparecerá al hacer el pedido. | ✅ Промокод {…} прийнято: знижка {…}% на це замовлення.<br>Знижка з’явиться під час оформлення. |
| 54 | 📋 Выбрать товары | 📋 Artikel auswählen | 📋 Elegir productos | 📋 Обрати товари |
| 55 | 🧾 Оформить заказ | 🧾 Bestellung aufgeben | 🧾 Hacer el pedido | 🧾 Оформити замовлення |
| 56 | ❌ Промокод «{…}» не найден или уже не действует. | ❌ Gutscheincode „{…}“ nicht gefunden oder nicht mehr gültig. | ❌ El código «{…}» no existe o ya no es válido. | ❌ Промокод «{…}» не знайдено або він уже не діє. |
| 57 | 🎟 Ввести другой | 🎟 Anderen Code eingeben | 🎟 Introducir otro | 🎟 Ввести інший |
| 58 | Каталог | Katalog | Catálogo | Каталог |
| 59 | Выберите товар 👇 | Bitte wählen Sie einen Artikel 👇 | Elija un producto 👇 | Оберіть товар 👇 |
| 60 | 🧺 Корзина / оформить | 🧺 Warenkorb / bestellen | 🧺 Carrito / pedir | 🧺 Кошик / оформити |
| 61 | ⬅️ Все разделы | ⬅️ Alle Kategorien | ⬅️ Todas las secciones | ⬅️ Усі розділи |
| 62 | ✏️ Свой вес | ✏️ Eigene Menge | ✏️ Otra cantidad | ✏️ Своя вага |
| 63 | ⬅️ Назад | ⬅️ Zurück | ⬅️ Atrás | ⬅️ Назад |
| 64 | Сколько добавить в корзину? | Wie viel möchten Sie in den Warenkorb legen? | ¿Cuánto desea añadir al carrito? | Скільки додати в кошик? |
| 65 | Ответьте на это сообщение: сколько взять {…}. | Antworten Sie auf diese Nachricht: gewünschte Menge {…}. | Responda a este mensaje: cuánto desea, {…}. | Дайте відповідь на це повідомлення: скільки взяти {…}. |
| 66 | код: | Code: | código: | код: |
| 67 | Например 0,7 | z. B. 0,7 | Por ejemplo 0,7 | Наприклад 0,7 |
| 68 | Этот товар | Dieser Artikel | Este producto | Цей товар |
| 69 |  — сейчас нет в наличии.<br>Выберите другой товар 👇 |  — derzeit nicht vorrätig.<br>Bitte wählen Sie einen anderen Artikel 👇 |  — no disponible ahora.<br>Elija otro producto 👇 |  — зараз немає в наявності.<br>Оберіть інший товар 👇 |
| 70 | ➕ Добавить ещё | ➕ Weitere Artikel | ➕ Añadir más | ➕ Додати ще |
| 71 | 🗑 Очистить корзину | 🗑 Warenkorb leeren | 🗑 Vaciar el carrito | 🗑 Очистити кошик |
| 72 | ✅ Добавлено: {…} — {…} — {…} €<br><br>🧺 Ваша корзина:<br>{…}• {…} — {…} — {…} €<br>💶 Итого: {…} € | ✅ Hinzugefügt: {…} — {…} — {…} €<br><br>🧺 Ihr Warenkorb:<br>{…}• {…} — {…} — {…} €<br>💶 Summe: {…} € | ✅ Añadido: {…} — {…} — {…} €<br><br>🧺 Su carrito:<br>{…}• {…} — {…} — {…} €<br>💶 Total: {…} € | ✅ Додано: {…} — {…} — {…} €<br><br>🧺 Ваш кошик:<br>{…}• {…} — {…} — {…} €<br>💶 Разом: {…} € |
| 73 | 🤔 Не понял количество. Нажмите «✏️ Свой вес» ещё раз и напишите число, например 0,7 или 250. | 🤔 Menge nicht erkannt. Tippen Sie erneut auf „✏️ Eigene Menge“ und schreiben Sie eine Zahl, z. B. 0,7 oder 250. | 🤔 No he entendido la cantidad. Pulse «✏️ Otra cantidad» de nuevo y escriba un número, por ejemplo 0,7 o 250. | 🤔 Не зрозумів кількість. Натисніть «✏️ Своя вага» ще раз і напишіть число, наприклад 0,7 або 250. |
| 74 | Эдделак | Eddelak | Eddelak | Еддельак |
| 75 | Марне | Marne | Marne | Марне |
| 76 | Брунсбюттель | Brunsbüttel | Brunsbüttel | Брунсбюттель |
| 77 | Хайде | Heide | Heide | Гайде |
| 78 | Другое место | Anderer Ort | Otro lugar | Інше місце |
| 79 | 🧺 Ваша корзина:<br>{…}💶 Итого: {…} €<br><br>📍 Куда доставить? Доставка бесплатно. | 🧺 Ihr Warenkorb:<br>{…}💶 Summe: {…} €<br><br>📍 Wohin sollen wir liefern? Die Lieferung ist kostenlos. | 🧺 Su carrito:<br>{…}💶 Total: {…} €<br><br>📍 ¿Adónde lo entregamos? La entrega es gratuita. | 🧺 Ваш кошик:<br>{…}💶 Разом: {…} €<br><br>📍 Куди доставити? Доставка безкоштовна. |
| 80 | 🧺 Ваша корзина:<br>{…}💶 Итого: {…} €<br><br>Минимальный заказ — 20 €. Добавьте ещё на {…} € 👇 | 🧺 Ihr Warenkorb:<br>{…}💶 Summe: {…} €<br><br>Mindestbestellwert — 20 €. Bitte fügen Sie noch Artikel für {…} € hinzu 👇 | 🧺 Su carrito:<br>{…}💶 Total: {…} €<br><br>Pedido mínimo: 20 €. Añada productos por {…} € más 👇 | 🧺 Ваш кошик:<br>{…}💶 Разом: {…} €<br><br>Мінімальне замовлення — 20 €. Додайте ще на {…} € 👇 |
| 81 | 🧺 Корзина пуста. | 🧺 Der Warenkorb ist leer. | 🧺 El carrito está vacío. | 🧺 Кошик порожній. |
| 82 | Сегодня 12–16 | Heute 12–16 | Hoy 12–16 | Сьогодні 12–16 |
| 83 | Сегодня 17–21 | Heute 17–21 | Hoy 17–21 | Сьогодні 17–21 |
| 84 | Завтра 12–16 | Morgen 12–16 | Mañana 12–16 | Завтра 12–16 |
| 85 | Завтра 17–21 | Morgen 17–21 | Mañana 17–21 | Завтра 17–21 |
| 86 | ⬅️ Другой город | ⬅️ Andere Stadt | ⬅️ Otra ciudad | ⬅️ Інше місто |
| 87 | 🕐 Когда удобно получить заказ? | 🕐 Wann möchten Sie die Bestellung erhalten? | 🕐 ¿Cuándo le viene bien recibir el pedido? | 🕐 Коли зручно отримати замовлення? |
| 88 | 🎟 Промокод {…} (−{…}%): −{…} €<br> | 🎟 Gutscheincode {…} (−{…}%): −{…} €<br> | 🎟 Código promocional {…} (−{…}%): −{…} €<br> | 🎟 Промокод {…} (−{…}%): −{…} €<br> |
| 89 | 💎 Бонусами: −{…} €<br> | 💎 Mit Bonus: −{…} €<br> | 💎 Con bonos: −{…} €<br> | 💎 Бонусами: −{…} €<br> |
| 90 | 🧾 Ваш заказ<br>{…}📍 {…}<br>🕐 {…}<br>💳 Оплата: онлайн или наличными при получении<br>🧺 Товары: {…} €<br>{…}{…}💶 К оплате: {…} €<br><br>✍️ Ответьте на это сообщение: напишите адрес доставки — улица, дом, город | 🧾 Ihre Bestellung<br>{…}📍 {…}<br>🕐 {…}<br>💳 Zahlung: online oder bar bei Erhalt<br>🧺 Artikel: {…} €<br>{…}{…}💶 Zu zahlen: {…} €<br><br>✍️ Antworten Sie auf diese Nachricht: Lieferadresse — Straße, Hausnummer, Stadt | 🧾 Su pedido<br>{…}📍 {…}<br>🕐 {…}<br>💳 Pago: en línea o en efectivo al recibirlo<br>🧺 Productos: {…} €<br>{…}{…}💶 A pagar: {…} €<br><br>✍️ Responda a este mensaje: escriba la dirección de entrega — calle, número, ciudad | 🧾 Ваше замовлення<br>{…}📍 {…}<br>🕐 {…}<br>💳 Оплата: онлайн або готівкою під час отримання<br>🧺 Товари: {…} €<br>{…}{…}💶 До сплати: {…} €<br><br>✍️ Дайте відповідь на це повідомлення: напишіть адресу доставки — вулиця, будинок, місто |
| 91 | Улица, дом, город | Straße, Hausnr., Stadt | Calle, número, ciudad | Вулиця, будинок, місто |
| 92 | 🧺 Корзина пуста. Нажмите /start, чтобы выбрать товары. | 🧺 Der Warenkorb ist leer. Tippen Sie auf /start, um Artikel auszuwählen. | 🧺 El carrito está vacío. Pulse /start para elegir productos. | 🧺 Кошик порожній. Натисніть /start, щоб обрати товари. |
| 93 | 🗑 Корзина очищена. | 🗑 Warenkorb geleert. | 🗑 Carrito vaciado. | 🗑 Кошик очищено. |
| 94 | {…}<br>🏠 Адрес доставки: {…}<br><br>📞 Ответьте на это сообщение: напишите ваш номер телефона | {…}<br>🏠 Lieferadresse: {…}<br><br>📞 Antworten Sie auf diese Nachricht: Ihre Telefonnummer | {…}<br>🏠 Dirección de entrega: {…}<br><br>📞 Responda a este mensaje: escriba su número de teléfono | {…}<br>🏠 Адреса доставки: {…}<br><br>📞 Дайте відповідь на це повідомлення: напишіть ваш номер телефону |
| 95 | Номер телефона | Telefonnummer | Número de teléfono | Номер телефону |
| 96 | поз. | Pos. | art. | поз. |
| 97 | ✅ Спасибо! Заказ №{…} принят.<br>Мы свяжемся с вами, чтобы договориться о времени доставки.<br><br>💎 После доставки начислим {…} € бонусами.<br>Ваш баланс: {…} €<br><br>Новый заказ: /start | ✅ Vielen Dank! Bestellung Nr. {…} ist eingegangen.<br>Wir melden uns bei Ihnen, um die Lieferzeit abzustimmen.<br><br>💎 Nach der Lieferung schreiben wir Ihnen {…} € Bonus gut.<br>Ihr Guthaben: {…} €<br><br>Neue Bestellung: /start | ✅ ¡Gracias! Pedido n.º {…} recibido.<br>Nos pondremos en contacto con usted para acordar la hora de entrega.<br><br>💎 Tras la entrega le abonaremos {…} € en bonos.<br>Su saldo: {…} €<br><br>Nuevo pedido: /start | ✅ Дякуємо! Замовлення №{…} прийнято.<br>Ми зв’яжемося з вами, щоб домовитися про час доставки.<br><br>💎 Після доставки нарахуємо {…} € бонусами.<br>Ваш баланс: {…} €<br><br>Нове замовлення: /start |
| 98 | 🚚 Ваш заказ №{…} уже в пути! Скоро будем. | 🚚 Ihre Bestellung Nr. {…} ist unterwegs! Wir sind bald da. | 🚚 ¡Su pedido n.º {…} ya está en camino! Llegamos pronto. | 🚚 Ваше замовлення №{…} уже в дорозі! Скоро будемо. |
| 99 | ✅ Заказ №{…} доставлен. Приятного аппетита! 🐟<br><br>Оцените, пожалуйста, заказ: | ✅ Bestellung Nr. {…} wurde geliefert. Guten Appetit! 🐟<br><br>Bitte bewerten Sie die Bestellung: | ✅ Pedido n.º {…} entregado. ¡Buen provecho! 🐟<br><br>Por favor, valore el pedido: | ✅ Замовлення №{…} доставлено. Смачного! 🐟<br><br>Оцініть, будь ласка, замовлення: |
| 100 | 💎 Начислено {…} € бонусами за заказ №{…}. Баланс: {…} € | 💎 Ihnen wurden {…} € Bonus für Bestellung Nr. {…}. Guthaben: {…} € | 💎 Se le han abonado {…} € en bonos por el pedido n.º {…}. Saldo: {…} € | 💎 Нараховано {…} € бонусами за замовлення №{…}. Баланс: {…} € |
| 101 | 🎁 Ваш друг получил первый заказ — вам +3 € бонусами! Спасибо, что советуете RAIV FISH. | 🎁 Ihr Freund hat seine erste Bestellung erhalten — Sie bekommen +3 € Bonus! Danke, dass Sie RAIV FISH weiterempfehlen. | 🎁 Su amigo ha recibido su primer pedido: ¡+3 € en bonos para usted! Gracias por recomendar RAIV FISH. | 🎁 Ваш друг отримав перше замовлення — вам +3 € бонусами! Дякуємо, що радите RAIV FISH. |
| 102 | Спасибо за оценку {…}!<br>Будем рады видеть вас снова 🐟 | Danke für Ihre Bewertung {…}!<br>Wir freuen uns, Sie wiederzusehen 🐟 | ¡Gracias por su valoración {…}!<br>Será un placer volver a atenderle 🐟 | Дякуємо за оцінку {…}!<br>Будемо раді бачити вас знову 🐟 |
| 103 | 🛒 Новый заказ | 🛒 Neue Bestellung | 🛒 Nuevo pedido | 🛒 Нове замовлення |
| 104 | /start — каталог · /stop — отписаться от рассылок | /start — Katalog · /stop — Rundschreiben abbestellen | /start — catálogo · /stop — darse de baja de los envíos | /start — каталог · /stop — відписатися від розсилок |
| 105 | 🛒 К покупкам | 🛒 Zum Einkaufen | 🛒 Ir a la tienda | 🛒 До покупок |
| 106 | Вы отписались от рассылок. Заказы и бонусы сохранены.<br>/start — открыть каталог | Sie haben die Rundschreiben abbestellt. Bestellungen und Bonus bleiben erhalten.<br>/start — Katalog öffnen | Se ha dado de baja de los envíos. Sus pedidos y bonos se conservan.<br>/start — abrir el catálogo | Ви відписалися від розсилок. Замовлення та бонуси збережено.<br>/start — відкрити каталог |
| 107 | 💳 Можно оплатить заказ онлайн — {…} €<br>Apple Pay, Google Pay или карта, безопасно через Stripe.<br>Или наличными при получении — как удобно. | 💳 Sie können die Bestellung online bezahlen — {…} €<br>Apple Pay, Google Pay oder Karte, sicher über Stripe.<br>Oder bar bei Erhalt — wie es Ihnen passt. | 💳 Puede pagar el pedido en línea — {…} €<br>Apple Pay, Google Pay o tarjeta, de forma segura con Stripe.<br>O en efectivo al recibirlo, como prefiera. | 💳 Можна оплатити замовлення онлайн — {…} €<br>Apple Pay, Google Pay або картка, безпечно через Stripe.<br>Або готівкою під час отримання — як зручно. |
| 108 | 💳 Оплатить онлайн | 💳 Online bezahlen | 💳 Pagar en línea | 💳 Оплатити онлайн |
| 109 | 🛍 Корзина из витрины:<br>{…}💶 Итого: {…} €<br><br> | 🛍 Warenkorb aus dem Schaufenster:<br>{…}💶 Summe: {…} €<br><br> | 🛍 Carrito del escaparate:<br>{…}💶 Total: {…} €<br><br> | 🛍 Кошик із вітрини:<br>{…}💶 Разом: {…} €<br><br> |
| 110 | 🚗 Доставка бесплатно. Оформим? | 🚗 Die Lieferung ist kostenlos. Bestellung aufgeben? | 🚗 La entrega es gratuita. ¿Hacemos el pedido? | 🚗 Доставка безкоштовна. Оформлюємо? |
| 111 | Минимальный заказ 20 € — добавьте ещё товаров. | Mindestbestellwert 20 € — bitte fügen Sie weitere Artikel hinzu. | Pedido mínimo: 20 €. Añada más productos. | Мінімальне замовлення 20 € — додайте ще товарів. |
| 112 | ✅ Этот заказ уже оформлен и передан продавцу.<br>Новый заказ: /start | ✅ Diese Bestellung wurde bereits aufgegeben und an den Verkäufer übermittelt.<br>Neue Bestellung: /start | ✅ Este pedido ya está hecho y se ha enviado al vendedor.<br>Nuevo pedido: /start | ✅ Це замовлення вже оформлено й передано продавцю.<br>Нове замовлення: /start |
