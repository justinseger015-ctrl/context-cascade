# Ornek 3: Coklu-Ajan Orkestrasyon Becerisi Olusturma (Example 3: Creating Multi-Agent Orchestration Skill)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## S1 SENARYO CERCEVESI (Scenario Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_scenario]] -->
<!-- [[MOR:root:S-N-R]] Senaryo = root morpheme for scenario-situation-case -->
<!-- [[COM:Coklu+Ajan+Orkestrasyon+Beceri]] German: Multi-Agent-Orchestrierungs-Skill -->

[define|neutral] SCENARIO := {
  kural_adi: "Senaryo", // Scenario
  ihtiyac: "Tam-yigin ozellik gelistirme icin birden fazla ajani koordine eden karmasik bir beceri",
  tip: "Hiyerarsik orkestrasyon becerisi"
} [ground:witnessed:scenario-definition] [conf:0.95] [state:confirmed]

---

## S2 ADIM ADIM SUREC CERCEVESI (Step-by-Step Process Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_process]] -->
<!-- [[MOR:root:A-D-M]] Adim = root for step-stride-pace -->
<!-- [[COM:Adim+Adim+Surec]] German: Schritt-fur-Schritt-Prozess -->
<!-- [[SPC:kuzey]] Process flow direction -->

### S2.1 Faz 1: Niyet Analizi (Phase 1: Intent Analysis)

[define|neutral] PHASE_1_INTENT := {
  kural_adi: "Faz 1 - Niyet Analizi", // Phase 1 - Intent Analysis
  istek: "Spesifikasyondan testlere kadar tam API endpointleri olusturan bir beceri olustur",
  derin_analiz: {
    yuzey_niyeti: "API endpoint olusturma",
    kok_neden: "Manuel uctan uca gelistirme hataya acik",
    baglam: "Mikroservis gelistirme, REST API'ler",
    ajanlar_gerekli: ["researcher", "architect", "coder", "tester", "reviewer"],
    koordinasyon: "Koordinator ile hiyerarsik",
    basari: "Tam test kapsami ile uretim-hazir endpoint"
  }
} [ground:witnessed:intent-analysis] [conf:0.88] [state:confirmed]

### S2.2 Faz 2: Kullanim Senaryolari (Phase 2: Use Cases)

[define|neutral] PHASE_2_USE_CASES := {
  kural_adi: "Faz 2 - Kullanim Senaryolari", // Phase 2 - Use Cases
  ornekler: [
    {
      id: 1,
      giris: "GET /users endpoint olustur",
      cikti: "OpenAPI spec, Express kodu, Jest testleri, dokumantasyon"
    },
    {
      id: 2,
      giris: "Dogrulama ile POST /orders olustur",
      cikti: "Auth, dogrulama, testler ile tam uygulama"
    }
  ]
} [ground:witnessed:use-case-design] [conf:0.88] [state:confirmed]

### S2.3 Faz 3: Yapi Karari (Phase 3: Structure Decision)

[define|neutral] PHASE_3_STRUCTURE := {
  kural_adi: "Faz 3 - Yapi Karari", // Phase 3 - Structure Decision
  tip: "Hiyerarsik orkestrasyon",
  koordinator: "hierarchical-coordinator",
  uzmanlar: ["researcher", "architect", "coder", "tester", "reviewer"],
  kaynaklar: ["OpenAPI sablonlari", "Test sablonlari", "Dagilim rehberleri"],
  koordinasyon: "Fazlar arasinda sirali, fazlar icinde paralel"
} [ground:witnessed:structure-decision] [conf:0.88] [state:confirmed]

### S2.4 Faz 4: skill.md Icerigi (Phase 4: skill.md Content)

