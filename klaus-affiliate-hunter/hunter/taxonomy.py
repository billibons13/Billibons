"""Бытовые проблемы Klaus → типы товаров, которые действительно решают проблему.

keywords — немецкие слова, по которым проблема узнаётся в сценарии Klaus.
products — (тип товара, поисковый запрос на немецком, роль: solve/measure/prevent/protect).
season — месяцы пикового спроса (1–12); пусто — круглый год.
compliance — особые требования к рекламе этой группы товаров.
"""

KLAUS_CATEGORIES = (
    "Sanitär & Reparatur", "Schimmel & Feuchtigkeit", "Lüften & Entfeuchten", "Reinigung & Haushaltschemie",
    "Werkzeug & Kleinreparatur", "Elektro für Zuhause", "Ordnung & Aufbewahrung", "Küche & Haushalt",
    "Garten & Außenbereich", "Energie & Wasser sparen", "Dämmung & Wärmeschutz", "Haushaltsdefekte beheben",
    "Smart Home",
)

PROBLEMS = {
    "schimmel_bad": {
        "category": "Schimmel & Feuchtigkeit",
        "keywords": ("schimmel", "stockflecken", "schwarze fugen", "feuchte wand", "muffig", "kondenswasser"),
        "products": (
            ("Hygrometer", "digitales Hygrometer Thermometer innen", "measure"),
            ("Schimmelentferner", "Schimmelentferner chlorfrei Bad", "solve"),
            ("Feuchtigkeitsmessgerät", "Feuchtigkeitsmessgerät Wand Holz", "measure"),
            ("Luftentfeuchter", "Luftentfeuchter elektrisch Bad", "prevent"),
            ("Fugenreiniger / Fugenbürste", "Fugenbürste Fliesen", "solve"),
            ("Sanitärsilikon mit Fungizid", "Sanitärsilikon schimmelresistent", "solve"),
            ("Schutzhandschuhe & FFP2", "Nitril Handschuhe FFP2 Maske", "protect"),
        ),
        "season": (10, 11, 12, 1, 2, 3),
        "compliance": ("biocide", "safety_ppe"),
    },
    "luftfeuchte_lueften": {
        "category": "Lüften & Entfeuchten",
        "keywords": ("luftfeuchtigkeit", "lüften", "stoßlüften", "beschlagene fenster", "feucht", "trocknen wäsche"),
        "products": (
            ("Hygrometer", "Hygrometer digital", "measure"),
            ("Luftentfeuchter", "Luftentfeuchter Kompressor", "solve"),
            ("Raumentfeuchter mit Granulat", "Raumentfeuchter Granulat Box", "solve"),
            ("Fenster-Ventilator / Badlüfter", "Badlüfter leise Feuchtesensor", "prevent"),
        ),
        "season": (10, 11, 12, 1, 2, 3),
        "compliance": ("electrical",),
    },
    "kalk": {
        "category": "Reinigung & Haushaltschemie",
        "keywords": ("kalk", "kalkflecken", "wasserkocher", "duschkopf", "armatur", "perlator"),
        "products": (
            ("Entkalker", "Entkalker Zitronensäure", "solve"),
            ("Perlator-Set", "Perlator Strahlregler Set", "solve"),
            ("Duschkopf mit Antikalk-Noppen", "Duschkopf Antikalk", "prevent"),
            ("Abzieher für Dusche", "Duschabzieher", "prevent"),
        ),
        "season": (),
        "compliance": ("chemicals",),
    },
    "abfluss": {
        "category": "Sanitär & Reparatur",
        "keywords": ("abfluss", "verstopft", "rohr", "siphon", "gluckert", "haare im abfluss"),
        "products": (
            ("Pümpel / Saugglocke", "Saugglocke Abfluss", "solve"),
            ("Rohrreinigungsspirale", "Rohrreinigungsspirale 5 m", "solve"),
            ("Abflusssieb / Haarsieb", "Haarsieb Dusche Abfluss", "prevent"),
            ("Rohrzangen-Set", "Wasserpumpenzange Set", "solve"),
        ),
        "season": (),
        "compliance": ("chemicals",),
    },
    "heizung_fenster": {
        "category": "Dämmung & Wärmeschutz",
        "keywords": ("heizung", "heizkörper", "entlüften", "zugluft", "fenster dichtung", "heizkosten", "thermostat"),
        "products": (
            ("Heizkörper-Entlüftungsschlüssel", "Entlüftungsschlüssel Heizkörper", "solve"),
            ("Fensterdichtungsband", "Fensterdichtung selbstklebend", "solve"),
            ("Smartes Heizkörperthermostat", "smartes Heizkörperthermostat", "prevent"),
            ("Heizkörper-Reflexionsfolie", "Heizkörper Reflexionsfolie", "prevent"),
            ("Zugluftstopper", "Zugluftstopper Tür", "solve"),
        ),
        "season": (9, 10, 11, 12, 1, 2),
        "compliance": ("energy_claims",),
    },
    "kueche_fett": {
        "category": "Küche & Haushalt",
        "keywords": ("fett", "backofen", "dunstabzug", "kühlschrank", "eingebrannt", "angebrannt"),
        "products": (
            ("Backofenreiniger", "Backofenreiniger Gel", "solve"),
            ("Ceranfeldschaber", "Ceranfeldschaber", "solve"),
            ("Dunstabzug-Fettfilter", "Fettfilter Dunstabzugshaube", "prevent"),
            ("Kühlschrank-Thermometer", "Kühlschrankthermometer", "measure"),
        ),
        "season": (11, 12),
        "compliance": ("chemicals",),
    },
    "waesche_waschmaschine": {
        "category": "Haushaltsdefekte beheben",
        "keywords": ("waschmaschine", "wäsche", "flusensieb", "gummidichtung", "stinkt", "trockner"),
        "products": (
            ("Waschmaschinenreiniger", "Waschmaschinenreiniger", "solve"),
            ("Wäscheständer / Trockengestell", "Wäscheständer platzsparend", "prevent"),
            ("Wasserstopp / Aquastop", "Aquastop Waschmaschine", "prevent"),
        ),
        "season": (),
        "compliance": ("chemicals",),
    },
    "fliesen_fugen_silikon": {
        "category": "Werkzeug & Kleinreparatur",
        "keywords": ("silikon", "fuge", "fliese", "kartusche", "dichtfuge"),
        "products": (
            ("Silikonentferner / Fugenkratzer", "Silikon Entferner Werkzeug", "solve"),
            ("Kartuschenpistole", "Kartuschenpresse", "solve"),
            ("Sanitärsilikon", "Sanitärsilikon transparent", "solve"),
            ("Fugenglätter-Set", "Fugenglätter Set", "solve"),
            ("Fugenmörtel / Fugenstift", "Fugenweiß Stift", "solve"),
        ),
        "season": (),
        "compliance": (),
    },
    "kleinreparatur": {
        "category": "Werkzeug & Kleinreparatur",
        "keywords": ("dübel", "bohren", "tür quietscht", "schraube", "wackelt", "loch in der wand", "reparatur"),
        "products": (
            ("Akku-Bohrschrauber", "Akku Bohrschrauber 18V", "solve"),
            ("Dübel-Sortiment", "Dübel Set Sortiment", "solve"),
            ("Leitungssucher", "Leitungssucher Ortungsgerät", "protect"),
            ("Kriechöl / Sprühöl", "Kriechöl Spray", "solve"),
            ("Spachtelmasse", "Reparaturspachtel innen", "solve"),
        ),
        "season": (),
        "compliance": ("electrical",),
    },
    "strom_sparen": {
        "category": "Energie & Wasser sparen",
        "keywords": ("strom", "standby", "stromverbrauch", "energie", "steckdose", "stromkosten"),
        "products": (
            ("Energiekostenmessgerät", "Energiekostenmessgerät Steckdose", "measure"),
            ("Steckdosenleiste mit Schalter", "Steckdosenleiste schaltbar", "solve"),
            ("Smarte Steckdose", "smarte Steckdose Verbrauchsmessung", "solve"),
            ("LED-Leuchtmittel", "LED Lampe E27 warmweiß", "solve"),
        ),
        "season": (10, 11, 12, 1),
        "compliance": ("electrical", "energy_claims"),
    },
    "wasser_sparen": {
        "category": "Energie & Wasser sparen",
        "keywords": ("wasser sparen", "wasserverbrauch", "tropft", "wasserhahn tropft", "spülkasten", "wasserkosten"),
        "products": (
            ("Spar-Duschkopf", "Sparduschkopf", "solve"),
            ("Durchflussbegrenzer", "Durchflussbegrenzer Wasserhahn", "solve"),
            ("Dichtungs-Set Wasserhahn", "Dichtungsringe Sortiment Sanitär", "solve"),
        ),
        "season": (),
        "compliance": ("energy_claims",),
    },
    "garten": {
        "category": "Garten & Außenbereich",
        "keywords": ("garten", "rasen", "unkraut", "terrasse", "dachrinne", "laub", "hecke"),
        "products": (
            ("Fugenkratzer Terrasse", "Fugenkratzer Pflaster", "solve"),
            ("Laubrechen / Laubsauger", "Laubbläser Akku", "solve"),
            ("Dachrinnenschutz", "Dachrinnenschutz Gitter", "prevent"),
            ("Gartenschlauch-Set", "Gartenschlauch Set", "solve"),
        ),
        "season": (3, 4, 5, 6, 7, 8, 9, 10),
        "compliance": ("pesticide",),
    },
    "ordnung": {
        "category": "Ordnung & Aufbewahrung",
        "keywords": ("ordnung", "chaos", "aufbewahrung", "keller", "abstellraum", "schrank", "platz sparen"),
        "products": (
            ("Aufbewahrungsboxen", "Aufbewahrungsbox stapelbar", "solve"),
            ("Werkzeugwand / Lochwand", "Lochwand Werkzeug", "solve"),
            ("Schubladeneinsatz", "Schubladen Organizer", "solve"),
        ),
        "season": (1, 3, 4),
        "compliance": (),
    },
    "smart_home": {
        "category": "Smart Home",
        "keywords": ("smart", "app", "wassermelder", "rauchmelder", "sensor", "automatisch"),
        "products": (
            ("Wassermelder", "Wassermelder Alarm", "prevent"),
            ("Rauchwarnmelder (DIN EN 14604)", "Rauchmelder DIN EN 14604 10 Jahre", "protect"),
            ("Tür-/Fenstersensor", "Fenstersensor smart", "prevent"),
        ),
        "season": (),
        "compliance": ("electrical",),
    },
}

# Чем сложнее законно рекламировать товар, тем больше требований к ролику.
COMPLIANCE_NOTES = {
    "biocide": ("Biozid (BPR Art. 72): в рекламе обязательно «Biozidprodukte vorsichtig verwenden. Vor Gebrauch "
                "stets Etikett und Produktinformationen lesen.»; запрещены «ungiftig», «unschädlich», "
                "«umweltfreundlich» и т. п.; проверьте регистрационный номер BAuA (N-…)."),
    "chemicals": "Бытовая химия: показывать перчатки, проветривание; никогда не смешивать хлор и кислоту.",
    "safety_ppe": "СИЗ: не обещать защиту сверх класса (FFP2 ≠ полная защита от спор при больших площадях).",
    "electrical": "Электротовар: только с маркировкой CE и немецким продавцом/импортёром (ProdSG/GPSR); "
                  "работы на сети 230 В — Fachbetrieb.",
    "energy_claims": "Экономия энергии: только проверяемые цифры с источником; без «halbiert Ihre Heizkosten».",
    "pesticide": "Средства от сорняков/вредителей: только допущенные (BVL), без обещаний «unbedenklich».",
}
