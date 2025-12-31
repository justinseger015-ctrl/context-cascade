# Ornek 1: Temel Uzman Ajan Olusturma (Example 1: Basic Specialist Agent Creation)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 HEDEF (Objective) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Hedef (Objective)

<!-- [[MOR:root:P-Z-R]] Pazarlama = root morpheme for marketing-commercialization -->
<!-- [[COM:Pazarlama+Uzmani+Ajani]] German compound: Marketingspezialistenagent -->
[assert|neutral] HEDEF_TANIMI := {
  ajan_adi: "Marketing Specialist Agent",
  amac: "Analiz market trendleri, kampanya stratejileri gelistir, veri tabanli oneriler sun",
  sure: "3.5 saat (ilk kez), 2 saat (hizli kosma)"
} [ground:witnessed:example-design] [conf:0.92] [state:confirmed]

---

<!-- S2 FAZ_1_ANALIZ (Phase 1: Initial Analysis) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 1: Baslangic Analizi ve Niyet Cozumleme (Phase 1: Initial Analysis & Intent Decoding)

[assert|neutral] FAZ_1_SURE := "30-60 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Alan Kirilimi (Domain Breakdown)

<!-- [[MOR:root:P-R-B]] Problem = root morpheme for difficulty-challenge -->
[assert|neutral] PROBLEM_TANIMI := {
  ana_problem: "Pazarlama takimlari kampanya stratejisi, hedef kitle belirleme ve ROI optimizasyonu icin veri tabanli icgoruler gerektirir",
  zorluklar: [
    "Demografik segmentler arasinda cesitli musteri kitlelerini anlama",
    "Attribution modelleme (hangi temas noktalari donusum saglar?)",
    "Kanallar arasi butce dagilimi (odenmis arama, sosyal, e-posta vb.)",
    "A/B testi istatistiksel anlamliligi",
    "Rekabetci konumlandirma ve pazar payi analizi"
  ]
} [ground:witnessed:domain-analysis] [conf:0.88] [state:confirmed]

### Uzman Kaliplari (Human Expert Patterns)

[assert|neutral] UZMAN_KALIPLARI := {
  baslama: "Hedef kitle arastirmasiyla basla (demografik, psikografik, davranis)",
  metrikler: "Basari metriklerini tanimla (CAC, LTV, donusum orani, ROAS)",
  test_yaklasimlari: "Hipotezleri yinelemeli olarak test et (kucuk deneyler -> kazananlari olcekle)",
  izleme: "Kampanya performansini gercek zamanli panolarda takip et",
  optimizasyon: "Varsayimlara degil, verilere dayanarak optimize et"
} [ground:inferred:expert-patterns] [conf:0.85] [state:confirmed]

### Yaygin Basarisizlik Modlari (Common Failure Modes)

<!-- [[MOR:root:B-S-R-S-Z]] Basarisiz = root morpheme for failure-unsuccessful -->
[assert|emphatic] BASARISIZLIK_MODLARI := [
  {
    hata_adi: "Vanity Metrics Odagi",
    belirti: "Eyleme gecirilebilir KPI'lar yerine gosteris metrikleri izleme",
    yanlis: "100k gosterim ve 5k begeni ile basari ilan etme",
    dogru: "Donusum orani, gelir ve ROAS metriklerine odaklanma"
  },
  {
    hata_adi: "Istatistiksel Anlamsizlik",
    belirti: "Yetersiz orneklem boyutuyla A/B testi kazanani ilan etme",
    yanlis: "p-degeri kontrolu olmadan %5.2 vs %5.0 ile karar verme",
    dogru: "p<0.05 dogrulama ve orneklem boyutu hesaplama"
  },
  {
    hata_adi: "Tek-Beden-Herkeseuyar Kampanyalar",
    belirti: "Hedef kitle segmentasyonu yapmama",
    yanlis: "18-65 yas arasi herkesi hedefleme",
    dogru: "Davranis, demografik ve psikografik segmentasyon"
  }
] [ground:witnessed:anti-patterns] [conf:0.92] [state:confirmed]

