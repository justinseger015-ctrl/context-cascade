# Ornek 2: Ajan-Destekli Analiz Becerisi Olusturma (Example 2: Creating an Agent-Powered Analysis Skill)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## S1 SENARYO CERCEVESI (Scenario Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_scenario]] -->
<!-- [[MOR:root:S-N-R]] Senaryo = root morpheme for scenario-situation-case -->
<!-- [[COM:Ajan+Destekli+Analiz+Beceri]] German: Agenten-gestutzte-Analyse-Skill -->

[define|neutral] SCENARIO := {
  kural_adi: "Senaryo", // Scenario
  ihtiyac: "Kod kalitesini analiz eden ve detayli oneriler sunan bir beceri",
  tip: "Ajan-destekli beceri (code-analyzer, reviewer)"
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
  istek: "Python kod kalitesini analiz eden bir beceri olustur",
  derin_analiz: {
    yuzey_niyeti: "Kod kalite analizi",
    kok_neden: "Sistematik kalite kontrollerine ihtiyac var",
    baglam: "Pre-commit incelemeleri, kod optimizasyonu",
    ajanlar_gerekli: ["code-analyzer", "reviewer"],
    basari: "Eyleme gecirilebilir iyilestirme onerileri"
  }
} [ground:witnessed:intent-analysis] [conf:0.90] [state:confirmed]

### S2.2 Faz 2: Kullanim Senaryolari (Phase 2: Use Cases)

[define|neutral] PHASE_2_USE_CASES := {
  kural_adi: "Faz 2 - Kullanim Senaryolari", // Phase 2 - Use Cases
  ornekler: [
    {
      id: 1,
      giris: "God object iceren Python dosyasi",
      cikti: "Duzeltme onerileri ile tespit edilen anti-kaliplar"
    },
    {
      id: 2,
      giris: "Karmasik fonksiyonlar iceren modul",
      cikti: "Karmasiklik metrikleri + yeniden duzenleme rehberi"
    }
  ]
} [ground:witnessed:use-case-design] [conf:0.88] [state:confirmed]

### S2.3 Faz 3: Yapi Karari (Phase 3: Structure Decision)

[define|neutral] PHASE_3_STRUCTURE := {
  kural_adi: "Faz 3 - Yapi Karari", // Phase 3 - Structure Decision
  tip: "Ajan-destekli beceri",
  birincil_ajan: "code-analyzer",
  destek_ajanlar: ["reviewer"],
  kaynaklar: ["Analiz scriptleri", "En iyi uygulamalar referansi"],
  koordinasyon: "sirali" // sequential
} [ground:witnessed:structure-decision] [conf:0.90] [state:confirmed]

### S2.4 Faz 4: skill.md Icerigi (Phase 4: skill.md Content)

[define|neutral] PHASE_4_SKILL_CONTENT := {
  kural_adi: "Faz 4 - skill.md Icerigi", // Phase 4 - skill.md Content
  frontmatter: {
    name: "analyze-python-code-quality",
    description: "code-analyzer ve reviewer ajanlari kullanarak kapsamli Python kod kalite analizi. Uretim hazirliği icin Python dosyalarini incelerken kullan.",
    orchestration: {
      primary_agent: "code-analyzer",
      support_agents: ["reviewer"],
      coordination: "sequential"
    }
  },
  baslik: "# Python Kod Kalite Analizcisi",
  ozet: "Eyleme gecirilebilir iyilestirmeler ile Python kodunun sistematik analizi.",
  surec: [
    {
      faz: 1,
      ad: "Statik Analiz",
      ajan: "code-analyzer",
      kontroller: [
        "Karmasiklik ihlalleri (cyclomatic > 10)",
        "God objects (>15 metod)",
        "Parametre bombalari (>6 param)",
        "Derin ic ice yapi (>4 seviye)"
      ]
    },
    {
      faz: 2,
      ad: "En Iyi Uygulamalar Incelemesi",
      ajan: "reviewer",
      kontroller: [
        "PEP 8 uyumu",
        "Tip ipucu kapsami",
        "Dokumantasyon kalitesi",
        "Test kapsami bosluklari"
      ]
    },
    {
      faz: 3,
      ad: "Rapor Olustur",
      cikti: {
        ciddiyet_dereceleri: ["critical", "warning", "info"],
        ozel_satir_referanslari: true,
        duzeltme_onerileri: true,
        yeniden_duzenleme_kaliplari: true
      }
    }
  ]
} [ground:witnessed:skill-content] [conf:0.88] [state:confirmed]

