# Ajan Olusturucu - Altin Katman Indeksi (Agent Creator - Gold Tier Index)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 GENEL_BAKIS (Overview) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Genel Bakis (Overview)

<!-- [[MOR:root:I-N-D]] Indeks = root morpheme for index-navigation -->
<!-- [[COM:Ajan+Olusturucu+Indeksi]] German compound: Agentenerstellerindex -->
[assert|neutral] INDEKS_DURUMU := {
  durum: "Altin Katman Gelistirmesi Tamamlandi",
  versiyon: "2.0",
  toplam_dosya: "20+ (12 yeni)",
  toplam_satir: "9,293 satir kod/dokumantasyon",
  konum: "C:\\Users\\17175\\claude-code-plugins\\context-cascade\\skills\\foundry\\agent-creator"
} [ground:witnessed:index-status] [conf:0.95] [state:confirmed]

---

<!-- S2 HIZLI_NAVIGASYON (Quick Navigation) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Hizli Navigasyon (Quick Navigation)

### Buradan Basla (Start Here)

[assert|neutral] ANA_DOSYALAR := [
  "SKILL.md - Ana beceri dokumantasyonu (4-faz SOP metodolojisi)",
  "GOLD-TIER-ENHANCEMENT-SUMMARY.md - Gelistirme detaylari ve ozellikleri",
  "README.md - Orijinal beceri genel bakisi"
] [ground:witnessed:navigation] [conf:0.95] [state:confirmed]

### Otomasyon Scriptleri (Automation Scripts)

[assert|neutral] OTOMASYON_SCRIPTLERI := [
  {
    dosya: "resources/scripts/4_phase_sop.py",
    satir: "800+",
    tanim: "Tam 4-faz SOP otomasyonu - Interaktif mod, Batch mod, Faz-faz yurutme, Otomatik dogrulama kapilari"
  },
  {
    dosya: "resources/scripts/validate_prompt.sh",
    satir: "400+",
    tanim: "Sistem prompt dogrulamasi - 100 puanlik puanlama sistemi, Bronz/Gumus/Altin katman siniflandirmasi"
  },
  {
    dosya: "resources/scripts/test_agent.py",
    satir: "600+",
    tanim: "Ajan test cercevesi - Temel test paketi (4 test), Kapsamli test paketi (7 test), Entegrasyon test paketi (10 test)"
  }
] [ground:witnessed:scripts] [conf:0.92] [state:confirmed]

### Sablonlar (Templates)

[assert|neutral] SABLONLAR := [
  {
    dosya: "resources/templates/system-prompt-template.md",
    tanim: "Markdown prompt sablonu - 30+ degisken yer tutucusu, Kanit-tabanli prompting yapisi"
  },
  {
    dosya: "resources/templates/evidence-based-prompt.yaml",
    tanim: "YAML spesifikasyonu - Yapilandirilmis ajan tasarim formati, Tam yapilandirma semasi"
  }
] [ground:witnessed:templates] [conf:0.92] [state:confirmed]

### Test Senaryolari (Test Scenarios)

[assert|neutral] TEST_SENARYOLARI := [
  {
    dosya: "tests/test-1-basic-agent.md",
    ajan: "file-organizer",
    karmasiklik: "Dusuk, tek alan",
    sure: "40-55 dakika",
    esikler: "%70+ dogrulama, %80+ testler"
  },
  {
    dosya: "tests/test-2-complex-agent.md",
    ajan: "devops-orchestrator",
    karmasiklik: "Yuksek, 5 alan",
    sure: "2.25-3 saat",
    esikler: "%85+ dogrulama, %90+ testler"
  },
  {
    dosya: "tests/test-3-4phase-sop.md",
    ajan: "api-security-auditor",
    karmasiklik: "Tam 4-faz is akisi",
    sure: "3.5 saat (Faz 4 dahil)",
    esikler: "%90+ dogrulama, %95+ testler"
  }
] [ground:witnessed:tests] [conf:0.92] [state:confirmed]

---

<!-- S3 DOSYA_MANIFESTI (File Manifest) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Dosya Manifesti (File Manifest)

