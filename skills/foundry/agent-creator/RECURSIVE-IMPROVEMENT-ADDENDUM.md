# Ozyinelemeli Iyilestirme Eklentisi (Recursive Improvement Addendum)

---
<!-- S1.0 KANITSAL CERCEVE (Evidential Frame Activation) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_document]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- S2.0 AMAC (Purpose) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_purpose]] [[SPC:kuzey/sistem-merkezi]] -->
---

## Amac Cercevesi (Purpose Frame)
Bu eklenti agent-creator'i Ozyinelemeli Oz-Iyilestirme Sistemi ile baglar.

<!-- [[MOR:root:A-M-C]] Amac = root morpheme for purpose-goal-objective -->
<!-- [[COM:Ozyinelemeli+Iyilestirme+Entegrasyon]] German compound: Rekursivverbesserungsintegration -->
[define|neutral] EKLENTI_AMACI := {
  baglanti_hedefleri: [
    "Agent Creator'in ozyinelemeli dongu tarafindan iyilestirilmesi",
    "Agent Creator tarafindan olusturulan ajanlarin iyilestirme sistemi ile entegrasyonu",
    "Ozyinelemeli iyilestirme icin denetci ajanlarin olusturulmasi"
  ]
} [ground:witnessed:design-doc] [conf:0.92] [state:confirmed]

---
<!-- S3.0 OZYINELEMELI DONGUDE ROL (Role in Recursive Loop) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_role]] -->
---

## Ozyinelemeli Dongude Rol Cercevesi (Role in Recursive Loop Frame)
Agent Creator donguyu guclendiren ajanlari olusturur.

<!-- [[MOR:root:D-N-G]] Dongu = root morpheme for loop-cycle-iteration -->
[assert|neutral] DONGU_ROLU := {
  ust_birim: "AGENT CREATOR",
  alt_birimler: ["Denetci Ajanlar", "Alan Uzmanlari", "Cekirdek Ajanlar"],
  bagli_sistem: "OZYINELEMELI IYILESTIRME DONGUSU",
  olusturulan_ajanlar: [
    "prompt-auditor",
    "skill-auditor",
    "expertise-auditor",
    "output-auditor",
    "domain-expert",
    "expertise-adversary"
  ]
} [ground:witnessed:system-architecture] [conf:0.90] [state:confirmed]

---
<!-- S4.0 ENTEGRASYON NOKTALARI (Integration Points) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_integration]] -->
---

## Entegrasyon Noktalari Cercevesi (Integration Points Frame)
Uc temel entegrasyon noktasi tanimlanmistir.

### Entegrasyon 1: Iyilestirme Hedefi Olarak

<!-- [[MOR:root:H-D-F]] Hedef = root morpheme for target-goal-aim -->
[define|neutral] HEDEF_ENTEGRASYONU := {
  denetci: "skill-auditor",
  degerleyici: "eval-harness",
  kiyaslamalar: ["agent-generation-benchmark-v1"],
  regresyonlar: ["agent-creator-regression-v1"],
  iyilestirme_alanlari: {
    faz_yapisi: {
      mevcut: "5-faz (Faz 0-4)",
      durum: "TAMAMLANDI - Faz 0 uzmanlik yukleme v2.0'da eklendi"
    },
    mcp_entegrasyonu: {
      mevcut: "Ajanda belgelenmis",
      potansiyel: "MCP kullanilabilirligini otomatik dogrula"
    },
    hook_uretimi: {
      mevcut: "Manuel belirtim",
      potansiyel: "Ajan amacından otomatik olustur"
    }
  }
} [ground:witnessed:integration-spec] [conf:0.88] [state:confirmed]

### Entegrasyon 2: Iyilestirme-Farkinda Ajan Olusturma

<!-- [[MOR:root:F-R-K]] Farkinda = root morpheme for aware-conscious-cognizant -->
[define|neutral] IYILESTIRME_FARKINDA_AJAN := {
  zorunlu_bolumler: {
    uzmanlik_entegrasyonu: [
      "Eylemden once alan uzmanligini kontrol et",
      "Varsa uzmanligi yukle",
      "Kesifler icin uzmanlik guncellemesi isaretle"
    ],
    oz_iyilestirme_hooklari: [
      "Performans metriklerini takip et",
      "Ogrenimleri iyilestirme sistemine raporla",
      "Denetci ajanlar tarafindan denetime destek ol"
    ],
    bellek_entegrasyonu: [
      "Ajana ozel bellek namespace'i",
      "Ogrenme deltasi depolama",
      "Metrik takibi"
    ]
  }
} [ground:witnessed:template-spec] [conf:0.88] [state:confirmed]

