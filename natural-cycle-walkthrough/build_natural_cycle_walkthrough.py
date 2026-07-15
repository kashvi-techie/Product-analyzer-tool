from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VISUALS_DIR = ROOT / "evidence-visuals"

ACCESSED_DATE = "2026-07-15"

SOURCES = [
    {
        "sourceId": "NC-SRC-001",
        "title": "Natural Cycles Birth Control",
        "sourceUrl": "https://www.naturalcycles.com/birth-control",
        "sourceType": "website",
        "documentedFeatures": ["FDA-cleared positioning", "NC Birth Control mode", "Red/Green daily status", "subscription positioning"],
        "relevantAppSection": "Brand + Regulatory Trust",
        "evidenceStrength": "Official marketing and product positioning",
        "notes": "Use for brand/regulatory framing only; claims require citation when quoted.",
    },
    {
        "sourceId": "NC-SRC-002",
        "title": "How NC Birth Control works",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/11904213650205-How-NC-Birth-Control-works",
        "sourceType": "help article",
        "documentedFeatures": ["Green Days", "Red Days", "daily checking behavior", "learning-period behavior"],
        "relevantAppSection": "Today: Red or Green Fertility Status",
        "evidenceStrength": "Official support documentation",
        "notes": "Primary source for Red/Green behavioral interpretation.",
    },
    {
        "sourceId": "NC-SRC-003",
        "title": "How to make the most of the app: App tour",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/9209631867933-How-to-make-the-most-of-the-app-App-tour",
        "sourceType": "help article",
        "documentedFeatures": ["Today tab", "Add Data", "Graph tab", "Cycle Insights", "Learn tab", "Messages"],
        "relevantAppSection": "Daily Product Navigation",
        "evidenceStrength": "Official support documentation with app screenshots",
        "notes": "Strong source for app navigation and screen-level UI evidence.",
    },
    {
        "sourceId": "NC-SRC-004",
        "title": "Why should I measure my temperature?",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/360003289654-Why-should-I-measure-my-temperature",
        "sourceType": "help article",
        "documentedFeatures": ["temperature data", "ovulation detection", "cycle phase logic"],
        "relevantAppSection": "Daily Temperature Sync / Entry",
        "evidenceStrength": "Official support documentation",
        "notes": "Primary explanation for why temperature is algorithmically important.",
    },
    {
        "sourceId": "NC-SRC-005",
        "title": "What data does the algorithm use?",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/360003338473-What-data-does-the-algorithm-use",
        "sourceType": "help article",
        "documentedFeatures": ["algorithm data", "temperature", "period", "ovulation tests", "pregnancy tests", "emergency contraception"],
        "relevantAppSection": "Add Data",
        "evidenceStrength": "Official support documentation",
        "notes": "Separates algorithm-impacting data from optional trackers.",
    },
    {
        "sourceId": "NC-SRC-006",
        "title": "What Trackers are available?",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/360003288654-What-Trackers-are-available",
        "sourceType": "help article",
        "documentedFeatures": ["cervical mucus", "sex drive", "skin", "pain", "sleep", "emotions", "personal trackers"],
        "relevantAppSection": "Trackers + Personal Patterns",
        "evidenceStrength": "Official support documentation",
        "notes": "Use to distinguish personal pattern discovery from fertility-status calculation.",
    },
    {
        "sourceId": "NC-SRC-007",
        "title": "What is Cycle Insights?",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/1500003527502-What-is-Cycle-Insights",
        "sourceType": "help article",
        "documentedFeatures": ["cycle length", "period duration", "ovulation day", "follicular phase", "luteal phase", "trends"],
        "relevantAppSection": "Cycle Insights + Trends",
        "evidenceStrength": "Official support documentation",
        "notes": "Use for trends and longitudinal insight evidence.",
    },
    {
        "sourceId": "NC-SRC-008",
        "title": "What is Partner View?",
        "sourceUrl": "https://help.naturalcycles.com/hc/en-us/articles/360009136618-What-is-Partner-View",
        "sourceType": "help article",
        "documentedFeatures": ["shared fertility status", "selected shared trackers", "partner notifications", "definitions"],
        "relevantAppSection": "Partner View",
        "evidenceStrength": "Official support documentation",
        "notes": "Primary source for partner behavior.",
    },
    {
        "sourceId": "NC-SRC-009",
        "title": "Natural Cycles on Oura Ring",
        "sourceUrl": "https://www.naturalcycles.com/oura",
        "sourceType": "device page",
        "documentedFeatures": ["Oura integration", "temperature synchronization", "device setup"],
        "relevantAppSection": "Select Measuring Device",
        "evidenceStrength": "Official device integration page",
        "notes": "Use for wearable ecosystem evidence.",
    },
    {
        "sourceId": "NC-SRC-010",
        "title": "Natural Cycles with Apple Watch",
        "sourceUrl": "https://www.naturalcycles.com/apple-watch",
        "sourceType": "device page",
        "documentedFeatures": ["Apple Watch integration", "wrist temperature", "device setup"],
        "relevantAppSection": "Select Measuring Device",
        "evidenceStrength": "Official device integration page",
        "notes": "Use only where Apple Watch support is explicitly documented.",
    },
    {
        "sourceId": "NC-SRC-011",
        "title": "Natural Cycles on Garmin",
        "sourceUrl": "https://www.naturalcycles.com/garmin",
        "sourceType": "device page",
        "documentedFeatures": ["Garmin integration", "supported Garmin devices", "temperature synchronization"],
        "relevantAppSection": "Select Measuring Device",
        "evidenceStrength": "Official device integration page",
        "notes": "Use for Garmin support only.",
    },
    {
        "sourceId": "NC-SRC-012",
        "title": "Natural Cycles Privacy Policy",
        "sourceUrl": "https://www.naturalcycles.com/privacy",
        "sourceType": "website",
        "documentedFeatures": ["privacy", "research consent", "data handling", "account deletion"],
        "relevantAppSection": "Settings, Privacy & Device Management",
        "evidenceStrength": "Official policy page",
        "notes": "Use for privacy claims; avoid paraphrasing legal meaning too strongly.",
    },
    {
        "sourceId": "NC-SRC-013",
        "title": "Natural Cycles Instructions for Use / User Manual",
        "sourceUrl": "https://www.naturalcycles.com/user-manual",
        "sourceType": "user manual",
        "documentedFeatures": ["intended use", "mode-specific instructions", "safety instructions", "medical wording"],
        "relevantAppSection": "Safety + Instructions",
        "evidenceStrength": "Official user manual",
        "notes": "Use for safety wording and mode constraints; do not rewrite medical instructions.",
    },
    {
        "sourceId": "NC-SRC-014",
        "title": "FDA: De Novo classification request for Natural Cycles",
        "sourceUrl": "https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN170052.pdf",
        "sourceType": "regulatory document",
        "documentedFeatures": ["regulatory positioning", "classification", "contraceptive app context"],
        "relevantAppSection": "Brand + Regulatory Trust",
        "evidenceStrength": "FDA regulatory documentation",
        "notes": "Use only for regulatory positioning, not UX flow reconstruction.",
    },
]


