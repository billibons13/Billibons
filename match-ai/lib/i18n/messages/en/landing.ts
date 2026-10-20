export const landing = {
  meta: {
    title: "AI match analysis from a screenshot",
    description:
      "Upload a screenshot of a sports match and get a structured AI analysis in seconds: key factors, signals, risks and a transparent confidence score.",
  },
  hero: {
    eyebrow: "AI vision for sports matches",
    title: "AI analyzes the match in seconds.",
    subtitle:
      "Upload a screenshot of any match. Our AI recognizes the teams and returns a structured, transparent analysis — key factors, signals, risks and a confidence score.",
    primaryCta: "Try for free",
    secondaryCta: "How it works",
    note: "3 free analyses every month · No credit card required",
  },
  mock: {
    label: "Example of the analysis dashboard",
    upload: "screenshot.png",
    recognized: "Match recognized",
    analyzing: "Structured analysis",
    confidence: "Confidence",
    summary: "Summary",
    summaryText: "Home side in stronger recent form; head-to-head record is balanced.",
    signals: "Signals",
    risks: "Risks",
    positive: "Positive",
    negative: "Negative",
  },
  trust: {
    label: "Why it's different",
    items: {
      ai: { title: "AI powered", text: "Vision models read the screenshot" },
      fast: { title: "Fast analysis", text: "Results in seconds, not hours" },
      structured: { title: "Structured insights", text: "Factors, signals, risks" },
      secure: { title: "Secure data", text: "Your images stay private" },
    },
  },
  how: {
    eyebrow: "How it works",
    title: "From screenshot to structured insight",
    subtitle: "Four steps. No spreadsheets, no manual data entry.",
    steps: {
      upload: { title: "Upload", text: "Drop a screenshot from any sports app or website — PNG, JPEG or WEBP." },
      recognize: { title: "Recognize", text: "AI vision identifies the sport, teams, competition and visible match data." },
      analyze: { title: "Analyze", text: "The model weighs form, head-to-head, home advantage and other factors." },
      review: { title: "Review", text: "Read a clear breakdown with signals, risks, uncertainties and confidence." },
    },
  },
  demo: {
    eyebrow: "Analysis preview",
    title: "Every analysis follows the same clear structure",
    subtitle: "Transparent reasoning instead of a black box. When data is insufficient, the AI says so.",
    teamA: "Team A",
    teamB: "Team B",
    league: "Example league · Matchday 12",
    confidence: "Confidence",
    keyFactors: "Key factors",
    factors: {
      form: { title: "Form", detail: "Team A won 4 of its last 5 matches." },
      h2h: { title: "Head-to-head", detail: "Last 6 meetings: 2 wins each, 2 draws." },
      home: { title: "Home advantage", detail: "Team A plays at home, where it is stronger." },
      recent: { title: "Recent performance", detail: "Team B conceded in each of its last 4 away games." },
    },
    impact: { positive: "Positive", negative: "Negative", neutral: "Neutral" },
    uncertainties: "Uncertainties",
    uncertaintyText: "Line-ups not confirmed at the time of the screenshot.",
    explainButton: "What is this example?",
    explainTitle: "About this example",
    explainBody:
      "The teams, numbers and factors shown here are invented to illustrate the structure of an analysis. They are not a real prediction and not produced from real match data. Real analyses depend on what the AI can read from your screenshot — and return \"insufficient data\" when it can't support a conclusion.",
  },
  features: {
    eyebrow: "Features",
    title: "Built for clarity, not hype",
    subtitle: "Everything you need to understand a match faster.",
    items: {
      vision: { title: "AI Vision Analysis", text: "Reads scores, teams, odds and stats directly from your screenshot." },
      recognition: { title: "Match Recognition", text: "Identifies sport, competition and teams automatically." },
      structured: { title: "Structured Insights", text: "Key factors, positive and negative signals, risks and uncertainties." },
      confidence: { title: "Confidence Score", text: "A transparent score that reflects data quality — never a promise." },
      history: { title: "Analysis History", text: "Revisit and compare your past analyses at any time." },
      dashboard: { title: "Personal Dashboard", text: "Your plan, usage and analyses in one calm place." },
    },
  },
  pricing: {
    eyebrow: "Pricing",
    title: "Simple plans that grow with you",
    subtitle: "Start free. Upgrade when you need more analyses.",
    perMonth: "/ month",
    analysesPerMonth: "{count} analyses per month",
    popular: "Most popular",
    preliminary: "Prices are preliminary and may change before launch. Taxes may apply.",
    plans: {
      free: { name: "Free", description: "Try AI match analysis.", cta: "Start free" },
      pro: { name: "Pro", description: "For regular analysis.", cta: "Get Pro" },
      premium: { name: "Premium", description: "For power users.", cta: "Get Premium" },
    },
    featureList: {
      free: ["Structured AI analysis", "Confidence score", "Analysis history"],
      pro: ["Everything in Free", "More analyses every month", "Full analysis history"],
      premium: ["Everything in Pro", "Highest monthly volume", "Best for daily use"],
    },
  },
  faq: {
    eyebrow: "FAQ",
    title: "Questions, answered",
    items: [
      {
        q: "How does the AI analysis work?",
        a: "You upload a screenshot. A vision model extracts the visible match information (sport, teams, competition, score or odds if shown). A second step analyzes that data and returns a structured result with key factors, signals, risks, uncertainties and a confidence score. If the data is not sufficient, the AI returns \"insufficient data\" instead of guessing.",
      },
      {
        q: "Which screenshots can I upload?",
        a: "Screenshots from sports apps, live-score websites or broadcasts in PNG, JPEG or WEBP format, up to {maxMb} MB. The clearer the teams and match details are visible, the better the result.",
      },
      {
        q: "How many analyses can I run for free?",
        a: "The Free plan includes {freeCount} analyses per month. Paid plans include more — see Pricing above.",
      },
      {
        q: "Are my images stored?",
        a: "Images are stored privately and only for a configurable retention period (by default {retentionDays} days), after which they are deleted automatically. They are never shown publicly.",
      },
      {
        q: "Can I cancel my subscription?",
        a: "Yes. You can cancel at any time; your plan stays active until the end of the current billing period.",
      },
    ],
  },
  finalCta: {
    title: "Ready to try AI analysis?",
    subtitle: "Create a free account and analyze your first match in under a minute.",
    cta: "Start free",
  },
} as const;
