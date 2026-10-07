# Tender-Radar — продукт для ремесленных фирм (КП-черновик)

Задача: T-20261007-0031 · Исполнитель: 💼 Sales · Дата: 07.10.2026 · Основание: `bau-hunter/docs/AUDIT.md`, `bau-hunter/docs/PLAN.md`,
стиль цен — `raiv-fish-bot/OFFER.md`, `raiv-fish-bot/PRICES.md`.

**Статус: ЧЕРНОВИК. Ничего не опубликовано и не отправлено. Цены — предложение, цены утверждает владелец.**
Метки: **[ПРОВЕРЕНО]** — есть в AUDIT/PLAN с проверкой; **[ПРЕДПОЛОЖЕНИЕ]** — оценка, рынок или право без проверки.
В Make ничего не делалось.

---

# ЧАСТЬ 1. ДЛЯ ВЛАДЕЛЬЦА (RU)

## 0. Коротко
- Идея: тот же конвейер Bau-Lead-Hunter (поиск тендеров → SCORE → расчёт/риски → черновик КП), но **для чужих фирм**:
  каждое утро в Telegram — тендеры по их Gewerk и региону. Ежемесячная подписка.
- **Честное условие продаж:** системы ещё нет — PLAN.md на согласовании, этап 1 (TED + карточки) не запущен [ПРОВЕРЕНО].
  Продавать можно только после того, как этапы 1–2 отработают у нас ≥ 7 дней по критериям PLAN §9. До этого — максимум
  «пилот бесплатно / за символическую цену» 2–3 знакомым фирмам.
- **Главный риск ценности:** TED показывает только тендеры **выше порога ЕС** (работы ≈ 5,4–5,5 млн € на весь объект) [ПРОВЕРЕНО: AUDIT §3].
  Для малой фирмы интересны лоты своего Gewerk внутри таких объектов, но часть малых лотов может публиковаться только национально
  [ПРЕДПОЛОЖЕНИЕ: «Losregel» 20 % / лоты < 1 млн € — юридически не проверено]. Поток только из TED для одного Gewerk в одном
  регионе может быть **тонким** (единицы в неделю) [ПРЕДПОЛОЖЕНИЕ]. Полноценный продукт — после этапа 5 (oeffentlichevergabe.de, ниже порога).
- **Make:** текущий тариф Core 10 000 кредитов уже на 55 % израсходован за 7 дней [ПРОВЕРЕНО]. Клиентов на этом тарифе не обслужить —
  нужна отдельная организация/тариф Make под Tender-Radar (решение владельца, §12 PLAN, вопрос 1).

## 1. Проблема малой фирмы
- Владелец фирмы (3–15 человек) сам на объекте, вечером — сметы и счета. Времени просматривать порталы каждый день нет [ПРЕДПОЛОЖЕНИЕ, типичный профиль].
- Объявления разбросаны: TED (выше порога), oeffentlichevergabe.de, service.bund.de, порталы земель (SH, HH, HB, NI, MV), DTVP,
  evergabe-online [ПРОВЕРЕНО: список источников в AUDIT §3]. Ниже порога ЕС — самая «малая» часть рынка — разбросана сильнее всего.
- Поиск по CPV-кодам неудобен: Trockenbau, Maler, Fliesen и т. п. прячутся в лотах больших объектов («Neubau Grundschule – Los 7 Trockenbauarbeiten»).
- Срок подачи часто 3–5 недель [ПРЕДПОЛОЖЕНИЕ]; нашёл поздно — не успел посчитать.
- Платные сервисы-агрегаторы тендеров существуют (напр. DTAD, Vergabe24, Auftragsbörsen) — уровень цен и функции мы не проверяли
  [ПРЕДПОЛОЖЕНИЕ: ориентир «десятки–сотни €/мес»; перед продажей сделать сравнение на 1 страницу].

## 2. Ценность: что фирма получает каждое утро
В 07:00–08:00 сообщение в Telegram (бот Tender-Radar, только их чат):
- «Сегодня 3 новых тендера по Trockenbau в Ihrem Gebiet»;
- по каждому: заказчик (Vergabestelle), место (PLZ/NUTS), Gewerk/лот, срок подачи (дней осталось), процедура, оценочная стоимость (если опубликована),
  кнопка «Открыть объявление» (ссылка на TED/платформу);
