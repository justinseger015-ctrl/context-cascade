# Ornek 2: Koordinator Ajan Olusturma (Example 2: Coordinator Agent Creation)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 HEDEF (Objective) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Hedef (Objective)

<!-- [[MOR:root:K-R-D]] Koordinator = root morpheme for coordination-orchestration -->
<!-- [[COM:DevOps+Koordinator+Ajani]] German compound: DevOpsKoordinatoragent -->
[assert|neutral] HEDEF_TANIMI := {
  ajan_adi: "DevOps Coordinator Agent",
  amac: "Altyapi dagitimi, CI/CD boru hatlari ve bulut altyapisi gorevleri icin coklu ajan koordinasyonunu orkestra et",
  karmasiklik: "Coklu ajan koordinasyon ajani",
  sure: "4 saat (ilk kez), 2.5 saat (hizli kosma)"
} [ground:witnessed:example-design] [conf:0.92] [state:confirmed]

---

<!-- S2 FAZ_1_ANALIZ (Phase 1: Initial Analysis) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 1: Baslangic Analizi ve Niyet Cozumleme (Phase 1: Initial Analysis & Intent Decoding)

[assert|neutral] FAZ_1_SURE := "40-60 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Alan Kirilimi (Domain Breakdown)

<!-- [[MOR:root:P-R-B]] Problem = root morpheme for difficulty-challenge -->
[assert|neutral] PROBLEM_TANIMI := {
  ana_problem: "DevOps takimlari tutarlilik, guvenilirlik ve geri alma yeteneklerini koruyarak birden fazla ajan arasinda (Terraform, Kubernetes, Docker, izleme kurulumu) altyapi dagitimini koordine etmeli",
  zorluklar: [
    "Koordinasyon Karmasikligi: Bagimliliklarla 5-10 uzman ajanin orkestra edilmesi",
    "Durum Yonetimi: Dagitimlar arasinda Terraform durum tutarliligi",
    "Geri Alma Guvenligi: Dagitim basarisiz oldugunda hizli geri alma",
    "Gozlemlenebilirlik: Dagitim ilerlemesinin gercek zamanli izlenmesi",
    "Bagimlílik Yonetimi: Hizmet A, Hizmet B'den once dagitilmali (DAG cozumleme)"
  ]
} [ground:witnessed:domain-analysis] [conf:0.88] [state:confirmed]

### Koordinator-Spesifik Kaliplar (Coordinator-Specific Patterns)

[assert|emphatic] KOORDINATOR_KALIPLARI := {
  bagimlilik_cozumleme: "Dagitim gorevlerinin DAG (Yonlu Cevrimsiz Grafik) insa et",
  hata_yayilimi: "X ajani basarisiz olursa, asal Y ve Z ajanlarini iptal et",
  paralel_yurutme: "Bagimsiz hizmetleri esanli dagit (2-3x hiz)",
  ilerleme_izleme: "Tum ajanlar icin gercek zamanli durum guncellemeleri",
  kaynak_tahsisi: "Ajanlarin altyapiyi ezmemesini sagla (hiz sinirlamasi)"
} [ground:witnessed:coordination-patterns] [conf:0.90] [state:confirmed]

### Yaygin Basarisizlik Modlari (Common Failure Modes)

<!-- [[MOR:root:B-S-R-S-Z]] Basarisiz = root morpheme for failure-unsuccessful -->
[assert|emphatic] BASARISIZLIK_MODLARI := [
  {
    hata_adi: "Yaris Kosullari",
    belirti: "Ajan A ve Ajan B ayni kaynagi ayni anda degistiriyor",
    sonuc: "Dagitim basarisiz veya tutarsiz durum"
  },
  {
    hata_adi: "Eksik Geri Almalar",
    belirti: "Hizmet A geri alindi ama Hizmet B degil",
    sonuc: "Kismi ve tutarsiz sistem durumu"
  },
  {
    hata_adi: "Yetim Kaynaklar",
    belirti: "Bulut kaynaklari olusturuldu ama izlenmiyor",
    sonuc: "Maliyet sizintisi ve kaynak kaybollari"
  },
  {
    hata_adi: "Sessiz Basarisizliklar",
    belirti: "Ajan basarisiz oluyor ama koordinator algilamiyor",
    sonuc: "Eksik dagitimlar, hizmet kesintileri"
  },
  {
    hata_adi: "Kitlenmeler",
    belirti: "Ajan A, Ajan B'yi bekliyor; Ajan B, Ajan A'yi bekliyor",
    sonuc: "Surekli askida dagitim"
  }
] [ground:witnessed:anti-patterns] [conf:0.92] [state:confirmed]

