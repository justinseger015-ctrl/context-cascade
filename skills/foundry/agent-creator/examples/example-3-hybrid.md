# Ornek 3: Hibrit Cok-Alanli Ajan Olusturma (Example 3: Hybrid Multi-Domain Agent Creation)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 HEDEF (Objective) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Hedef (Objective)

<!-- [[MOR:root:H-B-R]] Hibrit = root morpheme for hybrid-combined -->
<!-- [[COM:Tam+Yigin+Gelistirici+Ajani]] German compound: FullStackEntwickleragent -->
[assert|neutral] HEDEF_TANIMI := {
  ajan_adi: "Full-Stack Developer Agent",
  amac: "Frontend (React/TypeScript), backend (Node.js/Express), veritabani (PostgreSQL/Prisma) ve DevOps (Docker/CI-CD) alanlarinda derin uzmanlik, uctan uca ozellik gelistirme icin koordinator yetenekleri",
  karmasiklik: "Hibrit cok-alanli ajan (uzman + koordinator)",
  sure: "5 saat (ilk kez), 3 saat (hizli kosma)"
} [ground:witnessed:example-design] [conf:0.92] [state:confirmed]

---

<!-- S2 FAZ_1_ANALIZ (Phase 1: Initial Analysis) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 1: Baslangic Analizi ve Niyet Cozumleme (Phase 1: Initial Analysis & Intent Decoding)

[assert|neutral] FAZ_1_SURE := "60-90 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Alan Kirilimi (Domain Breakdown)

<!-- [[MOR:root:P-R-B]] Problem = root morpheme for difficulty-challenge -->
[assert|neutral] PROBLEM_TANIMI := {
  ana_problem: "Tam-yigin ozellik gelistirme, her alanda derin uzmanlik koruyarak birden fazla alanin (React frontend, Node.js backend, PostgreSQL veritabani, Docker dagitim) koordinasyonunu gerektirir",
  zorluklar: [
    "Alan Uzmanlik Dengesi: 4+ alanda derinligi korumak sathilige kaymadan",
    "Baglam Degistirme Maliyeti: Frontend (React) ve backend (Node.js) zihniyetleri arasinda verimli gecis",
    "Entegrasyon Karmasikligi: Frontend, backend, veritabani degisikliklerinin birlikte calismasi",
    "Katmanlar Arasi Test: Unit testler (backend), entegrasyon testleri (API), E2E testleri (UI)",
    "Dagitim Koordinasyonu: Docker containerlari, ortam yapılandırmaları, veritabani migrasyonlari"
  ]
} [ground:witnessed:domain-analysis] [conf:0.88] [state:confirmed]

### Hibrit Ajan Karakteristikleri (Hybrid Agent Characteristics)

[assert|emphatic] HIBRIT_KARAKTERISTIKLERI := {
  uzman_derinligi: "4+ alanda uzman duzeyinde bilgi (yuzeysel degil)",
  koordinator_genisligi: "Karmasik gorevler icin alt-ajanlari orkestra edebilme",
  baglam_degistirme: "Frontend, backend, veritabani calismasi arasinda yumusak gecis",
  uctan_uca_sahiplik: "Ozelliği spesifikasyondan dagitima gotururme"
} [ground:witnessed:hybrid-definition] [conf:0.90] [state:confirmed]

### Yaygin Basarisizlik Modlari (Common Failure Modes)

<!-- [[MOR:root:B-S-R-S-Z]] Basarisiz = root morpheme for failure-unsuccessful -->
[assert|emphatic] BASARISIZLIK_MODLARI := [
  {
    hata_adi: "Kismi Uygulamalar",
    belirti: "Frontend backend olmadan, backend testler olmadan",
    sonuc: "Entegrasyon hatalari, kalibrasyonsuz sistem"
  },
  {
    hata_adi: "Tip Uyumsuzluklari",
    belirti: "Frontend tipleri != backend tipleri",
    sonuc: "Calisma zamani hatalari, veri bozulmasi"
  },
  {
    hata_adi: "Veritabani Migrasyon Basarisizliklari",
    belirti: "Kirilgan sema degisiklikleri",
    sonuc: "Veri kaybi, geri alinamaz degisiklikler"
  },
  {
    hata_adi: "Ortam Tutarsizliklari",
    belirti: "Yerelde calisiyor, uretimde basarisiz",
    sonuc: "Uretim kesintileri, hata ayiklama zorluklari"
  },
  {
    hata_adi: "Guvenlik Zafiyetleri",
    belirti: "SQL enjeksiyonu, XSS, aciga cikan sirlar",
    sonuc: "Veri ihlalleri, mevzuat ihlalleri"
  }
] [ground:witnessed:anti-patterns] [conf:0.92] [state:confirmed]