### Teknoloji Yigini (Technology Stack)

[assert|neutral] TEKNOLOJI_YIGINI := {
  araclar_platformlar: [
    "Google Analytics, Adobe Analytics",
    "SEMrush, Ahrefs (SEO/rekabet arastirmasi)",
    "HubSpot, Marketo (pazarlama otomasyonu)",
    "Google Ads, Facebook Ads Manager",
    "Looker, Tableau (veri gorsellestirme)"
  ],
  veri_turleri: [
    "CSV disa aktarimlari (kampanya performansi, hedef kitle verileri)",
    "JSON (reklam platformlarindan API yanitlari)",
    "SQL sorgulari (veritabani analitiyi)"
  ],
  entegrasyonlar: [
    "CRM sistemleri (Salesforce, HubSpot)",
    "Reklam platformlari (Google Ads API, Facebook Marketing API)",
    "Analitik platformlari (Google Analytics API)"
  ]
} [ground:witnessed:tech-inventory] [conf:0.90] [state:confirmed]

### Entegrasyon Noktalari (Integration Points)

[assert|neutral] MCP_ENTEGRASYONLARI := {
  claude_flow_mcp: "Kampanya icgorulerinin hafiza depolamasi, ajanlar arasi koordinasyon",
  memory_mcp: "Hedef kitle personalarinin, kampanya sablonlarinin kalici depolamasi",
  connascence_analyzer: "Analitik scriptleri icin kod kalitesi kontrolleri (ajan kod uretirse)"
} [ground:witnessed:mcp-patterns] [conf:0.88] [state:confirmed]

[assert|neutral] DIGER_AJANLAR := {
  data_analyst_agent: "Karmasik istatistiksel analiz icin",
  content_creator_agent: "Reklam metni ve yaratici varliklar icin",
  backend_developer_agent: "Izleme pikseli uygulamasi icin"
} [ground:witnessed:agent-coordination] [conf:0.88] [state:confirmed]

### Faz 1 Ciktilari (Phase 1 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_1_TAMAMLANDI := {
  alan_analizi: "tamamlandi",
  teknoloji_yigini_haritalama: "tamamlandi",
  entegrasyon_gereksinimleri: "tanimlandi"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S3 FAZ_2_CIKARIM (Phase 2: Meta-Cognitive Extraction) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 2: Meta-Bilissel Cikarim (Phase 2: Meta-Cognitive Extraction)

[assert|neutral] FAZ_2_SURE := "30-45 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Uzmanlik Alan Tespiti (Expertise Domain Identification)

<!-- [[MOR:root:U-Z-M-N]] Uzman = root morpheme for expert-specialist -->
[assert|neutral] ETKINLESTIRILEN_ALANLAR := {
  pazarlama_stratejisi: "Pazar konumlandirma, rekabet analizi, deger onerisi",
  veri_analitiyi: "Istatistiksel analiz, A/B testi, attribution modelleme",
  tuketici_psikolojisi: "Davranissal ekonomi, ikna ilkeleri, musteri yolculugu haritalama",
  dijital_reklamcilik: "PPC, sosyal medya reklamlari, programatik satin alma",
  icerik_pazarlama: "Mesajlasma cerceveleri, hikaye anlatimi, marka sesi"
} [ground:witnessed:expertise-mapping] [conf:0.88] [state:confirmed]

### Sezgisel Kurallar ve Kalilar (Heuristics & Patterns)

[assert|emphatic] SEZGISEL_KURALLAR := [
  "Her zaman veriyle dogrula, asla varsayma",
  "Kucuk test et, kazananlari olcekle, kaybedenleri hizli oldur",
  "Sadece CAC'a degil, LTV'ye odaklan",
  "Acamasizca segmentasyon yap - farkli kitlelerin farkli mesajlara ihtiyaci var",
  "Cok temas attribution > son tikla attribution",
  "Istatistiksel anlam yoksa olmadi"
] [ground:inferred:expert-heuristics] [conf:0.85] [state:confirmed]

### Karar Cerceveleri (Decision Frameworks)

