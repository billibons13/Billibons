"""Определения Make-инструментов для официальных API: Awin Publisher API и Amazon Creators API.

Ключи хранятся только в Make (запрос на подключение «Klaus Affiliate Hunter — Awin & Amazon Creators API»).
Когда ключи подключены, инструменты создаются через Make MCP `tools_create` с ID ключа/подключения:

  python3 make/api_tools.py --awin-key <ID ключа apikeyauth> --amazon-conn <ID подключения oauth2>
  → make/api_tools.json (список готовых определений для tools_create)

Форматы взяты из официальной документации:
- Awin: https://api.awin.com, авторизация «Authorization: Bearer <token>»;
  GET /publishers/{id}/programmes?relationship=joined&countryCode=DE,
  POST /publishers/{id}/linkbuilder/generate {advertiserId, destinationUrl, shorten},
  GET /publishers/{id}/transactions/?startDate&endDate&timezone.
- Amazon Creators API: https://creatorsapi.amazon/catalog/v1/{getItems|searchItems}, OAuth2 client credentials,
  заголовок x-marketplace: www.amazon.de, тело в camelCase (partnerTag, itemIds, keywords, searchIndex, resources).
  Для ключей версии 3.x заголовок — «Bearer <token>» (его ставит OAuth-подключение Make). Ключи версии 2.x
  требуют «Bearer <token>, Version 2.x» — тогда нужен отдельный сценарий получения токена.
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
AWIN = "https://api.awin.com/publishers/{{var.input.publisher_id}}"
AMAZON = "https://creatorsapi.amazon/catalog/v1"
AMAZON_RESOURCES = [
    "itemInfo.title", "itemInfo.byLineInfo", "itemInfo.features", "itemInfo.manufactureInfo",
    "itemInfo.classifications", "offersV2.listings.price", "offersV2.listings.availability",
    "offersV2.listings.merchantInfo", "offersV2.listings.condition", "offersV2.listings.isBuyBoxWinner",
    "customerReviews.count", "customerReviews.starRating", "browseNodeInfo.websiteSalesRank",
    "browseNodeInfo.browseNodes.salesRank", "images.primary.medium",
]
META = {"expect": []}
COMMON = {"parseResponse": True, "stopOnHttpError": False, "allowRedirects": True, "shareCookies": False,
          "requestCompressedContent": True}


def _inp(name, desc, required=True, typ="text"):
    return {"name": name, "type": typ, "required": required, "description": desc}


def awin_tools(key_id):
    auth = {"authenticationType": "apiKey", "apiKeyKeychain": key_id}
    pub = _inp("publisher_id", "Awin Publisher ID")
    return [
        {"name": "Klaus Affiliate Hunter — Awin: Programme (joined, DE)",
         "description": "Awin Publisher API: Programme mit Status joined für Deutschland (advertiserId, Name, Domain, deeplinkEnabled).",
         "inputs": [pub],
         "module": {"module": "http:MakeRequest", "version": 4, "parameters": auth, "metadata": META, "mapper": {
             "url": AWIN + "/programmes", "method": "get",
             "queryParameters": [{"name": "relationship", "value": "joined"}, {"name": "countryCode", "value": "DE"}],
             **COMMON}}},
        {"name": "Klaus Affiliate Hunter — Awin: Tracking-Link erzeugen",
         "description": "Awin Link Builder: offizieller Tracking-Link für eine Produkt-URL eines Advertisers (nur bei joined).",
         "inputs": [pub, _inp("advertiser_id", "Awin advertiserId (Zahl)"), _inp("destination_url", "Produkt-URL")],
         "module": {"module": "http:MakeRequest", "version": 4, "parameters": auth, "metadata": META, "mapper": {
             "url": AWIN + "/linkbuilder/generate", "method": "post", "contentType": "json", "inputMethod": "jsonString",
             "jsonStringBodyContent": '{"advertiserId": {{var.input.advertiser_id}}, '
                                      '"destinationUrl": "{{var.input.destination_url}}", "shorten": false}',
             **COMMON}}},
        {"name": "Klaus Affiliate Hunter — Awin: Transaktionen",
         "description": "Awin Transaktionen (Verkäufe, Provisionen, Status) für einen Zeitraum — für Feedback/Statistik.",
         "inputs": [pub, _inp("start_date", "yyyy-MM-ddT00:00:00"), _inp("end_date", "yyyy-MM-ddT23:59:59 (max. 31 Tage)")],
         "module": {"module": "http:MakeRequest", "version": 4, "parameters": auth, "metadata": META, "mapper": {
             "url": AWIN + "/transactions/", "method": "get",
             "queryParameters": [{"name": "startDate", "value": "{{var.input.start_date}}"},
                                 {"name": "endDate", "value": "{{var.input.end_date}}"},
                                 {"name": "timezone", "value": "Europe/Berlin"}],
             **COMMON}}},
    ]


def amazon_tools(conn_id):
    auth = {"authenticationType": "oAuth", "oAuthAccount": conn_id}
    res = json.dumps(AMAZON_RESOURCES)
    head = [{"name": "x-marketplace", "value": "www.amazon.de"}]
    tag = _inp("partner_tag", "Ihr Amazon.de Partner-Tag (…-21)")
    return [
        {"name": "Klaus Affiliate Hunter — Amazon: getItems",
         "description": "Amazon Creators API getItems (amazon.de): Titel, Marke, Preis, Verfügbarkeit, Verkäufer, Bewertungen, Rang für bis zu 10 ASINs.",
         "inputs": [tag, _inp("asins", 'JSON-Array der ASINs, z. B. ["B0XXXXXXX1"]')],
         "module": {"module": "http:MakeRequest", "version": 4, "parameters": auth, "metadata": META, "mapper": {
             "url": AMAZON + "/getItems", "method": "post", "headers": head, "contentType": "json",
             "inputMethod": "jsonString",
             "jsonStringBodyContent": '{"partnerTag": "{{var.input.partner_tag}}", "itemIds": {{var.input.asins}}, '
                                      '"resources": %s}' % res,
             **COMMON}}},
        {"name": "Klaus Affiliate Hunter — Amazon: searchItems",
         "description": "Amazon Creators API searchItems (amazon.de): Suche nach Stichwort in einer Kategorie, bis 10 Ergebnisse mit Preis/Verfügbarkeit.",
         "inputs": [tag, _inp("keywords", "Suchbegriff auf Deutsch"),
                    _inp("search_index", "Kategorie, z. B. DIY, HomeAndKitchen, Garden, Lighting", False)],
         "module": {"module": "http:MakeRequest", "version": 4, "parameters": auth, "metadata": META, "mapper": {
             "url": AMAZON + "/searchItems", "method": "post", "headers": head, "contentType": "json",
             "inputMethod": "jsonString",
             "jsonStringBodyContent": '{"partnerTag": "{{var.input.partner_tag}}", "keywords": "{{var.input.keywords}}", '
                                      '"searchIndex": "{{ifempty(var.input.search_index; \\"All\\")}}", "itemCount": 10, '
                                      '"resources": %s}' % res,
             **COMMON}}},
    ]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--awin-key", type=int)
    ap.add_argument("--amazon-conn", type=int)
    a = ap.parse_args()
    tools = (awin_tools(a.awin_key) if a.awin_key else []) + (amazon_tools(a.amazon_conn) if a.amazon_conn else [])
    json.dump(tools, open(os.path.join(HERE, "api_tools.json"), "w"), ensure_ascii=False, indent=1)
    print(f"ok: {len(tools)} Tools → make/api_tools.json")
