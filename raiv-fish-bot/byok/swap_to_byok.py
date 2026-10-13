"""T-0038: заменить anthropic-claude:simpleTextPrompt (ключ Make, платится кредитами)
на anthropic-claude:createAMessage с подключением владельца (BYOK).

Запуск: python3 swap_to_byok.py <blueprint_in.json> <blueprint_out.json> <conn_id> <out_expr>
  conn_id  — id подключения anthropic-claude в Make (появится после того, как владелец вставит ключ);
  out_expr — выражение ответа createAMessage, например 'content[1].text'
             (проверяется одним тестовым прогоном ДО замены рабочих сценариев — [ПРЕДПОЛОЖЕНИЕ] до теста).
Модель, промпт и max_tokens не меняются. Ключ в файлы не попадает — только id подключения.
"""
import json, re, sys

src, dst, conn, out_expr = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
bp = json.load(open(src))
swapped = []

def walk(flow):
    for m in flow:
        if m.get("module") == "anthropic-claude:simpleTextPrompt":
            mp = m.get("mapper", {})
            m["module"] = "anthropic-claude:createAMessage"
            m["parameters"] = {"__IMTCONN__": conn}
            m["mapper"] = {
                "model": mp["model"],
                "max_tokens": mp.get("max_tokens", 1024),
                "messages": [{"role": "user", "inputType": "single", "content": mp["textPrompt"]}],
            }
            m.get("metadata", {}).pop("restore", None)
            swapped.append(m["id"])
        for r in m.get("routes") or []:
            walk(r.get("flow", []))
        if m.get("onerror"):
            walk(m["onerror"])

walk(bp.get("flow", []))
s = json.dumps(bp, ensure_ascii=False)
for mid in swapped:
    s = re.sub(r"\{\{%d\.result\}\}" % mid, "{{%d.%s}}" % (mid, out_expr), s)
    s = s.replace("%d.result" % mid, "%d.%s" % (mid, out_expr))
assert "sk-ant" not in s
open(dst, "w").write(s)
print("swapped modules:", swapped)
