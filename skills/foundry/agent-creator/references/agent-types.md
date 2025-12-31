# Ajan Turleri ve Kaliplari (Agent Types & Patterns)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 GENEL_BAKIS (Overview) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Genel Bakis (Overview)

<!-- [[MOR:root:A-J-N]] Ajan = root morpheme for agent-actor-executor -->
<!-- [[COM:Ajan+Turleri+Referansi]] German compound: Agententypenreferenz -->
[assert|neutral] AJAN_KATEGORILERI := {
  uzman_ajanlar: "Tek alanda derin uzmanlik",
  koordinator_ajanlar: "Coklu ajan orkestrasyonu, is akisi yonetimi",
  hibrit_ajanlar: "Cok alanli uzmanlik + koordinasyon yetenekleri"
} [ground:witnessed:classification] [conf:0.95] [state:confirmed]

---

<!-- S2 UZMAN_AJANLAR (Specialist Agents) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Tur 1: Uzman Ajanlar (Type 1: Specialist Agents)

### Karakteristikler (Characteristics)

[assert|neutral] UZMAN_KARAKTERISTIKLERI := {
  tek_alan_odagi: "Tek spesifik alanda uzman (pazarlama, frontend gelistirme, veri analizi)",
  derin_bilgi: "Alan araclari, kaliplari, en iyi uygulamalar konusunda kapsamli anlayis",
  ozerk_yurutme: "Alana ozgu gorevleri bagimsiz olarak tamamlayabilir",
  sinirli_koordinasyon: "Nadiren alt-ajan olusturur (alan icinde kendine yeterli)"
} [ground:witnessed:specialist-definition] [conf:0.92] [state:confirmed]

### Ne Zaman Kullanilir (When to Use)

[assert|emphatic] UZMAN_KULLANIM_DURUMLARI := [
  "Derin alan uzmanligi gerektiren gorevler",
  "Tek alan icindeki yinelenen is akislari",
  "Hizin onemli oldugu durumlar (koordinasyon yuku yok)",
  "Tutarlilik kritik oldugunda (alana ozgu en iyi uygulamalar)"
] [ground:witnessed:use-cases] [conf:0.90] [state:confirmed]

### Ornekler (Examples)

[assert|neutral] UZMAN_ORNEKLERI := [
  {
    ajan: "Pazarlama Uzmani",
    alan: "Pazarlama stratejisi, kampanya optimizasyonu, hedef kitle analitiyi",
    araclar: ["Google Analytics", "SEMrush", "HubSpot"],
    komutlar: ["/campaign-analyze", "/audience-segment", "/ab-test-design", "/roi-calculate"],
    koordinasyon: "Minimal (sadece karmasik istatistikler icin Veri Analistine devreder)"
  },
  {
    ajan: "Frontend Gelistirici Uzmani",
    alan: "React, TypeScript, UI/UX, erisilebilirlik",
    araclar: ["React 18", "Vite", "TailwindCSS", "Vitest"],
    komutlar: ["/react-component", "/frontend-optimize", "/accessibility-audit"],
    koordinasyon: "Yok (frontend alaninda tamamen ozerk)"
  },
  {
    ajan: "Veritabani Uzmani",
    alan: "PostgreSQL, sorgu optimizasyonu, sema tasarimi",
    araclar: ["PostgreSQL 15", "Prisma", "pgAdmin", "EXPLAIN ANALYZE"],
    komutlar: ["/db-schema", "/db-migration", "/db-optimize-query", "/db-backup"],
    koordinasyon: "Minimal (API kontratlari icin Backend Gelistiriciyle koordinasyon)"
  }
] [ground:witnessed:examples] [conf:0.88] [state:confirmed]

### Olusturma Suresi (Creation Time)

[assert|neutral] UZMAN_SURE := {
  ilk_kez: "3-4 saat (Faz 1-4 tam)",
  hizli_kosma: "1.5-2 saat (sablonlarla deneyimli olusturucular)"
} [ground:witnessed:timing] [conf:0.90] [state:confirmed]

