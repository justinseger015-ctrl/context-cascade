# Skill-Forge Bilissel Mimari Entegrasyonu (Cognitive Architecture Integration)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## S1 AMAC VE SURUM (Purpose and Version Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_item]] -->
<!-- [[MOR:root:M-M-R]] Mimari = root morpheme for architecture-structure-design -->
<!-- [[COM:Bilissel+Mimari+Entegrasyon]] German: Kognitive-Architektur-Integration -->

[define|neutral] ADDENDUM_META := {
  surum: "3.1.0", // version
  amac: "VERIX, VERILINGUA, DSPy, GlobalMOO entegrasyonu", // purpose
  hedef_beceri: "skill-forge", // target skill
  durum: "aktif" // status: active
} [ground:witnessed:version-header] [conf:0.95] [state:confirmed]

---

## S2 GENEL BAKIS CERCEVESI (Overview Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_principle]] -->
<!-- [[MOR:root:N-Z-R]] Nazar = root for view-observe-overview -->
<!-- [[SPC:kuzey]] Primary reference direction -->

[assert|neutral] OVERVIEW_STATEMENT := {
  tanim: "Skill-forge icin bilissel mimari entegrasyonu", // definition
  yetenekler: [
    "VERIX uyumlu beceri uretimi", // VERIX-compliant skill generation
    "VERILINGUA cerceve aktivasyonu", // VERILINGUA frame activation
    "DSPy optimizasyonu", // DSPy optimization
    "GlobalMOO cok-amacli izleme" // GlobalMOO multi-objective tracking
  ],
  cikti_kalitesi: "uretim-seviyesi" // output quality: production-grade
} [ground:witnessed:architecture-design] [conf:0.90] [state:confirmed]

---

## S3 VERIX ENTEGRASYON CERCEVESI (VERIX Integration Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_rule]] -->
<!-- [[MOR:root:V-R-X]] Verix = root for verify-evidence-express -->
<!-- [[COM:Verix+Uyum+Kontrol]] German: Verix-Konformitats-Kontrolle -->

### S3.1 Beceri VERIX Uyumlu Talimatlar Uretir (Skills Output VERIX-Compliant Instructions)

[define|neutral] VERIX_CONFIG_SCHEMA := {
  kural_adi: "VERIX Yapilandirma Semasi", // rule name
  tanimlar: {
    strictness: ["relaxed", "moderate", "strict"],
    required_markers: ["ground", "confidence"],
    optional_markers: ["state"],
    output_format: ["L0_full", "L1_compressed", "L2_minimal"]
  },
  varsayilan_degerler: {
    strictness: "moderate",
    output_format: "L1_compressed"
  }
} [ground:witnessed:verix-spec] [conf:0.92] [state:confirmed]

### S3.2 VERIX ile Beceri Talimatlari (Skill Instructions with VERIX)

[assert|neutral] VERIX_ANNOTATION_PROCESS := {
  kural_adi: "Faz 5b Gelistirmesi", // Phase 5b Enhancement
  onceki_durum: "Run the test suite to verify changes",
  sonraki_durum: "[assert|neutral] Run the test suite to verify changes [ground:testing-sop.md] [conf:0.95]",
  arac: "VerixAnnotator",
  parametreler: ["strictness", "compression"]
} [ground:witnessed:phase-5b-design] [conf:0.88] [state:confirmed]

---

## S4 VERILINGUA ENTEGRASYON CERCEVESI (VERILINGUA Integration Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_frame]] -->
<!-- [[MOR:root:C-R-C]] Cerceve = root for frame-boundary-structure -->
<!-- [[COM:Verilingua+Cerceve+Secim]] German: Verilingua-Rahmen-Auswahl -->

### S4.1 Faz 0.5 Gelistirmesi: Beceri-Spesifik Cerceve Secimi (Phase 0.5: Skill-Specific Frame Selection)