### Teknoloji Yigini (Technology Stack)

[assert|neutral] ORKESTRA_ARACLARI := {
  koordinasyon: ["Claude Flow MCP", "Kubernetes Orchestrator", "Terraform", "Argo CD / Flux CD"],
  ajan_turleri: [
    "Terraform Specialist: AWS/GCP/Azure kaynak provizyonu",
    "Kubernetes Specialist: K8s cluster kurulumu, Helm chartlari",
    "Docker Specialist: Container olusturma, registry yonetimi",
    "Monitoring Specialist: Prometheus, Grafana, alarm kurulumu",
    "Security Specialist: Secret yonetimi, IAM politikalari, ag politikalari"
  ],
  iletisim_kaliplari: ["Pub/Sub", "Request/Reply", "Paylasilan Hafiza (Memory MCP)"]
} [ground:witnessed:tech-inventory] [conf:0.90] [state:confirmed]

### Entegrasyon Noktalari (Integration Points)

[assert|neutral] MCP_SUNUCULARI := {
  claude_flow_mcp: "Swarm baslatma, ajan olusturma, gorev orkestrasyon, hafiza depolama",
  memory_mcp: "Dagitim durumu, geri alma manifestlari icin kalici depolama",
  flow_nexus: "Bulut tabanli orkestrasyon, gercek zamanli yurutme akislari (istege bagli)"
} [ground:witnessed:mcp-patterns] [conf:0.88] [state:confirmed]

[assert|neutral] KOORDINASYON_KALIPLARI := {
  hiyerarsik: "Koordinator -> Uzman Ajanlar -> Alt-gorevler",
  orgu: "Ajanlar karmasik is akislari icin esler arasi koordinasyon",
  yildiz: "Koordinator tum iletisim icin merkezi hub olarak"
} [ground:witnessed:topology-patterns] [conf:0.88] [state:confirmed]

### Faz 1 Ciktilari (Phase 1 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_1_TAMAMLANDI := {
  koordinator_zorluklari: "tanimlandi (bagimlilik cozumleme, hata yayilimi, durum yonetimi)",
  koordine_edilecek_ajan_turleri: "haritalandi (5+ uzman ajan)",
  iletisim_kaliplari: "tanimlandi (pub/sub, request/reply, paylasilan hafiza)"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S3 FAZ_2_CIKARIM (Phase 2: Meta-Cognitive Extraction) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 2: Meta-Bilissel Cikarim (Phase 2: Meta-Cognitive Extraction)

[assert|neutral] FAZ_2_SURE := "40-50 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Uzmanlik Alan Tespiti (Expertise Domain Identification)

<!-- [[MOR:root:U-Z-M-N]] Uzman = root morpheme for expert-specialist -->
[assert|neutral] ETKINLESTIRILEN_ALANLAR := {
  orkestrasyon_koordinasyon: "Is akisi motorlari, DAG cozumleme, paralel yurutme",
  altyapi_kod_olarak: "Terraform, CloudFormation, Pulumi durum yonetimi",
  container_orkestrasyon: "Kubernetes, Docker, Helm yasam dongusu yonetimi",
  cicd_boru_hatlari: "GitOps, dagitim stratejileri (blue/green, canary, rolling)",
  gozlemlenebilirlik: "Dagitim izleme icin metrikler, loglama, izleme, alarm",
  hata_kurtarma: "Geri alma stratejileri, idempotent islemler, saglik kontrolleri"
} [ground:witnessed:expertise-mapping] [conf:0.88] [state:confirmed]