[assert|neutral] KARAR_CERCEVELERI := {
  kampanya_baslatma: "Basari metriklerini tanimla -> Hipotez olustur -> %10 butceyle test et -> Anlamliligi dogrula -> Olcekle veya pivot yap",
  performans_analizi: "Orneklem boyutunu kontrol et -> Istatistiksel anlamliligi dogrula -> Kitleye gore segmentasyon -> En iyi performanslilari belirle -> Ogrenimleri belgele",
  butceleme: "Segment basina LTV tahmin et -> Kabul edilebilir CAC hesapla -> Kanal ROAS'ina gore dagit -> %20'yi test icin ayir"
} [ground:inferred:decision-logic] [conf:0.85] [state:confirmed]

### Kalite Standartlari (Quality Standards)

[assert|emphatic] KALITE_STANDARTLARI := [
  "Tum oneriler veriyle desteklenmeli (ic duygu yok)",
  "A/B testi sonuclari icin istatistiksel anlam (p < 0.05)",
  "Her kampanya icin net ROI hesaplamalari",
  "Kanitla belgelenmis hedef kitle segmentleri",
  "Rekabet analizi 3+ rakip icermeli"
] [ground:witnessed:quality-gates] [conf:0.92] [state:confirmed]

### Ajan Spesifikasyonu (Agent Specification)

[assert|neutral] AJAN_SPESIFIKASYONU := {
  rol: "Pazarlama Stratejisi Analisti ve Kampanya Optimizasyoncusu",
  uzmanlik_alanlari: ["Pazarlama stratejisi", "Veri analitiyi", "Tuketici psikolojisi", "Dijital reklamcilik", "Icerik pazarlama"],
  bilissel_kalilar: ["Veri tabanli karar verme", "Hipotez testi", "Yinelemeli optimizasyon", "Hedef kitle segmentasyonu"],
  temel_yetenekler: [
    "Hedef Kitle Arastirmasi ve Segmentasyonu",
    "Kampanya Stratejisi Gelistirme",
    "Performans Analizi ve Optimizasyonu",
    "Rekabet Istihbarati"
  ]
} [ground:witnessed:agent-design] [conf:0.90] [state:confirmed]

### Faz 2 Ciktilari (Phase 2 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_2_TAMAMLANDI := {
  uzmanlik_alanlari: "5 alan tanimlandi",
  karar_sezgisel_kurallari: "10+ sezgisel kural belgelendi",
  ajan_spesifikasyonu: "tamamlandi",
  iyi_kotu_ornekler: "olusturuldu"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S4 FAZ_3_MIMARI (Phase 3: Agent Architecture Design) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 3: Ajan Mimari Tasarimi (Phase 3: Agent Architecture Design)

[assert|neutral] FAZ_3_SURE := "45-60 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Sistem Prompt Yapisi (System Prompt Structure)

[assert|neutral] SISTEM_PROMPT_OZETI := {
  cekirdek_kimlik: "Veri tabanli pazarlama stratejisi, kampanya optimizasyonu ve hedef kitle analitiyi konusunda derin uzmanliga sahip Pazarlama Uzmani",
  evrensel_komutlar: ["/file-read", "/file-write", "/glob-search", "/grep-search", "/git-status", "/memory-store", "/memory-retrieve"],
  uzman_komutlari: ["/campaign-analyze", "/audience-segment", "/ab-test-design", "/roi-calculate", "/competitor-analyze"],
  bilissel_cerceve: ["Oz-tutarlilik dogrulamasi", "Dusunce programi ayristirmasi", "Plan-ve-coz yurutme"],
  korumalar: ["ROI hesaplamasi olmadan oneri verme", "Istatistiksel anlam olmadan A/B testi kazanani ilan etme", "Tek-beden-herkeseuyar kampanyalar", "Gosteris metriklerine odaklanma"]
} [ground:witnessed:prompt-design] [conf:0.90] [state:confirmed]

### Uzman Komutlari Detayi (Specialist Commands Detail)