[define|neutral] FRAME_MAPPING_SCHEMA := {
  kural_adi: "Beceri Cerceve Eslestirmesi", // Skill Frame Mapping
  eslestirmeler: [
    {
      alan: "development",
      birincil: "aspectual",
      ikincil: ["morphological"],
      aktivasyon: "Sostoyanie zavershenia - Track completion state"
    },
    {
      alan: "research",
      birincil: "evidential",
      ikincil: ["morphological"],
      aktivasyon: "Kaynak dogrulama - Verify all sources"
    },
    {
      alan: "quality",
      birincil: "evidential",
      ikincil: ["aspectual"],
      aktivasyon: "Kanitsal cerceve - Evidence-based analysis"
    },
    {
      alan: "orchestration",
      birincil: "compositional",
      ikincil: ["aspectual", "honorific"],
      aktivasyon: "Zusammensetzung - Build coordinated structure"
    },
    {
      alan: "documentation",
      birincil: "compositional",
      ikincil: ["honorific"],
      aktivasyon: "Baustein-Struktur - Structured documentation"
    }
  ]
} [ground:witnessed:frame-registry] [conf:0.90] [state:confirmed]

### S4.2 Uretilen Becerilerde Cerceve Gomme (Frame Embedding in Generated Skills)

[assert|neutral] GENERATED_SKILL_TEMPLATE := {
  kural_adi: "Cerceve ile Uretilmis Beceri Sablonu", // Generated Skill Template with Frame
  zorunlu_alanlar: [
    "name",
    "version",
    "cognitive_architecture.verilingua.primary_frame",
    "cognitive_architecture.verilingua.activation_phrase",
    "cognitive_architecture.verix.strictness",
    "cognitive_architecture.verix.required_markers"
  ],
  ornek_talimat: "[assert|neutral] Step 1: {instruction} [ground:sop-doc] [conf:0.90]"
} [ground:witnessed:template-design] [conf:0.88] [state:confirmed]

---

## S5 DSPY ENTEGRASYON CERCEVESI (DSPy Integration Frame)
<!-- [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_module]] -->
<!-- [[MOR:root:O-P-T]] Optimum = root for optimize-best-improve -->
<!-- [[COM:DSPy+Beceri+Uretim+Modul]] German: DSPy-Skill-Generierungs-Modul -->

### S5.1 DSPy Modulu Olarak Beceri Uretimi (Skill Generation as DSPy Module)

[define|neutral] DSPY_SIGNATURE := {
  kural_adi: "Beceri Uretim Imzasi", // Skill Generation Signature
  girisler: {
    user_request: "Hangi beceri olusturulacak", // what skill to create
    target_domain: "Beceri alani", // skill domain
    complexity: "simple | medium | complex"
  },
  ciktilar: {
    skill_yaml: "cognitive_architecture ile YAML onmatter",
    skill_content: "VERIX isaretleyicileri ile SKILL.md icerigi",
    frame_activation: "Cok dilli cerceve aktivasyon bolumu",
    verix_compliance: "VERIX isaretleyici kapsami 0-1",
    test_cases: "Dogrulama test vakalari"
  }
} [ground:reported:dspy-documentation] [conf:0.85] [state:confirmed]

### S5.2 Beceri Kalitesi icin DSPy Optimizasyonu (DSPy Optimization for Skill Quality)

[assert|neutral] OPTIMIZATION_METRIC := {
  kural_adi: "Beceri Kalite Metrigi", // Skill Quality Metric
  agirliklar: {
    verix_compliance: 0.30,
    frame_score: 0.30,
    test_coverage: 0.20,
    cognitive_architecture_presence: 0.20
  },
  arac: "Teleprompter",
  hedef: "compile ile optimize edilmis forge"
} [ground:reported:dspy-teleprompter] [conf:0.80] [state:provisional]

---

## S6 GLOBALMOO ENTEGRASYON CERCEVESI (GlobalMOO Integration Frame)
<!-- [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_objective]] -->
<!-- [[MOR:root:A-M-C]] Amac = root for objective-goal-purpose -->
<!-- [[COM:GlobalMOO+Cok+Amacli+Optimizasyon]] German: GlobalMOO-Mehrziel-Optimierung -->