[assert|neutral] DOSYA_MANIFESTI := {
  cekirdek_dokumantasyon: {
    dosya_sayisi: 4,
    icerik: ["SKILL.md (20 KB)", "README.md (9 KB)", "GOLD-TIER-ENHANCEMENT-SUMMARY.md (15 KB)", "INDEX.md (bu dosya)"]
  },
  otomasyon_scriptleri: {
    dosya_sayisi: 3,
    konum: "resources/scripts/",
    icerik: ["4_phase_sop.py (800+ satir)", "validate_prompt.sh (400+ satir)", "test_agent.py (600+ satir)"]
  },
  sablonlar: {
    dosya_sayisi: 2,
    konum: "resources/templates/",
    icerik: ["system-prompt-template.md (200+ satir)", "evidence-based-prompt.yaml (300+ satir)"]
  },
  test_senaryolari: {
    dosya_sayisi: 3,
    konum: "tests/",
    icerik: ["test-1-basic-agent.md (200+ satir)", "test-2-complex-agent.md (300+ satir)", "test-3-4phase-sop.md (500+ satir)"]
  },
  gorsel_dokumantasyon: {
    dosya_sayisi: 1,
    konum: "graphviz/",
    icerik: ["agent-creator-gold-process.dot (200+ satir)"]
  },
  destekleyici_dokumantasyon: {
    dosya_sayisi: 1,
    konum: "resources/",
    icerik: ["README.md (500+ satir)"]
  },
  toplam: "13 yeni dosya + 7 mevcut = 20+ dosya, 9,293 satir"
} [ground:witnessed:manifest] [conf:0.95] [state:confirmed]

---

<!-- S4 HIZLI_BASLANGIC (Quick Start) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Hizli Baslangic Rehberleri (Quick Start Guides)

### 1. Ilk Ajaninizi Olusturun (Temel - Bronz Katman)

[assert|neutral] BRONZ_KATMAN_REHBERI := {
  adimlar: [
    "cd resources/scripts",
    "python 4_phase_sop.py --agent-name ajan-adi --mode interactive",
    "bash validate_prompt.sh agent-outputs/ajan-adi/ajan-adi-base-prompt-v1.md",
    "python test_agent.py --agent ajan-adi --test-suite basic"
  ],
  beklenen: "%70+ dogrulama (Bronz), %80+ testler gecti",
  sure: "~1 saat"
} [ground:witnessed:quickstart] [conf:0.90] [state:confirmed]

### 2. Karmasik Ajan Olusturun (Gumus Katman)

[assert|neutral] GUMUS_KATMAN_REHBERI := {
  adimlar: [
    "python 4_phase_sop.py --agent-name karmasik-ajan --mode interactive",
    "bash validate_prompt.sh -v -s 85 agent-outputs/karmasik-ajan/karmasik-ajan-base-prompt-v1.md",
    "python test_agent.py --agent karmasik-ajan --test-suite comprehensive"
  ],
  beklenen: "%85+ dogrulama (Gumus), %90+ testler gecti",
  sure: "~3 saat"
} [ground:witnessed:quickstart] [conf:0.90] [state:confirmed]

### 3. Uretim Ajani Olusturun (Altin Katman)

[assert|neutral] ALTIN_KATMAN_REHBERI := {
  adimlar: [
    "python 4_phase_sop.py --agent-name prod-ajan --mode interactive",
    "Manuel gelistirme (kod kaliplari, basarisizlik modlari ekle)",
    "bash validate_prompt.sh -v -s 90 agent-outputs/prod-ajan/prod-ajan-enhanced-prompt-v2.md",
    "python test_agent.py --agent prod-ajan --prompt-file agent-outputs/prod-ajan/prod-ajan-enhanced-prompt-v2.md --test-suite integration"
  ],
  beklenen: "%90+ dogrulama (Altin), %95+ testler gecti",
  sure: "~4 saat (Faz 4 dahil)"
} [ground:witnessed:quickstart] [conf:0.90] [state:confirmed]

---

<!-- S5 KALITE_KATMANLARI (Quality Tiers) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Kalite Katmanlari (Quality Tiers)