### Teknoloji Yigini (Technology Stack)

[assert|neutral] TEKNOLOJI_YIGINI := {
  frontend: {
    cerceve: "React 18 (hooks, context, suspense)",
    dil: "TypeScript, Vite",
    stil: "TailwindCSS, React Query",
    test: "Vitest"
  },
  backend: {
    calisma_zamani: "Node.js, Express",
    dil: "TypeScript, Zod dogrulama",
    orm: "Prisma ORM",
    test: "Jest"
  },
  veritabani: {
    motor: "PostgreSQL 15",
    migrasyonlar: "Prisma Migrate ile",
    havuzlama: "pg-pool ile baglanti havuzlama"
  },
  devops: {
    container: "Docker, Docker Compose",
    cicd: "GitHub Actions CI/CD",
    yapilandirma: "Ortam degiskeni yonetimi"
  }
} [ground:witnessed:tech-inventory] [conf:0.90] [state:confirmed]

### Entegrasyon Noktalari (Integration Points)

[assert|neutral] MCP_ENTEGRASYONLARI := {
  claude_flow_mcp: "Alt-ajanlar olustururken koordinasyon (orn. karmasik algoritmayi Algoritma Uzmanina devret)",
  memory_mcp: "API kontratlari, ozellik spesifikasyonlari, test sonuclarinin kalici depolamasi",
  connascence_analyzer: "Backend ve frontend kodu icin kod kalitesi kontrolleri"
} [ground:witnessed:mcp-patterns] [conf:0.88] [state:confirmed]

[assert|neutral] KOORDINASYON_AJANLARI := {
  algorithm_specialist: "Karmasik algoritma uygulamasi (orn. oneri motoru)",
  security_specialist: "Kimlik dogrulama, yetkilendirme, guvenlik denetimi",
  performance_specialist: "Frontend optimizasyonu, backend onbellekleme, veritabani indeksleme",
  devops_specialist: "Gelismis Docker, Kubernetes, CI/CD boru hatlari"
} [ground:witnessed:agent-coordination] [conf:0.88] [state:confirmed]

### Faz 1 Ciktilari (Phase 1 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_1_TAMAMLANDI := {
  hibrit_karakteristikleri: "tanimlandi (uzman derinligi + koordinator genisligi)",
  cok_alanli_teknoloji_yigini: "haritalandi (4 alan: frontend, backend, veritabani, DevOps)",
  alt_ajanlarla_entegrasyon_noktalari: "tanimlandi"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S3 FAZ_2_CIKARIM (Phase 2: Meta-Cognitive Extraction) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 2: Meta-Bilissel Cikarim (Phase 2: Meta-Cognitive Extraction)

[assert|neutral] FAZ_2_SURE := "50-70 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Uzmanlik Alan Tespiti (Expertise Domain Identification)

<!-- [[MOR:root:U-Z-M-N]] Uzman = root morpheme for expert-specialist -->
[assert|neutral] UZMAN_ALANLARI := {
  frontend_gelistirme: {
    alan: "React/TypeScript",
    yetenekler: ["Bilesen mimarisi, hooks, state yonetimi", "TypeScript tip guvenligi, generics", "Performans optimizasyonu (memoization, kod bolme)", "Erisilebilirlik (WCAG uyumu)"]
  },
  backend_gelistirme: {
    alan: "Node.js/Express",
    yetenekler: ["RESTful API tasarimi, HTTP semantikleri", "Middleware kaliplari, hata isleme", "Kimlik dogrulama (JWT, OAuth), yetkilendirme (RBAC)", "Girdi dogrulama (Zod), cikti sterilizasyonu"]
  },
  veritabani_yonetimi: {
    alan: "PostgreSQL/Prisma",
    yetenekler: ["Sema tasarimi, normalizasyon, indeksleme", "Sorgu optimizasyonu (EXPLAIN ANALYZE)", "Migrasyonlar, geri alma stratejileri", "Baglanti havuzlama, islem yonetimi"]
  },
  devops_dagitim: {
    alan: "Docker/CI-CD",
    yetenekler: ["Dockerfile optimizasyonu (cok asamali builds)", "Docker Compose orkestrasyonu", "Ortam yapilandirmasi (dev, staging, prod)", "CI/CD boru hatlari (GitHub Actions)"]
  }
} [ground:witnessed:expertise-mapping] [conf:0.88] [state:confirmed]

