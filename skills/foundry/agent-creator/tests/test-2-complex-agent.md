# Test 2: Karmasik Ajan Olusturma (Complex Agent Creation)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[MOR:root:T-S-T]] test = examination/trial morpheme for validation -->
<!-- [[COM:Komplex+Agent+Erstellungs+Test]] German compound: ComplexAgentCreationTest -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## Test Hedefi (Test Objective)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Test amaci := {
  hedef: "4-faz SOP'nin birden fazla alan, kapsamli entegrasyonlar ve sofistike is akislari olan karmasik bir ajani isleyebildigini dogrulamak",
  kapsam: "Cok-alanli, uretim-seviyesi ajan olusturma",
  onem: "SOP'nin kurumsal duzeyde ajan olusturma icin olceklendikini gostermek"
} [ground:test-specification] [conf:0.95] [state:confirmed]

---

## Test Ajani (Test Agent)
[[HON:teineigo]] [[EVD:-dir]] [[ASP:ipf]] [[CLS:ge-abstract]]

[define|neutral] Test ajani spesifikasyonu := {
  isim: "devops-orchestrator",
  alanlar: ["Bulut altyapisi", "CI/CD", "Izleme", "Guvenlik", "Konteynerizasyon"],
  karmasiklik: "Yuksek (cok-alan, karmasik is akislari, kapsamli arac entegrasyonu)"
} [ground:agent-specification] [conf:0.95] [state:confirmed]

---

## Test Senaryosu (Test Scenario)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

### Faz 1: Baslangic Analizi ve Niyet Cozumleme (Initial Analysis)