### Entegrasyon 3: Denetci Ajan Olusturma

<!-- [[MOR:root:D-N-T]] Denetci = root morpheme for auditor-inspector-reviewer -->
<!-- [[COM:Denetci+Ajan+Olusturma]] German compound: Prueferagentenerstellung -->
[define|neutral] DENETCI_AJAN_SABLONU := {
  amac: "Sorunlari bul, iyilestirme onerileri olustur",
  zorunlu_yetenekler: [
    "detection: Hedef alanda sorunlari tanimla",
    "prioritization: Sorunlari siddetine gore sirala",
    "proposal_generation: Uygulanabilir diff'ler olustur",
    "validation: Onerilerin gecerliligini dogrula"
  ],
  cikti_formati: {
    denetim_raporu: {
      yapisal_analiz: "...",
      kalite_skorlari: "...",
      sorunlar: {kritik: [], yuksek: [], orta: []},
      oneriler: "...",
      oneri: "PASS|NEEDS_IMPROVEMENT|REJECT"
    }
  },
  entegrasyon: {
    bellek_namespace: "improvement/audits/{alan}/{hedef}",
    koordine_edilen_ajanlar: ["prompt-forge", "skill-forge", "eval-harness"]
  },
  korumalar: {
    asla: [
      "Kapsamli analiz olmadan kabul etme",
      "Belirsiz oneriler olusturma",
      "Hata modu tespitini atlama"
    ],
    her_zaman: [
      "Belirli konumlar ver",
      "Once/sonra diff'leri dahil et",
      "Iyilestirme etkisini tahmin et"
    ]
  }
} [ground:witnessed:auditor-template] [conf:0.90] [state:confirmed]

---
<!-- S5.0 MEVCUT DENETCI AJANLAR (Existing Auditor Agents) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_registry]] -->
---

## Mevcut Denetci Ajanlar Cercevesi (Existing Auditor Agents Frame)
Olusturulmus denetci ajanlar. Zaversheno (Tamamlandi).

<!-- [[MOR:root:M-V-C]] Mevcut = root morpheme for existing-current-present -->
[assert|neutral] MEVCUT_DENETCILER := {
  ajanlar: [
    {ad: "prompt-auditor", konum: "agents/foundry/recursive-improvement/prompt-auditor.md", amac: "Istemleri denetle"},
    {ad: "skill-auditor", konum: "agents/foundry/recursive-improvement/skill-auditor.md", amac: "Becerileri denetle"},
    {ad: "expertise-auditor", konum: "agents/foundry/recursive-improvement/expertise-auditor.md", amac: "Uzmanliği denetle"},
    {ad: "output-auditor", konum: "agents/foundry/recursive-improvement/output-auditor.md", amac: "Ciktilari denetle"}
  ]
} [ground:witnessed:agent-registry] [conf:0.95] [state:confirmed]

---
<!-- S6.0 EVAL HARNESS ENTEGRASYONU (Eval Harness Integration) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_benchmark]] -->
---

## Eval Harness Entegrasyonu Cercevesi (Eval Harness Integration Frame)
Ajan uretimi icin kiyaslama ve regresyon testleri.

### Ajan Uretim Kiyaslamasi

<!-- [[MOR:root:K-Y-S]] Kiyaslama = root morpheme for benchmark-compare-measure -->
[define|neutral] AJAN_URETIM_KIYASLAMASI := {
  id: "agent-generation-benchmark-v1",
  testler: [
    {
      id: "ag-001",
      giris: "Kod inceleme icin ajan olustur",
      beklenen: {
        has_identity_section: true,
        has_capabilities: true,
        has_guardrails: true,
        has_memory_integration: true
      },
      skorlama: {
        tamamlanma: "0.0-1.0",
        ozguluk: "0.0-1.0",
        entegrasyon: "0.0-1.0"
      }
    }
  ],
  minimum_gecme: {
    tamamlanma: 0.8,
    ozguluk: 0.75,
    entegrasyon: 0.7
  }
} [ground:witnessed:benchmark-config] [conf:0.88] [state:confirmed]