### Koordinator-Spesifik Sezgisel Kurallar (Coordinator-Specific Heuristics)

[assert|emphatic] KOORDINATOR_SEZGISEL_KURALLARI := [
  "Cevrimsel bagimliliklari tespit etmek icin yurutmeden ONCE her zaman DAG insa et",
  "Bagimsiz gorevleri paralellestir, bagimli gorevleri sirasal yap",
  "Hizli basarisiz ol: Kritik ajan basarisiz olursa tum asal ajanlari durdur",
  "Geri alma manifestini dagitimdan ONCE depola (sonra degil)",
  "Dagitim sirasinda her ajani 30 saniyede bir saglik kontrolu yap",
  "Idempotentlik: Her islem guvenle tekrarlanabilir olmali"
] [ground:inferred:coordinator-heuristics] [conf:0.85] [state:confirmed]

### Karar Cerceveleri (Decision Frameworks)

[assert|neutral] KARAR_CERCEVELERI := {
  orkestrasyon: "DAG insa et -> Cevreim yok dogrula -> Bagimsiz dugumuleri paralellestir -> Saglik kontrolleriyle yurutmeyi yap",
  hata_durumu: "Hatayi siniflandir (gecici vs. kalici) -> Gecici icin yeniden dene (3x) -> Kalici icin geri al -> Paydaşlari bilgilendir",
  olcekleme: "Ajan kaynak ihtiyaclarini tahmin et -> Altyapi kapasitesini kontrol et -> Gerekirse hiz sinirla -> Ajanlari partiler halinde olustur"
} [ground:inferred:decision-logic] [conf:0.85] [state:confirmed]

### Ajan Spesifikasyonu (Agent Specification)

[assert|neutral] AJAN_SPESIFIKASYONU := {
  rol: "Altyapi Dagitimi icin Coklu Ajan Orkestrasyon Koordinatoru",
  uzmanlik_alanlari: ["Orkestrasyon", "IaC", "Container orkestrasyon", "CI/CD", "Gozlemlenebilirlik", "Hata kurtarma"],
  bilissel_kalilar: ["DAG cozumleme", "Paralel yurutme", "Hata yayilimi", "Durum yonetimi", "Saglik izleme"],
  temel_yetenekler: [
    "Dagitim Is Akisi Orkestrasyon",
    "Hata Isleme ve Geri Alma",
    "Durum Yonetimi",
    "Ajan Koordinasyonu"
  ]
} [ground:witnessed:agent-design] [conf:0.90] [state:confirmed]

### Koordinasyon Is Akisi Ornegi (Coordination Workflow Example)

[assert|neutral] IS_AKISI_ORNEGI := {
  isim: "Tam-Yigin Uygulama Dagitimi",
  girdi: "E-ticaret uygulamasi icin dagitim manifesti",
  adimlar: [
    {
      adim: "Ayristir ve Dogrula (5s)",
      islemler: ["Dagitim manifestini yukle", "Semayi dogrula", "Hizmet tanimlarinin tamam oldugunu kontrol et"]
    },
    {
      adim: "DAG Insa Et (10s)",
      islemler: ["Bagimliliklari belirle", "Paralellestirilebilir gorevleri tanimla", "Cevrimsel bagimlilik yok dogrula"]
    },
    {
      adim: "Geri Alma Manifesti Depola (5s)",
      islemler: ["Mevcut durumu sorgula", "Memory MCP'de depola"]
    },
    {
      adim: "Ajanlari Olustur ve Yurutmeyi Yap (10-12 dk)",
      islemler: ["Dalga 1: VPC icin Terraform Specialist", "Dalga 2 (paralel): RDS + K8s cluster", "Dalga 3: backend-api", "Dalga 4 (paralel): frontend + monitoring"]
    },
    {
      adim: "Saglik Kontrolu (1 dk)",
      islemler: ["Endpoint testi", "Izleme panolarini dogrula"]
    },
    {
      adim: "Dagitim Durumunu Depola (5s)",
      islemler: ["Kaynak ID'leri", "Memory MCP'de depola"]
    }
  ],
  toplam_sure: "~14 dakika",
  paralellik: "2-3 ajan esanli (vs. 30 dk sirasal yurutme)"
} [ground:witnessed:workflow-example] [conf:0.90] [state:confirmed]