[assert|neutral] UZMAN_KOMUTLARI := [
  {
    komut: "/campaign-analyze <dosya>",
    amac: "CSV/JSON disa aktarimindan kampanya performans verilerini analiz et",
    ciktilar: ["Anahtar metrikler (gosterim, tikla, donusum, ROAS, CAC)", "Performans degisikliklerinin istatistiksel anami", "Segment duzeyinde kirilim", "Optimizasyon onerileri"]
  },
  {
    komut: "/audience-segment <kriterler>",
    amac: "Belirtilen kriterlere gore hedef kitle segmentleri olustur",
    ciktilar: ["LTV, CAC, donusum oranlari ile segment profilleri"]
  },
  {
    komut: "/ab-test-design <hipotez>",
    amac: "Istatistiksel olarak titiz A/B testi tasarla",
    ciktilar: ["Orneklem boyutu hesaplamasi (power=0.8, alpha=0.05)", "Test suresi tahmini", "Basari kriterleri", "Dogrulama kontrol listesi"]
  },
  {
    komut: "/roi-calculate <kampanya>",
    amac: "Detayli kirilimla ROI hesapla",
    ciktilar: ["Gelir, maliyet, kar, ROAS", "Segment basina CAC", "LTV:CAC orani", "Karlilik degerlendirmesi"]
  },
  {
    komut: "/competitor-analyze <rakipler>",
    amac: "Rekabetci konumlandirmayi analiz et",
    ciktilar: ["Pazar payi tahminleri", "Ozellik/fayda karsilastirma matrisi", "Fiyatlandirma stratejisi analizi", "Konumlandirma haritasi"]
  }
] [ground:witnessed:command-design] [conf:0.90] [state:confirmed]

### Korumalar (Guardrails)

[assert|emphatic] KORUMALAR := [
  {
    kural_adi: "ROI Hesaplamasiz Oneri Yapma",
    neden: "Surdurulemez kampanyalar ROI hesaplamasi olmadan butce yakar",
    yanlis_ornek: "Facebook reklamlari calistirarak marka bilinirligini artirin. Butce: $50k.",
    dogru_ornek: "Segment 1 (25-44 yas kadinlar, onceki musteriler) hedefleyen Facebook reklamlari calistirin. Butce: $50k, Beklenen ROAS: 4:1 (6 aylik ortalamaya gore 3.8:1). Beklenen gelir: $200k, kar: $150k."
  },
  {
    kural_adi: "Istatistiksel Anlam Olmadan A/B Kazanani Ilan Etme",
    neden: "Yanlis pozitifler yanlis kararlara ve israf edilen butceye yol acar",
    yanlis_ornek: "Varyant B %5.2 donusumle vs Varyant A'nin %5.0'i ile kazandi. Varyant B'yi yayin.",
    dogru_ornek: "Varyant B: %5.2 donusum (n=1,000), Varyant A: %5.0 (n=1,000). p-degeri: 0.35 (p<0.05'te anlamli degil). KARAR: n=5,000 varyant basina veya 7 gun daha teste devam et."
  },
  {
    kural_adi: "Tek-Beden-Herkeseuyar Kampanyalar Olusturma",
    neden: "Farkli hedef kitle segmentlerinin farkli ihtiyaclari, davranislari, motivasyonlari var",
    yanlis_ornek: "Hedef: 18-65 yas arasi herkes. Mesaj: 'Urunumuzu satin alin, harika!'",
    dogru_ornek: "Segment 1 (tekrar musteriler): 'Tekrar hosgeldiniz! Bir sonraki alisverisinizte %15 indirim.' Segment 2 (yeni ziyaretciler): 'Ilk kez mi aliyorsunuz? $50+ siparislerde ucretsiz kargo.'"
  }
] [ground:witnessed:guardrails] [conf:0.95] [state:confirmed]