VISUALS = {
    "today-birth-control": "https://help.naturalcycles.com/hc/article_attachments/36735104896541",
    "today-plan-pregnancy": "https://help.naturalcycles.com/hc/article_attachments/36735104897181",
    "add-data": "https://help.naturalcycles.com/hc/article_attachments/25438382881693",
    "graph": "https://help.naturalcycles.com/hc/article_attachments/36735104900509",
    "cycle-insights": "https://help.naturalcycles.com/hc/article_attachments/23345560369053",
    "learn-tab": "https://help.naturalcycles.com/hc/article_attachments/25438397911581",
}


SCREENS = [
    {
        "title": "Executive Summary",
        "section": "Executive Summary",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-001", "NC-SRC-002", "NC-SRC-003", "NC-SRC-013"],
        "takeaway": "Natural Cycles turns daily temperature and cycle data into one high-clarity fertility decision: Red or Green.",
        "facts": [
            "Natural Cycles positions itself as a regulated fertility product rather than a general wellness tracker.",
            "Official materials describe NC Birth Control, Plan Pregnancy, and pregnancy-related experiences.",
            "The core daily behavior is checking fertility status after data entry or synchronization.",
            "Temperature is a core input for detecting ovulation and calculating fertility status.",
        ],
        "docs": [
            "Official support documentation describes Red Days and Green Days as the main daily decision output in NC Birth Control.",
            "The app tour documents Today, Add Data, Graph, Cycle Insights, Learn, and Messages as core app areas.",
            "The user manual should be treated as the source of truth for safety-sensitive instructions.",
        ],
        "hypothesis": "The product appears designed around reducing a complex reproductive-health model into a binary daily action while using regulation and science to build confidence.",
        "questions": ["Which screens are shown before subscription in each country?", "Which official screenshots are current for the latest Android build?"],
        "oni": "ONI can learn from the idea of one clear daily status, but translate it into pregnancy-care guidance rather than contraception logic.",
    },
    {
        "title": "Sources + Evidence Rules",
        "section": "Sources",
        "mode": "All modes",
        "visual": None,
        "sourceIds": [source["sourceId"] for source in SOURCES],
        "takeaway": "This Natural Cycle analysis is reconstructed from official documentation, not direct Indian Android app access.",
        "facts": [
            "Only official Natural Cycles, support, user manual, device/integration, privacy, and FDA sources are used.",
            "User-supplied screenshots are not treated as official evidence for this rebuild.",
            "Where no official UI screenshot is available, the presentation uses a documentation-only evidence card.",
        ],
        "docs": ["Every screen stores source IDs, URLs, source types, and evidence strength."],
        "hypothesis": "The strongest analysis comes from separating official behavior from missing UI evidence instead of filling gaps with recreated screens.",
        "questions": ["Which exact app version do official screenshots represent?", "Are all official screenshots current across iOS and Android?"],
        "oni": "ONI should keep research discipline visible when benchmarking regulated healthcare products.",
    },
    {
        "title": "Complete Product Journey Map",
        "section": "Journey Map",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-001", "NC-SRC-002", "NC-SRC-003", "NC-SRC-013"],
        "takeaway": "The full Natural Cycles journey is assembled from official evidence, not observed as one continuous captured flow.",
        "facts": [
            "Documented flow: trust and mode selection lead into assessment, account/subscription, device setup, daily data, algorithm processing, fertility status, and longitudinal insights.",
            "Some transitions are documented across separate support pages rather than captured as one continuous screen recording.",
            "The recommended presentation flow uses dashed connectors for probable relationships and warning labels for missing UI evidence.",
        ],
        "docs": [
            "Brand + Regulatory Trust → Choose Primary Goal / Mode → Eligibility & Health Assessment → Account + Subscription → Select Measuring Device → Consent & Permissions → Daily Temperature Sync / Entry → Add Data → Algorithm Processing → Today: Red or Green Fertility Status → Calendar + Graph → Cycle Insights + Trends → Trackers + Personal Patterns → Partner View → Settings, Privacy & Device Management.",
        ],
        "hypothesis": "The product architecture appears to prioritize trust and compliance before long-term daily habit formation.",
        "questions": ["Which onboarding steps vary by mode, geography, device, and subscription state?"],
        "oni": "ONI can use a similar journey map discipline: trust first, then inputs, then daily decision clarity, then longitudinal care.",
    },
    {
        "title": "Brand + Regulatory Trust",
        "section": "Brand + Regulatory Trust",
        "mode": "NC Birth Control",
        "visual": None,
        "sourceIds": ["NC-SRC-001", "NC-SRC-014"],
        "takeaway": "Natural Cycles builds trust through regulatory positioning before asking users to rely on the product daily.",
        "facts": [
            "Official positioning emphasizes FDA-cleared / regulated birth-control framing.",
            "FDA documentation is used only for regulatory positioning in this audit.",
            "Regulatory trust is central to Natural Cycles’ differentiation from ordinary period trackers.",
        ],
        "docs": [
            "Official Natural Cycles and FDA sources document regulatory positioning.",
            "This does not by itself prove every onboarding screen shown to every user.",
        ],
        "hypothesis": "Regulatory language appears designed to reduce perceived risk and justify subscription/device friction.",
        "questions": ["Which regulatory trust claims are shown in-app before subscription?", "How does wording differ by market?"],
        "oni": "ONI can surface clinician, hospital, and safety credibility before asking for health data, while avoiding vague medical trust claims.",
    },
    {
        "title": "Choose Primary Goal / Mode",
        "section": "Choose Primary Goal / Mode",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-001", "NC-SRC-013"],
        "takeaway": "Mode choice changes the user’s primary decision: avoid pregnancy, plan pregnancy, or understand pregnancy/cycle state.",
        "facts": [
            "Official materials describe mode-specific experiences including NC Birth Control and Plan Pregnancy.",
            "Mode selection determines what daily status means to the user.",
            "Direct official mode-selection UI screenshot was not found in the collected source set.",
        ],
        "docs": ["User manual and product pages should be treated as source of truth for mode constraints."],
        "hypothesis": "The mode choice likely functions as a safety-critical routing step, not a casual personalization preference.",
        "questions": ["What exact eligibility questions appear before each mode?", "Which modes are available by geography?"],
        "oni": "ONI should route users by care context before asking detailed questions: pregnant, planning, postpartum, period care, or exploring.",
    },
    {
        "title": "Eligibility + Health Assessment",
        "section": "Eligibility & Health Assessment",
        "mode": "NC Birth Control",
        "visual": None,
        "sourceIds": ["NC-SRC-013"],
        "takeaway": "Safety-sensitive products need eligibility checks, but the UI evidence for exact screens remains incomplete.",
        "facts": [
            "Official instructions describe safety and intended-use boundaries.",
            "A complete official UI sequence for eligibility assessment was not found in the collected public screenshots.",
            "This screen is documentation-only in the audit.",
        ],
        "docs": ["User manual should govern eligibility, contraindications, and safety wording."],
        "hypothesis": "Eligibility likely protects both user safety and regulatory compliance before core app access.",
        "questions": ["Which eligibility answers block access, warn the user, or change the mode recommendation?"],
        "oni": "ONI should distinguish high-impact safety screening from optional personalization and explain why sensitive questions are asked.",
    },
    {
        "title": "Account + Subscription",
        "section": "Account + Subscription",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-001"],
        "takeaway": "Natural Cycles appears subscription-first, which may strengthen business value but adds access friction.",
        "facts": [
            "Official product pages present plan and subscription positioning.",
            "Pricing and availability can change and should be verified before presentation.",
            "No continuous official UI capture was found for the account-to-subscription sequence.",
        ],
        "docs": ["Use official pricing pages only for current price claims."],
        "hypothesis": "Subscription-first access appears designed to monetize before long-term habit formation, enabled by strong trust positioning.",
        "questions": ["What exactly is free before subscription?", "Does setup differ for returning users?"],
        "oni": "ONI should be careful with monetization timing: show care value and trust before asking users to pay or commit.",
    },
    {
        "title": "Select Measuring Device",
        "section": "Select Measuring Device",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-009", "NC-SRC-010", "NC-SRC-011"],
        "takeaway": "Device selection is not a minor setting; it defines whether the user can reliably supply algorithm data.",
        "facts": [
            "Official pages document Oura Ring, compatible Apple Watch, Garmin devices, NC Band, and basal thermometer pathways.",
            "The measuring method affects the daily data-entry or synchronization habit.",
            "Exact in-app selection UI is not fully captured in the official source set.",
        ],
        "docs": [
            "Official device pages describe integration setup and supported devices.",
            "The audit treats device pages as documentation evidence, not screenshots of the app flow.",
        ],
        "hypothesis": "Device choice appears to reduce manual effort and increase data consistency, but introduces cost and compatibility friction.",
        "questions": ["Which devices are supported in India?", "How does the app handle failed sync or missing temperature data?"],
        "oni": "ONI can integrate wearables for interpretation, not raw data display: sleep, HR trends, activity, hydration, and pregnancy-stage context.",
    },
    {
        "title": "Consent + Permissions",
        "section": "Consent & Permissions",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-012", "NC-SRC-013"],
        "takeaway": "Privacy and sensitive-data handling are part of the product experience, not just legal infrastructure.",
        "facts": [
            "Official privacy materials describe sensitive data handling and user controls.",
            "Optional research consent and data handling should be cited directly rather than summarized loosely.",
            "Exact permission screens were not found in the collected official UI screenshots.",
        ],
        "docs": ["Privacy policy and user manual are the source of truth for legal/privacy claims."],
        "hypothesis": "Trust-sensitive users may need privacy reassurance before connecting wearables or entering intimate data.",
        "questions": ["Where does research consent appear in the app?", "How visible is account deletion during normal use?"],
        "oni": "ONI should separate interaction consent, medical consent, privacy consent, and data-sharing consent in simple language.",
    },
    {
        "title": "Temperature Data → Algorithm → Fertility Status",
        "section": "Algorithm Processing",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-004", "NC-SRC-005"],
        "takeaway": "Natural Cycles’ product value is not collecting temperature; it is interpreting temperature into a daily status.",
        "facts": [
            "Official documentation explains that temperature helps detect ovulation-related shifts.",
            "Algorithm-relevant data includes temperature and other documented inputs.",
            "The output is a fertility status that the user checks daily.",
        ],
        "docs": [
            "Temperature data → hormone-related temperature shifts → ovulation detection → fertile-window calculation → daily fertility status.",
        ],
        "hypothesis": "The algorithm explanation appears designed to convert measurement effort into perceived scientific value.",
        "questions": ["How much algorithm explanation is shown in-app versus in help content?", "How are uncertainty and missing data explained?"],
        "oni": "ONI should translate sensor data into meaning: what changed, why it matters, what to do today, and when to contact a clinician.",
    },
    {
        "title": "Today View: NC Birth Control",
        "section": "Today: Red or Green Fertility Status",
        "mode": "NC Birth Control",
        "visual": "today-birth-control",
        "sourceIds": ["NC-SRC-003"],
        "takeaway": "The Today view centers the app around a single daily decision.",
        "facts": [
            "Official app-tour screenshot shows a Today tab for NC Birth Control.",
            "Today view can show daily fertility status, cycle day, logged information, and prediction overview.",
            "The screenshot is official support evidence, not a full observed app session.",
        ],
        "docs": ["App tour documents Today as a main screen and entry point to status and daily information."],
        "hypothesis": "The Today screen appears designed to make the product usable as a daily habit rather than a deep analytics tool.",
        "questions": ["Which Today modules vary by user stage and missing data?", "What happens after late/missing temperature?"],
        "oni": "ONI’s dashboard should similarly answer one question first: what should I do today?",
    },
    {
        "title": "Today View: Plan Pregnancy",
        "section": "Today: Red or Green Fertility Status",
        "mode": "Plan Pregnancy",
        "visual": "today-plan-pregnancy",
        "sourceIds": ["NC-SRC-003"],
        "takeaway": "The same Today architecture can support a different user goal by changing the meaning of status.",
        "facts": [
            "Official app-tour screenshot includes a Plan Pregnancy version of the Today tab.",
            "The daily output is adapted to the user’s mode.",
            "The app tour is the source of visual evidence.",
        ],
        "docs": ["Mode-specific Today screens are documented in official support materials."],
        "hypothesis": "Natural Cycles appears to reuse a common daily UI architecture across modes while changing status interpretation.",
        "questions": ["Which pregnancy-planning predictions are visible without subscription?", "Which status labels differ by mode?"],
        "oni": "ONI can reuse one daily-care architecture across pregnancy stages while changing the content by week, risk, and emotional state.",
    },
    {
        "title": "Green Day vs Red Day",
        "section": "Red / Green Status",
        "mode": "NC Birth Control",
        "visual": None,
        "sourceIds": ["NC-SRC-002", "NC-SRC-013"],
        "takeaway": "Red/Green status makes the safety-critical daily decision visually simple, but users must understand the conditions.",
        "facts": [
            "Green Day is documented as a not-fertile status in NC Birth Control when used as directed.",
            "Red Day indicates possible fertility and the need to use protection or abstain from vaginal intercourse.",
            "Status should be checked daily and may change when new data is added.",
            "More Red Days may appear while the algorithm is learning the cycle.",
        ],
        "docs": [
            "Do not paraphrase safety instructions in a way that changes their meaning.",
            "Use the manual/support wording when presenting externally.",
        ],
        "hypothesis": "The binary color model appears designed to reduce cognitive load for a high-stakes decision.",
        "questions": ["How does the app explain uncertainty or changed status after new data?", "How are warnings localized?"],
        "oni": "ONI can use Green/Yellow/Red care triage for symptoms, but must avoid oversimplifying medical risk.",
    },
    {
        "title": "Add Data",
        "section": "Add Data",
        "mode": "All modes",
        "visual": "add-data",
        "sourceIds": ["NC-SRC-003", "NC-SRC-005", "NC-SRC-006"],
        "takeaway": "Natural Cycles separates algorithm-relevant data from personal trackers, which clarifies what affects the output.",
        "facts": [
            "Official screenshot evidence shows Add Data as a core app action.",
            "Official documentation separates algorithm-impacting data from optional trackers.",
            "Algorithm data includes temperature, period/bleeding, ovulation tests, pregnancy tests, and emergency contraception where documented.",
            "Personal trackers support pattern discovery and may not directly affect Red/Green status.",
        ],
        "docs": ["Use official support docs when explaining whether a data type affects the algorithm."],
        "hypothesis": "This hierarchy appears designed to keep data entry medically meaningful without making every tracker feel equally important.",
        "questions": ["How clearly does the app label algorithm-impacting fields inside the UI?", "Are all trackers visible by default?"],
        "oni": "ONI should distinguish clinical data, context data, emotional data, and optional habit trackers so users understand why they are logging each item.",
    },
    {
        "title": "Calendar + Graph",
        "section": "Calendar + Graph",
        "mode": "All modes",
        "visual": "graph",
        "sourceIds": ["NC-SRC-003"],
        "takeaway": "Calendar and graph views turn daily data into a longitudinal cycle story.",
        "facts": [
            "Official app-tour screenshot documents the Graph tab.",
            "Graph/calendar views support reviewing cycle patterns and fertility-related predictions.",
            "The exact calendar UI screenshot was not found in the collected official source set.",
        ],
        "docs": ["App tour documents Graph as a main navigation area."],
        "hypothesis": "The graph likely serves advanced users who want evidence behind the daily status.",
        "questions": ["How does the app explain graph uncertainty to non-expert users?", "What calendar states are visible in each mode?"],
        "oni": "ONI can show pregnancy trends in a way that explains change over time without overwhelming the daily dashboard.",
    },
    {
        "title": "Cycle Insights + Trends",
        "section": "Cycle Insights + Trends",
        "mode": "All modes",
        "visual": "cycle-insights",
        "sourceIds": ["NC-SRC-007", "NC-SRC-003"],
        "takeaway": "Cycle Insights converts repeated daily logging into longer-term self-knowledge.",
        "facts": [
            "Official materials document Cycle Insights and trends.",
            "Documented insight areas include cycle length, period duration, average ovulation day, follicular phase, luteal phase, atypical/irregular-cycle flags, measuring streak, added tests, logged sex, and personal tracker patterns.",
            "Official screenshot evidence exists through support materials.",
        ],
        "docs": ["Cycle Insights should be treated as longitudinal analysis rather than a single-day screen."],
        "hypothesis": "Insights likely support retention by rewarding consistent data entry with personalized feedback.",
        "questions": ["Which insights require a minimum amount of logged data?", "Which insights are premium-gated?"],
        "oni": "ONI can transform repeated pregnancy logs into weekly care insights, appointment prep, and doctor-ready summaries.",
    },
    {
        "title": "Trackers + Personal Patterns",
        "section": "Trackers + Personal Patterns",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-006"],
        "takeaway": "Optional trackers broaden the product from fertility status to personal pattern discovery.",
        "facts": [
            "Official tracker documentation includes cervical mucus, sex drive, skin, pain and symptoms, sleep, emotions, and related personal trackers.",
            "These trackers support personal insights and patterns.",
            "The audit does not assume every tracker affects fertility status.",
        ],
        "docs": ["Use the algorithm-data source separately when discussing fertility-status impact."],
        "hypothesis": "Trackers appear to increase retention and personalization without overloading the core Red/Green decision.",
        "questions": ["Which trackers are enabled by default?", "Can users hide sensitive trackers?"],
        "oni": "ONI can personalize tracker depth by comfort level: beginner, clinical, partner-support, and doctor-review views.",
    },
    {
        "title": "Partner View",
        "section": "Partner View",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-008"],
        "takeaway": "Partner View extends the care context beyond the individual user without making the partner the primary account owner.",
        "facts": [
            "Official documentation describes shared fertility status and selected shared trackers.",
            "Partner View can include tracker graph, definitions, notifications, and pregnancy-week or trimester notifications where applicable.",
            "The partner experience is officially documented but an authentic UI screenshot was not found in the collected set.",
        ],
        "docs": ["Partner sharing should be described only within documented capabilities."],
        "hypothesis": "Partner View appears designed to reduce communication burden and increase shared accountability.",
        "questions": ["How granular are sharing controls?", "How are privacy boundaries explained to the primary user?"],
        "oni": "ONI’s partner mode should help the partner support the mother through weekly changes, appointments, emotional needs, and emergency contacts.",
    },
    {
        "title": "Settings, Privacy + Device Management",
        "section": "Settings, Privacy & Device Management",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-009", "NC-SRC-010", "NC-SRC-011", "NC-SRC-012"],
        "takeaway": "Device management and privacy controls are core product infrastructure because the system depends on sensitive longitudinal data.",
        "facts": [
            "Official pages document device integrations and privacy/data handling.",
            "Account deletion, consent, and data protection claims should be cited directly.",
            "Official UI screenshots for settings/privacy screens were not found in the collected source set.",
        ],
        "docs": ["Privacy policy and device pages should be used as separate evidence types."],
        "hypothesis": "Settings likely become more important after wearable connection and partner sharing are enabled.",
        "questions": ["How easy is it to revoke partner access?", "Where can a user change measuring device?"],
        "oni": "ONI should make wearable controls, partner access, doctor sharing, and data deletion visible and understandable.",
    },
    {
        "title": "What ONI Can Learn From Natural Cycles",
        "section": "ONI Comparison",
        "mode": "All modes",
        "visual": None,
        "sourceIds": ["NC-SRC-001", "NC-SRC-002", "NC-SRC-003", "NC-SRC-007", "NC-SRC-008"],
        "takeaway": "ONI should borrow the product logic of clear daily guidance, not the contraception model itself.",
        "facts": [
            "Natural Cycles shows the value of one clear daily status.",
            "It separates algorithm-relevant inputs from optional personal trackers.",
            "It uses scientific and regulatory evidence as trust infrastructure.",
            "It extends the experience through wearables, longitudinal trends, and partner access.",
        ],
        "docs": [
            "Limitations visible in this research: device/subscription friction, clinical tone, reliance on consistent temperature data, geographic/app availability constraints, and limited direct app observation.",
        ],
        "hypothesis": "ONI can differentiate by making evidence-led guidance feel warmer, more emotionally supportive, and more care-team connected.",
        "questions": ["What is ONI’s equivalent of Red/Green status: Daily Focus, symptom triage, appointment readiness, or risk monitor?"],
        "oni": "Build a pregnancy-care daily status that combines week, symptoms, context, wearable signals, and doctor escalation into one calm action.",
    },
]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:54]