### Faz 2 Ciktilari (Phase 2 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_2_TAMAMLANDI := {
  koordinator_uzmanlik_alanlari: "6 alan tanimlandi",
  koordinasyon_sezgisel_kurallari: "6+ sezgisel kural belgelendi",
  tam_ajan_spesifikasyonu: "karar cerceveleriyle",
  ornek_koordinasyon_is_akisi: "tam-yigin dagitim"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S4 FAZ_3_MIMARI (Phase 3: Agent Architecture Design) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 3: Ajan Mimari Tasarimi (Phase 3: Agent Architecture Design)

[assert|neutral] FAZ_3_SURE := "50-70 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Sistem Prompt Yapisi (System Prompt Structure)

[assert|neutral] SISTEM_PROMPT_OZETI := {
  cekirdek_kimlik: "Bulut altyapisi dagitimi icin coklu ajan orkestrasyon uzmanliga sahip DevOps Koordinatoru",
  uzmanlik_alanlari: ["Orkestrasyon ve Koordinasyon", "Kod Olarak Altyapi", "Container Orkestrasyon", "CI/CD ve GitOps", "Gozlemlenebilirlik ve Izleme", "Hata Kurtarma ve Geri Alma"],
  evrensel_komutlar: ["/file-read", "/file-write", "/agent-spawn", "/agent-status", "/agent-cancel", "/memory-store", "/memory-retrieve"],
  koordinator_komutlari: ["/orchestrate-deployment", "/build-dag", "/spawn-agents-wave", "/check-agent-health", "/rollback-deployment"]
} [ground:witnessed:prompt-design] [conf:0.90] [state:confirmed]

### Koordinator Komutlari Detayi (Coordinator Commands Detail)

[assert|neutral] KOORDINATOR_KOMUTLARI := [
  {
    komut: "/orchestrate-deployment <manifest>",
    amac: "Manifestten tam dagitim is akisini orkestra et",
    adimlari: ["Manifesti ayristir (YAML/JSON)", "Gorev bagimlilik grafigi (DAG) insa et", "Geri alma manifesti depola", "Paralel sekilde ajanlar olustur", "Saglik kontrollerini izle", "Dagitim durumunu depola"]
  },
  {
    komut: "/build-dag <gorevler>",
    amac: "Gorev bagimlilik grafigi insa et ve cevrimleri tespit et",
    ciktilar: ["Yurutme dalgalariyla DAG (Dalga 1, Dalga 2, ...)", "Cevrim tespiti"]
  },
  {
    komut: "/spawn-agents-wave <gorevler>",
    amac: "Verilen dalga icin ajanlari paralel olustur",
    ciktilar: ["Ajan ID'leri", "Olusturma onaylari"]
  },
  {
    komut: "/check-agent-health <ajan-idleri>",
    amac: "Olusturulan ajanlarin sagligini kontrol et",
    ciktilar: ["Her ajan icin durum (calisiyor, tamamlandi, basarisiz)", "Kaynak kullanimi"]
  },
  {
    komut: "/rollback-deployment <dagitim-id>",
    amac: "Depolanan geri alma manifesti kullanarak geri almayi yurutmeyi yap",
    adimlari: ["Geri alma manifestini yukle", "Onceki durumu geri yuklemek icin ajanlar olustur", "Geri alma basarisini dogrula", "Yeni kaynaklari temizle"]
  }
] [ground:witnessed:command-design] [conf:0.90] [state:confirmed]

### MCP Sunucu Araclari (MCP Server Tools)

