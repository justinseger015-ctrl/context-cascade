# Test 3: Tam 4-Faz SOP Uctan Uca (Complete 4-Phase SOP End-to-End)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[MOR:root:T-S-T]] test = examination/trial morpheme for validation -->
<!-- [[COM:Voll+Vier+Phasen+SOP+End+Zu+End+Test]] German compound: Full4PhaseSoPEndToEndTest -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## Test Hedefi (Test Objective)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Test amaci := {
  hedef: "Faz 4 teknik gelistirme dahil tam 4-faz SOP metodolojisini uctan uca dogrulamak",
  sonuc: "Uretim-hazir ajan uretmek",
  onem: "Tam SOP'nin Gold-kademe, uretim-hazir ajanlar urettigini gostermek"
} [ground:test-specification] [conf:0.95] [state:confirmed]

---

## Test Ajani (Test Agent)
[[HON:teineigo]] [[EVD:-dir]] [[ASP:ipf]] [[CLS:ge-abstract]]

[define|neutral] Test ajani spesifikasyonu := {
  isim: "api-security-auditor",
  alan: "API guvenlik analizi ve guvenlik acigi tespiti",
  karmasiklik: "Orta (uzman alan, teknik derinlik)"
} [ground:agent-specification] [conf:0.95] [state:confirmed]

---

## Test Senaryosu (Test Scenario)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

### Faz 1: Baslangic Analizi ve Niyet Cozumleme (30-45 dk)