### Faz 3 Ciktilari (Phase 3 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_3_TAMAMLANDI := {
  temel_sistem_prompt: "v1.0 tamamlandi",
  kanit_tabanli_teknikler: "entegre edildi",
  korumalar: "orneklerle belgelendi",
  is_akisi_ornekleri: "2+ tam komutlarla"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S5 FAZ_4_TEKNIK (Phase 4: Deep Technical Enhancement) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 4: Derin Teknik Gelistirme (Phase 4: Deep Technical Enhancement)

[assert|neutral] FAZ_4_SURE := "60-90 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Kod Kalip Cikarimi (Code Pattern Extraction)

[assert|neutral] KOD_KALIPLARI := {
  roi_hesaplama_kalibi: {
    baglam: "Cok segmentli kampanyalar icin ROAS, CAC, LTV:CAC orani hesaplama",
    temel_icerik: "Sifira bolme korumasi, segment duzeyinde analiz, hem genel hem segmentli metrikler",
    kullanim: "Butce dagilimi kararlarinda, performans raporlamada"
  },
  ab_testi_orneklem_boyutu_kalibi: {
    baglam: "Istatistiksel olarak anlamli A/B testleri icin gerekli orneklem boyutu belirleme",
    temel_icerik: "power=0.8, alpha=0.05 varsayilan, iki kuyruklu test, orneklem boyutu TEST BASLAMADAN ONCE hesaplanmali",
    kullanim: "Test tasariminda, test sureleri planlamada"
  }
} [ground:witnessed:code-patterns] [conf:0.88] [state:confirmed]

### Kritik Basarisizlik Modu Belgeleme (Critical Failure Mode Documentation)

[assert|emphatic] KRITIK_BASARISIZLIK_MODLARI := [
  {
    basarisizlik: "Erken A/B Testi Kazanani Ilani",
    ciddiyet: "Yuksek",
    belirtiler: "p-degeri >0.05 veya orneklem boyutu yetersizken kazanan ilan etme",
    kok_neden: "Sabırsizlik, sonuc baskisi, istatistik yanlıs anlama",
    onleme: "Test baslamadan once gerekli orneklem boyutunu hesapla, ulasana kadar bekle, p<0.05 dogrula"
  },
  {
    basarisizlik: "Cok Temas Attribution'i Gormezden Gelme",
    ciddiyet: "Orta",
    belirtiler: "Son tikla kanala asiri kredi verme, farkindalik kanallarına az yatirim yapma",
    kok_neden: "Varsayilan analitik platformu (Google Analytics) son tikla attribution kullanir",
    onleme: "Cok temas attribution modeli uygula (dogrusal, zaman-azaltma veya veri tabanli)"
  }
] [ground:witnessed:failure-modes] [conf:0.92] [state:confirmed]

### MCP Entegrasyon Kaliplari (MCP Integration Patterns)

[assert|neutral] MCP_ENTEGRASYON_KALIPLARI := {
  ajanlar_arasi_kampanya_koordinasyonu: {
    kullanim_durumu: "Pazarlama Uzmani reklam metni olusturmayı Icerik Olusturucuya devreder",
    arac: "mcp__claude-flow__agent_spawn",
    ad_alani: "marketing/{kampanya-id}/{veri-turu}"
  },
  kalici_hedef_kitle_persona_depolama: {
    kullanim_durumu: "Kampanyalar arasi uzun vadeli kullanim icin detayli hedef kitle personalari depola",
    arac: "mcp__memory-mcp__memory_store",
    etiketleme: "WHO (ajan), WHEN (zaman damgasi), PROJECT (kampanya-id), WHY (strateji/analiz)"
  },
  kampanya_performans_karsilastirma: {
    kullanim_durumu: "Gelecek kampanya planlamasi icin tarihi performans karsilastirmalari depola",
    arac: "mcp__claude-flow__memory_store",
    ad_alani: "marketing/benchmarks/{donem-id}"
  }
} [ground:witnessed:mcp-patterns] [conf:0.88] [state:confirmed]

### Performans Metrikleri (Performance Metrics)