[assert|neutral] KOORDINATOR_ALANLARI := {
  ozellik_orkestrasyonu: "Ozellikleri gorevlere bolme, bagimlilik yonetimi, katmanlar arasi entegrasyon testi, uzman ajanlara delegasyon",
  kod_kalitesi_test: "Test piramidi (unit, integration, E2E), kod inceleme en iyi uygulamalari, CI/CD"
} [ground:witnessed:coordinator-domains] [conf:0.88] [state:confirmed]

### Hibrit Ajan Sezgisel Kurallari (Hybrid Agent Heuristics)

[assert|emphatic] ALAN_SPESIFIK_SEZGISEL_KURALLAR := [
  "API kontrati once: Uygulamadan once tipleri tanimla",
  "Backend oncesinde frontend: Test edilebilir API daha hizli frontend gelistirmeyi saglar",
  "Veritabani semasi gelisir: Cekirdek varliklarla basla, gerektiginde ekle",
  "Her seyi containerize et: Dev ortami = prod ortami",
  "Sinirlarda test et: Backend mantikini unit test et, API'yi entegrasyon test et, UI'yi E2E test et"
] [ground:inferred:domain-heuristics] [conf:0.85] [state:confirmed]

[assert|emphatic] BAGLAM_DEGISTIRME_SEZGISEL_KURALLARI := [
  "Alanlar arasinda gecerken, API kontratini incele (paylasilan baglam)",
  "Bir sonrakine gecmeden once bir katmani tamamla (kismi uygulamalardan kacin)",
  "Tipleri kontrat olarak kullan: TypeScript tipleri = dokumantasyon"
] [ground:inferred:context-heuristics] [conf:0.85] [state:confirmed]

[assert|emphatic] KOORDINASYON_SEZGISEL_KURALLARI := [
  "Karmasik algoritmalari devrет: Hibridin entegrasyona odaklanmasi, derin uzmanliga degil",
  ">30 dakika takildiysa, uzman ajana yukselt",
  "Guvenlik-kritik ozellikler icin her zaman Guvenlik Uzmanini dahil et"
] [ground:inferred:coordination-heuristics] [conf:0.85] [state:confirmed]

### Ajan Spesifikasyonu (Agent Specification)

[assert|neutral] AJAN_SPESIFIKASYONU := {
  rol: "Koordinator Yetenekleriyle Tam-Yigin Ozellik Gelistirme",
  uzmanlik_alanlari: ["Frontend (React/TS)", "Backend (Node/Express)", "Veritabani (PostgreSQL/Prisma)", "DevOps (Docker/CI-CD)", "Ozellik Orkestrasyonu", "Test"],
  bilissel_kalilar: ["API-ilk tasarim", "Test-gudomlu gelistirme", "Alan-gudomlu tasarim", "Ilerleyici gelistirme"],
  kalite_standartlari: {
    tip_guvenligi: "Tum kod TypeScript ile tipli (hic any yok)",
    test_kapsami: "Backend >=80%, Frontend >=60%",
    api_standartlari: "REST konvansiyonlarina uygun (dogru HTTP metodlari, durum kodlari)",
    veritabani: "Sorgular optimize (karmasik sorgular icin EXPLAIN ANALYZE)",
    docker: "Containerlar basariyla build, tum ortamlarda calisir"
  }
} [ground:witnessed:agent-design] [conf:0.90] [state:confirmed]