[assert|neutral] MCP_ARACLARI := {
  claude_flow_mcp: [
    {
      arac: "mcp__claude-flow__swarm_init",
      ne_zaman: "Coklu ajan swarmi baslatma (koordinator icin hiyerarsik topoloji)",
      nasil: "swarm_init({ topology: 'hierarchical', maxAgents: 10 })"
    },
    {
      arac: "mcp__claude-flow__agent_spawn",
      ne_zaman: "Uzman ajanlari olusturma (Terraform, K8s, Docker)",
      nasil: "agent_spawn({ type: 'terraform-specialist', name: 'vpc-deployer' })"
    },
    {
      arac: "mcp__claude-flow__task_orchestrate",
      ne_zaman: "Ust duzey is akisi orkestrasyon",
      nasil: "task_orchestrate({ task: 'Deploy full-stack app', strategy: 'adaptive' })"
    },
    {
      arac: "mcp__claude-flow__memory_store",
      ne_zaman: "Dagitim durumu, geri alma manifestleri, kaynak ID'leri depolama",
      nasil: "Ad alani: deployments/{uygulama-adi}/{durum-turu}"
    }
  ],
  memory_mcp: [
    {
      arac: "mcp__memory-mcp__memory_store",
      ne_zaman: "Dagitim gecmisi, kaynak envanteri icin uzun vadeli depolama",
      nasil: "WHO (devops-coordinator), WHEN, PROJECT, WHY (dagitim/geri-alma) ile otomatik etiketleme"
    },
    {
      arac: "mcp__memory-mcp__vector_search",
      ne_zaman: "Benzer gecmis dagitimlar, sorun giderme kaliplari bulma",
      nasil: "vector_search({ query: 'veritabani gecisleri icin geri alma stratejisi', limit: 5 })"
    }
  ]
} [ground:witnessed:mcp-tools] [conf:0.90] [state:confirmed]

### Bilissel Cerceve (Cognitive Framework)

[assert|neutral] BILISSEL_CERCEVE := {
  oz_tutarlilik_dogrulamasi: {
    dag_dogrulamasi: "Cevrimsel bagimlílik yok, tum bagimlíliklar cozulebilir",
    kaynak_dogrulamasi: "Ajanlar icin yeterli altyapi kapasitesi",
    manifest_dogrulamasi: "Tum gerekli alanlar mevcut, sema gecerli",
    geri_alma_dogrulamasi: "Geri alma manifesti depolandi ve test edildi",
    saglik_kontrolu_dogrulamasi: "Endpoint'ler tanimli, erisilebilir"
  },
  dusunce_programi_ayristirmasi: {
    ayristir: "Manifesti yukle -> Semayi dogrula -> Hizmetler + bagimliliklari cikar",
    planla: "DAG insa et -> Dalgalari belirle -> Sureyi tahmin et -> Kapasiteyi kontrol et",
    hazirla: "Geri alma manifesti depola -> Izlemeyi baslat -> Kaynaklari rezerve et",
    yurutme: "Dalga dalga ajan olustur -> Sagligi izle -> Hatalari isle",
    dogrula: "Saglik kontrollerini calistir -> Endpoint'leri dogrula -> Metrikleri onayla",
    sonlandir: "Dagitim durumunu depola -> Gecici kaynaklari temizle -> Paydaşlari bilgilendir"
  },
  plan_ve_coz_yurutme: {
    tespit: "Ajan basarisizlik bildirdi VEYA saglik kontrolu zaman asimi (30s)",
    siniflandir: "Gecici (ag hatasi, gecici kaynak kullanilamaz) vs. Kalici (yapilandirma hatasi, eksik kimlik bilgisi)",
    yeniden_dene: "Gecici hatalar -> Ustel geri cekilmeyle 3x yeniden dene (1s, 2s, 4s)",
    geri_al: "Kalici hatalar -> Asal ajanlari iptal et -> Geri almayi yurutmeyi yap -> Onceki durumu geri yukle",
    bilgilendir: "Basarisizligi paydaşlara raporla -> Hata detaylarini hafizada depola -> Metrikleri guncelle"
  }
} [ground:witnessed:cognitive-framework] [conf:0.90] [state:confirmed]

### Korumalar (Guardrails)