---

<!-- S3 KOORDINATOR_AJANLAR (Coordinator Agents) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Tur 2: Koordinator Ajanlar (Type 2: Coordinator Agents)

### Karakteristikler (Characteristics)

[assert|neutral] KOORDINATOR_KARAKTERISTIKLERI := {
  orkestrasyon_odagi: "Is akislarini yonetir, birden fazla uzman ajani olusturur/koordine eder",
  genis_bilgi: "Birden fazla alanin anlasilmasi (hicbirinde derin uzmanlik degil)",
  bagimlilik_yonetimi: "Gorev bagimliliklarini cozer, yurutme DAG'lari olusturur",
  hata_kurtarma: "Basarisizliklari, geri almalari, yuksealtmeleri yonetir",
  durum_yonetimi: "Dagitim durumunu, kaynak envanterlerini izler"
} [ground:witnessed:coordinator-definition] [conf:0.92] [state:confirmed]

### Ne Zaman Kullanilir (When to Use)

[assert|emphatic] KOORDINATOR_KULLANIM_DURUMLARI := [
  "Coklu ajan is akislari (5+ ajan)",
  "Karmasik bagimlíliklar (sirasal, paralel, kosullu yurutme)",
  "Altyapi orkestrasyonu (DevOps, CI/CD)",
  "Hata kurtarmanin kritik oldugu durumlar (geri alma yetenekleri)"
] [ground:witnessed:use-cases] [conf:0.90] [state:confirmed]

### Ornekler (Examples)

[assert|neutral] KOORDINATOR_ORNEKLERI := [
  {
    ajan: "DevOps Koordinatoru",
    orkestra_eder: ["Terraform", "Kubernetes", "Docker", "Monitoring ajanlar"],
    is_akislari: ["Altyapi dagitimi", "Geri alma", "Saglik izleme"],
    temel_kalilar: ["DAG cozumleme", "Paralel yurutme", "Hata kurtarma"],
    durum: ["Dagitim manifestleri", "Kaynak ID'leri", "Geri alma durumu"]
  },
  {
    ajan: "Proje Yonetici Koordinatoru",
    orkestra_eder: ["Gelistirici", "Tasarimci", "Testci", "Inceleyici ajanlar"],
    is_akislari: ["Ozellik gelistirme", "Sprint planlama", "Surum yonetimi"],
    temel_kalilar: ["Gorev ayristirma", "Bagimlilik izleme", "Ilerleme izleme"],
    durum: ["Proje zaman cizelgesi", "Gorev atamalari", "Tamamlanma durumu"]
  },
  {
    ajan: "CI/CD Boru Hatti Koordinatoru",
    orkestra_eder: ["Build", "Test", "Guvenlik Tarama", "Dagitim ajanlar"],
    is_akislari: ["Surekli entegrasyon", "Surekli dagitim", "Geri alma"],
    temel_kalilar: ["Boru hatti asamalari", "Basarisizlik isleme", "Artifact yonetimi"],
    durum: ["Build artifactlari", "Test sonuclari", "Dagitim gecmisi"]
  }
] [ground:witnessed:examples] [conf:0.88] [state:confirmed]

### Olusturma Suresi (Creation Time)

[assert|neutral] KOORDINATOR_SURE := {
  ilk_kez: "4-5 saat (orkestrasyon mantigi karmasik)",
  hizli_kosma: "2.5-3 saat (DAG sablonlariyla)"
} [ground:witnessed:timing] [conf:0.90] [state:confirmed]

---

<!-- S4 HIBRIT_AJANLAR (Hybrid Agents) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Tur 3: Hibrit Ajanlar (Type 3: Hybrid Agents)

### Karakteristikler (Characteristics)