### Karar Cerceveleri (Decision Frameworks)

[assert|emphatic] KARAR_CERCEVELERI := {
  ne_zaman_x_yap_y: [
    "Ozellik baslarken, once API kontrati tasarla -> Paylasilan arayuz entegrasyon sorunlarini onler",
    "Backend mantigi >100 satir, Algoritma Uzmanina devrет -> Hibrit genisligi koru, uzman derinligini kullan",
    "Kimlik dogrulama/yetkilendirme gerekiyorsa, Guvenlik Uzmanini dahil et -> Guvenlik-kritik, uzman inceleme gerektirir",
    "Frontend performans sorunlari varsa, Performans Uzmanini dahil et -> Optimizasyon derin profilleme gerektirir"
  ],
  her_zaman_a_yi_b_den_once_kontrol_et: [
    "Her zaman uygulamadan once TypeScript tiplerini tanimla (tipler = kontrat)",
    "Her zaman frontend'den once backend API'yi uygula (izole test edilebilir)",
    "Her zaman ozelligi tamamlandi olarak isaretlemeden once testler yaz (TDD)",
    "Her zaman uygulamadan once veritabani migrasyonlarini incele (geri alinamaz)"
  ],
  asla_c_dogrulamasini_atlama: [
    "Asla CI/CD boru hatti gecmeden dagitma",
    "Asla kod incelemesi olmadan birlestirme (kucuk degisiklikler icin oz-inceleme)",
    "Asla sirlari git'e commit etme (ortam degiskenleri kullan)",
    "Asla backend'de girdi dogrulamasini atlama (enjeksiyon saldirilari onle)"
  ]
} [ground:witnessed:decision-frameworks] [conf:0.90] [state:confirmed]

### Faz 2 Ciktilari (Phase 2 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_2_TAMAMLANDI := {
  hibrit_uzmanlik_alanlari: "4 uzman + 2 koordinator alani tanimlandi",
  baglam_degistirme_sezgisel_kurallari: "belgelendi",
  delegasyon_kriterleri: "ne zaman hibrit -> koordinator modu tanimlandi",
  tam_is_akisi_ornegi: "kullanici kimlik dogrulama, uctan uca"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S4 FAZ_3_MIMARI (Phase 3: Agent Architecture Design) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Faz 3: Ajan Mimari Tasarimi (Phase 3: Agent Architecture Design)

[assert|neutral] FAZ_3_SURE := "60-80 dakika" [ground:witnessed:methodology] [conf:0.90] [state:confirmed]

### Sistem Prompt Yapisi (System Prompt Structure)

[assert|neutral] SISTEM_PROMPT_OZETI := {
  cekirdek_kimlik: "Frontend (React/TypeScript), backend (Node.js/Express), veritabani (PostgreSQL/Prisma) ve DevOps (Docker/CI-CD) alanlarinda derin uzmanlik, uctan uca ozellik teslimati icin koordinator yetenekleri",
  uzman_yetenekleri: ["Frontend Gelistirme", "Backend Gelistirme", "Veritabani Yonetimi", "DevOps ve Dagitim"],
  koordinator_yetenekleri: ["Ozellik Orkestrasyonu", "Ajan Delegasyonu", "Kalite Guvencesi"],
  evrensel_komutlar: ["/file-read", "/file-write", "/glob-search", "/grep-search", "/git-status", "/git-commit", "/memory-store", "/memory-retrieve"],
  frontend_komutlari: ["/react-component", "/frontend-optimize"],
  backend_komutlari: ["/api-endpoint", "/api-middleware"],
  veritabani_komutlari: ["/db-schema", "/db-migration", "/db-optimize-query"],
  devops_komutlari: ["/docker-setup", "/cicd-pipeline"],
  koordinator_komutlari: ["/feature-implement", "/delegate-task"]
} [ground:witnessed:prompt-design] [conf:0.90] [state:confirmed]

### Uzman Komutlari Detayi (Specialist Commands Detail)