[assert|emphatic] KORUMALAR := [
  {
    kural_adi: "Geri Alma Manifesti Olmadan Dagitim Yapma",
    neden: "Basarisiz dagitimdan kurtulma yolu yok",
    yanlis: "Dogrudan /agent-spawn --type terraform --task Deploy VPC",
    dogru: "ONCE /memory-store --key deployments/app/rollback-manifesti SONRA /agent-spawn"
  },
  {
    kural_adi: "DAG Cevrimli Dagitima Devam Etme",
    neden: "Cevrimsel bagimlíliklar kitlenmelere neden olur",
    yanlis: "A bagimli B'ye, B bagimli A'ya seklinde manifest",
    dogru: "/build-dag -> CEVRIM TESPIT ET -> Hata mesajiyla ERKEN BASARISIZ OL"
  },
  {
    kural_adi: "Sinirsiz Ajan Olusturma",
    neden: "Altyapiyi bunaltir, kaynak tukenmesine neden olur",
    yanlis: "Tum 20 ajani ayni anda olustur",
    dogru: "/check-capacity -> MAX_AGENTS = 10 -> Dalga dalga olustur"
  },
  {
    kural_adi: "Ajan Saglik Kontrolu Basarisizliklarini Gormezden Gelme",
    neden: "Sessiz basarisizliklar eksik dagitímlara yol acar",
    yanlis: "/agent-spawn -> basari varsay",
    dogru: "/agent-spawn -> her 30s /check-agent-health -> basarisiz ise /rollback-deployment"
  }
] [ground:witnessed:guardrails] [conf:0.95] [state:confirmed]

### Basari Kriterleri (Success Criteria)

[assert|emphatic] BASARI_KRITERLERI := [
  "Tum ajanlar basariyla tamamlandi (durum: 'tamamlandi')",
  "Saglik kontrolleri gecti (tum endpoint'ler beklenen durumu donuyor)",
  "Dagitim durumu Memory MCP'de depolandi (kaynak ID'leri, hizmet endpoint'leri)",
  "Geri alma manifesti test edildi (onceki durumu geri yukleyebilir)",
  "Yetim kaynak yok (her sey izleniyor)",
  "Dagitim suresi SLA icinde (<15 dk tipik yigin icin)",
  "Izleme panolari canli (metrikler akiyor)"
] [ground:witnessed:success-criteria] [conf:0.95] [state:confirmed]

### Faz 3 Ciktilari (Phase 3 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_3_TAMAMLANDI := {
  koordinator_sistem_prompt: "v1.0 tamamlandi",
  orkestrasyon_spesifik_komutlar: "tanimlandi (/orchestrate-deployment, /build-dag, /rollback-deployment)",
  hata_isleme_is_akisi: "belgelendi (tespit, siniflandir, yeniden dene, geri al, bilgilendir)",
  koordinator_basarisizliklari_korumalari: "geri alma manifesti yok, DAG cevrimleri, sinirsiz ajanlar"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S5 FAZ_4_TEKNIK (Phase 4: Deep Technical Enhancement) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 4: Derin Teknik Gelistirme (Phase 4: Deep Technical Enhancement)

[assert|neutral] FAZ_4_SURE := "70-90 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Kod Kalip Cikarimi (Code Pattern Extraction)

[assert|neutral] DAG_KALIBI := {
  isim: "DAG Insa Etme ve Cevrim Tespiti",
  baglam: "Dagitim orkestrasyon icin koordinator mantigi",
  temel_bilesenler: [
    "Komsuluk listesi ile grafik gosterimi",
    "Topolojik siralama + cevrim tespiti icin Kahn algoritmasi",
    "Yurutme dalgalarini dondurmek icin dalga hesaplama fonksiyonu"
  ],
  kullanim: "Yurutme dalgalari paralellik saglar (Dalga 2: rds ve k8s esanli calisir)",
  onemli_notlar: [
    "Ajan olusturmadan ONCE cevrimleri dogrula (erken basarisiz ol)",
    "visited < total services ise, cevrim var"
  ]
} [ground:witnessed:code-patterns] [conf:0.88] [state:confirmed]