def source_lookup() -> dict[str, dict]:
    return {source["sourceId"]: source for source in SOURCES}


def write_placeholder(screen_id: str, title: str, subtitle: str, source_label: str) -> str:
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)
    path = VISUALS_DIR / f"{screen_id.lower()}-{slug(title)}.svg"
    title_escaped = html.escape(title)
    subtitle_escaped = html.escape(subtitle)
    source_escaped = html.escape(source_label)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1280" viewBox="0 0 720 1280">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff"/>
      <stop offset="100%" stop-color="#f6edf3"/>
    </linearGradient>
  </defs>
  <rect width="720" height="1280" rx="44" fill="url(#bg)"/>
  <rect x="54" y="64" width="612" height="1152" rx="38" fill="#ffffff" stroke="#ead8e5" stroke-width="2"/>
  <circle cx="360" cy="318" r="106" fill="#87006f" opacity=".11"/>
  <text x="360" y="304" text-anchor="middle" font-family="Arial, sans-serif" font-size="32" font-weight="700" fill="#87006f">Official Evidence Card</text>
  <text x="360" y="380" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#54464f">UI screenshot not found</text>
  <foreignObject x="96" y="500" width="528" height="250">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Arial,sans-serif;color:#18151a;text-align:center;font-size:38px;font-weight:800;line-height:1.18;">{title_escaped}</div>
  </foreignObject>
  <foreignObject x="106" y="780" width="508" height="180">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Arial,sans-serif;color:#6f6470;text-align:center;font-size:26px;line-height:1.35;">{subtitle_escaped}</div>
  </foreignObject>
  <text x="360" y="1100" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#8a7884">{source_escaped}</text>