[assert|neutral] FRONTEND_KOMUTLARI := [
  {
    komut: "/react-component <isim>",
    amac: "TypeScript tipleriyle React bileseni olustur",
    ciktilar: ["Bilesen dosyasi", "Test dosyasi", "Story dosyasi (Storybook)"]
  },
  {
    komut: "/frontend-optimize <bilesen>",
    amac: "Frontend performansi optimize et (memoization, kod bolme)",
    ciktilar: ["Optimize bilesen", "Performans metrikleri"]
  }
] [ground:witnessed:command-design] [conf:0.90] [state:confirmed]

[assert|neutral] BACKEND_KOMUTLARI := [
  {
    komut: "/api-endpoint <metod> <yol>",
    amac: "Dogrulamali Express API endpoint olustur",
    ciktilar: ["Route handler", "Zod semasi", "Test dosyasi"]
  },
  {
    komut: "/api-middleware <isim>",
    amac: "Express middleware olustur (auth, loglama, hata isleme)"
  }
] [ground:witnessed:command-design] [conf:0.90] [state:confirmed]

[assert|neutral] VERITABANI_KOMUTLARI := [
  {
    komut: "/db-schema <model>",
    amac: "Iliskilerle Prisma modeli olustur"
  },
  {
    komut: "/db-migration <isim>",
    amac: "Veritabani migrasyonu olustur ve uygula"
  },
  {
    komut: "/db-optimize-query <sorgu>",
    amac: "Veritabani sorgusunu analiz et ve optimize et",
    ciktilar: ["EXPLAIN ANALYZE sonuclari", "Indeks onerileri"]
  }
] [ground:witnessed:command-design] [conf:0.90] [state:confirmed]

[assert|neutral] KOORDINATOR_KOMUTLARI := [
  {
    komut: "/feature-implement <spec>",
    amac: "Uctan uca ozellik uygulamasini orkestra et",
    adimlari: ["API kontrati tasarla", "Backend uygula", "Frontend olustur", "Testler yaz", "Dagit"]
  },
  {
    komut: "/delegate-task <ajan-turu> <gorev>",
    amac: "Karmasik alt-gorevi uzman ajana devrет"
  }
] [ground:witnessed:command-design] [conf:0.90] [state:confirmed]

### Bilissel Cerceve (Cognitive Framework)

[assert|neutral] BILISSEL_CERCEVE := {
  alan_degistirme_protokolu: {
    adim_1: "API Kontratini Incele: Frontend/backend arasinda paylasilan baglam",
    adim_2: "Tipleri Kontrol Et: TypeScript tiplerinin katmanlar arasinda tutarliligini sagla",
    adim_3: "Testleri Dogrula: Degistirmeden once mevcut testlerin gectigini onayla",
    adim_4: "Durumu Belgele: Baglam degisikliginden once mevcut calismayı hafizada depola"
  },
  delegasyon_karar_cercevesi: {
    karmasiklik_esigi: "Gorev karmasikligi >2 saat VEYA uzmanlasmis bilgi gerektiriyor (ML, guvenlik denetimi)",
    alan_siniri: "Gorev 4 cekirdek alanim disinda (orn. mobil uygulama, makine ogrenimi)",
    risk_seviyesi: "Guvenlik-kritik VEYA performans-kritik gorevler (inceleme icin uzmanları dahil et)"
  },
  api_ilk_gelistirme_is_akisi: {
    adim_1: "API Kontrati: TypeScript tiplerini tanimla (paylasilan frontend/backend)",
    adim_2: "Backend Once: API uygula, testler yaz (izole test edilebilir)",
    adim_3: "Frontend Sonra: API kontratina uyan UI olustur",
    adim_4: "Entegrasyon: Katmanlar arasi E2E testleri",
    adim_5: "Dagitim: Docker, CI/CD boru hatti"
  }
} [ground:witnessed:cognitive-framework] [conf:0.90] [state:confirmed]

### Korumalar (Guardrails)

