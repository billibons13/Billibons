# 🧭 DIRECTOR runtime (бывш. Delivery Manager) — координатор конвейера лида (без LLM)

Версия карточки: **2.0** (13.10.2026, T-0041) · Тип: детерминированная логика Make, 0 токенов.
Где сейчас [ФАКТ]: LH-03 (приём), LH-10 (Analyst + gate карточки), LH-11 (Architect + Sales), LH-20 (кнопки и команды) —
собираются `scripts/generate_lh.py` (`lh03`, `lh10`, `lh11`, `lh20`). Целевое [ПЛАН]: отдельный сценарий **LH-30 Director Gate**
(аудит T-0039 этап 2, разделы E.1 и F) — вызывается после каждого агента, пишет `DIRECTOR_DECISION`, ведёт `stage_owner`.
Все пороги и веса — из `lh_settings` (`main`, `search`), в логике не захардкожены (кроме отмеченных ниже исключений).
Метки: **[ФАКТ]** — работает в Make · **[ПЛАН]** — нет в Make · **[ПРЕДПОЛОЖЕНИЕ]** — проверить.

## 1. Роль и цель
Довести каждый лид от NEW до решения владельца **без потерь, дублей и лишних трат**: проверить полноту результата
каждого агента (quality gate), выбрать следующий шаг, соблюсти SLA и показать владельцу только то, что стоит его времени.
Цель владельца — реальные коммерческие заказы → прибыль; DIRECTOR runtime экономит его внимание и кредиты.

Разделение ролей:
- **DIRECTOR runtime** — процесс и коммерческая маршрутизация лида (что дальше, кому, показать или архив).
- **Владелец** — все коммерческие решения: взять в работу, цена, контакт с клиентом, сделка.
- **SYSTEM GUARDIAN** — техническая исправность (сценарии, вебхуки, очереди, heartbeat). DIRECTOR runtime сбои не чинит.
- **Claude-DIRECTOR** (`raiv-fish-bot/agents/DIRECTOR.md`) — ежедневный надзор и изменения логики; runtime логику сам не меняет.

**Не делает:** не пишет клиентам, не ставит и не меняет цены, не подаёт ставки, не снимает паузу, не запускает платные
этапы (Architect/Sales) без кнопки владельца, не оценивает смысл текста (это Analyst).

### RACI по этапам
| Этап | R (делает) | A (отвечает) | C | I |
|---|---|---|---|---|
| Приём, дедуп (NEW) | Scout/LH-03 | DIRECTOR rt | — | владелец (📥) |
| Квалификация (ANALYZED) | Analyst/LH-10 | DIRECTOR rt | — | — |
| Gate G0 «показать / архив / ещё анализ» | DIRECTOR rt | DIRECTOR rt | Analyst | владелец |
| G1 «📝 ТЗ/КП» (сейчас ✅ Approve) | владелец | владелец | DIRECTOR rt | — |
| ТЗ + КП + расчёт (COMMERCIAL_READY) | Architect, Sales, Estimator [ПЛАН] | DIRECTOR rt | — | владелец |
| G2 «🚀 В работу» [ПЛАН] | владелец | владелец | DIRECTOR rt | Claude-DIRECTOR |
| Исполнение (IN_EXECUTION) [ПЛАН] | исполнитель | владелец | Claude-DIRECTOR | DIRECTOR rt |
| Итог WON/LOST | владелец | владелец | — | DIRECTOR rt (статистика) |
| Сбой сценария | GUARDIAN | Claude-DIRECTOR | DIRECTOR rt | владелец |

## 2. Входы
| Поле | Источник | Обяз. | Если нет |
|---|---|---|---|
| `lead_id`, `token` | вебхук (LH-03 → LH-10, LH-20 → LH-11) | да | неверный `token` → `SECURITY_DENIED`, ничего не делается |
| запись лида `lh_leads` (`status`, `attempts`, `grade`, `architect_run_id`, `sales_run_id`, `approved_at`, `more_analysis_at`) | 207950 | да | нет записи → кнопка отвечает «лид не найден», статус не создаётся |
| ответ Analyst (JSON: `lead_id`, `kind`, 10 `scores`, `reasons`, `budget`, `language`, `description_ru`, `risk_flags`) | LH-10 модуль 9–10 | да | невалиден → повтор / ERROR (§8) |
| `run_id`, `mode` (normal/more) | LH-20 → LH-11 | да | без `run_id` LH-11 не запускается (фильтр) |
| callback кнопки `действие|lead_id[|причина]` (≤ 64 байт), `chat_id` | Telegram → LH-20 | да | чужой chat_id → отказ, `SECURITY_DENIED` |
| `main`: `paused`, `daily_budget_usd`, `max_retry_attempts`, `retry_delays`, `hot/warm/cold_threshold`, `minimum_order_eur`, веса `w_*` | lh_settings | да | `ifempty` по умолчанию: 3 попытки, max_tokens 1500 |
| `day_<дата>.cost_usd` | lh_settings | нет | 0 |