[assert|neutral] HIBRIT_KARAKTERISTIKLERI := {
  cok_alanli_uzmanlik: "2-4 iliskili alanda derin bilgi",
  koordinator_yetenekleri: "Karmasik alt-gorevler icin alt-ajanlar olusturabilir",
  baglam_degistirme: "Alanlar arasinda verimli gecis",
  uctan_uca_sahiplik: "Birden fazla alani kapsayan ozellikleri tamamlar",
  akilli_delegasyon: "Ne zaman devrетme vs. dogrudan uygulama bilir"
} [ground:witnessed:hybrid-definition] [conf:0.92] [state:confirmed]

### Ne Zaman Kullanilir (When to Use)

[assert|emphatic] HIBRIT_KULLANIM_DURUMLARI := [
  "Tam-yigin ozellikler (frontend + backend + veritabani)",
  "Orta karmasiklikta ozellikler (standart auth, CRUD, formlar)",
  "Uctan uca sahiplik gerektiginde (tek ajan, tam teslimat)",
  "Iliskili teknoloji yiginlarina sahip projeler (React + Node.js)"
] [ground:witnessed:use-cases] [conf:0.90] [state:confirmed]

### Ornekler (Examples)

[assert|neutral] HIBRIT_ORNEKLERI := [
  {
    ajan: "Tam-Yigin Gelistirici",
    alanlar: ["Frontend (React/TS)", "Backend (Node.js)", "Veritabani (PostgreSQL)", "DevOps (Docker)"],
    koordinasyon: "Karmasik alt-gorevler icin Algoritma, Guvenlik, Performans uzmanlari olusturur",
    is_akisi: "API-ilk tasarim -> Backend -> Frontend -> Testler -> Dagitim",
    delegasyon: "Karmasiklik >2 saat VEYA 4 cekirdek alan disinda olunca devreder"
  },
  {
    ajan: "Veri Bilimci + ML Muhendisi",
    alanlar: ["Veri analizi (Python/pandas)", "ML modelleme (scikit-learn/PyTorch)", "ML ops (MLflow)", "Dagitim (FastAPI)"],
    koordinasyon: "ETL boru hatlari icin Veri Muhendisi, Kubernetes dagitimi icin DevOps olusturur",
    is_akisi: "Veri kesfetme -> Ozellik muhendisligi -> Model egitimi -> Dagitim -> Izleme",
    delegasyon: "Altyapi, karmasik ETL devreder"
  },
  {
    ajan: "Mobil + Backend Gelistirici",
    alanlar: ["Mobil (React Native)", "Backend (Node.js)", "Veritabani (PostgreSQL)", "API tasarimi"],
    koordinasyon: "Karmasik animasyonlar icin UI Tasarimci, auth icin Guvenlik Uzmani olusturur",
    is_akisi: "API tasarimi -> Backend -> Mobil UI -> Entegrasyon testleri -> App store dagitimi",
    delegasyon: "UI cilalama, guvenlik denetimleri devreder"
  }
] [ground:witnessed:examples] [conf:0.88] [state:confirmed]

### Olusturma Suresi (Creation Time)

[assert|neutral] HIBRIT_SURE := {
  ilk_kez: "5-6 saat (birden fazla alan + koordinasyon mantigi)",
  hizli_kosma: "3-3.5 saat (cok alanli sablonlarla)"
} [ground:witnessed:timing] [conf:0.90] [state:confirmed]

---

<!-- S5 KARAR_MATRISI (Decision Matrix) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Karar Matrisi: Hangi Ajan Turu? (Decision Matrix: Which Agent Type?)

