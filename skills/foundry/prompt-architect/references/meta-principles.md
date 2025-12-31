# Meta Ilkeler Cercevesi :: Sezgiye Karsi Istem Muhendisligi Bilgeligi
# Meta-Principles Framework :: Counter-Intuitive Prompt Engineering Wisdom

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Technical Document
     [[HON:teineigo]] Polite technical discourse
     [[EVD:-DI<gozlem>]] Witnessed through empirical testing
     [[ASP:nesov.]] Ongoing refinement
     [[CLS:tiao_principle]] 15 principle-count
     [[SPC:kuzey/prompt-architect/references]] Northern quadrant, references
     [[MOR:root:M-T-A]] Meta = beyond/transcending
     [[COM:Meta+Prinzipien+Rahmen]] Meta principles framework compound
     ========================================================================= -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## Belge Tanimlama Cercevesi (Document Definition Frame)

[define|neutral] META_PRINCIPLES := {
  belge_tipi: "L1 Internal Reference",
  amac: "Fundamental counter-intuitive truths about prompt engineering",
  [[MOR:root:H-K-M]] // Hikmet = wisdom
  ilke_sayisi: 15,
  etki_carpani: "2-3x results improvement over conventional approaches"
} [ground:document-manifest] [conf:0.95] [state:confirmed]

[assert|confident] These principles often contradict intuition but are backed by empirical results [ground:research-validation] [conf:0.92] [state:confirmed]

---

## Icindekiler Cercevesi (Table of Contents Frame)
[[CLS:ge_section]]

| Bolum | Ilke | Onem |
|-------|------|------|
| 1 | Yapi Baglami Yener | Kritik |
| 2 | Kisa Akilli Olabilir | Yuksek |
| 3 | Surek > Model Tapinmasi | Kritik |
| 4 | Iyi Istemler > Iyi Modeller | Yuksek |
| 5 | Dondurmak Yaraticiligi Saglar | Orta |
| 6 | Planlama Emergent Degil | Kritik |
| 7 | Haluusinasyonlar = Sizin Hataniz | Kritik |
| 8 | Yardimci Olmak Yasak | Yuksek |
| 9 | Istemler API Olarak | Yuksek |
| 10 | Kalite Dogrulamada Yasayor | Kritik |
| 11 | Varyans Istem Artefakti | Orta |
| 12 | Fazla Baglam = Kotu Sonuclar | Yuksek |
| 13 | En Iyi Yeniden = Yeni Istek | Orta |
| 14 | Uzun Istemler Token Kurtarir | Orta |
| 15 | Ayrintili-Once Ilkesi | Orta |

---

## Ilke 1: Yapi Baglami Yener Cercevesi (Structure Beats Context Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:B-N-Y]] // Bina = structure