</svg>"""
    path.write_text(svg, encoding="utf-8")
    return f"evidence-visuals/{path.name}"


def build_screens() -> list[dict]:
    sources = source_lookup()
    screens = []
    total = len(SCREENS)
    for idx, item in enumerate(SCREENS, start=1):
        original_id = f"{idx:03d}"
        screen_id = f"NC-{slug(item['section']).upper()}-{original_id}"
        source_titles = [sources[source_id]["title"] for source_id in item["sourceIds"] if source_id in sources]
        if item["visual"] and item["visual"] in VISUALS:
            image = VISUALS[item["visual"]]
            definite_screenshot = True
            caption = "Official screenshot embedded in Natural Cycles support documentation."
        else:
            image = write_placeholder(screen_id, item["title"], "Documented behavior without a collected official UI screenshot.", source_titles[0] if source_titles else "Official source")
            definite_screenshot = False
            caption = "Official UI screenshot not found; this is a documentation-only research card."

        prev_id = f"{idx - 1:03d}" if idx > 1 else None
        next_id = f"{idx + 1:03d}" if idx < total else None
        source_links = [sources[source_id]["sourceUrl"] for source_id in item["sourceIds"] if source_id in sources]
        source_types = sorted({sources[source_id]["sourceType"] for source_id in item["sourceIds"] if source_id in sources})
        docs = item["docs"]
        docs.extend([f"{source_id}: {sources[source_id]['title']} — {sources[source_id]['sourceUrl']}" for source_id in item["sourceIds"] if source_id in sources])

        screens.append({
            "id": screen_id,
            "originalId": original_id,
            "app": "Natural Cycle",
            "order": idx,
            "total": total,
            "section": item["section"],
            "originalSection": item["section"],
            "title": item["title"],
            "image": image,
            "previousScreen": prev_id,
            "previousOriginal": prev_id,
            "userAction": "Documented/probable next step assembled from official source evidence.",
            "nextScreen": next_id,
            "nextOriginal": next_id,
            "observedFacts": item["facts"],
            "officialDocumentation": docs,
            "possibleReason": item["hypothesis"],
            "questions": item["questions"],
            "oniOpportunity": item["oni"],
            "developerNotes": {
                "Evidence type": "Official screenshot" if definite_screenshot else "Documentation only / missing UI screenshot",
                "Entry action": "Documented relationship from prior research card" if prev_id else "Start of Natural Cycle evidence presentation",
                "Exit action": "Continue to next documented research card" if next_id else "End of Natural Cycle evidence presentation",
                "Visible controls": "Use screenshot evidence if present; otherwise this is not a UI control map.",
                "Recorded destination": next_id or "End",
                "Missing destination": "Direct in-app transition not observed in local Android workflow.",
                "Data collected or displayed": item["title"],
                "Does it affect algorithm": "Yes / documented" if item["section"] in ["Add Data", "Algorithm Processing", "Daily Temperature Sync / Entry"] else "Depends on source; see documentation.",
                "Decision supported": item["takeaway"],
                "Device or integration required": "See source links for thermometer, NC Band, Oura, Apple Watch, or Garmin requirements.",
                "Source URLs": " | ".join(source_links),
                "Official caption": caption,
                "Accessed date": ACCESSED_DATE,
            },
            "tags": sorted(set(["Natural Cycle", item["mode"], item["section"], *source_types, "Official screenshot" if definite_screenshot else "Documentation only"])),
            "accessType": "Subscription / regulated product" if item["section"] in ["Account + Subscription", "Brand + Regulatory Trust"] else "Documented",
            "evidenceStatus": "Official screenshot" if definite_screenshot else "Official documentation",
            "sourceTimestamp": "Official public documentation",
            "sourceTimestampSeconds": None,
            "takeaway": item["takeaway"],
            "confidence": "High" if item["sourceIds"] else "Medium",
            "unverifiedClaim": "Claims are sourced from official documentation but have not been independently clinically revalidated in this audit.",
            "sourceEvidence": "; ".join(source_titles),
            "sourceLinks": source_links,
            "rawObservation": item["title"],
            "hotspots": [{"label": "Next documented screen", "target": next_id, "x": 8, "y": 84, "w": 84, "h": 9}] if next_id and definite_screenshot else [],
            "definitelyAppScreenshot": definite_screenshot,
            "modeShown": item["mode"],
        })
    return screens


def write_data(screens: list[dict]) -> None:
    payload = json.dumps(screens, indent=2, ensure_ascii=False)
    (ROOT / "natural-cycle-research-data.json").write_text(payload, encoding="utf-8")
    (ROOT / "natural-cycle-research-data.js").write_text(
        "window.NATURAL_CYCLE_RESEARCH_SCREENS = " + payload + ";\n"
        "window.NATURAL_CYCLE_SOURCES = " + json.dumps(SOURCES, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    (ROOT / "metadata.json").write_text(
        json.dumps({
            "app": "Natural Cycle",
            "screenCount": len(screens),
            "sourceCount": len(SOURCES),
            "accessedDate": ACCESSED_DATE,
            "researchLimitation": "Reconstructed from official public sources because local Indian Android app access was unavailable.",
        }, indent=2),
        encoding="utf-8",
    )
    with (ROOT / "screen-inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "id", "order", "title", "section", "modeShown", "evidenceStatus",
            "definitelyAppScreenshot", "previousScreen", "nextScreen", "sourceEvidence", "takeaway",
        ])
        writer.writeheader()
        for screen in screens:
            writer.writerow({key: screen.get(key, "") for key in writer.fieldnames})
    with (ROOT / "source-inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "sourceId", "title", "sourceUrl", "sourceType", "accessedDate",
            "documentedFeatures", "relevantAppSection", "evidenceStrength", "notes",
        ])
        writer.writeheader()
        for source in SOURCES:
            row = dict(source)
            row["accessedDate"] = ACCESSED_DATE
            row["documentedFeatures"] = "; ".join(source["documentedFeatures"])
            writer.writerow(row)
    (ROOT / "flow-map.json").write_text(
        json.dumps([
            {
                "from": screen["originalId"],
                "action": screen["userAction"],
                "to": screen["nextScreen"] or "End",
                "connector": "solid" if screen["evidenceStatus"] == "Official screenshot" else "dashed",
                "status": screen["evidenceStatus"],
            }
            for screen in screens
        ], indent=2),
        encoding="utf-8",
    )
    (ROOT / "source-inventory.json").write_text(json.dumps(SOURCES, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "missing-screens-and-questions.md").write_text(
        "# Missing Evidence Report\n\n"
        "- Local Indian Android app access was not available, so this is not a direct observed walkthrough.\n"
        "- Exact mode-selection, eligibility, subscription, consent, privacy-settings, device-management, and partner-view UI screenshots were not found in the collected official source set.\n"
        "- Some official screenshots appear inside support documentation and may not represent the latest Android UI.\n"
        "- Medical and safety wording should be quoted from the official user manual/support pages during final presentation.\n"
        "- Pricing, device availability, and regional feature availability should be verified before external use.\n",
        encoding="utf-8",
    )
    (ROOT / "executive-summary.md").write_text(
        "# Natural Cycle Executive Summary\n\n"
        "Natural Cycles is a regulated fertility product for birth control, pregnancy planning, and cycle understanding. "
        "Its core daily behavior is collecting/syncing temperature and cycle data, processing that through a fertility algorithm, "
        "and returning a clear daily status. The strongest UX decision is the binary Red/Green daily decision model. "
        "The highest-friction points are device dependence, subscription-first access, consistent measurement requirements, and limited local availability for this research. "
        "ONI can learn from its clear data hierarchy, wearable integration, evidence-led trust, partner access, and longitudinal insights, while translating those patterns into pregnancy care rather than contraception logic.\n",
        encoding="utf-8",
    )


def write_index() -> None:
    template = (ROOT.parent / "flo-video-walkthrough" / "index.html").read_text(encoding="utf-8")
    html_text = template
    html_text = html_text.replace("Flo Product Research Walkthrough", "Natural Cycle Official Evidence Walkthrough")
    html_text = html_text.replace('<script src="flo-research-data.js"></script>', '<script src="natural-cycle-research-data.js"></script>')
    html_text = html_text.replace("<h1>Flo Journey</h1>", "<h1>Natural Cycle Evidence</h1>")
    html_text = html_text.replace('alt="Observed Flo screen"', 'alt="Official Natural Cycle evidence"')
    html_text = html_text.replace("window.FLO_RESEARCH_SCREENS", "window.NATURAL_CYCLE_RESEARCH_SCREENS")
    html_text = html_text.replace("--accent: #f05a8a;", "--accent: #87006f;")
    html_text = re.sub(
        r'<nav class="seg" aria-label="Switch product walkthrough">.*?</nav>',
        '<nav class="seg" aria-label="Switch product walkthrough">\n'
        '            <a href="../flo-video-walkthrough/index.html">Flo</a>\n'
        '            <a href="../clue-video-walkthrough/index.html">Clue</a>\n'
        '            <a class="active" href="./index.html">Natural Cycle</a>\n'
        '          </nav>',
        html_text,
        flags=re.S,
    )
    html_text = html_text.replace(
        '<details open><summary>Possible Reason <span class="hypothesis">(hypothesis)</span></summary><div class="detail-body"><p id="reason"></p></div></details>',
        '<details open><summary>Official Documentation</summary><div class="detail-body"><ul id="officialDocs"></ul></div></details>\n'
        '      <details open><summary>Possible Reason <span class="hypothesis">(hypothesis)</span></summary><div class="detail-body"><p id="reason"></p></div></details>',
    )
    html_text = html_text.replace(
        'reason: document.getElementById("reason"),',
        'reason: document.getElementById("reason"),\n      officialDocs: document.getElementById("officialDocs"),',
    )
    html_text = html_text.replace(
        'els.reason.textContent = s.possibleReason;',
        'renderList(els.officialDocs, s.officialDocumentation || [], "fact");\n      els.reason.textContent = s.possibleReason;',
    )
    html_text = html_text.replace(
        '<h2>Entry → Trust → Intent → Assessment → Dashboard → Retention → Premium</h2>',
        '<h2>Brand Trust → Mode → Assessment → Subscription → Device → Daily Status → Insights → Partner → Privacy</h2>',
    )
    (ROOT / "index.html").write_text(html_text, encoding="utf-8")


def main() -> None:
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)
    screens = build_screens()
    write_data(screens)
    write_index()


if __name__ == "__main__":
    main()