## 3. Выходы
- Поля лида: `status`, `status_at`, `error_code`, `error_message`, `tg_message_id`, `commercial_message_id`, `attempts`,
  `architect_run_id`, `sales_run_id`, `approved_at`, `contacted_at`, `won_at`, `lost_reason`, `deal_amount_eur` [ФАКТ];
  `stage_owner` ∈ {analyst, architect, sales, estimator, owner, executor, guardian, director} [ПЛАН].
  Схема решения — **общая с Claude-DIRECTOR** (`raiv-fish-bot/agents/DIRECTOR.md`, LH-3, `DIRECTOR_LH_v1`): runtime исполняет
  в Make машинную часть чек-листов Ч1/Ч2 (LH-5), Claude-DIRECTOR — смысловую и ежедневный надзор.
- `error_code` ∈ {`ANALYST_FAILED`, `TELEGRAM_SEND`, `ARCHITECT_FAILED`, `SALES_FAILED`, `BUDGET_OR_PAUSED`} [ФАКТ].
- `lh_log` `table=events` (поля `event`, `details`, `old_status`, `new_status`) [ФАКТ]: `LEAD_CREATED`, `DUPLICATE_DETECTED`,
  `ANALYST_STARTED`, `ANALYST_RETRY`, `ANALYST_COMPLETED`, `SCORE_CALCULATED`, `TELEGRAM_SENT`, `ERROR`, `BUDGET_PAUSED`,
  `OWNER_APPROVED`, `OWNER_REJECTED`, `MORE_ANALYSIS_REQUESTED`, `ARCHITECT_STARTED/COMPLETED/ERROR`, `SALES_STARTED/COMPLETED/ERROR`,
  `COMMERCIAL_SENT_TO_OWNER`, `OWNER_CONTACTED`, `OWNER_WON`, `OWNER_ARCHIVED`, `OWNER_LOST`, `DEAL_AMOUNT_SET`, `PAUSED`, `RESUMED`,
  `STORAGE_CLEANED`, `SECURITY_DENIED`. [ПЛАН] `DIRECTOR_DECISION`: `lead_id`, `stage`, `decision` ∈ {`NEXT_AGENT`, `MORE_ANALYSIS`,
  `REWORK`, `ARCHIVE`, `TO_OWNER_G1`, `TO_OWNER_G2`, `ESCALATE_OWNER`, `ESCALATE_GUARDIAN`, `HOLD`, `CLOSE`}, `stage_owner`,
  `reason` ≤ 200 знаков, `missing[]`, `run_id`. Для runtime добавлено `NOOP` — вызов/нажатие отклонено guard'ом (повтор, неверный токен, запрещённый переход); пишется только событие.
- `lh_log` `table=decisions` (кнопки владельца: `action`, `reason`, `owner_chat_id`, `telegram_message_id`) и `table=runs` (токены, стоимость, `attempt`, `prompt_version`).
- Сообщения **только владельцу** (бот-пульт): карточка 1, строка архива, коммерческая карточка, предупреждения о бюджете/ошибке.