[define|neutral] PHASE_4_SKILL_CONTENT := {
  kural_adi: "Faz 4 - skill.md Icerigi", // Phase 4 - skill.md Content
  frontmatter: {
    name: "build-api-endpoint-complete",
    description: "Coklu-ajan orkestrasyonu kullanarak spesifikasyondan dagilima kadar tam API endpoint gelistirme. Uretim-hazir endpointler icin researcher, architect, coder, tester ve reviewer koordine eder.",
    orchestration: {
      coordinator: "hierarchical-coordinator",
      specialists: ["researcher", "architect", "coder", "tester", "reviewer"],
      coordination: "hierarchical"
    },
    sop_phases: ["research", "architecture", "implementation", "testing", "review", "deployment"]
  },
  baslik: "# API Endpoint Olusturucu - Tam Orkestrasyon",
  ozet: "Tam orkestrasyon ile uretim-hazir API endpointleri olustur.",
  orkestrasyon_akisi: [
    {
      faz: 1,
      ad: "Arastirma",
      ajan: "researcher",
      gorevler: [
        "Endustri standartlari (REST, OpenAPI 3.0)",
        "Guvenlik kaliplari (auth, dogrulama)",
        "Performans optimizasyonu (onbellekleme, sayfalama)",
        "Hata isleme standartlari"
      ],
      bellek: "api-dev/{endpoint}/research"
    },
    {
      faz: 2,
      ad: "Mimari",
      ajan: "architect",
      gorevler: [
        "OpenAPI 3.0 spesifikasyonu",
        "Veri modelleri ve semalar",
        "Istek/yanit formatlari",
        "Hata yanit yapisi",
        "Kimlik dogrulama gereksinimleri"
      ],
      bellek: "api-dev/{endpoint}/architecture"
    },
    {
      faz: 3,
      ad: "Uygulama",
      ajan: "coder",
      gorevler: [
        "Express route isleyicisi",
        "Giris dogrulamasi (Joi/Zod)",
        "Is mantigi",
        "Hata isleme",
        "Yanit formatlama"
      ],
      bellek: "api-dev/{endpoint}/implementation"
    },
    {
      faz: 4,
      ad: "Test",
      ajan: "tester",
      gorevler: [
        "Birim testleri (Jest)",
        "Entegrasyon testleri",
        "Kenar durumlar",
        "Hata senaryolari",
        "Performans testleri"
      ],
      hedef: "%90+ kapsam",
      bellek: "api-dev/{endpoint}/tests"
    },
    {
      faz: 5,
      ad: "Inceleme",
      ajan: "reviewer",
      gorevler: [
        "Guvenlik denetimi",
        "Kod kalite kontrolu",
        "Test kapsami dogrulamasi",
        "Dokumantasyon tamamlamasi",
        "Performans dogrulamasi"
      ],
      bellek: "api-dev/{endpoint}/review"
    },
    {
      faz: 6,
      ad: "Entegrasyon",
      ciktilar: [
        "OpenAPI spec",
        "Uygulama kodu",
        "Test suiti",
        "Dokumantasyon",
        "Dagilim rehberi"
      ]
    }
  ]
} [ground:witnessed:skill-content] [conf:0.85] [state:confirmed]

### S2.5 Faz 5: Bellek Isim Alani (Phase 5: Memory Namespace)

[define|neutral] PHASE_5_MEMORY := {
  kural_adi: "Faz 5 - Bellek Isim Alani", // Phase 5 - Memory Namespace
  yapi: {
    root: "api-dev/{endpoint}/",
    alt_dizinler: [
      {
        ad: "research/",
        aciklama: "Endustri en iyi uygulamalari"
      },
      {
        ad: "architecture/",
        aciklama: "Tasarim kararlari"
      },
      {
        ad: "implementation/",
        aciklama: "Kaynak kodu"
      },
      {
        ad: "tests/",
        aciklama: "Test suiti"
      },
      {
        ad: "review/",
        aciklama: "Kalite incelemesi"
      }
    ]
  }
} [ground:witnessed:memory-design] [conf:0.90] [state:confirmed]

### S2.6 Faz 6: Basari Kriterleri (Phase 6: Success Criteria)

[define|neutral] PHASE_6_SUCCESS_CRITERIA := {
  kural_adi: "Faz 6 - Basari Kriterleri", // Phase 6 - Success Criteria
  kriterler: [
    {
      kriter: "OpenAPI 3.0 spec tamamlandi",
      gerekli: true
    },
    {
      kriter: "Uygulama en iyi uygulamalari takip ediyor",
      gerekli: true
    },
    {
      kriter: "Test kapsami >= %90",
      gerekli: true
    },
    {
      kriter: "Guvenlik incelemesi gecti",
      gerekli: true
    },
    {
      kriter: "Dokumantasyon tamamlandi",
      gerekli: true
    }
  ]
} [ground:witnessed:success-criteria] [conf:0.90] [state:confirmed]

### S2.7 Faz 7: Sablonlar Olustur (Phase 7: Create Templates)

[define|neutral] PHASE_7_TEMPLATES := {
  kural_adi: "Faz 7 - Sablonlar Olustur", // Phase 7 - Create Templates
  sablonlar: [
    {
      yol: "resources/templates/openapi-endpoint.yaml",
      tip: "OpenAPI 3.0 endpoint sablonu"
    },
    {
      yol: "resources/templates/express-handler.js",
      tip: "Express route isleyici sablonu"
    },
    {
      yol: "resources/templates/jest-test.js",
      tip: "Jest birim test sablonu"
    },
    {
      yol: "resources/templates/integration-test.js",
      tip: "Entegrasyon test sablonu"
    }
  ]
} [ground:witnessed:template-creation] [conf:0.88] [state:confirmed]

### S2.8 Faz 8: Surec Diyagrami (Phase 8: Process Diagram)