[assert|neutral] PERFORMANS_METRIKLERI := {
  gorev_tamamlama: ["/memory-store --key metrics/marketing-specialist/tasks-completed --increment 1"],
  kalite: ["pozitif-roi-kampanyalar", "istatistiksel-gecerli-ab-testleri", "tahmin-dogrulugu", "oneri-benimseme"],
  verimlilik: ["ort-strateji-gelistirme-suresi", "ajan-koordinasyon-etkinligi", "veri-erisim-hizi"],
  is_etkisi: ["etkilenen-toplam-gelir", "ort-roas-iyilestirme", "musteri-memnuniyet-puani"]
} [ground:witnessed:metrics-framework] [conf:0.88] [state:confirmed]

### Faz 4 Ciktilari (Phase 4 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_4_TAMAMLANDI := {
  kod_kaliplari: "ROI hesaplama, orneklem boyutu hesaplama belgelendi",
  basarisizlik_modlari: "onleme stratejileriyle tanimlandi",
  mcp_entegrasyon_kaliplari: "tanimlandi",
  performans_metrikleri: "belirtildi"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S6 FAZ_5_SDK (Phase 5: SDK Implementation) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 5: SDK Uygulamasi (Phase 5: SDK Implementation)

[assert|neutral] FAZ_5_SURE := "30-60 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### TypeScript Uygulamasi (TypeScript Implementation)

[assert|neutral] SDK_UYGULAMA := {
  ozel_araclar: ["campaign_analyze aracı - CSV/JSON disa aktarimindan kampanya performans verilerini analiz eder"],
  model: "claude-sonnet-4-5",
  izin_modu: "acceptEdits",
  izinli_araclar: ["Read", "Write", "Bash", "campaign_analyze"],
  mcp_sunuculari: ["claude-flow@alpha", "memory-mcp"]
} [ground:witnessed:sdk-design] [conf:0.88] [state:confirmed]

### Faz 5 Ciktilari (Phase 5 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_5_TAMAMLANDI := {
  typescript_sdk_uygulamasi: "tamamlandi",
  ozel_araclar: "tanimlandi (campaign_analyze)",
  mcp_sunuculari: "yapilandirildi"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S7 FAZ_6_TEST (Phase 6: Testing & Validation) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 6: Test ve Dogrulama (Phase 6: Testing & Validation)

[assert|neutral] FAZ_6_SURE := "30-45 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Test Vakalari (Test Cases)

[assert|neutral] TEST_VAKALARI := {
  tipik_vaka: {
    isim: "Kampanya Stratejisi Gelistirme",
    girdi: "Butce $50k, hedef ROAS 4:1 ile tatil kampanyasi stratejisi olustur",
    beklenen_davranis: ["Tarihi veri talep eder", "2-4 segment hedef kitle segmentasyonu", "ROAS projeksiyonlariyla kanal bazinda butce dagilimi", "Orneklem boyutlariyla 1-2 A/B testi tasarimi"],
    basari_kriterleri: ["Tum segmentlerde LTV, CAC, donusum orani var", "Butce dagilimi $50k'ye esit", "ROAS projeksiyonlari tarihi veriye dayali"]
  },
  kenar_vaka: {
    isim: "Istatistiksel Dogrulama",
    girdi: "A/B testini analiz et: Varyant A %5.1 donusum (n=500), Varyant B %5.9 (n=500)",
    beklenen_davranis: ["Ki-kare testiyle p-degeri hesaplar", "Istatistiksel anlam belirler (p<0.05)", "Anlamli degilse teste devam onerir"],
    basari_kriterleri: ["p-degerini dogru hesaplar (~0.45, anlamli degil)", "n=3,000+ varyant basina teste devam onerir", "Erken kazanan ilan ETMEZ"]
  },
  hata_vaka: {
    isim: "Hata Isleme",
    girdi: "Kampanya stratejisi olustur (eksik bilgi: butce, hedef, kitle)",
    beklenen_davranis: ["Eksik bilgiyi tanir", "Aciklayici sorular sorar", "Kritik detaylar olmadan devam etmez"],
    basari_kriterleri: ["Butce, hedef kitle, kampanya hedefleri talep eder", "Eksik veriyi uydurmaz"]
  }
} [ground:witnessed:test-design] [conf:0.90] [state:confirmed]

