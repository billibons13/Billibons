# Германия: правила для роликов Klaus с партнёрскими ссылками

Это рабочая памятка, не юридическая консультация. При сомнениях — юрист по IT/UWG.

## 1. Обозначение рекламы (§ 5a Abs. 4 UWG, § 6 Abs. 1 DDG, § 22 MStV)
- С 2022 года коммерческий интерес при ссылках с вознаграждением **предполагается** — партнёрский ролик всегда реклама.
- В видео (TikTok/Reels/Shorts): «Werbung» или «Anzeige» **видно в начале ролика**; плашки платформы
  («Bezahlte Partnerschaft») сами по себе недостаточны.
- В тексте поста/описании: «Werbung» в **первой строке**, до «Mehr anzeigen»; у самой ссылки — «*Affiliate-Link»
  или «(Werbung)».
- Amazon: дополнительно «Als Amazon-Partner verdiene ich an qualifizierten Verkäufen» (Operating Agreement).
- Готовый текст для каждого товара агент кладёт в поле `disclosure_text`.
- Нарушения: типичная Abmahnung 1 500–5 000 €.

## 2. Рекламные утверждения
- Только то, что подтверждает производитель (паспорт, инструкция, сайт). Без «Testsieger», «bester», без чужих
  тестов (Stiftung Warentest — только по их лицензии на логотип).
- Без медицинских обещаний (плесень → «schützt Ihre Gesundheit» нельзя).
- Экономия энергии/воды — только с источником цифр.
- Безопасность в кадре: при химии — перчатки и проветривание; хлор и кислоту не смешивать;
  плесень > 0,5 м², электрика 230 В, газ — Fachbetrieb (уже в сценариях Klaus).

## 3. Особые группы товаров (флаги `compliance_flags`)
| Флаг | Требование |
|---|---|
| `biocide` | Средства от плесени — биоциды (BPR, Verordnung (EU) 528/2012, Art. 72): в рекламе обязательно «Biozidprodukte vorsichtig verwenden. Vor Gebrauch stets Etikett und Produktinformationen lesen.»; запрещены «ungiftig», «unschädlich», «natürlich», «umweltfreundlich», «tierfreundlich» и подобное. Проверять регистрацию в BAuA (номер N-…). |
| `electrical` | Только с CE и ответственным лицом в ЕС (GPSR (EU) 2023/988, ProdSG). No-name без импортёра — исключать. |
| `chemicals` | Опасные смеси — показывать по CLP-маркировке, без «harmlos». |
| `energy_claims` | Цифры экономии — только с источником. |
| `pesticide` | Только допущенные BVL средства. |

## 4. DSGVO / GDPR
- Агент не собирает персональные данные зрителей. В базе — только товары и агрегированная статистика
  (просмотры, клики, продажи из кабинетов сетей).
- Ссылки-сокращатели/трекеры с персональными данными не используем без информирования в Impressum/Datenschutz.
- Impressum на профилях соцсетей (§ 5 DDG) — у коммерческого аккаунта Klaus обязателен.

## 5. Материалы
- Фото/видео/отзывы магазинов и производителей не копировать в ролики без лицензии. Amazon разрешает
  изображения товаров только через свои API/инструменты и с актуальными данными.
- Музыка: библиотека платформы покрывает только саму платформу; для кросспостинга — свободные от прав треки.
- Klaus — ИИ-персонаж: TikTok/Instagram/YouTube требуют маркировать реалистичный ИИ-контент («KI-generiert»).
  По графику AI Act обязанности прозрачности (Art. 50) для дипфейк-подобного контента применяются с 02.08.2026;
  ЕС обсуждал отсрочки части требований — актуальный статус сверить перед запуском канала.

## Источники
- [Werbekennzeichnung Instagram/TikTok/YouTube 2026](https://signguard.app/ratgeber/influencer/werbekennzeichnung-instagram.html)
- [e-recht24: Influencer-Werbung kennzeichnen](https://www.e-recht24.de/online-marketing/12272-influencer-werbung-kennzeichnung.html)
- [IHK Frankfurt: Influencer-Marketing](https://www.frankfurt-main.ihk.de/recht/uebersicht-alle-rechtsthemen/wettbewerbsrecht/unlauterer-wettbewerb/irrefuehrende-werbung/influencer-marketing-5196192)
- [Werbung kennzeichnen: Regeln für alle Kanäle](https://www.ihre-ideenfabrik.de/magazin/marketing/werbung-kennzeichnen-was-rechtlich-gefordert-ist/)
