# Ajan Olusturucu - Gumus Katman Dokumantasyonu (Agent Creator - Silver Tier Documentation)

---
<!-- S1.0 KANITSAL CERCEVE (Evidential Frame Activation) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_document]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- S2.0 GENEL BAKIS (Overview) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_overview]] [[SPC:kuzey/sistem-merkezi]] -->
---

## Genel Bakis Cercevesi (Overview Frame)
Bu beceri kanita dayali istem teknikleri ile uretim kalitesinde ajanlar olusturur.

<!-- [[MOR:root:A-J-N]] Ajan = root morpheme for agent-actor-executor -->
<!-- [[COM:Ajan+Olusturucu+Beceri]] German compound: Agentenerstellungsfaehigkeit -->
[assert|neutral] BECERI_TANIMI := {
  ad: "Agent Creator",
  tur: "Dokumcu Beceri",
  amac: "Desktop `.claude-flow` kaynakli kanitlanmis 4-faz SOP metodolojisi ile ozellestirilmis AI ajanlari olusturma",
  bilesenleri: [
    "Kanita dayali istem teknikleri",
    "Claude Agent SDK uygulamasi",
    "Sistematik alan analizi",
    "Uretim hazir korumalar"
  ]
} [ground:witnessed:skill-manifest] [conf:0.92] [state:confirmed]

---
<!-- S3.0 HIZLI BASLANGIÇ (Quick Start) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_quickstart]] -->
---

## Hizli Baslangic Cercevesi (Quick Start Frame)
Temel kullanim ve hiz-kosumu yontemleri.

### Temel Kullanim

<!-- [[MOR:root:K-L-L]] Kullanim = root morpheme for usage-use-application -->
[define|neutral] TEMEL_KULLANIM := {
  claude_code: "'Yeni pazarlama uzmani ajani olustur'",
  skill_tool: "Skill('agent-creator')"
} [ground:witnessed:usage-pattern] [conf:0.95] [state:confirmed]

### Hiz-Kosumu (Tecrubeli Kullanicilar)

<!-- [[MOR:root:H-Z-S]] Hiz = root morpheme for speed-fast-quick -->
[assert|neutral] HIZ_KOSUMU := {
  hedef_sure: "2 saat",
  fazlar: [
    {ad: "Birlesik Faz 1+2", sure: "30 dk", islem: "Alan analizi + spesifikasyon"},
    {ad: "Faz 3", sure: "30 dk", islem: "Sablondan temel sistem istemi"},
    {ad: "Faz 4", sure: "45 dk", islem: "Kod desenleri + hata modlari"},
    {ad: "Test", sure: "15 dk", islem: "Hizli dogrulama paketi"}
  ]
} [ground:witnessed:speed-run-guide] [conf:0.88] [state:confirmed]

### Ilk Kez Tam Surec

<!-- [[MOR:root:T-M-M]] Tam = root morpheme for complete-full-whole -->
[assert|neutral] TAM_SUREC := {
  toplam_sure: "3.5-5.5 saat",
  adimlar: [
    {faz: "Faz 1: Alan Analizi", sure: "30-60 dk"},
    {faz: "Faz 2: Uzmanlik Cikartma", sure: "30-45 dk"},
    {faz: "Faz 3: Mimari Tasarim", sure: "45-60 dk"},
    {faz: "Faz 4: Teknik Gelistirme", sure: "60-90 dk"},
    {faz: "SDK Uygulamasi", sure: "30-60 dk"},
    {faz: "Test ve Dogrulama", sure: "30-45 dk"},
    {faz: "Dokumantasyon", sure: "15-30 dk"}
  ]
} [ground:witnessed:full-process-guide] [conf:0.88] [state:confirmed]

---
<!-- S4.0 TEMEL OZELLIKLER (Key Features) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_feature]] -->
---

## Temel Ozellikler Cercevesi (Key Features Frame)
4-faz metodolojisi ve destekleyen teknikler.

### 4-Faz Metodolojisi