### S6.1 Cok-Amacli Beceri Kalitesi (Multi-Objective Skill Quality)

[define|neutral] MOO_OBJECTIVES := {
  proje_id: "skill-forge-optimization",
  amaclar: [
    {
      ad: "verix_compliance",
      tanim: "Talimatlarda VERIX isaretleyici kapsami",
      yon: "maximize",
      agirlik: 0.25
    },
    {
      ad: "frame_alignment",
      tanim: "VERILINGUA cerceve aktivasyon kalitesi",
      yon: "maximize",
      agirlik: 0.20
    },
    {
      ad: "sop_completeness",
      tanim: "Tum gerekli bolumlerin mevcudiyeti",
      yon: "maximize",
      agirlik: 0.20
    },
    {
      ad: "test_coverage",
      tanim: "Test vakalari kullanim senaryolarini kapsar",
      yon: "maximize",
      agirlik: 0.15
    },
    {
      ad: "adversarial_pass_rate",
      tanim: "Faz 7a cekismeli testini gecer",
      yon: "maximize",
      agirlik: 0.15
    },
    {
      ad: "token_efficiency",
      tanim: "Beceri boyutu vs karmasiklik",
      yon: "minimize",
      agirlik: 0.05
    }
  ]
} [ground:witnessed:moo-config] [conf:0.88] [state:confirmed]

### S6.2 Uc-MOO Kaskadi ile Entegrasyon (Integration with Three-MOO Cascade)

[assert|neutral] CASCADE_PHASES := {
  kural_adi: "Uc-MOO Kaskad Fazlari", // Three-MOO Cascade Phases
  fazlar: [
    {
      id: "A",
      ad: "Yapi optimizasyonu", // Structure optimization
      islemler: ["Beceri bolum organizasyonu", "VERIX katiligi ayarlama"]
    },
    {
      id: "B",
      ad: "Kenar durum kesfi", // Edge case discovery
      islemler: ["Beceri basarisizlik modlari bulma", "Cekismeli test kapsamini genisletme"]
    },
    {
      id: "C",
      ad: "Uretim rafine", // Production refinement
      islemler: ["Optimal yapilandirmaya damitma", "Son beceri uretimi"]
    }
  ],
  cikti: "Pareto sinirinda en iyi yapilandirma"
} [ground:reported:cascade-documentation] [conf:0.82] [state:provisional]

---

## S7 GELISTIRILMIS FAZ AKISI (Enhanced Phase Flow Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_process]] -->
<!-- [[MOR:root:F-Z]] Faz = root for phase-stage-step -->
<!-- [[COM:Gelistirilmis+Faz+Akis]] German: Verbesserter-Phasen-Fluss -->