- Plus: оценка 0–100 и HOT/WARM/COLD + 2–3 причины («Gewerk passt, Frist 12 Tage, PQ-VOB gefordert»);
- Pro: по кнопке — расчёт по **их** ставкам, список рисков, черновик Anschreiben/Bieterfrage на немецком.
Почему Telegram: бот уже умеем, бесплатен, не нужна почтовая рассылка (UWG/DSGVO проще), кнопки [ПРОВЕРЕНО: архитектура PLAN §2].
Альтернатива для немецких клиентов — e-mail-дайджест по их явному согласию (позже) [ПРЕДПОЛОЖЕНИЕ: часть Handwerker Telegram не используют, скорее WhatsApp].

## 3. Пакеты (предложение — цены утверждает владелец)

| Пакет | Что входит | Цена/мес (предложение) | За год (2 мес. в подарок) |
|---|---|---|---|
| **Basic** | Ежедневный дайджест: 1 регион (до 5 NUTS-кодов или PLZ + радиус), 1–2 Gewerke по CPV, ссылки на объявления, без AI | **39 €** | 390 € |
| **Plus** ⭐ | Всё из Basic + **SCORE** (AI-оценка Haiku: HOT/WARM/COLD, причины) + тонкий фильтр по Gewerk по тексту лота, до 3 Gewerke, настройки «мин. срок / мин. сумма», команда /settings | **79 €** | 790 € |
| **Pro** | Всё из Plus + по кнопке: **расчёт по ставкам фирмы** (объёмы с источником, себестоимость, цена, прибыль — арифметика без AI), **риски** (чек-лист PLAN §6), **черновик** Anschreiben / Bieterfrage DE; лимит: 8 расчётов + 5 черновиков в месяц, сверх — 12 €/шт | **149 €** | 1 490 € |

**Настройка (разово, опционально):**
| | Цена (предложение) | Что |
|---|---|---|
| Basic | 0 € (при годовой оплате) / 49 € | бот, регион, CPV, тест 1 день |
| Plus | 99 € | + калибровка SCORE на 10 реальных тендерах вместе с клиентом |
| Pro | 249 € | + ввод ставок фирмы (Stundensatz, €/м², наценки), данные фирмы для черновиков, 1 тестовый расчёт вместе |

**Пилот:** первые 3 фирмы — 1 месяц бесплатно, далее −50 % на 3 месяца в обмен на отзыв и разрешение на кейс (с их письменного согласия).
**Нижняя граница (предложение):** Basic 29 €, Plus 59 €, Pro 119 €.
Условия: помесячно, отмена до конца месяца; оплата вперёд. Kleinunternehmer §19 UStG — без НДС (уточнить у Steuerberater) [ПРЕДПОЛОЖЕНИЕ].

### 3.1 Себестоимость на одного клиента (честная оценка) [ПРЕДПОЛОЖЕНИЕ — проверяется на этапах 1–2]
База — PLAN §10: BH-01 ~300 кредитов/мес, пульт ~450, Haiku-анализ ~18 кредитов, Sonnet-расчёт ~90, Sonnet-КП ~70 (через модуль Make «Anthropic Claude»);
BYOK (свой ключ Anthropic, HTTP-модуль) ≈ 1 кредит за вызов + токены по прайсу Anthropic [ПРОВЕРЕНО: цифры из PLAN, сами цифры PLAN — оценка].

Допущения:
- A1. Поиск TED делается **один раз на регион** для всех клиентов, затем раздача по фильтрам клиентов → ~300 кредитов/мес делятся между клиентами региона.
- A2. На клиента: 30 дайджестов × ~3 кредита + ~50 нажатий × 3 = ~240 кредитов/мес.
- A3. Plus: ~40 AI-оценок/мес (не все тендеры, только прошедшие pre-score).
- A4. Pro: 8 расчётов + 5 черновиков (лимит пакета).
- A5. Цена кредита Make ≈ 1 € за 1 000 кредитов (тариф Core ≈ 10 €/10 000) — **сверить с актуальным прайсом Make** [ПРЕДПОЛОЖЕНИЕ].
- A6. Claude BYOK: Haiku ~0,005 $/оценка, Sonnet ~0,05 $/вызов (длинный текст объявления/LV дороже) [ПРЕДПОЛОЖЕНИЕ, по ценам из настроек LH].