[assert|neutral] Faz 1 alan dagilimi := {
  problem: "REST ve GraphQL API'lerinin otomatik guvenlik denetimi",
  anahtar_zorluklar: [
    "Kimlik dogrulama bypass guvenlik aciklari",
    "Yetkilendirme kusurlari (IDOR, ayricalik yukseltme)",
    "Enjeksiyon saldirilari (SQL, NoSQL, komut)",
    "Hiz sinirlamasi ve DoS korumasi",
    "Hassas veri ifsa",
    "CORS yanlis yapilandirmalari"
  ],
  teknoloji_yigini: {
    test_araclari: ["OWASP ZAP", "Burp Suite", "Postman"],
    guvenlik_cerceveleri: ["OWASP Top 10", "SANS CWE Top 25"],
    api_spesifikasyonlari: ["OpenAPI/Swagger", "GraphQL sema"],
    kimlik_dogrulama: ["OAuth 2.0", "JWT", "API anahtarlari"],
    diller: ["Python (requests, httpx)", "Node.js"]
  },
  entegrasyonlar: {
    mcp: ["Claude Flow", "GitHub (bulgulari raporla)"],
    harici: ["OWASP ZAP API", "guvenlik acigi veritabanlari"]
  }
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 1 beklenen ciktilar := {
  ciktilar: [
    "Guvenlik odakli alan analizi",
    "Guvenlik acigi taksonomisi",
    "Test araci envanteri",
    "Guvenlik platformlari ile entegrasyon"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 1 dogrulama kapilari := {
  kontroller: [
    "6+ guvenlik zorlugu belirlendi",
    "Guvenlik cercevesi haritalamasi tamamlandi",
    "Arac entegrasyon desenleri tanimlandi",
    "Guvenlik acigi taksonomisi kapsamli"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 2: Meta-Bilissel Cikarim (30-40 dk)

[assert|neutral] Faz 2 uzmanlik alanlari := {
  alanlar: [
    "API guvenlik test metodolojileri",
    "Kimlik dogrulama ve yetkilendirme desenleri",
    "Yaygin guvenlik acigi desenleri (OWASP Top 10)",
    "Guvenli kodlama pratikleri",
    "Uyumluluk cerceveleri (PCI DSS, GDPR, SOC 2)"
  ]
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 karar cerceveleri := {
  bulussal_kurallar: [
    "Auth test ederken her zaman hem authn HEM DE authz test et",
    "Acik izin olmadan asla yikici testler yapma",
    "Her zaman once SSL/TLS yapilandirmasini dogrula",
    "Guvenlik acigi bulunca ciddiyet seviyesine gore siniflandir (CVSS)",
    "Yuk testinden once her zaman hiz sinirlamasini test et",
    "Isteklerden hassas verileri asla logla veya sakla",
    "Yukseltme yaparken kanitlayici-kavrami (PoC) dahil et",
    "Raporlamadan once yanlis pozitifleri her zaman dogrula",
    "Enjeksiyon test ederken once guvenli payload kullan",
    "'Guvenilir' API olsa bile kimlik dogrulama testini asla atlama"
  ]
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 kalite standartlari := {
  standartlar: {
    hedef_1: "Yuksek-ciddiyet bulgularinda sifir yanlis positif",
    hedef_2: "Tam OWASP Top 10 kapsamasi",
    hedef_3: "Eyleme gecirilebilir iyilestirme rehberligi",
    hedef_4: "Genel <%5 yanlis positif orani",
    hedef_5: "Sorumlu ifsa ile uyumluluk"
  }
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 beklenen ciktilar := {
  ciktilar: [
    "Guvenlik ajani spesifikasyonu",
    "Guvenlik acigi ornekleri (iyi/kotu)",
    "Kenar durumlar (ozel auth, mikroservisler, vb.)",
    "Etik test koruma raylari"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 dogrulama kapilari := {
  kontroller: [
    "5+ uzmanlik alani belirlendi",
    "10+ karar bulussal kurali belgelendi",
    "Guvenlik ornekleri ciddiyet derecelendirmesi iceriyor",
    "Etik test koruma raylari tanimlandi"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 3: Ajan Mimari Tasarimi (40-50 dk)

[assert|neutral] Faz 3 temel prompt yapisi := {
  cekirdek_kimlik: {
    uzmanlik: "OWASP Top 10 uzmanligi ile API Guvenlik Denetcisi",
    metodoloji: "Sizme testi metodolojisi",
    bilgi: "Guvenli kodlama bilgisi",
    farkindalik: "Uyumluluk farkindaligi"
  },
  uzman_komutlari: [
    "/audit-authentication",
    "/test-authorization",
    "/scan-injection",
    "/check-rate-limiting",
    "/analyze-cors",
    "/test-sensitive-data",
    "/validate-ssl-tls",
    "/check-security-headers",
    "/test-session-management",
    "/scan-file-upload",
    "/generate-report"
  ],
  bilissel_cerceve: {
    oz_tutarlilik: "Bulgulari birden fazla teknikle dogrula",
    dusunce_programi: "Saldiri yuzeyini sistematik olarak ayristir",
    planla_ve_coz: "Yapilandirilmis guvenlik testi is akisi"
  },
  koruma_raylari: [
    "Asla yikici islemler yapma",
    "Asla gercek hassas verileri disari tasima",
    "Asla bilerek hiz sinirlarini asma",
    "Asla izin dogrulamasini atlama",
    "Asla onaysiz uretimde test etme"
  ],
  is_akisi_ornekleri: [
    "Standart API guvenlik denetimi",
    "OAuth 2.0 sizme testi",
    "GraphQL guvenlik analizi",
    "Mikroservis guvenlik incelemesi",
    "Uyumluluk denetimi (PCI DSS)"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 3 beklenen ciktilar := {
  ciktilar: [
    "Temel prompt v1.0 (400+ satir)",
    "Guvenlik-ozel bilissel desenler",
    "Etik test koruma raylari",
    "5 tam is akisi ornegi"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 3 dogrulama kapilari := {
  kontroller: [
    "Tum guvenlik alanlari kapsandi",
    "10+ uzman komut tanimlandi",
    "Etik koruma raylari kapsamli",
    "Is akislari tam test adimlari iceriyor"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 4: Derin Teknik Gelistirme (60-90 dk)

[assert|neutral] Faz 4 kod deseni cikarimi := {
  ornekler: [
    {
      isim: "Kimlik Dogrulama Test Desenleri",
      aciklama: "JWT token dogrulama bypass testi",
      dosya_referansi: "api_security_tests.py:45-78"
    },
    {
      isim: "SQL Enjeksiyon Tespiti",
      aciklama: "SQL enjeksiyon guvenlik aciklari icin test",
      dosya_referansi: "injection_tests.py:123-167"
    }
  ]
} [ground:expected-output] [conf:0.90] [state:confirmed]

[assert|neutral] Faz 4 kritik hata modu dokumantasyonu := {
  ornek: {
    isim: "IDOR ile Kimlik Dogrulama Bypass",
    ciddiyet: "Kritik",
    belirtiler: "Kullanici diger kullanicilara ait kaynaklara erisebiliyor",
    kok_neden: "Kimlik dogrulamadan sonra yetkilendirme kontrolleri eksik",
    onleme: "Kaynak erisiminden once yetkilendirme kontrolu uygula"
  }
} [ground:expected-output] [conf:0.90] [state:confirmed]

[assert|neutral] Faz 4 MCP entegrasyon desenleri := {
  ornekler: [
    {
      islem: "Guvenlik acigi bulgularini sakla",
      arac: "mcp__claude-flow__memory_store",
      anahtar_deseni: "api-security-auditor/audit-123/findings"
    },
    {
      islem: "GitHub'a raporla",
      arac: "mcp__github__create_issue",
      etiketler: ["security", "high-severity"]
    }
  ]
} [ground:expected-output] [conf:0.90] [state:confirmed]

[assert|neutral] Faz 4 performans metrikleri := {
  kategoriler: [
    {
      isim: "Guvenlik Acigi Tespiti",
      metrikler: ["buluna-guvenlik-acigi", "ciddiyet-dagilimi"]
    },
    {
      isim: "Denetim Kalitesi",
      metrikler: ["yanlis-pozitifler", "kapsama", "endpoint-basina-sure"]
    },
    {
      isim: "Uyumluluk",
      metrikler: ["pci-dss-kontroller", "gdpr-uyumluluk"]
    }
  ]
} [ground:expected-output] [conf:0.90] [state:confirmed]

[assert|neutral] Faz 4 beklenen ciktilar := {
  ciktilar: [
    "Gelistirilmis prompt v2.0 (600+ satir)",
    "15+ guvenlik test kod deseni",
    "10+ tespitli hata modu",
    "Tam MCP entegrasyon ornekleri",
    "Guvenlik metrikleri cercevesi",
    "Uyumluluk kontrol listesi sablonlari"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 4 dogrulama kapilari := {
  kontroller: [
    "15+ dosya referansli kod deseni",
    "Tum OWASP Top 10 kapsandi",
    "Etik test koruma raylari kodda zorlanmis",
    "MCP desenleri tam sozdizimi gosteriyor",
    "Metrikler surekli iyilestirme sagliyor"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

---

## Tam Test Yurutme (Complete Test Execution)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### Tam 4-Faz Calistirma

[assert|neutral] Tam calistirma komutu := {
  komut: "python 4_phase_sop.py --agent-name api-security-auditor --mode interactive",
  calisma_dizini: "C:\\Users\\17175\\claude-code-plugins\\ruv-sparc-three-loop-system\\skills\\agent-creator\\resources\\scripts",
  notlar: [
    "Faz 1-3 otomatik",
    "Faz 4 manuel gelistirme (kod desenleri, hata modlari, metrikler)"
  ]
} [ground:test-setup] [conf:0.90] [state:confirmed]

### Dogrulama

[assert|neutral] Dogrulama komutu := {
  komut: "bash ../scripts/validate_prompt.sh agent-outputs/api-security-auditor/api-security-auditor-enhanced-prompt-v2.md -v -s 90",
  beklenen: "Skor >= 90% (Gold kademe)"
} [ground:validation-step] [conf:0.90] [state:confirmed]

### Kapsamli Test

[assert|neutral] Kapsamli test komutu := {
  komut: "python ../scripts/test_agent.py --agent api-security-auditor --prompt-file agent-outputs/api-security-auditor/api-security-auditor-enhanced-prompt-v2.md --test-suite comprehensive",
  beklenen: "95%+ testler gecti"
} [ground:test-step] [conf:0.90] [state:confirmed]

### Entegrasyon Testi

[assert|neutral] Entegrasyon test komutu := {
  komut: "python ../scripts/test_agent.py --agent api-security-auditor --test-suite integration",
  beklenen: "Tum entegrasyon testleri gecti"
} [ground:test-step] [conf:0.90] [state:confirmed]

---

## Basari Kriterleri (Success Criteria)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Faz Tamamlanma := {
  kontroller: [
    "Faz 1 kapsamli guvenlik analizi ile tamamlandi",
    "Faz 2 guvenlik uzmanligi ve etik koruma raylari belgeledi",
    "Faz 3 is akislari ile yapilandirilmis temel prompt olusturdu",
    "Faz 4 teknik derinlik ve kod desenleri ile gelistirdi"
  ]
} [ground:acceptance-criteria] [conf:0.90] [state:confirmed]

[assert|neutral] Kalite Kapilari := {
  kontroller: [
    "Dogrulama skoru >= 90% (Gold kademe)",
    "Kapsamli test paketi >= 95% gecme orani",
    "Entegrasyon testleri %100 gecti",
    "Gelistirilmis prompt 600+ satir teknik derinlik"
  ]
} [ground:acceptance-criteria] [conf:0.90] [state:confirmed]

[assert|neutral] Uretim Hazirligi := {
  kontroller: [
    "15+ guvenlik test kod deseni",
    "10+ hata modu belgelendi",
    "Tam OWASP Top 10 kapsamasi",
    "Etik test koruma raylari zorlaniyor",
    "MCP entegrasyonlari tam belirlendi",
    "Performans metrikleri cercevesi"
  ]
} [ground:acceptance-criteria] [conf:0.90] [state:confirmed]

[assert|neutral] Dokumantasyon := {
  kontroller: [
    "Tum 4 faz ciktilari kaydedildi",
    "Ajan spesifikasyonu tamam",
    "Test raporlari uretildi",
    "Dogrulama raporlari uretildi"
  ]
} [ground:acceptance-criteria] [conf:0.90] [state:confirmed]

---

## Beklenen Sure (Expected Duration)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Sure tahmini := {
  faz_1: "35 dakika",
  faz_2: "35 dakika",
  faz_3: "45 dakika",
  faz_4: "75 dakika (teknik gelistirme)",
  test_ve_dogrulama: "15 dakika",
  toplam: "3.5 saat"
} [ground:time-estimate] [conf:0.85] [state:confirmed]

---

## Notlar (Notes)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

[assert|neutral] Test notu := {
  aciklama: "Bu test, tam 4-faz SOP metodolojisinin uretim-hazir ajan urettigini gosterir",
  kapsam: [
    "Gomulmus derin alan uzmanligi",
    "Kanit-tabanli prompt teknikleri",
    "Teknik kod desenleri ve tam uygulamalar",
    "Kapsamli hata modu dokumantasyonu",
    "Tam MCP entegrasyon spesifikasyonlari",
    "Surekli iyilestirme metrikleri"
  ],
  basari_anlami: "Tam 4-faz SOP takip edildiginde gercek teknik derinlige sahip Gold-kademe, uretim-hazir ajanlar uretir"
} [ground:test-documentation] [conf:0.88] [state:confirmed]

---

<promise>TEST_3_4PHASE_SOP_VCL_V3.1.1_VERIX_COMPLIANT</promise>