[define|neutral] ENHANCED_PHASE_FLOW := {
  kural_adi: "Gelistirilmis Beceri Uretim Akisi", // Enhanced Skill Generation Flow
  fazlar: [
    {
      id: "0",
      ad: "Sema Tanimi", // Schema Definition
      durum: "mevcut" // existing
    },
    {
      id: "0.5",
      ad: "Bilissel Cerceve Tasarimi", // Cognitive Frame Design
      durum: "GELISTIRILMIS", // ENHANCED
      adimlar: [
        "Beceri alanini analiz et",
        "VERILINGUA cerceve(ler) sec",
        "Cok dilli aktivasyon cumlesini hazirla",
        "Semaya cognitive_architecture ekle"
      ]
    },
    {
      id: "1-1b",
      ad: "Niyet Analizi + CoV", // Intent Analysis + CoV
      durum: "mevcut"
    },
    {
      id: "2-4",
      ad: "Kullanim Senaryosu + Mimari", // Use Case + Architecture
      durum: "mevcut"
    },
    {
      id: "5",
      ad: "Talimat Isleme", // Instruction Crafting
      durum: "GELISTIRILMIS",
      adimlar: [
        "Emir kipinde talimat yaz",
        "Tum iddialara VERIX anotasyonu uygula",
        "Dayanak ve guven kapsamini dogrula"
      ]
    },
    {
      id: "5b",
      ad: "Talimat Dogrulama + VERIX Dogrulama", // Instruction Verification + VERIX Validation
      durum: "GELISTIRILMIS",
      adimlar: [
        "Cekismeli yanlis yorumlama testi",
        "VERIX uyum kontrolu (minimum %70)",
        "Cerceve aktivasyon dogrulamasi"
      ]
    },
    {
      id: "6-7",
      ad: "Kaynak Gelistirme + Dogrulama", // Resource Development + Validation
      durum: "mevcut"
    },
    {
      id: "7a",
      ad: "Cekismeli Test", // Adversarial Testing
      durum: "mevcut"
    },
    {
      id: "7b",
      ad: "Dokumantasyon Denetimi", // Documentation Audit
      durum: "mevcut"
    },
    {
      id: "8",
      ad: "Metrik Izleme", // Metrics Tracking
      durum: "GELISTIRILMIS",
      adimlar: [
        "V0 -> V1 -> V2 iyilestirmeyi izle",
        "VERIX uyum deltasini kaydet",
        "Cerceve hizalama deltasini kaydet",
        "GlobalMOO'ya gonder"
      ]
    },
    {
      id: "9",
      ad: "GlobalMOO Optimizasyonu", // GlobalMOO Optimization
      durum: "YENI",
      adimlar: [
        "Uc-MOO Kaskadini calistir",
        "Pareto sinirini guncelle",
        "Optimal beceri yapilandirmasini damit"
      ]
    }
  ]
} [ground:witnessed:phase-design] [conf:0.90] [state:confirmed]

---

## S8 KALITE KAPILARI CERCEVESI (Quality Gates Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_gate]] -->
<!-- [[MOR:root:K-L-T]] Kalite = root for quality-value-standard -->
<!-- [[COM:Kalite+Kapi+Kontrol]] German: Qualitats-Gate-Kontrolle -->

### S8.1 VERIX Uyum Kapisi (VERIX Compliance Gate - Phase 5b)

[define|neutral] VERIX_QUALITY_GATE := {
  kural_adi: "VERIX Kalite Kapisi", // VERIX Quality Gate
  faz: "5b",
  gereksinimler: {
    minimum_instruction_coverage: 0.70,
    required_ground_types: ["sop_reference", "external_doc"],
    confidence_range: [0.6, 1.0],
    block_on_failure: true
  }
} [ground:witnessed:quality-gate-spec] [conf:0.92] [state:confirmed]

### S8.2 Cerceve Hizalama Kapisi (Frame Alignment Gate - Phase 0.5)

[define|neutral] FRAME_QUALITY_GATE := {
  kural_adi: "Cerceve Kalite Kapisi", // Frame Quality Gate
  faz: "0.5",
  gereksinimler: {
    frame_selection_required: true,
    activation_phrase_required: true,
    minimum_frame_score: 0.60,
    multilingual_optional: true
  },
  not: "v3.1'de cok dilli istege bagli" // multilingual optional in v3.1
} [ground:witnessed:quality-gate-spec] [conf:0.90] [state:confirmed]

### S8.3 GlobalMOO Yakinlasma Kapisi (GlobalMOO Convergence Gate - Phase 9)

[define|neutral] MOO_QUALITY_GATE := {
  kural_adi: "MOO Yakinlasma Kapisi", // MOO Convergence Gate
  faz: "9",
  gereksinimler: {
    minimum_pareto_points: 3,
    convergence_threshold: 0.02,
    required_objectives_covered: 4
  },
  not: "6 amactan en az 4u optimize edilmis olmali" // at least 4 of 6 objectives optimized
} [ground:witnessed:quality-gate-spec] [conf:0.88] [state:confirmed]

---

## S9 BELLEK ENTEGRASYONU CERCEVESI (Memory Integration Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_store]] -->
<!-- [[MOR:root:B-L-K]] Bellek = root for memory-store-retain -->
<!-- [[COM:Bellek+Entegrasyon+Depolama]] German: Speicher-Integration-Ablage -->