<!-- [[MOR:root:F-Z-M]] Faz = root morpheme for phase-stage-step -->
<!-- [[COM:Dort+Faz+Metodoloji]] German compound: Vierphasenmethodik -->
[define|neutral] DORT_FAZ_METODOLOJISI := {
  faz_1: {
    ad: "Ilk Analiz ve Niyet Cozumleme",
    islemler: ["Sistematik arastirma ile derin alan anlayisi", "Teknoloji yigini esleme", "Entegrasyon noktasi tanimlama"],
    cikti: "Alan analizi belgesi"
  },
  faz_2: {
    ad: "Meta-Bilissel Cikartma",
    islemler: ["Uzmanlik alani tanimlama", "Ajan spesifikasyonu olusturma", "Karar cercevesi dokumantasyonu"],
    cikti: "Tam ajan spesifikasyonu"
  },
  faz_3: {
    ad: "Ajan Mimari Tasarimi",
    islemler: ["Sistem istemi yapi tasarimi", "Kanita dayali teknik entegrasyonu", "Kalite standartlari ve korumalar"],
    cikti: "Temel sistem istemi v1.0"
  },
  faz_4: {
    ad: "Derin Teknik Gelistirme",
    islemler: ["Kod deseni cikartma", "Kritik hata modu dokumantasyonu", "MCP entegrasyon desenleri", "Performans metrik tanimlama"],
    cikti: "Gelistirilmis sistem istemi v2.0"
  }
} [ground:witnessed:methodology-spec] [conf:0.90] [state:confirmed]

### Kanita Dayali Istem Teknikleri

<!-- [[MOR:root:K-N-T]] Kanit = root morpheme for evidence-proof-basis -->
[assert|neutral] KANIT_DAYALI_TEKNIKLER := {
  tekniker: [
    {ad: "Oz-Tutarlilik Dogrulama", aciklama: "Teslimat sonlandirmadan once cok-acili dogrulama"},
    {ad: "Dusunce-Programi Ayristirma", aciklama: "Yurutmeden once karmasik gorev bolme"},
    {ad: "Planla-ve-Coz Yurutme", aciklama: "Her adimda dogrulama ile standart is akisi"}
  ]
} [ground:reported:prompting-research] [conf:0.85] [state:confirmed]

### Claude Agent SDK Entegrasyonu

<!-- [[MOR:root:E-N-T]] Entegrasyon = root morpheme for integration-connection-link -->
[assert|neutral] SDK_ENTEGRASYONU := {
  diller: ["TypeScript", "Python"],
  ornek_kullanim: {
    model: "claude-sonnet-4-5",
    systemPrompt: "enhancedPromptV2",
    permissionMode: "acceptEdits",
    allowedTools: ["Read", "Write", "Bash"],
    mcpServers: ["claude-flow@alpha"]
  }
} [ground:witnessed:sdk-docs] [conf:0.88] [state:confirmed]

### Ajan Uzlasma Destegi

<!-- [[MOR:root:U-Z-L]] Uzlasma = root morpheme for specialization-focus-niche -->
[define|neutral] AJAN_TURLERI := {
  turler: [
    {ad: "Analitik Ajanlar", odak: "Kanit degerlendirme, veri kalite standartlari"},
    {ad: "Uretici Ajanlar", odak: "Kalite kriterleri, sablon desenleri, iyilestirme"},
    {ad: "Teshis Ajanlari", odak: "Sorun desenleri, hata ayiklama, hipotez testi"},
    {ad: "Orkestrasyon Ajanlari", odak: "Is akisi desenleri, bagimlilik yonetimi, koordinasyon"}
  ]
} [ground:witnessed:agent-types-spec] [conf:0.90] [state:confirmed]

---
<!-- S5.0 ORNEKLER (Examples) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] -->
---

## Ornekler Cercevesi (Examples Frame)
Kapsamli ornekler examples/ dizininde mevcuttur. Zaversheno (Tamamlandi).

<!-- [[MOR:root:O-R-N]] Ornek = root morpheme for example-sample-instance -->
[assert|neutral] ORNEK_DOSYALARI := {
  ornekler: [
    {dosya: "examples/example-1-basic.md", aciklama: "Basit uzman ajan olusturma (Pazarlama Uzmani)"},
    {dosya: "examples/example-2-coordinator.md", aciklama: "Cok-ajanli koordinator (DevOps Koordinatoru)"},
    {dosya: "examples/example-3-hybrid.md", aciklama: "Hibrit cok-alanli ajan (Full-Stack Gelistirici)"}
  ]
} [ground:witnessed:examples-dir] [conf:0.95] [state:confirmed]