| На клиента/мес | Basic | Plus | Pro |
|---|---|---|---|
| Доля поиска (A1, при 5 клиентах в регионе) | ~60 | ~60 | ~60 |
| Дайджест + пульт (A2) | ~240 | ~240 | ~240 |
| SCORE Haiku через модуль Make (40 × 18) | — | ~720 | ~720 |
| Расчёт+риски Sonnet (8 × 90) | — | — | ~720 |
| Черновики Sonnet (5 × 70) | — | — | ~350 |
| **Итого кредиты (модуль Make)** | **~300** | **~1 020** | **~2 090** |
| ≈ € по A5 | ~0,3 € | ~1 € | ~2,1 € |
| **Вариант BYOK**: кредиты / Claude | ~300 / 0 | ~340 / ~0,2 $ | ~355 / ~0,9 $ |
| Доля тарифа/платформы и бота (Make-организация под продукт, ~16 €/мес на 5–10 клиентов, как в PRICES.md) | ~2–3 € | ~2–3 € | ~2–3 € |
| **Прямые расходы, ≈** | **~3 €** | **~4 €** | **~5 €** |
| Время владельца/поддержки (главная статья!) | ~0,5 ч | ~1 ч | ~2–3 ч |
| **Остаётся (до налогов, без учёта времени)** | **~36 €** | **~75 €** | **~144 €** |

Вывод: AI и Make — копейки на клиента; реальная себестоимость — **время** (настройка, ответы, проверка качества) и **риск ошибки поиска**.
Важно: при 10+ клиентах в одной Make-организации суммарно 3 000–20 000 кредитов/мес → нужен тариф выше Core [ПРЕДПОЛОЖЕНИЕ].
Технически под мультиклиентность нужна доработка PLAN: таблица клиентов (chat_id, NUTS, CPV, пакет, лимиты), раздача по фильтрам,
изоляция ставок/данных каждой фирмы, AV-Vertrag (DSGVO Art. 28) для ставок и данных фирм [ПРЕДПОЛОЖЕНИЕ, не юрконсультация]. Отдельная задача теханализу.

## 4. Честные пределы (говорим клиенту прямо)
1. **Сначала только TED (выше порога ЕС).** oeffentlichevergabe.de (ниже порога, вся Германия) — позже, этап 5 PLAN. Порталы земель
   и платные площадки (MyHammer, Check24) не автоматизируются — только ссылки/вручную [ПРОВЕРЕНО: AUDIT §3].
2. **Не все тендеры.** Нет гарантии полноты: ошибки CPV у заказчика, позднее появление в TED, объявления только на земельных порталах.
3. **Нет гарантии победы** и количества заказов. Мы находим и оцениваем, не выигрываем.
4. **Подаёт фирма сама** через e-Vergabe-платформу (регистрация, формуляры, LV с ценами, подпись). Бот ничего не подаёт и никому не пишет.
5. **Расчёт Pro — ориентир, не Kalkulation:** только по ставкам фирмы; без LV — «не надёжно / не оценить»; с LV ±15–25 % [ПРЕДПОЛОЖЕНИЕ: PLAN §5].
   Нет ставки → «UNKNOWN», а не выдуманное число.
6. **AI ошибается:** SCORE — подсказка, решение за фирмой.
7. **Не юридическая консультация** по Vergaberecht, Tariftreue, PQ-VOB.

## 5. Демо-сценарий (3 минуты)
Подготовка: тестовый бот, заранее заведённый профиль «Trockenbau, PLZ 2xxxx, радиус 80 км»; **реальные** тендеры из TED за вчера
(не выдумывать; если за день ничего — показать архив за неделю и честно сказать про поток).