[define|neutral] MEMORY_STORAGE_SCHEMA := {
  kural_adi: "Beceri Uretim Sonuclari Depolama", // Store Skill Generation Outcomes
  namespace: "foundry-optimization",
  layer: "long-term",
  key_pattern: "skill-forge/generations/{skillId}",
  metadata_fields: {
    WHO: "skill-forge",
    WHEN: "ISO timestamp",
    PROJECT: "meta-loop",
    WHY: "skill-generation"
  },
  depolanan_metrikler: [
    "skillName",
    "domain",
    "verixScore",
    "frameScore",
    "testCount"
  ]
} [ground:witnessed:memory-mcp-design] [conf:0.90] [state:confirmed]

---

## S10 CAPRAZ-BECERI KOORDINASYON CERCEVESI (Cross-Skill Coordination Frame)
<!-- [[HON:sonkeigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_relation]] -->
<!-- [[MOR:root:K-R-D]] Koordinasyon = root for coordinate-arrange-organize -->
<!-- [[COM:Capraz+Beceri+Koordinasyon]] German: Kreuz-Skill-Koordination -->

[define|neutral] COORDINATION_MATRIX := {
  kural_adi: "Digeri Dokumcul Becerilerle Entegrasyon", // Integration with Other Foundry Skills
  entegrasyonlar: [
    {
      beceri: "prompt-architect",
      zamanlama: "Faz 5 talimat islemeden once", // Before Phase 5
      amac: "Kanit-temelli teknikler kullanarak beceri talimatlarini optimize et",
      veri_akisi: "skill_instructions -> optimized_instructions"
    },
    {
      beceri: "agent-creator",
      zamanlama: "Faz 6 kaynak gelistirmeden sonra", // After Phase 6
      amac: "Beceriyi calistiran ajanlar olustur",
      veri_akisi: "skill_spec -> agent_system_prompt"
    },
    {
      beceri: "cognitive-lensing",
      zamanlama: "Faz 0.5 cerceve secimi", // Phase 0.5 frame selection
      amac: "Beceri alani icin optimal bilissel cerceve sec",
      veri_akisi: "skill_domain -> selected_frame"
    },
    {
      beceri: "eval-harness",
      zamanlama: "Faz 7 dogrulama", // Phase 7 validation
      amac: "Benchmark ve regresyon testleri calistir",
      veri_akisi: "generated_skill -> test_results"
    }
  ]
} [ground:witnessed:coordination-design] [conf:0.88] [state:confirmed]

---

## S11 SONUC CERCEVESI (Conclusion Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-end -->
<!-- [[COM:Sonuc+Ozet+Bildiri]] German: Schlussfolgerung-Zusammenfassung -->
Zaversheno. (Russian: Complete.)

[assert|confident] ADDENDUM_SUMMARY := {
  amac: "Skill-forge icin tam bilissel mimari entegrasyonu", // purpose
  entegrasyonlar: [
    {
      sistem: "VERIX",
      yetenekler: "Tum beceri talimatlarinda epistemik isaretleyiciler"
    },
    {
      sistem: "VERILINGUA",
      yetenekler: "Faz 0.5'te cerceve secimi gomulu"
    },
    {
      sistem: "DSPy",
      yetenekler: "Optimize edilebilir DSPy modulu olarak beceri uretimi"
    },
    {
      sistem: "GlobalMOO",
      yetenekler: "Uc-MOO Kaskadi ile cok-amacli izleme"
    }
  ],
  kalite_kapilari: ["VERIX Uyum", "Cerceve Hizalama", "MOO Yakinlasma"],
  ciktilar: [
    "VERIX-uyumlu talimatlarla beceriler",
    "Tum becerilerde bilissel cerceve aktivasyonu",
    "DSPy teleprompter ile optimize edilmis beceri kalitesi",
    "GlobalMOO Pareto siniri ile beceri etkinligi izleme"
  ]
} [ground:witnessed:implementation] [conf:0.90] [state:confirmed]

---

*Promise: `<promise>COGNITIVE_ARCHITECTURE_ADDENDUM_VCL_V3.1.1_COMPLIANT</promise>`*