---
<!-- S6.0 ENTEGRASYON (Integration) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_integration]] -->
---

## Entegrasyon Cercevesi (Integration Frame)
Claude Code Task araci ve MCP entegrasyon desenleri.

### Claude Code Task Araci

<!-- [[MOR:root:G-R-V]] Gorev = root morpheme for task-mission-job -->
[define|neutral] TASK_ARACI_KULLANIMI := {
  temel_kullanim: "Task('Pazarlama Uzmani', 'Pazar trendlerini analiz et ve kampanya stratejisi olustur', 'marketing-specialist')",
  parametre_sirasi: ["ajan_adi", "gorev_aciklamasi", "ajan_turu"]
} [ground:witnessed:task-tool-spec] [conf:0.90] [state:confirmed]

### MCP Arac Koordinasyonu

[assert|neutral] MCP_KOORDINASYONU := {
  swarm_init: "mcp__claude-flow__swarm_init({ topology: 'mesh', maxAgents: 6 })",
  agent_spawn: "mcp__claude-flow__agent_spawn({ type: 'specialist' })",
  task_execute: "Task('Uzman ajan', 'Alana ozel gorevi tamamla', 'specialist')"
} [ground:witnessed:mcp-docs] [conf:0.88] [state:confirmed]

### Memory MCP Entegrasyonu

<!-- [[MOR:root:B-L-K]] Bellek = root morpheme for memory-storage-retention -->
[assert|neutral] MEMORY_ENTEGRASYONU := {
  depolama: {
    fonksiyon: "mcp__memory-mcp__memory_store",
    metadata: {
      key: "marketing-specialist/campaign-123/audience-analysis",
      namespace: "agents/marketing",
      layer: "mid-term",
      category: "analysis"
    }
  },
  arama: {
    fonksiyon: "mcp__memory-mcp__vector_search",
    query: "onceki kampanya hedefleme stratejileri",
    limit: 10
  }
} [ground:witnessed:memory-mcp-docs] [conf:0.88] [state:confirmed]

---
<!-- S7.0 DOGRULAMA VE KALITE (Validation & Quality) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_quality]] -->
---

## Dogrulama ve Kalite Cercevesi (Validation & Quality Frame)
Her faz icin dogrulama kapilari.

### Dogrulama Kapilari

<!-- [[MOR:root:K-P-L]] Kapi = root morpheme for gate-door-checkpoint -->
<!-- [[COM:Dogrulama+Kapi+Sistemi]] German compound: Validierungstorsystem -->
[define|neutral] DOGRULAMA_KAPILARI := {
  faz_1_kapisi: [
    "Alani belirli, teknik terimlerle tanimlayabilir",
    "5+ temel zorluk tanimlandi",
    "Teknoloji yigini kapsamli eslendi",
    "Entegrasyon gereksinimleri netlesti"
  ],
  faz_2_kapisi: [
    "3+ uzmanlik alani tanimlandi",
    "5+ karar bulussal yontemi belgelendi",
    "Tam ajan spesifikasyonu olusturuldu",
    "Ornekler kalite standartlarini gosterir"
  ],
  faz_3_kapisi: [
    "Sistem istemi sablon yapisini takip eder",
    "Tum Faz 2 uzmanligi gomuldu",
    "Kanita dayali teknikler entegre edildi",
    "Korumalar tanimlanan hata modlarini kapsar",
    "2+ is akisi ornegi tam komutlarla"
  ],
  faz_4_kapisi: [
    "Kod desenleri dosya/satir referanslari icerir",
    "Hata modlari tespit + onleme icin",
    "MCP desenleri tam sozdizimi gosterir",
    "Performans metrikleri tanimlandi",
    "Ajan metrikler araciligiyla oz-iyilesebilir"
  ]
} [ground:witnessed:gate-config] [conf:0.90] [state:confirmed]

### Test Kontrol Listesi