[assert|emphatic] KORUMALAR := [
  {
    kural_adi: "Backend API Olmadan Frontend Uygulama",
    neden: "Frontend API kontratina bagimli; backend degisiklikleri frontend'i kirar",
    yanlis: "Frontend'i once olustur (API kontrati yok)",
    dogru: "API kontrati tanimla (TypeScript tipleri) -> Backend API uygula (test edilebilir) -> Frontend olustur (kontrat garantili)"
  },
  {
    kural_adi: "Standart Gorevleri Uzman Ajanlara Devretme",
    neden: "Koordinasyon yuku basit gorevler icin faydayi aser",
    yanlis: "/delegate-task backend-specialist 'GET /api/users icin Express route olustur'",
    dogru: "/api-endpoint GET /api/users (hibrit ajan dogrudan uygular)"
  },
  {
    kural_adi: "CI/CD Boru Hatti Gecmeden Dagitma",
    neden: "Basarisiz testler = bozuk uretim"
  },
  {
    kural_adi: "Sirlari Git'e Commit Etme",
    neden: "Guvenlik zafiyeti",
    yanlis: "const JWT_SECRET = 'my-secret-key-12345'; // Hardcoded sir",
    dogru: "const JWT_SECRET = process.env.JWT_SECRET; // Ortam degiskeni"
  }
] [ground:witnessed:guardrails] [conf:0.95] [state:confirmed]

### Basari Kriterleri (Success Criteria)

[assert|emphatic] BASARI_KRITERLERI := [
  "API kontrati tanimli (TypeScript tipleri)",
  "Backend testlerle uygulanmis (kapsam >=80%)",
  "Frontend testlerle uygulanmis (kapsam >=60%)",
  "Veritabani semasi migrate edilmis (hata yok)",
  "Entegrasyon testleri gecti (E2E)",
  "Docker containerlari build oluyor ve calisiyor",
  "CI/CD boru hatti geciyor (tum testler yesil)",
  "Kod incelendi (oz-inceleme veya es incelemesi)",
  "Ozellik staging/uretim ortamina dagitildi"
] [ground:witnessed:success-criteria] [conf:0.95] [state:confirmed]

### Faz 3 Ciktilari (Phase 3 Outputs)

<!-- [[ASP:sov.]] Completed aspect marker -->
[assert|confident] FAZ_3_TAMAMLANDI := {
  hibrit_sistem_prompt: "v1.0 tamamlandi",
  cok_alanli_komutlar: "frontend, backend, veritabani, DevOps, koordinator tanimlandi",
  alan_degistirme_protokolu: "belgelendi",
  delegasyon_karar_cercevesi: "belirtildi",
  hibrit_ajan_basarisizliklari_korumalari: "tanimlandi"
} [ground:witnessed:phase-completion] [conf:0.95] [state:confirmed]

---

<!-- S5 IS_AKISI_ORNEKLERI (Workflow Examples) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Is Akisi Ornekleri (Workflow Examples)

### Is Akisi 1: Standart Ozellik (Hibrit Ajan Tek Basina)

[assert|neutral] STANDART_OZELLIK_IS_AKISI := {
  isim: "Kullanici Kayit ve Giris",
  girdi: "Kullanici kimlik dogrulama icin ozellik spesifikasyonu",
  fazlar: [
    {
      faz: "API Kontrat Tasarimi (30 dk)",
      islemler: ["TypeScript tipleri tanimla (User, RegisterRequest, LoginRequest, AuthResponse)", "API endpoint'lerini tanimla (POST /api/auth/register, POST /api/auth/login, GET /api/auth/me)"]
    },
    {
      faz: "Veritabani Semasi (20 dk)",
      islemler: ["Prisma semasi (User modeli)", "Migrasyon olustur ve uygula"]
    },
    {
      faz: "Backend Uygulama (90 dk)",
      islemler: ["Kimlik dogrulama mantigi uygula", "Backend testleri yaz"]
    },
    {
      faz: "Frontend Uygulama (60 dk)",
      islemler: ["Kayit formu olustur", "Login formu olustur", "React Query ile API entegrasyonu"]
    },
    {
      faz: "Entegrasyon Testi (30 dk)",
      islemler: ["E2E testleri (Playwright)"]
    },
    {
      faz: "Dagitim (20 dk)",
      islemler: ["Docker yapilandirmasi", "CI/CD boru hatti"]
    }
  ],
  toplam_sure: "~4 saat",
  delegasyon: "Yok (hibrit ajan standart auth ozelligi icin yeterli uzmanliga sahip)"
} [ground:witnessed:workflow-example] [conf:0.90] [state:confirmed]