| Время | Что показываем | Что говорим (DE, суть) |
|---|---|---|
| 0:00–0:30 | Вопрос клиенту | «Wie finden Sie heute Ausschreibungen? Wie viel Zeit kostet das pro Woche?» — слушаем, не перебиваем |
| 0:30–1:15 | Утреннее сообщение в Telegram: 3 тендера, срок, место, кнопка «Bekanntmachung öffnen» → открываем реальную страницу TED | «Jeden Morgen um 7 Uhr — nur Ihr Gewerk, nur Ihre Region. Ein Klick zur Original-Bekanntmachung.» |
| 1:15–1:55 | Plus: карточка с SCORE 78/WARM и причинами; показываем, как отклонённый тендер не мешает | «Die KI sortiert vor: passt das Gewerk, reicht die Frist, werden Nachweise wie PQ-VOB verlangt?» |
| 1:55–2:35 | Pro: кнопка «Kalkulation» → позиции с источником количества и **вашими** ставками, флаги рисков; кнопка «Entwurf» → Anschreiben DE | «Gerechnet wird mit Ihren Sätzen. Fehlt ein Satz, steht da UNKNOWN — keine erfundenen Zahlen.» |
| 2:35–3:00 | Честные пределы + следующий шаг | «Aktuell EU-weite Ausschreibungen, unterschwellige folgen. Abgeben tun Sie selbst über die Vergabeplattform. Wollen wir 30 Tage kostenlos testen?» |

## 6. Сегменты и каналы (10)

**Правовая рамка [ПРЕДПОЛОЖЕНИЕ, не юрконсультация]:** UWG §7 Abs. 2 (Nr. 2 — e-mail/автоматические средства, Nr. 1 — телефон; нумерацию сверить с актуальной редакцией): реклама **по e-mail** (и SMS/мессенджер-рассылки)
без **предварительного явного согласия** — недопустимо, **и для B2B тоже**. Звонок предпринимателю допустим только при «mutmaßliche
Einwilligung» (предполагаемый конкретный интерес) — суды толкуют узко, поэтому холодные звонки по списку тоже не делаем.
Публичные справочники Handwerkskammer (Handwerksrolle/Betriebsbörse) — **только для понимания рынка и подготовки к встречам**,
не для рассылок. Сообщение в LinkedIn/XING — индивидуальное, с персональным поводом, не массовое (правовая оценка мессенджеров соцсетей
неоднозначна → консервативно: только после контакта/реакции). Никаких покупных баз.

| # | Сегмент / канал | Как (законно) | Оценка |
|---|---|---|---|
| 1 | **Собственная сеть владельца**: знакомые Handwerker, субподрядчики, коллеги по Innenausbau | личный разговор, демо на телефоне, пилот | ⭐ лучший старт: тёплый контакт, быстрая обратная связь |
| 2 | **Русско-/украиноязычные ремесленники в Германии** (Telegram-/FB-сообщества, сарафан) | полезные посты в группах по правилам группы, ответ на входящие; RU-интерфейс как преимущество | ⭐ ниша, где у владельца язык и доверие [ПРЕДПОЛОЖЕНИЕ: размер сегмента не проверен] |
| 3 | **Innungen** (Maler- und Lackierer, Elektro, SHK, Dachdecker, Fliesenleger) и **Kreishandwerkerschaften** | письмо/звонок в **Geschäftsstelle** как партнёрское предложение (не реклама членам): доклад 10 мин на Innungsversammlung «Öffentliche Aufträge für kleine Betriebe», скидка членам | ⭐ один разговор = доступ к десяткам фирм; рекомендация Innung = доверие |
| 4 | **Handwerkskammer** (Hamburg, Lübeck, Flensburg, Oldenburg, Bremen, Schwerin …): Betriebsberatung, Auftragsberatungsstelle, Unternehmerabende | участие в открытых мероприятиях, знакомство с консультантами; справочник — только для исследования | доверие высокое, процесс медленный [ПРЕДПОЛОЖЕНИЕ] |
| 5 | **Отраслевые выставки**: NordBau (Neumünster), региональные Bau-/Handwerksmessen | посещение, разговоры у стендов, визитка с QR на демо-бота; стенд — позже | контакты с согласием на месте [ПРЕДПОЛОЖЕНИЕ: даты сверить] |
| 6 | **Facebook-группы** для Handwerker / Trockenbauer / Maler (DE) | экспертный контент («Wo finde ich Ausschreibungen unter 1 Mio €?»), без спама, по правилам админов; ответы в личке только на запрос | inbound, дёшево |
| 7 | **LinkedIn / XING**: владельцы фирм, Bauleiter, Kalkulatoren | профиль + посты-кейсы; личное сообщение только после реакции/контакта или общего мероприятия | средне; для DE-рынка XING ещё жив [ПРЕДПОЛОЖЕНИЕ] |
| 8 | **Партнёры-мультипликаторы**: Steuerberater/Unternehmensberater для Handwerk, Baustoffhändler, поставщики Handwerkersoftware, PQ-VOB-консультанты | партнёрская программа: 1 месяц бесплатно их клиентам / комиссия 10–20 % первого года (решение владельца) | хорошо масштабируется |
| 9 | **Inbound-сайт / лендинг** с демо и формой (согласие DSGVO) + SEO «Ausschreibungen Trockenbau Schleswig-Holstein» + небольшой Google Ads тест | заявка = согласие на контакт; можно подключить к существующему intake 7743356 по образцу | медленно, но законно и масштабируемо; Ads — бюджет решает владелец |
| 10 | **Generalunternehmer / Bietergemeinschaften**: GU ищут Nachunternehmer; малые фирмы хотят объединяться под большие лоты | разговор с GU как с партнёром; функция «ищу партнёра на лот» — идея на будущее | ниша [ПРЕДПОЛОЖЕНИЕ] |
| + | **Реферальная программа** для действующих клиентов: месяц бесплатно за приведённую фирму | только с их собственным обращением к коллегам | после первых 5 клиентов |