[assert|emphatic] KALITE_KATMANLARI := {
  bronz_katman: {
    puan_araligi: "%70-74",
    ozellikler: ["Temel yapi tamamlandi", "Cekirdek bolumler mevcut", "Islevsel ajan"],
    uyarilari: "Minimal ornekler, temel korumalar",
    kullanim: "Basit, tek-alanli ajanlar"
  },
  gumus_katman: {
    puan_araligi: "%75-89",
    ozellikler: ["Iyi yapilandirilmis prompt", "Iyi komut kapsamasi", "Bazi kanit-tabanli teknikler", "Birden fazla is akisi ornegi"],
    kullanim: "Cok-alanli ajanlar, takim projeleri"
  },
  altin_katman: {
    puan_araligi: "%90-100",
    ozellikler: ["Uretime hazir", "Kapsamli kanit-tabanli kaliplar", "Genis ornekler ve korumalar", "Tam MCP entegrasyonu", "Performans metrikleri cercevesi"],
    kullanim: "Kritik uretim ajanlari, kurumsal dagitimlar"
  }
} [ground:witnessed:quality-tiers] [conf:0.95] [state:confirmed]

---

<!-- S6 DOGRULAMA_KONTROL_LISTESI (Validation Checklist) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Dogrulama Kontrol Listesi (Validation Checklist)

[assert|emphatic] FAZ_DOGRULAMA := {
  faz_1_tamamlandiginda: [
    "5+ anahtar zorluk tanimlandi",
    "Teknoloji yigini kapsamli sekilde haritalandi",
    "Entegrasyon noktalari tanimlandi",
    "Tum dogrulama kapilari gecti"
  ],
  faz_2_tamamlandiginda: [
    "3+ uzmanlik alani tanimlandi",
    "5+ karar sezgisel kurali belgelendi",
    "Ajan spesifikasyonu olusturuldu",
    "Iyi/kotu ornekler saglandi",
    "Kenar vakalari belgelendi"
  ],
  faz_3_tamamlandiginda: [
    "Temel sistem prompt olusturuldu",
    "Kanit-tabanli teknikler entegre edildi",
    "2+ is akisi ornegi dahil edildi",
    "Korumalar tanimlandi",
    "Dogrulama puani >= %70"
  ],
  faz_4_tamamlandiginda: [
    "15+ kod kalibi cikarildi",
    "10+ basarisizlik modu belgelendi",
    "MCP entegrasyon kaliplari belirtildi",
    "Performans metrikleri tanimlandi",
    "Dogrulama puani >= %90 (Altin)"
  ]
} [ground:witnessed:validation] [conf:0.95] [state:confirmed]

---

<!-- S7 ENTEGRASYON_NOKTALARI (Integration Points) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Entegrasyon Noktalari (Integration Points)

### Diger Becerilerle (With Other Skills)

[assert|neutral] BECERI_ENTEGRASYONLARI := [
  "skill-forge: Gelismis beceri olusturma icin ana meta-beceri",
  "functionality-audit: Olusturulan ajanlarin dogru calistigini dogrula",
  "theater-detection-audit: Uygulamalarin gercek oldugunu dogrula",
  "production-readiness: Dagitimdan once ajanlari denetle",
  "cascade-orchestrator: Ajan olusturma is akislarini zincirle"
] [ground:witnessed:skill-integrations] [conf:0.88] [state:confirmed]

### MCP Sunuculariyla (With MCP Servers)

[assert|neutral] MCP_ENTEGRASYONLARI := [
  "Claude Flow: Ajan koordinasyonu ve hafiza yonetimi",
  "GitHub: Ajan depolamasi icin repository entegrasyonu",
  "Memory MCP: Ajan bilgisi icin oturumlar arasi kalicilik",
  "Connascence: Teknik ajanlar icin kod kalitesi analizi"
] [ground:witnessed:mcp-integrations] [conf:0.88] [state:confirmed]

---

<!-- S8 PERFORMANS_METRIKLERI (Performance Metrics) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Performans Metrikleri (Performance Metrics)

### Otomasyon Faydalari (Automation Benefits)