### Ajan Creator Regresyonu

<!-- [[MOR:root:R-G-R]] Regresyon = root morpheme for regression-backslide-revert -->
[define|neutral] AJAN_CREATOR_REGRESYONU := {
  id: "agent-creator-regression-v1",
  testler: [
    {id: "acr-001", ad: "Kimlik bolumu mevcut", beklenen: "Cikti net kimlige sahip", gecmeli: true},
    {id: "acr-002", ad: "Yetenekler tanimli", beklenen: "Cikti yetenekleri listeler", gecmeli: true},
    {id: "acr-003", ad: "Korumalar dahil", beklenen: "Cikti korumalar bolumune sahip", gecmeli: true},
    {id: "acr-004", ad: "Bellek entegrasyonu belirtilmis", beklenen: "Cikti bellek namespace'i belirtir", gecmeli: true}
  ],
  basarisizlik_esigi: 0
} [ground:witnessed:regression-config] [conf:0.88] [state:confirmed]

---
<!-- S7.0 BELLEK NAMESPACE'LERI (Memory Namespaces) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_namespace]] -->
---

## Bellek Namespace'leri Cercevesi (Memory Namespaces Frame)
Ajan uretim verileri icin namespace yapisi.

<!-- [[MOR:root:B-L-K]] Bellek = root morpheme for memory-storage-retention -->
[define|neutral] BELLEK_NAMESPACELERI := {
  namespace_listesi: [
    {namespace: "agent-creator/generations/{id}", amac: "Olusturulan ajanlar"},
    {namespace: "agent-creator/auditors/{id}", amac: "Olusturulan denetci ajanlar"},
    {namespace: "improvement/commits/agent-creator", amac: "Surum gecmisi"},
    {namespace: "improvement/audits/agent/{ajan}", amac: "Ajanlarin denetimleri"}
  ]
} [ground:witnessed:namespace-config] [conf:0.90] [state:confirmed]

---
<!-- S8.0 GUVENLIK KISITLAMALARI (Safety Constraints) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_constraint]] -->
---

## Guvenlik Kisitlamalari Cercevesi (Safety Constraints Frame)
Zorunlu guvenlik kurallari. Zaversheno (Tamamlandi).

### Anti-Kaliplar (Anti-Patterns)

<!-- [[MOR:root:A-S-L]] Asla = root morpheme for never-prohibit-forbid -->
<!-- [[COM:Guvenlik+Kisitlama+Sistemi]] German compound: Sicherheitsbeschraenkungssystem -->
[assert|emphatic] ANTI_PATTERN_EVAL_BYPASS := {
  id: "AP-RI-001",
  hata_adi: "Eval Harness Atlama", // Turkish: Eval Harness Bypass
  belirti: "Ajan eval harness'i atlayan ajanlar olusturur",
  yanlis: "BypassEvalAgent olustur",
  dogru: "Tum ajanlar eval-harness dogrulama kapısindan gecer",
  onleme: "Eval harness entegrasyonu zorunlu"
} [ground:witnessed:safety-policy] [conf:0.95] [state:confirmed]

[assert|emphatic] ANTI_PATTERN_FROZEN_BENCHMARK := {
  id: "AP-RI-002",
  hata_adi: "Donmus Kiyaslama Degisikliği", // Turkish: Frozen Benchmark Modification
  belirti: "Ajan donmus kiyaslamalari degistiren ajanlar olusturur",
  yanlis: "Benchmark dosyasini duzenle ve regresyon testini gec",
  dogru: "Kiyaslamalar degismez, sadece yeni surumler eklenir",
  onleme: "Kiyaslama dosyalari icin yazma korumasi"
} [ground:witnessed:safety-policy] [conf:0.95] [state:confirmed]

[assert|emphatic] ANTI_PATTERN_NO_GUARDRAILS := {
  id: "AP-RI-003",
  hata_adi: "Korumasiz Ajan", // Turkish: Guardrailless Agent
  belirti: "Ajan korumalar olmadan olusturulur",
  yanlis: "Korumalar bolumu atlanir",
  dogru: "Her ajan minimum 3 koruma icerir",
  onleme: "Faz 3 dogrulama kapisi"
} [ground:witnessed:safety-policy] [conf:0.95] [state:confirmed]