**Лучшие 3 канала для старта:** (1) своя сеть + русскоязычное сообщество ремесленников → пилоты; (2) Innungen/Kreishandwerkerschaften
как партнёры (доклад + скидка членам); (3) inbound: лендинг + полезный контент в FB/LinkedIn.

## 7. Что нужно от владельца (решения)
1. Утвердить/изменить цены пакетов, настройки и пилота (§3).
2. Продаём только после этапов 1–2 Bau у себя? (рекомендация Sales — да).
3. Make под продукт: отдельная организация/тариф или BYOK (§3.1) — деньги.
4. Публикация лендинга, постов, выход на Innungen — только после «да» владельца.

---

# TEIL 2. FÜR KUNDEN (DE) — ENTWURF

> **Entwurf – nicht veröffentlicht. Preise sind ein Vorschlag und vorbehaltlich Freigabe durch den Inhaber.**

## Tender-Radar — öffentliche Aufträge für Ihr Gewerk, jeden Morgen in Telegram

### Das Problem
Sie stehen tagsüber auf der Baustelle, abends schreiben Sie Angebote und Rechnungen. Für das tägliche Durchsuchen von
Vergabeportalen bleibt keine Zeit. Ausschreibungen sind auf viele Plattformen verteilt — TED, Bundes- und Landesportale,
kommunale Vergabestellen. Ihr Gewerk versteckt sich oft als Los in einem Großprojekt („Neubau Grundschule – Los 7 Trockenbau“).
Wer zu spät davon erfährt, schafft die Kalkulation nicht mehr.

### Die Lösung
Tender-Radar sucht täglich nach neuen öffentlichen Bauausschreibungen für **Ihr Gewerk** in **Ihrer Region**
(Trockenbau, Maler, Fliesen, Elektro, SHK, Dach u. a.) und schickt Ihnen jeden Morgen eine kurze Übersicht in Telegram:
- Auftraggeber, Ort, Gewerk/Los, Angebotsfrist (verbleibende Tage), Verfahrensart, geschätzter Wert (falls veröffentlicht);
- ein Klick zur Original-Bekanntmachung;
- optional: KI-Bewertung, Kalkulation mit **Ihren** Sätzen, Risiko-Check und Entwurf für Anschreiben oder Bieterfrage.