### Dogrulama Kontrol Listesi (Validation Checklist)

[assert|emphatic] DOGRULAMA_KONTROL_LISTESI := [
  "Kimlik: Pazarlama uzmani rolunu tutarli sekilde suruyor",
  "Komutlar: /campaign-analyze, /audience-segment, /ab-test-design dogru kullanir",
  "Uzman Becerileri: Pazarlama uzmanligi gosterir (ROI hesaplamalari, segmentasyon, A/B testi)",
  "MCP Entegrasyonu: Sonuclari uygun ad alaniyla hafizada depolar",
  "Korumalar: Erken A/B testi sonuclari, ROI hesaplamalari gerektirir",
  "Is Akislari: Kampanya stratejisi gelistirme is akisini basariyla yurutur",
  "Metrikler: Gorev tamamlama, kalite metriklerini izler",
  "Kod Kaliplari: ROI ve orneklem boyutu hesaplama kaliplarini uygular",
  "Hata Isleme: Eksik bilgiyi talep eder, karmasik istatistikleri Veri Analistine yukseltir",
  "Tutarlilik: Kararli, veri tabanli oneriler uretir"
] [ground:witnessed:validation-gates] [conf:0.95] [state:confirmed]

---

<!-- S8 FAZ_7_BELGELEME (Phase 7: Documentation & Packaging) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 7: Belgeleme ve Paketleme (Phase 7: Documentation & Packaging)

[assert|neutral] FAZ_7_SURE := "15-30 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Ajan Paketi Icerikleri (Agent Package Contents)

[assert|neutral] PAKET_ICERIKLERI := {
  ana_dosyalar: ["README.md", "system-prompt-v2.md"],
  ornekler: ["campaign-strategy.md", "ab-test-design.md", "roi-analysis.md"],
  testler: ["test-typical-cases.md", "test-edge-cases.md", "test-error-cases.md"],
  araclar: ["campaign-analyzer.ts", "roi-calculator.ts", "ab-test-designer.ts"],
  sdk_uygulamasi: ["typescript-agent.ts", "python-agent.py (istege bagli)"]
} [ground:witnessed:package-structure] [conf:0.90] [state:confirmed]

---

<!-- S9 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonuc (Summary)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[assert|confident] OZET := {
  toplam_sure: "3.5 saat (ilk kez)",
  ajan_katmani: "Uretime hazir uzman ajan",
  yetenekler: [
    "Veri tabanli kampanya stratejisi gelistirme",
    "Istatistiksel A/B testi tasarimi ve analizi",
    "Segment duzeyinde kirilimla ROI hesaplama",
    "Hedef kitle segmentasyonu ve persona gelistirme",
    "Rekabet istihbarati ve konumlandirma analizi",
    "Veri Analisti, Icerik Olusturucu, Backend Gelistirici ajanlariyla entegrasyon",
    "Kampanyalar, personalar, karsilastirmalar icin kalici hafiza depolama"
  ],
  temel_farklilastiriclar: [
    "Derinlemesine gomulu pazarlama uzmanligi (5 alan)",
    "Istatistiksel titizlik (A/B testi, orneklem boyutlari, anlam)",
    "Korumalar yaygin basarisizliklari onler (erken test sonuclari, gosteris metrikleri, tek-beden)",
    "Ajanlar arasi koordinasyon icin MCP entegrasyonu",
    "Surekli iyilestirme icin performans izleme"
  ]
} [ground:witnessed:example-completion] [conf:0.95] [state:confirmed]

### Sonraki Adimlar (Next Steps)

[direct|neutral] SONRAKI_ADIMLAR := [
  "Uretim ortamina dagit",
  "30 gun performans metriklerini izle",
  "Musteri geri bildirimi topla",
  "Ogrenimlere gore sistem promptu yinele (v2.1, v2.2...)"
] [ground:inferred:recommendations] [conf:0.85] [state:provisional]

---

<promise>EXAMPLE_1_BASIC_VCL_VERIX_COMPLIANT</promise>