## 4. Машина состояний лида
```
            ┌──── дубль → (лид не создаётся, DUPLICATE_DETECTED)
Scout/LH-03 ▼
NEW ──LH-10──► ANALYZED ──gate G0──► SENT_TO_TELEGRAM (карточка 1) ──✅ ap──► APPROVED ──LH-11──► TECHNICAL_SPEC_READY
 │  (пауза/бюджет: ждёт)   │                │  ❌ rj → REJECTED                                  │
 │                         └─ COLD/REJECT ─► ARCHIVED (1 строка)                              ▼
 └─ 3 неудачи ─► ERROR ◄── сбой Telegram / Architect / Sales / бюджет ──────────── COMMERCIAL_READY
                  │ ✅ ap (повтор разрешён)                                                   ▼
                  └──────────────► APPROVED                    SENT_TO_TELEGRAM (карточка 2, есть commercial_message_id)
                                                                 │ 🚀 G2 [ПЛАН]          │ 📞 ct      │ 📦 ar   │ ❌ ls
                                                                 ▼                       ▼            ▼         ▼
                                                           IN_EXECUTION [ПЛАН] ─► CONTACTED ─► WON / LOST    ARCHIVED
```
| Из | В | Кто / триггер | Условие (guard) | SLA | Definition of Done этапа |
|---|---|---|---|---|---|
| — | NEW | LH-03 | нет совпадения `url_hash`/`text_hash`/`client+title` | — | запись с `lead_id`, хешами, `found_at`; `LEAD_CREATED` |
| NEW | ANALYZED | LH-10 | `paused ≠ true`, расход дня < бюджета, JSON валиден | ≤ 5 мин (с повторами ≤ 12 мин) | 10 оценок 0–10, `kind`, `score`, `grade`, `card_text`; `ANALYST_COMPLETED` + `runs` |
| ANALYZED | SENT_TO_TELEGRAM | LH-10 gate | grade HOT/WARM | **карточка ≤ 15 мин от NEW** | `tg_message_id` записан, `TELEGRAM_SENT` |
| ANALYZED | ARCHIVED | LH-10 gate | grade COLD/REJECT | ≤ 15 мин | строка с причиной (cap или худший критерий); кнопки ✅/❌/🔍 остаются |
| ARCHIVED (автоархив G0) | APPROVED | ✅ `ap` владельца | `can_run`; в ответе «⚠️ Grade COLD/REJECT: запущено по вашему решению» | — | как у APPROVED |
| SENT_TO_TELEGRAM | APPROVED | ✅ `ap` | `can_run` (§6) | — | `architect_run_id = run_id`, `OWNER_APPROVED`, decision |
| SENT_TO_TELEGRAM | REJECTED | ❌ `rj` → причина `rr` | — | — | причина в `decisions` |
| APPROVED | TECHNICAL_SPEC_READY → COMMERCIAL_READY → SENT_TO_TELEGRAM | LH-11 | `run_id` = `architect_run_id`, бюджет есть | ≤ 10 мин (дальше — «завис») | `architect_json`, `sales_json`, min ≤ rec ≤ target, `commercial_message_id` |
| COMMERCIAL / SENT | CONTACTED / WON / LOST / ARCHIVED | кнопки `ct`/`wn`/`ls`→`lr`/`ar` | лид найден | — | статус + `*_at`, событие `OWNER_*` |
| SENT (карточка 2) | IN_EXECUTION [ПЛАН] | 🚀 G2 | `commercial_message_id` есть, статус не финальный | чек-лист ≤ 1 мин | чек-лист владельцу; клиенту ничего |
| любой рабочий | ERROR | сбой | §8 | сообщение ≤ 1 мин | `error_code`, `error_message` ≤ 300 знаков, событие |
| ERROR | APPROVED | ✅ `ap` повтор | статус ERROR | — | новый `run_id` |

Финальные статусы **WON, LOST, ARCHIVED, CONTACTED** не перетираются поздним результатом LH-11 (`KEEP`, D3) [ФАКТ].
Известные пробелы [ФАКТ → ПЛАН]: (1) `SENT_TO_TELEGRAM` используется для карточки 1 и 2 — различать по `commercial_message_id`;
(2) кнопки `ar`/`wn`/`ls` не проверяют исходный статус — 📦 после 🏆 перезапишет WON; нужен белый список переходов;
(3) LH-10 показывает полную карточку только HOT/WARM и **не читает** `search.send_grades_csv` (там HOT,WARM,COLD);
(4) задержка повтора ограничена 300 с (`min(300; …)`): настройка «1,5,30 мин» фактически даёт 1, 5, 5 мин.

## 5. Правила (неизменные правила владельца)
- Клиенту ничего не уходит автоматически. «💬 Client Message» и «📞 Contacted» только показывают текст и фиксируют факт — отправляет владелец вручную.
- Цены Sales — предложение; сумма сделки = рекомендованная цена только до `/won <сумма>` владельца. Платежи, ставки на площадке, исполнители — только отдельным «да» владельца.
- Платные этапы (Architect + Sales ≈ 155 кредитов) — только кнопкой владельца; углублённый прогон — **1 раз на лид**.
- **Ручная пауза владельца не снимается никогда**: `paused = false` пишет только `/resume`. Автопауза по бюджету тоже снимается только `/resume` (на следующий день сама не снимается) [ФАКТ].
- Секреты (`internal_token`, `webhook_secret`, токены) не попадают в сообщения, `details`, `error_message`; в событии — только `token_present=yes|no`.
- Удаление данных — нет. Очистка тяжёлых полей LOST/ARCHIVED > `cleanup_days` (вариант A) — по решению владельца T-0009 [ФАКТ].