### Pakete *(Vorschlag – Preise vorbehaltlich Freigabe)*
| Paket | Leistung | Monatlich | Jährlich (2 Monate gratis) |
|---|---|---|---|
| **Basic** | Täglicher Digest: 1 Region, 1–2 Gewerke, Links zu den Bekanntmachungen | 39 € | 390 € |
| **Plus** ⭐ | + KI-Bewertung (Score 0–100, HOT/WARM/COLD mit Begründung), feiner Gewerk-Filter, bis 3 Gewerke, eigene Mindestfrist/-summe | 79 € | 790 € |
| **Pro** | + Kalkulation auf Basis Ihrer Sätze, Risiko-Check (Fristen, Nachweise, Bürgschaften, Vertragsstrafen …), Entwurf Anschreiben/Bieterfrage — 8 Kalkulationen und 5 Entwürfe pro Monat inklusive | 149 € | 1 490 € |

**Einrichtung (optional):** Basic 49 € (bei Jahreszahlung 0 €) · Plus 99 € · Pro 249 € (Erfassung Ihrer Sätze und Firmendaten, Test-Kalkulation gemeinsam).
Monatlich kündbar. Gemäß §19 UStG wird keine Umsatzsteuer berechnet *(vor Veröffentlichung prüfen)*.
**Pilot:** die ersten 3 Betriebe testen 30 Tage kostenlos.

### Was Tender-Radar nicht kann — ehrlich gesagt
- **Start mit EU-weiten Ausschreibungen (TED, oberhalb der EU-Schwellenwerte).** Unterschwellige Ausschreibungen (oeffentlichevergabe.de) folgen in einer späteren Ausbaustufe.
- Keine Garantie auf Vollständigkeit aller Ausschreibungen.
- **Keine Garantie auf Zuschlag** oder Aufträge.
- **Das Angebot geben Sie selbst ab** — über die jeweilige e-Vergabe-Plattform. Tender-Radar reicht nichts ein und schreibt niemandem in Ihrem Namen.
- Die Kalkulation ist eine Orientierung auf Basis Ihrer Sätze, keine verbindliche Kalkulation. Fehlende Sätze werden als „UNKNOWN“ angezeigt, nicht geschätzt.
- Keine Rechtsberatung zu Vergaberecht, Tariftreue oder Präqualifikation.

### So starten Sie
1. 3-Minuten-Demo ansehen.
2. Gewerke, Region (PLZ + Radius) und Paket wählen.
3. Bot in Telegram starten — am nächsten Morgen kommt der erste Digest.

Kontakt: Telegram @esusnob *(vor Veröffentlichung vom Inhaber bestätigen)*

---

## Erstnachricht — ENTWURF (nur nach Kontakt oder Einwilligung verwenden)

> **Nur verwenden, wenn** die Person uns angesprochen hat, auf einer Veranstaltung/Messe Kontakt bestand und sie um Infos gebeten hat,
> oder eine dokumentierte Einwilligung vorliegt (UWG §7). **Nicht** als Kaltmail, nicht an Adressen aus Verzeichnissen. Versand nur durch den Inhaber.

**Betreff:** Tender-Radar – wie besprochen: öffentliche Ausschreibungen für [Gewerk] in [Region]

Guten Tag Herr/Frau [Name],

vielen Dank für das Gespräch [bei/auf: Anlass, Datum]. Wie besprochen, hier kurz zu Tender-Radar:

Jeden Morgen bekommen Sie in Telegram eine Übersicht neuer öffentlicher Ausschreibungen für [Gewerk] im Umkreis von [X] km um [Ort] —
mit Frist, Auftraggeber und direktem Link zur Bekanntmachung. Auf Wunsch bewertet eine KI vorab, ob sich ein Angebot lohnt,
und rechnet mit Ihren eigenen Sätzen.

Ehrlich vorab: Wir starten mit EU-weiten Ausschreibungen (TED); unterschwellige folgen. Abgeben tun Sie wie gewohnt selbst über die Vergabeplattform.

Wenn Sie möchten, richte ich Ihnen einen kostenlosen 30-Tage-Test ein — dafür brauche ich nur Gewerk(e), PLZ und Radius.
Passt Ihnen ein kurzer Termin (10 Minuten) am [Tag] oder [Tag]?

Wenn Sie keine weiteren Nachrichten wünschen, genügt eine kurze Antwort.

Mit freundlichen Grüßen
[Name] · [Firma] · [Telefon] · [Impressum-Angaben]

---
_Черновик Sales для Директора. Цены, публикация, сообщения клиентам — только после решения владельца._