### S2.5 Faz 5: Kaynaklar Olustur (Phase 5: Create Resources)

[define|neutral] PHASE_5_RESOURCES := {
  kural_adi: "Faz 5 - Kaynaklar Olustur", // Phase 5 - Create Resources
  scripts: {
    yol: "resources/scripts/analyze.py",
    icindekiler: {
      importlar: ["ast", "complexity"],
      fonksiyonlar: ["analyze_file(filepath)"],
      cikti: "results"
    }
  }
} [ground:witnessed:resource-creation] [conf:0.85] [state:confirmed]

### S2.6 Faz 6: Referans Olustur (Phase 6: Create Reference)

[define|neutral] PHASE_6_REFERENCE := {
  kural_adi: "Faz 6 - Referans Olustur", // Phase 6 - Create Reference
  yol: "references/best-practices.md",
  icerik: {
    baslik: "# Python Kalite Standartlari",
    bolumler: [
      {
        ad: "Karmasiklik Limitleri",
        kurallar: [
          "Cyclomatic complexity: <=10",
          "Fonksiyon uzunlugu: <=50 satir",
          "Sinif metodlari: <=15"
        ]
      },
      {
        ad: "NASA Standartlari",
        kurallar: [
          "Parametreler: <=6",
          "Ic ice yapi derinligi: <=4"
        ]
      }
    ]
  }
} [ground:reported:best-practices] [conf:0.85] [state:confirmed]

### S2.7 Faz 7: Dizin Yapisi (Phase 7: Directory Structure)

[define|neutral] PHASE_7_STRUCTURE := {
  kural_adi: "Faz 7 - Dizin Yapisi", // Phase 7 - Directory Structure
  yapi: {
    root: "analyze-python-code-quality/",
    dosyalar: [
      "skill.md",
      "README.md",
      "examples/example-analysis.md",
      "references/best-practices.md",
      "resources/scripts/analyze.py",
      "graphviz/workflow.dot"
    ]
  },
  kalite_seviyesi: "Gumus (Uretim Hazir)"
} [ground:witnessed:directory-structure] [conf:0.90] [state:confirmed]

---

## S3 SONUC CERCEVESI (Result Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_result]] -->
<!-- [[MOR:root:S-N-C]] Sonuc = root for result-outcome-conclusion -->
<!-- [[COM:Sonuc+Ozet+Bildiri]] German: Ergebnis-Zusammenfassung -->
Zaversheno. (Russian: Complete.)

[assert|confident] EXAMPLE_RESULT := {
  amac: "Tam kaynaklarla uretim-hazir ajan-destekli beceri", // purpose
  sure: "~45 dakika",
  cikti: "Gumus-seviye ajan-destekli beceri",
  anahtar_cikarimlar: [
    "Birincil ve destek ajanlar koordinasyonu",
    "Analiz scriptleri ile kaynak dizini",
    "En iyi uygulamalar ile referans dokumantasyonu",
    "Sirali ajan koordinasyonu"
  ]
} [ground:witnessed:example-completion] [conf:0.90] [state:confirmed]

---

*Promise: `<promise>EXAMPLE_2_AGENT_POWERED_SKILL_VCL_V3.1.1_COMPLIANT</promise>`*