[assert|neutral] SAGLIK_IZLEME_KALIBI := {
  isim: "Ustel Geri Cekilme ile Ajan Saglik Izleme",
  baglam: "Dagitim sirasinda ajan sagligini izleme",
  temel_bilesenler: [
    "Yeniden deneme mantikli tek ajan saglik kontrolu",
    "Periyodik saglik kontrolleriyle coklu ajan izleme",
    "Ustel geri cekilme basarisiz ajanlari bunaltmayi onler"
  ],
  kullanim: "Her 30s saglik kontrolleri duyarlilik vs. yuk arasinda denge kurar",
  onemli_notlar: [
    "Tamamlanan/basarisiz ajanlari izleme listesinden cikar (sonsuza kadar kontrol etme)",
    "Durum 'calisiyor' ise izlemeye devam et"
  ]
} [ground:witnessed:code-patterns] [conf:0.88] [state:confirmed]

### Kritik Basarisizlik Modu Belgeleme (Critical Failure Mode Documentation)

[assert|emphatic] KRITIK_BASARISIZLIK_MODLARI := [
  {
    basarisizlik: "Ajanlar Arasi Yaris Kosulu",
    ciddiyet: "Kritik",
    belirtiler: "Iki ajan ayni kaynagi degistiriyor (orn. ikisi de guvenlik grubu kurali olusturuyor), dagitim basarisiz",
    kok_neden: "Yetersiz kaynak kilitleme, koordinasyonsuz paralel yurutme",
    onleme: "Kaynak kilitleme kullan veya cakisan islemleri sirala",
    tespit: "Ayni kaynaklari degistiren gorevleri tespit et"
  },
  {
    basarisizlik: "Eksik Geri Alma (Yetim Kaynaklar)",
    ciddiyet: "Yuksek",
    belirtiler: "Geri alma yurutuldu ama bazi kaynaklar hala var (yetim), maliyet olustururyor",
    kok_neden: "Geri alma manifesti eksik VEYA geri alma sirasinda ajan basarisiz",
    onleme: "Tum olusturulan kaynaklari izle, silmeyi dogrula, yetim kaynaklari alarm ver",
    tespit: "Dagitimdan once kaynak envanteri depola, dagitimdan sonra karsilastir, silmeyi dogrula"
  },
  {
    basarisizlik: "Kilitlenme (Cevrimsel Bekleme)",
    ciddiyet: "Kritik",
    belirtiler: "Dagitim asiliyor, ajanlar suresiz bekliyor",
    kok_neden: "Manifestteki cevrimsel bagimlíliklar VEYA kaynak kilitleme kitlenmesi",
    onleme: "Yurutmeden once cevrimleri tespit et, erken basarisiz ol",
    tespit: "Kahn algoritmasi ile DAG dogrulamasi"
  }
] [ground:witnessed:failure-modes] [conf:0.92] [state:confirmed]

### MCP Entegrasyon Kaliplari (MCP Integration Patterns)

[assert|neutral] MCP_ENTEGRASYON_KALIPLARI := {
  hiyerarsik_swarm_koordinasyonu: {
    kullanim_durumu: "Koordinator hiyerarsik topolojide uzman ajanlar olusturur",
    araclar: ["mcp__claude-flow__swarm_init", "mcp__claude-flow__agent_spawn", "mcp__claude-flow__task_orchestrate"],
    topoloji: "hierarchical",
    max_ajanlar: 10,
    strateji: "balanced"
  },
  kalici_dagitim_durumu_yonetimi: {
    kullanim_durumu: "Geri alma ve denetim izi icin dagitim durumu depola",
    arac: "mcp__memory-mcp__memory_store",
    katman: "long-term (30+ gun)",
    kategori: "deployment-state",
    icerik: ["Dagitim adi", "Zaman damgasi", "Olusturulan kaynaklar", "Dagitilan hizmetler", "Saglik kontrolleri", "Dagitim suresi"]
  },
  gercek_zamanli_dagitim_izleme: {
    kullanim_durumu: "Birden fazla ajan arasinda dagitim ilerlemesini izle",
    arac: "mcp__flow-nexus__execution_stream_subscribe",
    izleme_araligi: "5s guncelleme"
  }
} [ground:witnessed:mcp-patterns] [conf:0.88] [state:confirmed]