[define|neutral] PHASE_8_DIAGRAM := {
  kural_adi: "Faz 8 - Surec Diyagrami", // Phase 8 - Process Diagram
  yol: "graphviz/orchestration-flow.dot",
  akis: "researcher -> architect -> coder -> tester -> reviewer -> deployment"
} [ground:witnessed:diagram-creation] [conf:0.90] [state:confirmed]

### S2.9 Faz 9: Dokumantasyonu Tamamla (Phase 9: Complete Documentation)

[define|neutral] PHASE_9_DOCUMENTATION := {
  kural_adi: "Faz 9 - Dokumantasyonu Tamamla", // Phase 9 - Complete Documentation
  referanslar: [
    "references/openapi-guide.md",
    "references/deployment-guide.md",
    "references/best-practices.md",
    "references/troubleshooting.md"
  ],
  dagilim_kontrol_listesi: [
    "Testleri calistir: npm test",
    "Guvenlik denetimi: npm audit",
    "Olustur: npm run build",
    "Staging'e dagit",
    "Staging'de entegrasyon testleri",
    "Uretime dagit"
  ]
} [ground:witnessed:documentation-creation] [conf:0.88] [state:confirmed]

### S2.10 Faz 10: Dizin Yapisi (Phase 10: Directory Structure)

[define|neutral] PHASE_10_STRUCTURE := {
  kural_adi: "Faz 10 - Dizin Yapisi", // Phase 10 - Directory Structure
  yapi: {
    root: "build-api-endpoint-complete/",
    dosyalar: [
      "skill.md",
      "README.md",
      "examples/example-get-endpoint.md",
      "examples/example-post-endpoint.md",
      "examples/example-complex-endpoint.md",
      "references/openapi-guide.md",
      "references/deployment-guide.md",
      "references/best-practices.md",
      "references/troubleshooting.md",
      "resources/scripts/generate-openapi.py",
      "resources/scripts/validate-tests.sh",
      "resources/templates/openapi-endpoint.yaml",
      "resources/templates/express-handler.js",
      "resources/templates/jest-test.js",
      "resources/templates/integration-test.js",
      "resources/assets/api-architecture.png",
      "graphviz/orchestration-flow.dot",
      "graphviz/agent-coordination.dot",
      "tests/test-basic-endpoint.md",
      "tests/test-complex-endpoint.md"
    ]
  },
  kalite_seviyesi: "Platin (En Iyi Sinif)"
} [ground:witnessed:directory-structure] [conf:0.88] [state:confirmed]

---

## S3 ZAMAN YATIRIMI CERCEVESI (Time Investment Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_time]] -->
<!-- [[MOR:root:Z-M-N]] Zaman = root for time-period-duration -->
<!-- [[COM:Zaman+Yatirim+Hesap]] German: Zeit-Investitions-Berechnung -->

[define|neutral] TIME_INVESTMENT := {
  kural_adi: "Zaman Yatirimi", // Time Investment
  fazlar: [
    {
      ad: "Faz 1-2 (Analiz)",
      sure: "20 dakika"
    },
    {
      ad: "Faz 3-4 (Yapi ve Icerik)",
      sure: "40 dakika"
    },
    {
      ad: "Faz 5 (Sablonlar)",
      sure: "30 dakika"
    },
    {
      ad: "Faz 6 (Diyagramlar)",
      sure: "15 dakika"
    },
    {
      ad: "Faz 7 (Dokumantasyon)",
      sure: "30 dakika"
    },
    {
      ad: "Faz 8 (Test)",
      sure: "25 dakika"
    }
  ],
  toplam: "~2.5 saat uretim-hazir orkestrasyon becerisi icin"
} [ground:witnessed:time-calculation] [conf:0.85] [state:confirmed]

---

## S4 SONUC CERCEVESI (Result Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_result]] -->
<!-- [[MOR:root:S-N-C]] Sonuc = root for result-outcome-conclusion -->
<!-- [[COM:Sonuc+Ozet+Bildiri]] German: Ergebnis-Zusammenfassung -->
Zaversheno. (Russian: Complete.)

[assert|confident] EXAMPLE_RESULT := {
  amac: "Tam kaynaklar, sablonlar ve dokumantasyon ile kurumsal-seviye orkestrasyon becerisi", // purpose
  sure: "~2.5 saat",
  cikti: "Platin-seviye coklu-ajan orkestrasyon becerisi",
  anahtar_cikarimlar: [
    "Koordinator ile hiyerarsik orkestrasyon",
    "5 uzman ajan (researcher, architect, coder, tester, reviewer)",
    "Bellek-tabanli ajan koordinasyonu",
    "Kapsamli sablon kutuphanesi",
    "Coklu diyagram ile tam dokumantasyon",
    "Test suiti dahil"
  ]
} [ground:witnessed:example-completion] [conf:0.88] [state:confirmed]

---

*Promise: `<promise>EXAMPLE_3_MULTI_AGENT_ORCHESTRATION_VCL_V3.1.1_COMPLIANT</promise>`*