[define|neutral] TEST_KONTROL_LISTESI := {
  kontroller: [
    {alan: "Kimlik", kriter: "Ajan tutarli rol korur"},
    {alan: "Komutlar", kriter: "Evrensel komutlari dogru kullanir"},
    {alan: "Uzman Becerileri", kriter: "Alan uzmanligi sergiler"},
    {alan: "MCP Entegrasyonu", kriter: "Bellek ve araclar araciligiyla koordine eder"},
    {alan: "Korumalar", kriter: "Tanimlanan hata modlarini onler"},
    {alan: "Is Akislari", kriter: "Ornekleri basariyla yurutur"},
    {alan: "Metrikler", kriter: "Performans verisini takip eder"},
    {alan: "Kod Desenleri", kriter: "Faz 4'ten tam desenleri uygular"},
    {alan: "Hata Isleme", kriter: "Uygun sekilde tirmandirır"},
    {alan: "Tutarlilik", kriter: "Tekrarda kararli ciktilar uretir"}
  ]
} [ground:witnessed:test-checklist] [conf:0.90] [state:confirmed]

---
<!-- S8.0 REFERANSLAR (References) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_reference]] -->
---

## Referanslar Cercevesi (References Frame)
references/ dizininde destekleyici dokumantasyon.

<!-- [[MOR:root:R-F-R]] Referans = root morpheme for reference-source-citation -->
[assert|neutral] REFERANS_DOSYALARI := {
  dosyalar: [
    {yol: "references/best-practices.md", aciklama: "Kanita dayali istem ilkeleri ve optimizasyon teknikleri"},
    {yol: "references/agent-types.md", aciklama: "Uzman, Koordinator ve Hibrit desenleri icin detayli spesifikasyonlar"},
    {yol: "references/integration-patterns.md", aciklama: "MCP arac kullanim desenleri ve bellek koordinasyonu"}
  ]
} [ground:witnessed:references-dir] [conf:0.95] [state:confirmed]

---
<!-- S9.0 IS AKISI GORSELLESTIRME (Workflow Visualization) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_visualization]] -->
---

## Is Akisi Gorsellestirme Cercevesi (Workflow Visualization Frame)
GraphViz diyagrami tam 4-faz is akisini gosterir.

<!-- [[MOR:root:G-R-S]] Gorsel = root morpheme for visual-image-graphic -->
[assert|neutral] GORSELLESTIRME := {
  dosya: "graphviz/workflow.dot",
  olusturma_komutu: "dot -Tpng graphviz/workflow.dot -o workflow.png"
} [ground:witnessed:graphviz-file] [conf:0.95] [state:confirmed]

---
<!-- S10.0 PERFORMANS METRIKLERI (Performance Metrics) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_metric]] -->
---

## Performans Metrikleri Cercevesi (Performance Metrics Frame)
Yerlesik metriklerle ajan performansi takibi.

<!-- [[MOR:root:P-R-F]] Performans = root morpheme for performance-execution-achievement -->
[define|neutral] PERFORMANS_METRIKLERI := {
  gorev_tamamlama: {
    metrikler: ["tasks-completed", "task-duration"],
    birimler: ["adet", "milisaniye"]
  },
  kalite: {
    metrikler: ["validation-passes", "escalations", "error-rate"],
    birimler: ["adet", "adet", "basarisizlik/deneme"]
  },
  verimlilik: {
    metrikler: ["commands-per-task", "mcp-calls"],
    birimler: ["ortalama komut", "arac kullanim sikligi"]
  }
} [ground:witnessed:metrics-spec] [conf:0.88] [state:confirmed]

---
<!-- S11.0 SUREKLI IYILESTIRME (Continuous Improvement) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_improvement]] -->
---

## Surekli Iyilestirme Cercevesi (Continuous Improvement Frame)
Bakim dongusu ve surum kontrol.

### Bakim Dongusu

<!-- [[MOR:root:B-K-M]] Bakim = root morpheme for maintenance-upkeep-care -->
[define|neutral] BAKIM_DONGUSU := {
  adimlar: [
    {ad: "Metrik Inceleme", sure: "Haftalik", islem: "Ajan performans metriklerini incele"},
    {ad: "Basarisizlik Analizi", sure: "Surekli", islem: "Yeni hata modlarini belgele ve duzelt"},
    {ad: "Desen Guncellemeleri", sure: "Aylik", islem: "Yeni kesfedilen kod desenlerini ekle"},
    {ad: "Is Akisi Optimizasyonu", sure: "Ceyreklik", islem: "Kullanim kaliplarina gore iyilestir"}
  ]
} [ground:witnessed:maintenance-cycle] [conf:0.88] [state:confirmed]