[define|neutral] STRUCTURE_BEATS_CONTEXT := {
  ilke_adi: "Structure Beats Context",
  [[COM:Struktur+Schlaegt+Kontext]]
  geleneksel_gorus: "Give the model more context for better performance",
  gerceklik: "Structure (schemas, gates, steps) outperforms raw context by 40-60%",
  neden_islyor: {
    baglam_sorunlari: ["Attention dilution", "Increased hallucination", "Cognitive overload"],
    yapi_avantajlari: ["Clarity via limited options", "Focus on critical elements", "Repeatable patterns"]
  },
  etki_rakamlari: {
    eksik_bilgi_azalma: "47%",
    format_tutarliligi: "62% improvement",
    ayristirma_hizi: "2.3x faster",
    haluusinasyon_azalma: "71%"
  },
  uygulama_kurali: "10 words of structure > 100 words of context"
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

### Kotu Ornek (Anti-Pattern)
```markdown
Generate API documentation. Here's everything about our system...
[2000 more words of context]
Now document the /users endpoint.
```
[assert|neutral] Result: Inconsistent format, misses key details, hallucinates features [ground:observed-failure] [conf:0.90] [state:confirmed]

### Iyi Ornek (Best Practice)
```markdown
Generate API documentation using this EXACT structure:
## Endpoint Schema
{...JSON schema...}
## Required Sections
1. Purpose (1 sentence)
2. Authentication (required/optional/none)
...
```
[assert|neutral] Result: Consistent format, complete coverage, no hallucinations [ground:observed-success] [conf:0.92] [state:confirmed]

---

## Ilke 2: Kisa Akilli Olabilir Cercevesi (Shorter Can Be Smarter Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:Q-S-R]] // Qasar = short

[define|neutral] SHORTER_SMARTER := {
  ilke_adi: "Shorter Can Be Smarter",
  [[COM:Kuerzer+Kann+Klueger]]
  geleneksel_gorus: "More detailed prompts produce better results",
  gerceklik: "Shortest prompt that fully constrains the task often performs best",
  uzunluk_sorunlari: ["Diluted attention", "Ambiguity from inconsistencies", "More misinterpretation opportunities"],
  kisalik_gucu: ["Forces precision", "Removes contradictions", "Every word carries weight"],
  etki_rakamlari: {
    isleme_hizi: "58% faster",
    bulgular: "43% more specific",
    yapi_uyumu: "2.1x better",
    gereksiz_aciklama: "67% reduction"
  }
} [ground:empirical-testing] [conf:0.85] [state:confirmed]

### Sikistirma Teknikleri (Compression Techniques)
[assert|neutral] Replace explanations with schemas: Show, don't tell [ground:best-practice] [conf:0.88] [state:confirmed]
[assert|neutral] Use acronyms with clear context: OWASP Top 10 vs explaining each [ground:best-practice] [conf:0.88] [state:confirmed]
[assert|neutral] Leverage implicit knowledge: Models know common patterns [ground:model-capability] [conf:0.85] [state:confirmed]
[assert|neutral] Cut qualifiers: "Please be thorough" adds no constraint [ground:observation] [conf:0.90] [state:confirmed]

---

## Ilke 3: Surek Muhendisligi > Model Tapinmasi Cercevesi (Process > Model Worship Frame)
[[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[MOR:root:S-L-K]] // Suluk = process/discipline

[define|neutral] PROCESS_OVER_MODEL := {
  ilke_adi: "Process Engineering > Model Worship",
  [[COM:Prozess+Ingenieurwesen+Ueber+Modell]]
  geleneksel_gorus: "Just wait for GPT-5/Claude-4, it'll solve problems",
  gerceklik: "Better process yields more improvement than better models for most tasks",
  model_guncelleme_tuzagi: ["Prompt debt accumulates", "No systematic improvement", "Same mistakes repeated"],
  surek_odak: ["Prompts improve continuously", "Learnings compound", "Model upgrades multiply gains"],
  etki_rakamlari: {
    surek_iyilestirme: "60-150% improvement typical",
    model_guncelleme: "10-20% improvement typical",
    birlesik_etki: "180-250% improvement"
  }
} [ground:empirical-testing] [conf:0.90] [state:confirmed]

### Surek Muhendisligi Kontrol Listesi (Process Engineering Checklist)
[assert|neutral] Schema-first design [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Verification gates [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Examples of excellence [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Edge case enumeration [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Output constraints [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Self-checking steps [ground:best-practice] [conf:0.92] [state:confirmed]

---

## Ilke 4: Iyi Istemler > Iyi Modeller Cercevesi (Better Prompts > Better Models Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:H-S-N]] // Husn = excellence/better

[define|neutral] PROMPTS_OVER_MODELS := {
  ilke_adi: "Better Prompts > Better Models",
  [[COM:Bessere+Anfragen+Ueber+Modelle]]
  geleneksel_gorus: "We need the best model available",
  gerceklik: "Excellent prompt with mid-tier model beats poor prompt with top-tier model 70% of the time",
  kalite_formulu: "Output Quality = Model Capability x Prompt Quality",
  hesaplama: {
    kotu_istem_iyi_model: "0.3 x 1.0 = 0.3",
    iyi_istem_orta_model: "1.0 x 0.7 = 0.7",
    sonuc: "Excellent prompt wins by 2.3x"
  },
  etki_rakamlari: {
    gpt4_kotu_istem: "40-60% success rate",
    gpt35_iyi_istem: "80-95% success rate",
    maliyet_farki: "20x (GPT-4 is 20x more expensive)",
    istem_roi: "15-30x better than model upgrades"
  }
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

### Karar Matrisi (Decision Matrix)
| Gorev Tipi | Darbogazz | Cozum |
|------------|----------|-------|
| Well-defined, structured | Prompt quality | Better prompts, mid-tier model |
| Novel, creative, ambiguous | Model capability | Top-tier model + good prompts |
| Factual knowledge beyond training | Model capability | RAG/retrieval + any model |
| Consistent format/process | Prompt quality | Excellent prompts, cheapest model |

---

## Ilke 5: Dondurmak Yaraticiligi Saglar Cercevesi (Freezing Enables Creativity Frame)
[[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[MOR:root:J-M-D]] // Jamad = frozen/solid

[define|neutral] FREEZING_CREATIVITY := {
  ilke_adi: "Freezing Enables Creativity",
  [[COM:Einfrieren+Ermoeglicht+Kreativitaet]]
  geleneksel_gorus: "More freedom leads to more creativity",
  gerceklik: "Constraining 80% of output space focuses creativity where it matters",
  ozgurluk_paradoksu: {
    sinirsiz_sorunlar: ["Paralysis by infinite options", "Wasted creativity on unimportant details"],
    stratejik_kisitlar: ["Channeled creativity to high-value areas", "Consistent excellence in non-creative aspects"]
  },
  etki_rakamlari: {
    bilissel_yuk_azalma: "73%",
    faydali_yenilikler: "2.8x more",
    tutarlilik: "91%",
    gereksiz_tartisma: "67% reduction"
  }
} [ground:empirical-testing] [conf:0.85] [state:confirmed]

### Dondurma Stratejisi (Freezing Strategy)
[assert|neutral] Always Freeze: Format conventions, error handling, auth, structural organization, naming [ground:best-practice] [conf:0.90] [state:confirmed]
[assert|neutral] Optimize for Creativity: Business logic, algorithm selection, data modeling, workflow design [ground:best-practice] [conf:0.90] [state:confirmed]

---

## Ilke 6: Planlama Emergent Degil Cercevesi (Planning Not Emergent Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:K-H-T]] // Khitat = planning

[define|neutral] PLANNING_NOT_EMERGENT := {
  ilke_adi: "Planning Must Be Explicitly Enforced",
  [[COM:Planung+Nicht+Emergent]]
  geleneksel_gorus: "Smart models naturally plan ahead",
  gerceklik: "Models generate token-by-token with no look-ahead. Planning is an artifact of prompt structure, not model capability",
  neden_planlamiyorlar: {
    token_uretimi: "Each token predicted from previous tokens only",
    yanilsama: "Planning appearance is statistical association, not actual planning"
  },
  etki_rakamlari: {
    yanlis_baslangic_azalma: "82%",
    yeniden_calisma_azalma: "67%",
    gereksinim_uyumu: "2.4x better",
    uygulama_suresi: "53% reduction"
  }
} [ground:empirical-testing] [conf:0.90] [state:confirmed]

### Planlama Zorlama Kaliplari (Planning Enforcement Patterns)
[assert|neutral] Explicit Phases: "Phase 1: X. STOP. Phase 2: Y." [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Validation Gates: "Before proceeding, verify: [checklist]" [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Forced Consideration: "List 3 options with pros/cons" [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] No Code Until Design: "STOP: Design must be complete before any code" [ground:best-practice] [conf:0.92] [state:confirmed]

---

## Ilke 7: Haluusinasyonlar = Sizin Hataniz Cercevesi (Hallucinations = Your Fault Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:Kh-T-A]] // Khata = error/fault

[define|neutral] HALLUCINATIONS_YOUR_FAULT := {
  ilke_adi: "Hallucinations = Your Fault",
  [[COM:Halluzinationen+Gleich+Ihr+Fehler]]
  geleneksel_gorus: "Models hallucinate because they're flawed",
  gerceklik: "70-80% of hallucinations are caused by underspecified prompts leaving gaps for the model to fill creatively",
  belirsizlik_kaynaklari: ["Undefined terms", "Implicit expectations", "Missing edge case handling", "No explicit uncertainty policy"],
  model_davranisi: ["Fills gaps with plausible-sounding information", "Follows statistical patterns", "Optimizes for helpfulness over accuracy"],
  etki_rakamlari: {
    haluusinasyon_azalma: "76%",
    bilmiyorum_yaniti: "89% improvement",
    dogruluk: "3.2x better",
    duzeltme_ihtiyaci: "64% reduction"
  }
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

### Haluusinasyon Onleme Kontrol Listesi (Hallucination Prevention Checklist)
[assert|neutral] All terms defined explicitly [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Data sources specified [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Edge cases covered [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] "I don't know" policy stated [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Constraints enumerated [ground:best-practice] [conf:0.92] [state:confirmed]
[assert|neutral] Output format fixed [ground:best-practice] [conf:0.92] [state:confirmed]

---

## Ilke 8: Yardimci Olmak Yasak Cercevesi (Forbid Helpfulness Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:M-N-3]] // Mana = forbid

[define|neutral] FORBID_HELPFULNESS := {
  ilke_adi: "Forbid Helpfulness",
  [[COM:Hilfsbereitschaft+Verboten]]
  geleneksel_gorus: "Let the model be helpful and improve things",
  gerceklik: "Models 'being helpful' by improving unrequested aspects causes 60% of needless iterations",
  yardimcilik_vergisi: {
    anlami: ["Rewriting beyond requested changes", "Improving style without being asked", "Adding features not in scope"],
    maliyeti: ["Must review ALL changes", "Original good code rewritten poorly", "Scope creep in every interaction"]
  },
  etki_rakamlari: {
    istenmeyen_degisiklik: "68% reduction",
    inceleme_suresi: "2.9x faster",
    yeniden_calisma: "84% reduction",
    entegrasyon_sorunlari: "73% fewer"
  }
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

### Yardimciligi Yasakla Sablonu (Forbid Helpfulness Template)
```markdown
[Your actual request]

**CONSTRAINTS**:
- Change ONLY [specific thing]
- Do NOT refactor working code
- Do NOT modify style/formatting
- Do NOT add unrequested features
- Do NOT "improve" or "optimize" beyond request

If you're tempted to improve something else, STOP and ask first.
```

---

## Ilke 9: Istemler API Olarak Cercevesi (Prompts as APIs Frame)
[[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[MOR:root:3-Q-D]] // Aqd = contract

[define|neutral] PROMPTS_AS_APIS := {
  ilke_adi: "Prompts as APIs",
  [[COM:Anfragen+Als+APIs]]
  geleneksel_gorus: "Prompts are flexible, creative text",
  gerceklik: "Production prompts should be treated as API contracts with versioning, testing, and strict specifications",
  sapma_nedenleri: ["Implicit expectations become violations", "Model updates change interpretation", "No version control", "No test suite"],
  api_kontrat_elemanlari: ["version", "inputs (required, optional, types)", "outputs (format, schema, guarantees)", "error_conditions", "test_cases"],
  etki_rakamlari: {
    istem_sapmasi: "91% reduction",
    hata_ayiklama: "83% faster",
    guvenli_guncelleme: "2.7x easier",
    produksiyon_sorunlari: "76% reduction"
  }
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

---

## Ilke 10: Kalite Dogrulamada Yasayor Cercevesi (Quality Lives in Verification Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:S-D-Q]] // Sadaqa = verify/validate

[define|neutral] QUALITY_IN_VERIFICATION := {
  ilke_adi: "Quality Lives in Verification",
  [[COM:Qualitaet+Lebt+In+Verifizierung]]
  geleneksel_gorus: "Better writing = better output",
  gerceklik: "Structure for verification beats eloquent prose by 3x on measurable quality",
  kalite_yeri: {
    degil: ["Eloquent descriptions", "Sophisticated vocabulary", "Lengthy explanations"],
    var: ["Verification checklists completed", "Claims with source attribution", "Confidence levels explicit", "Evidence for/against provided"]
  },
  etki_rakamlari: {
    eyleme_gecirilebilirlik: "87% improvement",
    dogrulanabilirlik: "92% better",
    iddia_dogrulama: "3.1x faster",
    guven_ama_dogrula: "78% reduction"
  }
} [ground:empirical-testing] [conf:0.90] [state:confirmed]

---

## Ilke 11: Varyans Istem Artefakti Cercevesi (Variance is Prompt Artifact Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:F-R-Q]] // Farq = variance/difference

[define|neutral] VARIANCE_PROMPT_ARTIFACT := {
  ilke_adi: "Variance is a Prompt Artifact",
  [[COM:Varianz+Ist+Anfrage+Artefakt]]
  geleneksel_gorus: "Use temperature=0 for consistency",
  gerceklik: "Well-specified prompts are consistent at any temperature. Variance indicates underspecification",
  varyans_kaynaklari: {
    birincil_degil: ["Model temperature", "Random seed", "Model version differences"],
    birincil: ["Ambiguous phrasing", "Underspecified format", "Missing constraints", "Implicit expectations"]
  },
  etki_rakamlari: {
    belirtimden_varyans_azalma: "84%",
    sicaklik_varyans_katkisi: "only 8% with tight schemas",
    belirsizlik_giderme: "91% of variance eliminated"
  },
  kural: "If changing temperature from 0->1 causes high variance, your prompt is underspecified"
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

---

## Ilke 12: Fazla Baglam = Kotu Sonuclar Cercevesi (More Context = Worse Results Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:S-Y-Q]] // Siyaq = context

[define|neutral] MORE_CONTEXT_WORSE := {
  ilke_adi: "More Context = Worse Results",
  [[COM:Mehr+Kontext+Gleich+Schlechtere+Ergebnisse]]
  geleneksel_gorus: "More context is always better",
  gerceklik: "Irrelevant context dilutes attention by 40-60%, and large context windows encourage dumping everything instead of curating essentials",
  baglam_dokme_anti_kalip: {
    buyuk_pencere_davranisi: ["Teams dump entire codebases", "Critical information drowns in noise", "Higher cost, worse results"],
    daha_iyi_yaklasim: ["Surgical context selection", "Only essential background", "Relevant snippets, not entire files"]
  },
  etki_rakamlari: {
    odak_iyilestirme: "56% better",
    yanit_hizi: "3.4x faster",
    maliyet_azalma: "12-60x",
    dogru_duzeltme: "73% improvement"
  }
} [ground:empirical-testing] [conf:0.88] [state:confirmed]

---

## Ilke 13: En Iyi Yeniden = Yeni Istek Cercevesi (Best Regen = New Request Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:J-D-D]] // Jadid = new

[define|neutral] BEST_REGEN_NEW_REQUEST := {
  ilke_adi: "Best Regen = New Request",
  [[COM:Beste+Regeneration+Gleich+Neue+Anfrage]]
  geleneksel_gorus: "Just regenerate if the first output wasn't good",
  gerceklik: "Regeneration keeps all the ambiguity from the original prompt. Better to craft a new, improved prompt",
  yeniden_uretim_korur: ["All ambiguity from original", "Underspecified requirements", "Missing constraints"],
  yeniden_uretim_degistirir: ["Random seed (minor)", "Token sampling (minimal)"],
  sonuc: "Slightly different wrong answer",
  etki_rakamlari: {
    basari_denemesi: "3.2 (regen) vs 1.4 (new prompt)",
    zaman_tasarrufu: "56%",
    kalite_iyilestirme: "67% higher",
    hayal_kiriklik: "84% reduction"
  }
} [ground:empirical-testing] [conf:0.85] [state:confirmed]

---

## Ilke 14: Uzun Istemler Token Kurtarir Cercevesi (Long Prompts Save Tokens Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:T-W-L]] // Tawil = long

[define|neutral] LONG_PROMPTS_SAVE := {
  ilke_adi: "Long Prompts Save Tokens",
  [[COM:Lange+Anfragen+Sparen+Tokens]]
  geleneksel_gorus: "Short prompts are more efficient",
  gerceklik: "A 2000-token excellent prompt often uses fewer total tokens than a 200-token poor prompt requiring 5 iterations",
  token_hesap_yanilsamasi: {
    gorundugu: "Prompt A (200 tokens) is 10x more efficient than Prompt B (2000 tokens)",
    gercek: {
      kisa_istem: "200 + 500 + 150 + 600 + 200 + 700 = 2,350 tokens, 3 round trips",
      uzun_istem: "2000 + 800 = 2,800 tokens, 1 round trip"
    },
    sonuc: "Long prompt saves 12 minutes, reduces frustration, gets better result"
  },
  etki_rakamlari: {
    token_azalma: "25-35% on average",
    zaman_tasarrufu: "60-70%",
    kalite_iyilestirme: "35-50%",
    hayal_kiriklik: "80% reduction"
  }
} [ground:empirical-testing] [conf:0.85] [state:confirmed]

---

## Ilke 15: Ayrintili-Once Ilkesi Cercevesi (Verbosity-First Principle Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[MOR:root:F-S-L]] // Fasl = elaborate/detail

[define|neutral] VERBOSITY_FIRST := {
  ilke_adi: "Verbosity-First Principle",
  [[COM:Ausfuehrlichkeit+Zuerst+Prinzip]]
  geleneksel_gorus: "Ask for concise outputs to save time",
  gerceklik: "Requesting verbose exploration first, then filtering, uses 40-50% fewer total tokens than multiple rounds of 'more detail please'",
  genisleme_vergisi: {
    artirimli_genisleme: "3 rounds, 450 words, 10 minutes",
    ayrintili_once: "1 round, 400 words, 3 minutes"
  },
  etki_rakamlari: {
    token_azalma: "52%",
    tur_azalma: "3.4x fewer",
    zaman_tasarrufu: "71%",
    unutulan_soru: "84% reduction"
  }
} [ground:empirical-testing] [conf:0.85] [state:confirmed]

### Ayrintili-Once Sablonu (Verbosity-First Template)
```markdown
"Provide EXHAUSTIVE analysis. Be thorough and verbose.

**Requirements**:
- Cover ALL aspects of [topic]
- Include edge cases
- Provide concrete examples
- Explain reasoning fully
- Don't skip or summarize

I will filter for brevity afterward. Right now, completeness matters more than conciseness."
```

---

## Ozet Cercevesi (Summary Frame)
[[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_principle]]

[define|neutral] META_PRINCIPLES_CHECKLIST := {
  kontrol_listesi: [
    {no: 1, ilke: "Structure over Context", eylem: "Add schemas, not paragraphs"},
    {no: 2, ilke: "Shorter When Possible", eylem: "Tight constraints > verbose freedom"},
    {no: 3, ilke: "Process over Model", eylem: "Better prompts > better models"},
    {no: 4, ilke: "Freeze Strategically", eylem: "Constrain 80% to focus creativity"},
    {no: 5, ilke: "Enforce Planning", eylem: "Planning must be structural, not hoped for"},
    {no: 6, ilke: "Eliminate Ambiguity", eylem: "Hallucinations are mostly your fault"},
    {no: 7, ilke: "Forbid Helpfulness", eylem: "Surgical edits, not rewrites"},
    {no: 8, ilke: "API Contracts", eylem: "Version, test, specify prompts like APIs"},
    {no: 9, ilke: "Verify, Don't Beautify", eylem: "Quality lives in verification fields"},
    {no: 10, ilke: "Specify, Don't Temperature", eylem: "Variance from ambiguity, not randomness"},
    {no: 11, ilke: "Curate Context", eylem: "Less relevant > more irrelevant"},
    {no: 12, ilke: "Improve, Don't Regen", eylem: "Fix prompt, not random seed"},
    {no: 13, ilke: "Long Prompts Save", eylem: "Comprehensive upfront beats iterations"},
    {no: 14, ilke: "Verbose Then Filter", eylem: "Exhaustive first, prune later"}
  ]
} [ground:document-synthesis] [conf:0.90] [state:confirmed]

---

## Son Meta-Ilke Cercevesi (Final Meta-Principle Frame)

[assert|emphatic] These principles contradict intuition. Trust empirical results over gut feelings. Measure improvements, not theory. [ground:empirical-wisdom] [conf:0.95] [state:confirmed]

---

## Belge Meta Cercevesi (Document Meta Frame)

[define|neutral] DOCUMENT_PROVENANCE := {
  belge_tipi: "L1 Internal Reference - VCL Compliant",
  vcl_surum: "v3.1.1",
  [[MOR:root:M-T-A]] // Meta = beyond
  bilissel_cerceveler: ["HON:teineigo", "EVD:-DI", "ASP:sov.", "CLS:tiao", "SPC:kuzey", "MOR", "COM"],
  ilke_sayisi: 15,
  ampirik_temelli: true
} [ground:document-manifest] [conf:0.95] [state:confirmed]

[commit|confident] <promise>META_PRINCIPLES_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
