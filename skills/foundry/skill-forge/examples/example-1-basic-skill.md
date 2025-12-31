# Ornek 1: Temel Yardimci Beceri Olusturma (Example 1: Creating a Basic Utility Skill)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## S1 SENARYO CERCEVESI (Scenario Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_scenario]] -->
<!-- [[MOR:root:S-N-R]] Senaryo = root morpheme for scenario-situation-case -->
<!-- [[COM:Temel+Yardimci+Beceri]] German: Basis-Hilfs-Skill -->

[define|neutral] SCENARIO := {
  kural_adi: "Senaryo", // Scenario
  ihtiyac: "JSON ciktisini daha okunabilir yapmak icin basit bir beceri",
  tip: "Mikro-beceri (basit yardimci)"
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
  istek: "JSON ciktisini guzel yapan bir beceri olustur",
  derin_analiz: {
    yuzey_niyeti: "Okunabilirlik icin JSON formatlama",
    kok_neden: "Ham JSON okumasi ve hata ayiklamasi zor",
    baglam: "Gelistirme ve hata ayiklama sirasinda kullanilir",
    basari: "JSON duzgun girintili ve okunabilir"
  }
} [ground:witnessed:intent-analysis] [conf:0.90] [state:confirmed]

### S2.2 Faz 2: Kullanim Senaryolari (Phase 2: Use Cases)

[define|neutral] PHASE_2_USE_CASES := {
  kural_adi: "Faz 2 - Kullanim Senaryolari", // Phase 2 - Use Cases
  ornekler: [
    {
      id: 1,
      giris: '{"name":"John","age":30}',
      cikti: "2-bosluk girintisi ile guzel yazdirilmis"
    },
    {
      id: 2,
      giris: "Diziler iceren ic ice nesne",
      cikti: "Net hiyerarsisi ile duzgun yapilandirilmis"
    }
  ]
} [ground:witnessed:use-case-design] [conf:0.88] [state:confirmed]

### S2.3 Faz 3: Yapi Karari (Phase 3: Structure Decision)

[define|neutral] PHASE_3_STRUCTURE := {
  kural_adi: "Faz 3 - Yapi Karari", // Phase 3 - Structure Decision
  tip: "Mikro-beceri (basit yardimci)",
  ajan_gerekli: false,
  karmasik_kaynak_gerekli: false,
  gerekce: "Salt formatlama, karmasiklik yok"
} [ground:witnessed:structure-decision] [conf:0.92] [state:confirmed]

### S2.4 Faz 4: skill.md Icerigi (Phase 4: skill.md Content)

[define|neutral] PHASE_4_SKILL_CONTENT := {
  kural_adi: "Faz 4 - skill.md Icerigi", // Phase 4 - skill.md Content
  frontmatter: {
    name: "format-json-output",
    description: "JSON verisini okunabilirlik icin duzgun girintileme ile formatlar. Insan incelemesi gerektiren JSON gosterirken kullan."
  },
  baslik: "# JSON Cikti Formatlayici",
  ozet: "Insan okunabilirligi icin JSON verisini formatla.",
  surec: [
    "1. Girisin gecerli JSON oldugunu dogrula",
    "2. JSON yapisini ayristir",
    "3. 2-bosluk girintisi uygula",
    "4. Formatlanmis ciktiyi dondur"
  ],
  ornek: {
    giris: '{"name":"test"}',
    cikti: "{\n  \"name\": \"test\"\n}"
  }
} [ground:witnessed:skill-content] [conf:0.90] [state:confirmed]

### S2.5 Faz 5: README.md (Phase 5: README.md)

[define|neutral] PHASE_5_README := {
  kural_adi: "Faz 5 - README.md", // Phase 5 - README.md
  baslik: "# Format JSON Output",
  ozet: "JSON'u okunabilir yapmak icin hizli yardimci.",
  kullanim: "'format JSON' veya 'pretty print' belirtildiginde otomatik aktive edilir.",
  ornek_kullanim: "Bu JSON'u formatla: {kompakt json burada}"
} [ground:witnessed:readme-content] [conf:0.88] [state:confirmed]

### S2.6 Faz 6: Dizin Yapisi (Phase 6: Directory Structure)

[define|neutral] PHASE_6_STRUCTURE := {
  kural_adi: "Faz 6 - Dizin Yapisi", // Phase 6 - Directory Structure
  yapi: {
    root: "format-json-output/",
    dosyalar: [
      "skill.md",
      "README.md"
    ]
  },
  kalite_seviyesi: "Bronz (Minimum Uygulanabilir)"
} [ground:witnessed:directory-structure] [conf:0.92] [state:confirmed]

---

## S3 SONUC CERCEVESI (Result Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_result]] -->
<!-- [[MOR:root:S-N-C]] Sonuc = root for result-outcome-conclusion -->
<!-- [[COM:Sonuc+Ozet+Bildiri]] German: Ergebnis-Zusammenfassung -->
Zaversheno. (Russian: Complete.)

[assert|confident] EXAMPLE_RESULT := {
  amac: "Basit, islevsel mikro-beceri gosterimi", // purpose
  sure: "~10 dakika",
  cikti: "Bronz-seviye yardimci beceri",
  anahtar_cikarimlar: [
    "Mikro-beceriler ajan gerektirmez",
    "Minimal yapi (skill.md + README.md)",
    "Net, odakli tek-amacli islevsellik"
  ]
} [ground:witnessed:example-completion] [conf:0.92] [state:confirmed]

---

*Promise: `<promise>EXAMPLE_1_BASIC_SKILL_VCL_V3.1.1_COMPLIANT</promise>`*