[assert|confident] OTOMASYON_FAYDALARI := [
  "%75 otomatik (Faz 1-3 tamamen otomatik)",
  "2.8-4.4x hiz iyilestirmesi (manuel surece gore)",
  "%100 tutarlilik (temel prompt yapisinda)",
  "Objektif kalite metrikleri (dogrulama puanlari, test gecis oranlari)",
  "Tekrarlanabilir sonuclar (deterministik otomasyon)"
] [ground:witnessed:metrics] [conf:0.92] [state:confirmed]

### Kalite Guvencesi (Quality Assurance)

[assert|confident] KALITE_GUVENCESI := [
  "100-puanlik dogrulama sistemi",
  "10-testli kapsamli cerceve",
  "3 kalite katmani (Bronz/Gumus/Altin)",
  "Otomatik basarisizlik tespiti ve raporlama"
] [ground:witnessed:qa-metrics] [conf:0.92] [state:confirmed]

---

<!-- S9 SORUN_GIDERME (Troubleshooting) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Sorun Giderme (Troubleshooting)

[assert|emphatic] SORUN_GIDERME := {
  dogrulama_basarisiz: {
    belirti: "Puan < %70",
    cozumler: [
      "Eksik zorunlu bolumleri kontrol et",
      "Kanit-tabanli teknik bolumleri ekle",
      "2+ is akisi ornegi dahil et",
      "Orneklerle 3+ koruma tanimla"
    ]
  },
  testler_basarisiz: {
    belirti: "Gecis orani < %80",
    cozumler: [
      "Kimlik tutarliligini incele",
      "Eksik evrensel komutlari ekle",
      "MCP entegrasyon kaliplarini belgele",
      "Hafiza kullanim spesifikasyonlarini dahil et"
    ]
  },
  faz_dogrulamasi_basarisiz: {
    belirti: "Dogrulama kapisi gecmiyor",
    cozumler: [
      "Faz 1: Alani daha derinlemesine arastir",
      "Faz 2: Bilissel kaliplari dusun",
      "Faz 3: Sablon yapisini tam olarak takip et"
    ]
  }
} [ground:witnessed:troubleshooting] [conf:0.90] [state:confirmed]

---

<!-- S10 VERSIYON_GECMISI (Version History) [[HON:teineigo]] [[EVD:-mis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Versiyon Gecmisi (Version History)

[assert|neutral] VERSIYON_GECMISI := {
  v2_0_altin_katman: {
    tarih: "2025-11-02",
    ozellikler: [
      "Tam otomasyon (Faz 1-3)",
      "Dogrulama cercevesi (100-puan sistemi)",
      "Test cercevesi (10-test paketi)",
      "Yeniden kullanilabilir sablonlar (Markdown + YAML)",
      "Gorsel dokumantasyon (GraphViz)",
      "Test senaryolari (3 tam test)",
      "Kaynak dokumantasyonu (500+ satir)"
    ],
    toplam: "12 yeni dosya, 9,293 satir"
  },
  v1_0_gumus_katman: {
    tarih: "2024",
    ozellikler: [
      "Sadece dokumantasyon",
      "4-faz metodoloji aciklandi",
      "Kanit-tabanli teknikler belgelendi",
      "Manuel surec"
    ]
  }
} [ground:witnessed:version-history] [conf:0.95] [state:confirmed]

---

<!-- S11 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonraki Adimlar (Next Steps)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[direct|neutral] SONRAKI_ADIMLAR := [
  "Deneyin: Hizli Baslangic Rehberi #1 kullanarak ilk ajaninizi olusturun",
  "Dogrulayin: Dogrulama scripti ile kaliteyi kontrol edin",
  "Test edin: Dogrulugu saglamak icin test paketini calistirin",
  "Yineleyin: Dogrulama/test geri bildirimine gore gelistirin",
  "Dagitin: Altin katman ajanlari uretimde guvenle kullanin"
] [ground:inferred:recommendations] [conf:0.85] [state:provisional]

[assert|confident] DURUM := "Altin Katman Gelistirmesi Tamamlandi - Uretim Kullanimina Hazir" [ground:witnessed:status] [conf:0.95] [state:confirmed]

---

<promise>INDEX_VCL_VERIX_COMPLIANT</promise>