[assert|emphatic] KARAR_MATRISI := {
  gorev_kapsami: {
    tek_alan: "Uzman",
    coklu_ajan_is_akisi: "Koordinator",
    cok_alanli_ozellik: "Hibrit"
  },
  gereken_derinlik: {
    uzman_duzeyinde: "Uzman",
    genis_anlayis: "Koordinator",
    iki_dort_alanda_uzman: "Hibrit"
  },
  koordinasyon: {
    minimal: "Uzman",
    yuksek: "Koordinator",
    orta: "Hibrit"
  },
  hiz: {
    en_hizli: "Uzman (koordinasyon yuku yok)",
    daha_yavas: "Koordinator (koordinasyon)",
    orta: "Hibrit"
  },
  ornek_gorevler: {
    uzman: "PostgreSQL sorgularini optimize et",
    koordinator: "Tam-yigin uygulamayi dagit",
    hibrit: "Auth ozelligi olustur (frontend + backend)"
  }
} [ground:witnessed:decision-framework] [conf:0.92] [state:confirmed]

---

<!-- S6 UZMANLIK_KALIPLARI (Specialization Patterns) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Alana Gore Uzmanlik Kaliplari (Specialization Patterns by Domain)

### Analitik Ajanlar (Uzman) (Analytical Agents - Specialist)

[assert|neutral] ANALITIK_KALIP := {
  odak: "Veri analizi, kanit degerlendirme, dogrulama",
  temel_karakteristikler: [
    "Oz-tutarlilik dogrulamasi (cok acili kontroller)",
    "Istatistiksel titizlik (anlam testleri, guven araliklari)",
    "Veri kalitesi standartlari (tamliligi, dogruluk)"
  ],
  ornekler: ["Veri Analisti", "Arastirma Analisti", "Kalite Denetcisi", "A/B Test Analisti"]
} [ground:witnessed:pattern-analytical] [conf:0.88] [state:confirmed]

### Uretici Ajanlar (Uzman) (Generative Agents - Specialist)

[assert|neutral] URETICI_KALIP := {
  odak: "Icerik olusturma, tasarim, sentez",
  temel_karakteristikler: [
    "Plan-ve-coz yurutme (anahat -> taslak -> cilalama)",
    "Kalite kriterleri (okunabilirlik, etkilesim, dogruluk)",
    "Iyilestirme donguler (yinelemeli iyilestirme)"
  ],
  ornekler: ["Icerik Yazari", "Pazarlama Metin Yazari", "UI Tasarimci", "Dokumantasyon Uzmani"]
} [ground:witnessed:pattern-generative] [conf:0.88] [state:confirmed]

### Teshis Ajanlari (Uzman) (Diagnostic Agents - Specialist)

[assert|neutral] TESHIS_KALIBI := {
  odak: "Problem tanimlama, hata ayiklama, kok neden analizi",
  temel_karakteristikler: [
    "Dusunce programi ayristirmasi (problemi alt-problemlere bol)",
    "Hipotez uretme ve test etme",
    "Sistematik sorun giderme"
  ],
  ornekler: ["Hata Ayiklama Uzmani", "Performans Analizcisi", "Guvenlik Denetcisi", "Olay Yanit"]
} [ground:witnessed:pattern-diagnostic] [conf:0.88] [state:confirmed]

### Orkestrasyon Ajanlari (Koordinator) (Orchestration Agents - Coordinator)

[assert|neutral] ORKESTRASYON_KALIBI := {
  odak: "Is akisi koordinasyonu, ajan yonetimi, bagimlilik cozumleme",
  temel_karakteristikler: [
    "DAG insa etme ve cevrim tespiti",
    "Hiz sinirlamasiyla paralel yurutme",
    "Hata yayilimi ve geri alma"
  ],
  ornekler: ["DevOps Koordinatoru", "Proje Yonetici", "CI/CD Boru Hatti Koordinatoru", "Is Akisi Orkestratoru"]
} [ground:witnessed:pattern-orchestration] [conf:0.88] [state:confirmed]

### Cok-Alanli Ajanlar (Hibrit) (Multi-Domain Agents - Hybrid)

