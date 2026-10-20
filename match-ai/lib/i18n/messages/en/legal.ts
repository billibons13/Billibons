/**
 * Legal page TEMPLATES. Bracketed fields like [Company name] must be filled in
 * by the owner. These texts are not legal advice and do not guarantee GDPR or
 * any other legal compliance — have them reviewed by a qualified lawyer.
 */
export const legal = {
  legal: {
    templateNotice:
      "Template — this page is a structural draft. Fields in [brackets] must be completed by the operator. It is not legal advice and does not guarantee legal compliance; have it reviewed by a qualified lawyer before launch.",
    lastUpdated: "Last updated: [Date]",
    onThisPage: "On this page",
    privacy: {
      metaTitle: "Privacy policy",
      title: "Privacy policy",
      sections: [
        { h: "1. Controller", p: ["[Company name], [Street and number], [Postcode, City], [Country]. Email: [privacy contact email]. Representative: [Name of managing director]."] },
        { h: "2. Data protection officer", p: ["[Name and contact of the data protection officer, if appointed — or state that none is required.]"] },
        { h: "3. Data we process", p: ["Account data: email address, hashed password (handled by our authentication provider).", "Uploaded screenshots and the analysis results generated from them.", "Usage data: number of analyses per billing period, technical logs (IP address, timestamps) for security.", "Payment data: processed by our payment provider; we do not store full card details."] },
        { h: "4. Purposes and legal bases (Art. 6 GDPR)", p: ["Providing the service and your account — Art. 6(1)(b) GDPR (contract).", "Security, abuse prevention and logs — Art. 6(1)(f) GDPR (legitimate interests).", "Optional analytics — only with your consent, Art. 6(1)(a) GDPR. You can withdraw consent at any time via “Cookie settings”.", "Statutory retention of invoices — Art. 6(1)(c) GDPR (legal obligation)."] },
        { h: "5. AI processing of screenshots", p: ["Screenshots are sent to an AI provider ([AI provider name, country]) solely to produce your analysis. [Describe the provider's data retention and whether data is used for training.]"] },
        { h: "6. Processors and recipients", p: ["Hosting: [Hosting provider, region]. Database & authentication: [Database provider, region]. Payments: [Payment provider]. AI: [AI provider]. Analytics (consent only): [Analytics provider, region]."] },
        { h: "7. International transfers", p: ["[Describe transfers outside the EU/EEA and the safeguards used, e.g. EU Standard Contractual Clauses or adequacy decisions.]"] },
        { h: "8. Retention", p: ["Uploaded images are deleted automatically after a configurable period (default: [number] days). Account data is kept while your account exists. Invoices are retained as required by law ([period])."] },
        { h: "9. Your rights", p: ["You have the right of access, rectification, erasure, restriction, data portability and objection (Art. 15–21 GDPR), and the right to withdraw consent. You may lodge a complaint with a supervisory authority: [competent supervisory authority]."] },
        { h: "10. Cookies and local storage", p: ["We use strictly necessary storage (e.g. session cookies, your cookie choice). Analytics run only after your consent."] },
        { h: "11. Changes", p: ["We may update this policy. The current version is always available on this page."] },
      ],
    },
    terms: {
      metaTitle: "Terms of service",
      title: "Terms of service",
      sections: [
        { h: "1. Scope", p: ["These terms govern the use of the service provided by [Company name], [Address] (“we”)."] },
        { h: "2. The service", p: ["The service analyzes screenshots of sports matches with AI and returns a structured, informational analysis.", "AI analysis is informational and does not guarantee any outcome. It is not financial, betting or investment advice. You are solely responsible for any decisions you make."] },
        { h: "3. Account", p: ["You must provide accurate information and keep your credentials confidential. Minimum age: [age]."] },
        { h: "4. Plans, usage limits and payment", p: ["Each plan includes a monthly number of analyses. Paid plans are billed in advance per billing period via [Payment provider]. Prices: as shown on the pricing page at the time of purchase."] },
        { h: "5. Cancellation", p: ["You can cancel a subscription at any time, effective at the end of the current billing period. [Statutory right of withdrawal for consumers, if applicable.]"] },
        { h: "6. Acceptable use", p: ["You may only upload content you have the right to use. No unlawful content, no automated abuse, no attempts to circumvent limits."] },
        { h: "7. Availability", p: ["We aim for high availability but do not guarantee uninterrupted service. AI results may be incomplete or inaccurate."] },
        { h: "8. Liability", p: ["[Liability clause — to be drafted by a lawyer for the applicable jurisdiction.]"] },
        { h: "9. Governing law", p: ["[Governing law and place of jurisdiction.]"] },
        { h: "10. Changes to these terms", p: ["[Procedure for notifying users of changes.]"] },
      ],
    },
    imprint: {
      metaTitle: "Imprint",
      title: "Imprint",
      sections: [
        { h: "Provider", p: ["[Company name]", "[Street and number]", "[Postcode, City]", "[Country]"] },
        { h: "Represented by", p: ["[Name of managing director / owner]"] },
        { h: "Contact", p: ["Email: [contact email]", "Phone: [phone number]"] },
        { h: "Register entry", p: ["[Commercial register, court, registration number — if applicable]"] },
        { h: "VAT ID", p: ["[VAT identification number — if applicable]"] },
        { h: "Responsible for content", p: ["[Name, address — if required]"] },
        { h: "EU dispute resolution", p: ["[Information on online dispute resolution / consumer arbitration — if applicable.]"] },
      ],
    },
  },
} as const;