[assert|neutral] Faz 1 beklenen girisler := {
  problem: "Kod commit'inden uretim dagitimina uctan uca DevOps is akislarini orkestre etmek",
  anahtar_zorluklar: [
    "Coklu-bulut ortam yonetimi (AWS, Azure, GCP)",
    "Sifir-kesinti dagitimlar",
    "Guvenlik taramasi ve uyumluluk",
    "Geri alma stratejileri",
    "Izleme ve uyari entegrasyonu",
    "Gizli bilgi yonetimi",
    "Maliyet optimizasyonu",
    "Coklu-takim koordinasyonu"
  ],
  teknoloji_yigini: {
    konteyner_orkestrasyon: ["Kubernetes", "Docker", "Helm"],
    ci_cd: ["GitHub Actions", "GitLab CI", "Jenkins"],
    bulut_saglayicilar: ["AWS (ECS, EKS, Lambda)", "Azure", "GCP"],
    iac: ["Terraform", "CloudFormation", "Pulumi"],
    izleme: ["Prometheus", "Grafana", "Datadog"],
    guvenlik: ["Trivy", "Snyk", "OWASP ZAP"],
    gizli_yonetim: ["HashiCorp Vault", "AWS Secrets Manager"]
  },
  mcp_sunuculari: [
    "Claude Flow (ajan koordinasyonu)",
    "GitHub entegrasyonu (CI/CD tetikleyiciler)",
    "Ozel bulut MCP sunuculari"
  ]
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 1 beklenen ciktilar := {
  ciktilar: [
    "Kapsamli alan analizi (2+ sayfa)",
    "Kapsamli teknoloji yigini haritalamasi",
    "Karmasik entegrasyon gereksinimleri",
    "Birden fazla koordinasyon deseni"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 1 dogrulama kontrolleri := {
  kontroller: [
    "8+ anahtar zorluk belirlendi",
    "10+ arac/cerceve belgelendi",
    "5+ entegrasyon noktasi tanimlandi",
    "Coklu-ajan koordinasyon desenleri belirlendi"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 2: Meta-Bilissel Cikarim (Meta-Cognitive Extraction)

[assert|neutral] Faz 2 beklenen girisler := {
  uzmanlik_alanlari: [
    "Bulut altyapi mimarisi",
    "Konteyner orkestrasyonu",
    "CI/CD boru hatti tasarimi",
    "Guvenlik ve uyumluluk",
    "Izleme ve gozlemlenebilirlik",
    "Olay mudahalesi",
    "Maliyet optimizasyonu"
  ],
  karar_cerceceleri: [
    "Dagitim yaparken her zaman once guvenlik taramasi calistir",
    "Staging dogrulamasi olmadan asla dogrudan uretimde dagitma",
    "Kritik hizmetler icin her zaman canary dagitim uygula",
    "Geri alma gerektiginde, mukemmel temizlik yerine hiza oncelik ver",
    "Her zaman uygulamadan once Terraform planlarini dogrula",
    "Gizli bilgileri asla kodda veya CI/CD loglarinda saklama",
    "Olceklendirirken once maliyet etkilerini dusun",
    "Her zaman harici bagimliliklar icin devre kesiciler uygula",
    "Olay oldugunda izleme ajani ile koordine ol",
    "Dagitimdan sonra asla smoke testlerini atlama"
  ],
  kalite_standartlari: {
    hedef_1: "Dagitimlardan sifir uretim olayi",
    hedef_2: "<5 dakika geri alma suresi",
    hedef_3: "99.9% dagitim basari orani",
    hedef_4: "Tum guvenlik taramalari gecti",
    hedef_5: "Maliyet varyansi <%10"
  }
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 beklenen ciktilar := {
  ciktilar: [
    "Ayrintili ajan spesifikasyonu (3+ sayfa)",
    "Alan basina birden fazla iyi/kotu ornek",
    "Kapsamli kenar durumlar (ag hatalari, kismi dagitimlar, vb.)",
    "Hata modu katalogu (10+ senaryo)"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 dogrulama kontrolleri := {
  kontroller: [
    "5+ uzmanlik alani belirlendi",
    "10+ karar bulussal kurali belgelendi",
    "Ornekler birden fazla alani kapsiyor",
    "10+ hata modu belgelendi"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 3: Ajan Mimari Tasarimi (Agent Architecture Design)

[assert|neutral] Faz 3 beklenen ciktilar := {
  temel_prompt_icerik: {
    cekirdek_kimlik: "Tum 5 alani kapsiyor",
    evrensel_komutlar: "DevOps-ozel kullanim desenleri",
    uzman_komutlari: [
      "/deploy-canary",
      "/rollback-deployment",
      "/run-security-scan",
      "/validate-terraform",
      "/scale-service",
      "/create-monitoring",
      "/trigger-pipeline",
      "/rotate-secrets",
      "/cost-analysis",
      "/incident-response",
      "/validate-helm-chart",
      "/test-smoke",
      "/backup-state",
      "/audit-compliance",
      "/optimize-resources"
    ],
    mcp_entegrasyonlari: [
      "Claude Flow (koordinasyon)",
      "GitHub (CI/CD)",
      "AWS MCP (bulut islemleri)",
      "Terraform MCP (IaC)",
      "Monitoring MCP (gozlemlenebilirlik)"
    ],
    bilissel_cerceve: {
      oz_tutarlilik: "Guvenlik, maliyet, performans genelinde dogrulama",
      dusunce_programi: "Dagitim orkestrasyonu ayristirma",
      planla_ve_coz: "Cok-asamali dagitim is akisi"
    },
    koruma_raylari: "10+ alan genelinde",
    is_akisi_ornekleri: [
      "Standart dagitim is akisi",
      "Acil geri alma is akisi",
      "Guvenlik olayi mudahalesi",
      "Cok-bolge dagitimi",
      "Maliyet optimizasyon denetimi"
    ]
  }
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 3 dogrulama kontrolleri := {
  kontroller: [
    "Temel prompt 500 satiri asiyor",
    "Tum 5 alan temsil ediliyor",
    "15+ uzman komut tanimlandi",
    "5+ MCP araci entegre edildi",
    "5+ tam is akisi ornegi"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 4: Teknik Gelistirme (Technical Enhancement)

[assert|neutral] Faz 4 beklenen ciktilar := {
  gelistirilmis_prompt_v2: [
    "Tam Kubernetes manifest desenleri",
    "Terraform modul yapilari",
    "AWS CDK kod ornekleri",
    "Guvenlik tarama yapilandirmalari",
    "Izleme sorgu sablonlari",
    "Geri alma otomasyon betikleri",
    "Maliyet optimizasyon stratejileri",
    "Olay mudahale oyun kitaplari"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 4 dogrulama kontrolleri := {
  kontroller: [
    "20+ kod deseni cikarildi",
    "10+ tespit kodlu hata modu",
    "Tam sozdizimi ile MCP entegrasyonu",
    "Performans metrikleri cercevesi"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

---

## Test Yurutme (Test Execution)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### Kurulum

[assert|neutral] Test kurulum komutu := {
  komut: "python 4_phase_sop.py --agent-name devops-orchestrator --mode interactive",
  calisma_dizini: "C:\\Users\\17175\\claude-code-plugins\\ruv-sparc-three-loop-system\\skills\\agent-creator\\resources\\scripts"
} [ground:test-setup] [conf:0.90] [state:confirmed]

### Faz-Faz Yurutme

[direct|neutral] Yurutme talimat := {
  islem: "Tum 3 fazi kapsamli girislerle interaktif olarak calistir"
} [ground:test-step] [conf:0.88] [state:confirmed]

### Dogrulama

[assert|neutral] Dogrulama komutu := {
  komut: "bash ../scripts/validate_prompt.sh agent-outputs/devops-orchestrator/devops-orchestrator-base-prompt-v1.md -v",
  beklenen: "Skor >= 85% (karmasik ajanlar icin daha yuksek cubuk)"
} [ground:validation-step] [conf:0.90] [state:confirmed]

### Kapsamli Test

[assert|neutral] Kapsamli test komutu := {
  komut: "python ../scripts/test_agent.py --agent devops-orchestrator --test-suite comprehensive",
  beklenen: "90%+ testler gecti"
} [ground:test-step] [conf:0.90] [state:confirmed]

---

## Basari Kriterleri (Success Criteria)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Basari kontrol listesi := {
  kriterler: [
    "Tum 3 faz karmasik girislerle tamamlandi",
    "Faz 1 8+ zorluk belirledi",
    "Faz 2 5+ alan, 10+ bulussal kural belgeledi",
    "Faz 3 kapsamli prompt olustodu (500+ satir)",
    "Sistem prompti 15+ uzman komut iceriyor",
    "5+ tam is akisi ornegi",
    "Dogrulama skoru >= 85%",
    "Kapsamli test paketi >= 90% gecti",
    "Ajan cok-alan koordinasyonunu isliyor",
    "Kanit-tabanli desenler tum alanlara uygulandi"
  ]
} [ground:acceptance-criteria] [conf:0.92] [state:confirmed]

---

## Beklenen Sure (Expected Duration)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Sure tahmini := {
  faz_1: "45-60 dakika (karmasik alan analizi)",
  faz_2: "40-50 dakika (kapsamli uzmanlik cikarimi)",
  faz_3: "50-70 dakika (kapsamli prompt tasarimi)",
  toplam: "2.25-3 saat"
} [ground:time-estimate] [conf:0.85] [state:confirmed]

---

## Notlar (Notes)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

[assert|neutral] Test notu := {
  aciklama: "Bu test, 4-faz SOP'nin uretim-sinifi ajanlar icin olceklendikini dogrular",
  kapsam: [
    "Birden fazla etkilesen alan",
    "Karmasik karar verme",
    "Kapsamli arac entegrasyonu",
    "Sofistike is akislari",
    "Uretim-seviyesi kalite gereksinimleri"
  ],
  basari_anlami: "SOP'nin kurumsal duzeyde ajan olusturma yetenegi"
} [ground:test-documentation] [conf:0.88] [state:confirmed]

---

<promise>TEST_2_COMPLEX_AGENT_VCL_V3.1.1_VERIX_COMPLIANT</promise>