[assert|neutral] COK_ALANLI_KALIP := {
  odak: "Birden fazla alanda uctan uca ozellik teslimati",
  temel_karakteristikler: [
    "Baglam degistirme protokolu",
    "Delegasyon karar cercevesi",
    "Entegrasyon-ilk is akislari"
  ],
  ornekler: ["Tam-Yigin Gelistirici", "Veri Bilimci + ML Muhendisi", "Mobil + Backend Gelistirici"]
} [ground:witnessed:pattern-multi-domain] [conf:0.88] [state:confirmed]

---

<!-- S7 KARISIK_KALIPLAR (Mixing Patterns) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Karisik Kaliplar: Ne Zaman Birlestirmeli (Mixing Patterns: When to Combine)

### Uzman + Koordinator (Specialist + Coordinator)

[assert|neutral] UZMAN_KOORDINATOR_KARISIMI := {
  senaryo: "Uzman ajan bazen diger uzmanlarla koordine eder",
  ornek: "Guvenlik Uzmani ajani: Guvenlik denetimleri yapar (uzman), Gelismis testler icin Penetrasyon Testi ajani olusturur (koordinator)",
  uygulama: "Penetrasyon testi gerektiginde Penetrasyon Testi Uzmanina devret, Karmasik kriptografik analiz icin Kriptografi Uzmanina devret, Aksi halde guvenlik alaninda ozerk calis"
} [ground:witnessed:mixing-patterns] [conf:0.88] [state:confirmed]

### Hibrit + Yogun Koordinasyon (Hybrid + Extensive Coordination)

[assert|neutral] HIBRIT_YOGUN_KOORDINASYON := {
  senaryo: "Hibrit ajan sik sik devretir, koordinator gibi davranir",
  ornek: "Teknik Lider ajani: Mimari, backend, frontend uzmanligi var (hibrit), Uygulama icin sik sik Gelistirici ajanlar olusturur (koordinator), Ust duzey tasarim, kod inceleme, delegasyona odaklanir",
  uygulama: {
    devreder: ["Backend uygulamasi -> Backend Gelistirici", "Frontend uygulamasi -> Frontend Gelistirici", "Veritabani tasarimi -> Veritabani Uzmani"],
    odaklanir: ["Mimari tasarim", "API kontrat tanimi", "Kod inceleme", "Entegrasyon gozetimi"]
  },
  not: "Bu, alan uzmanligiyla saf koordinatore yakin (teknik liderler, mimarlar icin faydali)"
} [ground:witnessed:mixing-patterns] [conf:0.88] [state:confirmed]

---

<!-- S8 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonuc (Summary)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[assert|confident] OZET := {
  ajan_turleri: {
    uzman: "Derin tek-alan uzmanligi, ozerk, minimal koordinasyon",
    koordinator: "Coklu ajan orkestrasyonu, genis bilgi, hata kurtarma",
    hibrit: "Cok-alanli uzmanlik + koordinasyon, uctan uca sahiplik"
  },
  karar_kriterleri: {
    gorev_kapsami: "Tek alan -> Uzman | Coklu ajan -> Koordinator | Cok alanli ozellik -> Hibrit",
    gereken_derinlik: "Uzman duzeyinde -> Uzman | Genis anlayis -> Koordinator | 2-4 alanda uzman -> Hibrit",
    koordinasyon: "Minimal -> Uzman | Yuksek -> Koordinator | Orta -> Hibrit"
  },
  olusturma_karmasikligi: {
    uzman: "3-4 saat (en basit)",
    koordinator: "4-5 saat (orkestrasyon mantigi)",
    hibrit: "5-6 saat (en karmasik - birden fazla alan + koordinasyon)"
  },
  tavsiye: "Optimal performans icin ajan turunu gorev gereksinimlerine uygun sec"
} [ground:witnessed:summary] [conf:0.95] [state:confirmed]

---

<promise>AGENT_TYPES_VCL_VERIX_COMPLIANT</promise>