## 6. Gate G0 «показать / архив / ещё анализ» и идемпотентность
| Условие после Analyst | Решение (`decision`) | Сейчас |
|---|---|---|
| JSON невалиден, попытка < `max_retry_attempts` | повтор Analyst через `retry_delays` (`NEXT_AGENT` analyst) | [ФАКТ] |
| JSON невалиден, попытки исчерпаны | ERROR `ANALYST_FAILED`, владельцу «лид сохранён» (`ESCALATE_OWNER`) | [ФАКТ] |
| grade ∈ {HOT, WARM} и Ч1 полон | **показать владельцу** — карточка 1 + кнопки (`TO_OWNER_G1`) | [ФАКТ] без проверки Ч1 |
| grade ∈ {COLD, REJECT} | **архив** с причиной одной строкой (`ARCHIVE`) | [ФАКТ] |
| валиден, но не хватает 1–2 пунктов Ч1 (`description_ru` пуст при `language ≠ ru`, нет категории, подлинность без причины) | **ещё анализ** — 1 раз в рамках бюджета дня (`MORE_ANALYSIS`, stage_owner analyst); снова неполно → `ARCHIVE` «неполные данные» (видно в /today) | [ПЛАН] LH-30 |
| `kind = prospect` | не выше 59 → чаще всего архив | [ФАКТ] cap |
| пауза / бюджет 100 % | лид остаётся NEW (`HOLD`), владельцу ⛔ один раз | [ФАКТ] |
| сбой сценария / битая запись | `ESCALATE_GUARDIAN`, лид `HOLD` | [ПЛАН] |

Идемпотентность кнопок [ФАКТ]: ✅ `ap` генерирует `run_id` (uuid) и пишет его в `architect_run_id` **до** вызова LH-11;
повтор разрешён только если `architect_run_id` пуст, статус ERROR или APPROVED старше 10 мин; иначе ответ «уже одобрен».
LH-11 работает, только если `run_id` из запроса = `architect_run_id` и ≠ `sales_run_id` (второй вызов того же `run_id` — пустой).
🔍 `mx` — один раз (`more_analysis_at`). Кнопки после нажатия заменяются на «✅ Approved · …» / «❌ Rejected» (`callback_data = z`).
[ПЛАН] то же для 🚀 G2: `exec_run_id` + проверка статуса; повторное нажатие не создаёт второй план задач.

### Неполные и спорные данные
- Нет обязательного поля результата → не угадывать: `MORE_ANALYSIS` (1 раз) / `REWORK` (≤ 2 раз), затем архив или карточка с пометкой «неполно: …».
- Бюджет не указан → в карточке «не указан», `budget_eur` пуст, кап не применяется; курс неизвестен → «курс не задан».
- Статус лида не совпадает с ожидаемым для кнопки (например, ✅ по WON) → ничего не менять, ответить владельцу текущим статусом.
- Два источника расходятся (поздний результат LH-11 и финальный статус владельца) → прав владелец (`KEEP`).

### Примеры (вход → решение)
| # | Вход | Решение |
|---|---|---|
| 1 | NEW, пауза нет, бюджет дня 40 %; Analyst вернул валидный JSON, score 72 (WARM) | ANALYZED → карточка 1 → SENT_TO_TELEGRAM, `TELEGRAM_SENT` |
| 2 | Двойное нажатие ✅ за 3 с (второй callback, `architect_run_id` уже есть, статус APPROVED 3 с) | второй — «Уже одобрен…», LH-11 не вызывается, в журнале 1 `OWNER_APPROVED` |
| 3 | APPROVED 25 мин назад, `architect_json` нет, владелец жмёт ✅ снова (пограничный) | разрешено (> 10 мин): новый `run_id`; новый вызов LH-11 пройдёт фильтр, старый **не стартует** повторно, но если он ещё идёт — может дописать результат (проверки `run_id` в середине прогона нет — пробел [ФАКТ]) |
| 4 | Мусор: Analyst вернул текст вместо JSON 3 раза подряд | `ANALYST_RETRY` ×2, затем ERROR `ANALYST_FAILED` + сообщение владельцу; лид не потерян |
| 5 | Владелец нажал 🏆 Won во время углублённого прогона; позже Sales завершился | статус остаётся WON, событие «статус владельца WON сохранён» |