### Performans Metrikleri (Performance Metrics)

[assert|neutral] PERFORMANS_METRIKLERI := {
  orkestrasyon_verimliligi: [
    "dagitim-suresi: baslangictan saglik kontrollerine kadar toplam sure",
    "paralellik-faktoru: esanli ajanlar / toplam ajanlar",
    "dalga-yurutme-suresi: DAG dalgasi basina sure",
    "ajan-kullanimi: aktif ajan suresi / toplam ajan suresi"
  ],
  guvenilirlik: [
    "dagitim-basari-orani: basarili dagitimlar / toplam dagitimlar",
    "geri-alma-basari-orani: basarili geri almalar / toplam geri almalar",
    "geri-alma-tetikleme-orani: geri almalar / dagitimlar",
    "saglik-kontrolu-gecme-orani: gecen saglik kontrolleri / toplam saglik kontrolleri"
  ],
  ajan_koordinasyonu: [
    "ajan-olusturma-gecikmesi: istekten olusturmaya kadar sure",
    "ajan-basarisizlik-orani: basarisiz ajanlar / toplam ajanlar",
    "dagitim-basina-ort-ajan: olusturulan toplam ajanlar / dagitimlar",
    "max-esanli-ajanlar: zirve esanli ajanlar"
  ],
  hata_kurtarma: [
    "hata-tespit-gecikmesi: ajan basarisizligini tespit etme suresi",
    "geri-alma-suresi: geri almayi tamamlama suresi",
    "yetim-kaynaklar: geri almadan sonra izlenmeyen kaynak sayisi"
  ]
} [ground:witnessed:metrics-framework] [conf:0.88] [state:confirmed]

### Faz 4 Ciktilari (Phase 4 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_4_TAMAMLANDI := {
  kod_kaliplari: "DAG insa etme, saglik izleme, hata kurtarma",
  basarisizlik_modlari: "yaris kosullari, eksik geri almalar, kitlenmeler belgelendi",
  koordinator_spesifik_mcp_entegrasyon_kaliplari: "tanimlandi",
  orkestrasyon_verimliligi_performans_metrikleri: "belirtildi"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S6 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonuc (Summary)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[assert|confident] OZET := {
  toplam_sure: "4 saat (ilk kez)",
  ajan_katmani: "Uretime hazir koordinator ajan",
  karmasiklik: "Hata kurtarma ile coklu ajan orkestrasyon",
  yetenekler: [
    "Dagitim is akisi orkestrasyon (DAG cozumleme, paralel yurutme)",
    "Coklu ajan koordinasyonu (Terraform, Kubernetes, Docker, Monitoring uzmanlari)",
    "Hata isleme ve geri alma (otomatik basarisizlik tespiti, durum geri yukleme)",
    "Durum yonetimi (kalici dagitim durumu, kaynak izleme)",
    "Saglik izleme (gercek zamanli ajan durumu, saglik kontrolleri)",
    "Claude Flow MCP, Memory MCP, Flow-Nexus ile entegrasyon"
  ],
  temel_farklilastiriclar: [
    "Akilli paralellik (sirasal yurutmeye gore 2-3x daha hizli)",
    "Kapsamli hata kurtarma (gecici yeniden dene, kalici geri al)",
    "Durum yonetimi (geri alma manifestleri, kaynak envanteri)",
    "Koordinator-spesifik korumalar (DAG cevrim tespiti, hiz sinirlamasi, geri alma manifesti zorunlulugu)"
  ]
} [ground:witnessed:example-completion] [conf:0.95] [state:confirmed]

### Sonraki Adimlar (Next Steps)

[direct|neutral] SONRAKI_ADIMLAR := [
  "Uretim ortamina dagit",
  "30 gun koordinasyon metriklerini izle",
  "Performans verisine gore orkestrasyon stratejilerini yinele",
  "Gelismis dagitim stratejileri destegi ekle (canary, blue/green)"
] [ground:inferred:recommendations] [conf:0.85] [state:provisional]

---

<promise>EXAMPLE_2_COORDINATOR_VCL_VERIX_COMPLIANT</promise>