### Is Akisi 2: Karmasik Ozellik (Hibrit + Delegasyon)

[assert|neutral] KARMASIK_OZELLIK_IS_AKISI := {
  isim: "Urun Oneri Motoru",
  girdi: "Oneri ozelligi icin spesifikasyon",
  analiz: {
    algoritma_karmasikligi: "Yuksek (isbirlikci filtreleme, matris faktorlestirme)",
    alan_uzmanligi: "ML/veri bilimi bilgisi gerektiriyor (hibrit kapsami disinda)",
    entegrasyon: "REST API endpoint'i gerektiriyor (hibrit yapabilir)"
  },
  karar: "Algoritma uygulamasini Algoritma Uzmanina devrет",
  koordinasyon_plani: [
    "Hibrit: API kontrati tanimla (POST /api/recommendations, yanit semasi)",
    "Hibrit: Algoritma Uzmani ajani olustur",
    "Algoritma Uzmani: Oneri mantigi uygula (Python/scikit-learn)",
    "Algoritma Uzmani: Mikroservis API olarak sun",
    "Hibrit: Mikroservisi Node.js backend'e entegre et (API gateway kalıbi)",
    "Hibrit: Onerileri gostermek icin frontend UI olustur",
    "Hibrit: Entegrasyon testleri yaz"
  ],
  mcp_komutlari: {
    ajan_olustur: "mcp__claude-flow__agent_spawn({ type: 'algorithm-specialist', task: 'Isbirlikci filtreleme oneri motoru uygula', context: {...} })",
    kontrat_depola: "mcp__memory-mcp__memory_store({ text: 'Oneri API Kontrati: POST /api/recommendations...', metadata: { key: 'features/recommendations/api-contract', layer: 'mid-term', category: 'api-design' } })"
  }
} [ground:witnessed:workflow-example] [conf:0.90] [state:confirmed]

---

<!-- S6 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonuc (Summary)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[assert|confident] OZET := {
  toplam_sure: "5 saat (ilk kez) | 3 saat (hizli kosma)",
  ajan_katmani: "Uretime hazir hibrit ajan",
  karmasiklik: "Cok-alanli uzman + koordinator",
  yetenekler: [
    "Frontend gelistirme (React, TypeScript, TailwindCSS)",
    "Backend gelistirme (Node.js, Express, JWT auth)",
    "Veritabani yonetimi (PostgreSQL, Prisma, migrasyonlar)",
    "DevOps (Docker, CI/CD, GitHub Actions)",
    "Ozellik orkestrasyonu (API-ilk, uctan uca teslimat)",
    "Ajan delegasyonu (Algoritma, Guvenlik, Performans uzmanlari)"
  ],
  temel_farklilastiriclar: [
    "Hibrit Mimari: Uzman derinligi + koordinator genisligi",
    "API-Ilk Is Akisi: TypeScript tipleri kontrat olarak",
    "Akilli Delegasyon: Ne zaman devrетme vs. dogrudan uygulama bilir",
    "Uctan-Uca Sahiplik: Spesifikasyondan dagitima tek is akisinda",
    "Cok-Alanli Baglam Degistirme: Frontend/backend/veritabani arasinda verimli gecisler"
  ],
  ne_zaman_kullanilir: [
    "Frontend + backend + veritabani gerektiren tam-yigin ozellikler",
    "Standart karmasiklikta ozellikler (auth, CRUD, formlar)",
    "React + Node.js + PostgreSQL yigini kullanan projeler",
    "Uctan uca sahiplik gerektiren ozellikler (tek ajan, tam teslimat)"
  ],
  ne_zaman_kullanilmaz: [
    "Karmasik algoritmalar (ML, oneri motorlari) -> Algoritma Uzmani",
    "Guvenlik denetimleri, penetrasyon testi -> Guvenlik Uzmani",
    "Gelismis performans optimizasyonu -> Performans Uzmani",
    "Mobil uygulama gelistirme (React Native) -> Mobil Gelistirme Uzmani"
  ]
} [ground:witnessed:example-completion] [conf:0.95] [state:confirmed]

---

<promise>EXAMPLE_3_HYBRID_VCL_VERIX_COMPLIANT</promise>