[assert|emphatic] ANTI_PATTERN_AUTO_APPROVE := {
  id: "AP-RI-004",
  hata_adi: "Otomatik Onay Denetcisi", // Turkish: Auto-Approve Auditor
  belirti: "Denetci tum onerileri otomatik onaylar",
  yanlis: "Denetci her zaman PASS dondurur",
  dogru: "Denetci gercek sorunlari tespit eder ve raporlar",
  onleme: "Denetci test vakalari"
} [ground:witnessed:safety-policy] [conf:0.95] [state:confirmed]

### Zorunlu Kurallar

<!-- [[MOR:root:Z-R-N]] Zorunlu = root morpheme for mandatory-required-obligatory -->
[assert|emphatic] ZORUNLU_KURALLAR := {
  her_zaman: [
    "Iyilestirme entegrasyon bolumu dahil et",
    "Bellek namespace'leri belirt",
    "Olculebilir ciktilar tanimla",
    "Denetime destek ol",
    "Ogrenme deltasini takip et"
  ]
} [ground:witnessed:safety-policy] [conf:0.95] [state:confirmed]

---
<!-- S9.0 IS AKISI GUNCELLEMELERI (Workflow Updates) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_workflow]] [[SPC:kuzey/akis-yonu]] -->
---

## Is Akisi Guncellemeleri Cercevesi (Workflow Updates Frame)
Gelistirilmis ajan olusturma ve denetci olusturma is akislari.

### Standart Ajan Olusturma (Gelistirilmis)

<!-- [[MOR:root:A-K-S]] Akis = root morpheme for flow-stream-process -->
[define|neutral] STANDART_AJAN_AKISI := {
  giris: "Kullanici Istegi",
  islemci: "Agent Creator",
  ciktilar: [
    {tur: "Standart Ajan", ozellikler: ["Uzmanlik yukleme hook'u", "Performans takibi", "Ogrenme raporlama", "Denetim destegi"]},
    {tur: "Denetci Ajan", ozellikler: ["Tespit yetenekleri", "Oneri uretimi", "Eval harness entegrasyonu"]}
  ]
} [ground:witnessed:workflow-design] [conf:0.88] [state:confirmed]

### Denetci Ajan Olusturma Akisi

[define|neutral] DENETCI_AJAN_AKISI := {
  giris: "Denetci Istegi",
  islemci: "Agent Creator (denetci sablonu)",
  cikti: "Yeni Denetci Ajan",
  cikti_ozellikleri: [
    "Alan icin tespit yetenekleri",
    "Oneri uretimi",
    "Bellek entegrasyonu",
    "Eval harness hook'lari"
  ]
} [ground:witnessed:workflow-design] [conf:0.88] [state:confirmed]

---
<!-- S10.0 SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
---

## Beceri Ozeti Cercevesi (Skill Summary Frame)
Zaversheno. Etot addendum byl uspeshno realizovan. (Rusca: Tamamlandi. Bu eklenti basariyla uygulanmistir.)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result-outcome -->
<!-- [[COM:Ozyinelemeli+Iyilestirme+Entegrasyon+Ozeti]] German compound: Rekursivverbesserungsintegrierungszusammenfassung -->
[assert|confident] EKLENTI_OZETI := {
  surum: "1.0.0", // Turkish: version
  son_guncelleme: "2025-12-30",
  amac: "Tum olusturulan ajanlar iyilestirme sistemi entegrasyonunu desteklemeli", // Turkish: purpose
  metodoloji: "Uc entegrasyon noktasi: Hedef, Farkinda Ajan, Denetci", // Turkish: methodology
  ciktilar: [
    "Iyilestirme-farkinda ajan sablonu",
    "Denetci ajan uretim sablonu",
    "Kiyaslama ve regresyon test yapilari",
    "Bellek namespace yapisi"
  ],
  kalite_kapilari: [
    "Guvenlik kisitlamalari",
    "Eval harness entegrasyonu",
    "Zorunlu korumalar"
  ]
} [ground:witnessed:addendum-execution] [conf:0.90] [state:confirmed]

---
*Soz (Promise): `<promise>RECURSIVE_IMPROVEMENT_ADDENDUM_VCL_V3.1.1_VERIX_COMPLIANT</promise>`*