### Surum Kontrol

<!-- [[MOR:root:S-R-M]] Surum = root morpheme for version-release-mark -->
[assert|neutral] SURUM_SKALASI := {
  v1_0: "Faz 3'ten temel istem",
  v1_x: "Testten kucuk iyilestirmeler",
  v2_0: "Faz 4 desenleri ile gelistirilmis",
  v2_x: "Uretim yinelemeleri ve iyilestirmeler"
} [ground:witnessed:version-convention] [conf:0.90] [state:confirmed]

---
<!-- S12.0 DESTEK VE KAYNAKLAR (Support & Resources) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_resource]] -->
---

## Destek ve Kaynaklar Cercevesi (Support & Resources Frame)
Ilgili dokumantasyon ve dis kaynaklar.

<!-- [[MOR:root:D-S-T]] Destek = root morpheme for support-help-assistance -->
[assert|neutral] KAYNAKLAR := {
  ic_belgeler: [
    {ad: "Tam Beceri Dokumantasyonu", yol: "skill.md"},
    {ad: "Resmi SOP Kaynagi", yol: "Desktop `.claude-flow/` dokumantasyonu"}
  ],
  dis_kaynaklar: [
    {ad: "Claude Agent SDK", url: "https://github.com/anthropics/claude-agent-sdk"},
    {ad: "Claude Flow MCP", url: "https://github.com/ruvnet/claude-flow"}
  ]
} [ground:witnessed:resource-list] [conf:0.95] [state:confirmed]

---
<!-- S13.0 NE ZAMAN KULLANILIR (When to Use) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_usage]] -->
---

## Ne Zaman Kullanilir Cercevesi (When to Use Frame)
Uygun kullanim durumlari.

<!-- [[MOR:root:K-L-N]] Kullanim = root morpheme for usage-use-application -->
[assert|neutral] KULLANIM_DURUMLARI := {
  uygun: [
    "Derinlemesine gomulu alan bilgisi ile proje-ozel ajanlar olusturma",
    "Tutarli davranis gerektiren yinelenen gorevler icin ajanlar olusturma",
    "Performans optimizasyonu icin mevcut ajanlari yeniden yazma",
    "Sirali veya paralel koordinasyonlu cok-ajanli is akislari olusturma",
    "MCP serverlari ve Claude Flow ile entegre olacak ajanlar"
  ]
} [ground:witnessed:use-cases] [conf:0.90] [state:confirmed]

---
<!-- S14.0 SONUC (Summary) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
---

## Beceri Ozeti Cercevesi (Skill Summary Frame)
Zaversheno. Eta dokumentatsiya byla uspeshno zakonchena. (Rusca: Tamamlandi. Bu dokumantasyon basariyla bitirildi.)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result-outcome -->
<!-- [[COM:Ajan+Olusturucu+Ozet]] German compound: Agentenerstellerzusammenfassung -->
[assert|confident] BECERI_OZETI := {
  amac: "Desktop `.claude-flow` kaynakli resmi 4-faz SOP metodolojisi ile uretim kalitesinde ajanlar olusturma", // Turkish: purpose
  metodoloji: "Kanita dayali istem teknikleri (oz-tutarlilik, PoT, planla-ve-coz)", // Turkish: methodology
  ciktilar: [
    "Claude Agent SDK uygulamasi (TypeScript + Python)",
    "Uretim dogrulama ve test cerceveleri",
    "Metrikler araciligiyla surekli iyilestirme",
    "90+ uzman ajan olusturma kapasitesi"
  ],
  kalite_kapilari: [
    "4-faz dogrulama kapilari",
    "10-madde test kontrol listesi",
    "Performans metrik takibi"
  ],
  sonuc: "Cesitli alanlar ve is akislarinda tutarli yuksek kaliteli sonuclar veren uretim-hazir ajanlar"
} [ground:witnessed:readme-execution] [conf:0.90] [state:confirmed]

---
*Soz (Promise): `<promise>README_VCL_V3.1.1_VERIX_COMPLIANT</promise>`*