## 7. Самопроверка (перед каждой сменой статуса — guard в фильтре Make)
- [ ] токен вебхука и chat_id владельца проверены;
- [ ] переход есть в таблице §4, исходный статус совпадает (не финальный);
- [ ] для запуска платного этапа есть `run_id` от кнопки владельца и бюджет дня;
- [ ] обязательные поля результата есть и в диапазонах (оценки 0–10, min ≤ rec ≤ target, часы min ≤ max);
- [ ] записаны: поле статуса + `status_at` + событие `old_status → new_status`, кнопка — в `decisions`;
- [ ] сообщение уходит только в чат владельца, без секретов, ≤ 4000 знаков.

## 8. Ошибки и эскалация
| Событие | Обнаружение | Журнал | Кому | Автоповтор | Когда владелец |
|---|---|---|---|---|---|
| Analyst: невалидный JSON / MODEL_ERROR / REFUSAL | фильтр «JSON валиден» | `runs` FAILED + `ANALYST_RETRY` | DIRECTOR rt | да, до 3 раз (1/5/5 мин) | после 3-й: ERROR + сообщение |
| Telegram не принял карточку | onerror модуля sendMessage | ERROR `TELEGRAM_SEND` | GUARDIAN | нет | GUARDIAN-тревога (≥ 2 за сутки) |
| Architect / Sales сбой | фильтры LH-11 | ERROR `ARCHITECT_FAILED` / `SALES_FAILED` + событие | владелец | нет — кнопка «🔁 Повторить» (тот же guard) | сразу, с кнопкой |
| Бюджет 80 % / 100 % | расход дня | `warned_80`, `BUDGET_PAUSED` | владелец | нет | 80 % — предупреждение 1 раз в день; 100 % — пауза |
| Пауза / бюджет при Approve | фильтр LH-11 | ERROR `BUDGET_OR_PAUSED` | владелец | нет | сразу, «после /resume нажмите кнопку» |
| APPROVED без движения > 10 мин | `approved_at` | — | GUARDIAN (L1 > 1 ч) | повтор кнопкой разрешён | GUARDIAN-тревога |
| Противоречие (финальный статус + поздний результат) | `KEEP` | событие с «статус владельца сохранён» | — | — | нет |
| Неверный токен / чужой chat_id | фильтр | `SECURITY_DENIED` | GUARDIAN (L2 считает) | — | если > 3 за сутки |
| Лид в SLA-нарушении (NEW > 2 ч) | GD-01 | `guardian_state` | GUARDIAN → владелец | — | см. guardian.md |

## 9. Метрики и тест
- SLA/SLO: карточка ≤ 15 мин от NEW для ≥ 95 % лидов; повторных запусков LH-11 на одно нажатие = 0; лидов без конечного решения > 24 ч ≤ 5 %;
  доля карточек владельцу с решением ✅/❌ ≥ 70 % (иначе шум); ERROR ≤ 2 % лидов.
- Эталон: `lead-hunter/tests/golden_director.json` — 13 сценариев (9 по работающей логике, 4 [ПЛАН] LH-30 и пробелы; ситуация → статус + решение). Порог приёмки — 100 % (логика детерминированная).
- Б: **не измерен** (нужен прогон в Make тестовыми лидами `[TEST]` — стоит кредиты, по решению директора).

## 10. Экономичность и версия
- Операции Make: LH-10 ≈ 23 операции на лид + вызов Haiku (кредиты Make по токенам); LH-11 ≈ 155 кредитов (Architect + Sales Sonnet);
  кнопка LH-20 ≈ 4–8 операций; LH-30 [ПЛАН] — ≈ 6 операций на gate, без AI. Токенов DIRECTOR runtime — 0.
- Экономия: архив COLD/REJECT одной строкой (кнопки остаются — решение за владельцем), платные этапы только кнопкой, 1 углублённый прогон, Gatekeeper до AI.
- Версия = версия блюпринтов LH-03/10/11/20 (генератор `generate_lh.py`); откат — бэкап сценария в `lead-hunter/backup/` + ручной импорт LH-20 (лимит API ~45 КБ).

### Журнал изменений
| Версия | Дата | Что |
|---|---|---|
| 1.0 | 10.10 | Delivery Manager: статусы, повторы, бюджет, кнопки (этап 2–3) |
| 1.1 | 12.10 | D1–D3: Telegram onerror → Resume, финальные статусы не перетираются, защита повторного Approve |
| 2.0 | 13.10 | переименован в DIRECTOR runtime; машина состояний, RACI, SLA, DoD, gate G0, пробелы и [ПЛАН] LH-30; эталон `golden_director.json` |
