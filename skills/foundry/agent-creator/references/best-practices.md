# Ajan Olusturucu En Iyi Uygulamalar (Agent Creator Best Practices)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 KANIT_TABANLI_ILKELER (Evidence-Based Principles) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Kanit-Tabanli Prompting Ilkeleri (Evidence-Based Prompting Principles)

### 1. Oz-Tutarlilik Dogrulamasi (Self-Consistency Validation)

<!-- [[MOR:root:T-T-R]] Tutarlilik = root morpheme for consistency-coherence -->
[assert|neutral] OZ_TUTARLILIK_ILKESI := {
  ilke: "Birden fazla muhakeme yolu olustur ve en tutarli cevabi sec",
  uygulama_sablonu: "Ciktilari sonlandirmadan once birden fazla acidan dogrula: [Alana ozgu dogrulama 1], [Alana ozgu dogrulama 2], [Standartlarla capraz kontrol]",
  faydalar: [
    "Muhakemeyi capraz kontrol ederek halusinasyonlari azaltir",
    "%15-30 dogruluk iyilestirmesi (arastirmada kanitlanmis)",
    "Ajan guven kalibrasyonu olusturur"
  ]
} [ground:research:evidence-based-prompting] [conf:0.85] [state:confirmed]

[assert|neutral] OZ_TUTARLILIK_ORNEGI := {
  ajan: "Pazarlama Uzmani",
  dogrulama_adimlari: [
    "Veri Dogrulamasi: ROI hesaplamalari tarihi karsilastirmalarla uyusuyor mu?",
    "Segment Dogrulamasi: Tum hedef kitle segmentlerinde performans analiz ettim mi?",
    "Istatistiksel Dogrulama: A/B test sonuclari istatistiksel olarak anlamli mi (p<0.05)?",
    "Butce Dogrulamasi: Toplam dagitim butceye esit mi (+/-%5 test rezervi icin)?"
  ]
} [ground:witnessed:example] [conf:0.88] [state:confirmed]

### 2. Dusunce Programi (PoT) Ayristirmasi (Program-of-Thought Decomposition)

[assert|neutral] POT_ILKESI := {
  ilke: "Karmasik gorevleri yurutmeden ONCE ara adimlara ayristir",
  faydalar: [
    "Erken basarisizligi onler (hizli basarisiz ol)",
    "%20-40 planlama kalitesi iyilestirmesi",
    "Daha iyi hata kurtarma saglar (net geri alma noktalari)"
  ]
} [ground:research:evidence-based-prompting] [conf:0.85] [state:confirmed]

[assert|neutral] POT_ORNEGI := {
  ajan: "DevOps Koordinatoru",
  ayristirma: {
    ayristir: "Manifesti yukle -> Semayi dogrula -> Hizmetler + bagimliliklari cikar",
    planla: "DAG insa et -> Yurutme dalgalarini belirle -> Sureyi tahmin et -> Kapasiteyi kontrol et",
    hazirla: "Geri alma manifesti depola -> Izlemeyi baslat -> Kaynaklari rezerve et",
    yurutme: "Dalga dalga ajan olustur -> Sagligi izle -> Hatalari isle",
    dogrula: "Saglik kontrollerini calistir -> Endpoint'leri dogrula -> Metrikleri onayla",
    sonlandir: "Dagitim durumunu depola -> Gecici kaynaklari temizle -> Paydaşlari bilgilendir"
  }
} [ground:witnessed:example] [conf:0.88] [state:confirmed]

### 3. Plan-ve-Coz Yurutme (Plan-and-Solve Execution)

[assert|neutral] PLAN_VE_COZ_ILKESI := {
  ilke: "Yurutmeden once acik planlama fazı, her adimda dogrulama",
  is_akisi: ["PLANLA", "DOGRULA", "YURUTME", "DOGRULA", "BELGELE"],
  faydalar: [
    "%25-35 hata azaltma (dogrulama hatalari erken yakalar)",
    "Tutarlilik iyilestirmesi (tekrarlanabilir is akisi)",
    "Daha iyi isbirligi saglar (net fazlar)"
  ]
} [ground:research:evidence-based-prompting] [conf:0.85] [state:confirmed]

---

<!-- S2 SISTEM_PROMPT_OPTIMIZASYONU (System Prompt Optimization) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Sistem Prompt Optimizasyon Teknikleri (System Prompt Optimization Techniques)

### 1. Spesifik Uzmanlik ile Rol Netligi (Role Clarity with Specific Expertise)

[assert|emphatic] ROL_NETLIGI := {
  yanlis: "Uygulama olusturabilen bir gelistiriciyim.",
  dogru: "Frontend (React/TypeScript), backend (Node.js/Express), veritabani (PostgreSQL/Prisma) ve DevOps (Docker/CI-CD) alanlarinda derin uzmanliga sahip bir Tam-Yigin Gelistirici Ajaniyim. Sistematik alan analizi yoluyla, su alanlarda hassasiyet duzeyinde anlayisa sahibim: Frontend Gelistirme - React 18, hooks, TypeScript generics, TailwindCSS, erisilebilirlik; Backend Gelistirme - RESTful API'ler, JWT kimlik dogrulama, Zod dogrulama, middleware kaliplari...",
  neden_daha_iyi: [
    "Spesifik bilgi alanlarini etkinlestirir",
    "Net kapsam sinirlari belirler",
    "Daha iyi gorev yonlendirmesi saglar (ajan ne yapip yapamayacagini bilir)"
  ]
} [ground:witnessed:optimization-technique] [conf:0.92] [state:confirmed]

### 2. NE ZAMAN ve NASIL ile Komut Spesifikasyonlari (Command Specifications with WHEN and HOW)

[assert|emphatic] KOMUT_SPESIFIKASYONU := {
  yanlis: "/file-read - Dosyalari oku",
  dogru: "/file-read, /file-write, /glob-search, /grep-search; NE ZAMAN: Kampanya performans CSV'lerini okurken, strateji belgeleri yazarken, tarihi veri ararken; NASIL: /file-read campaigns/q3-performance.csv -> metrikleri ayristir -> trendleri analiz et",
  neden_daha_iyi: [
    "Komut kullanimi icin baglam saglar (sadece soz dizimi degil)",
    "Tam kaliplari gosterir (NASIL ornekleri)",
    "Komut yanlis kullanimini azaltir"
  ]
} [ground:witnessed:optimization-technique] [conf:0.92] [state:confirmed]

### 3. YANLIS vs. DOGRU Ornekleriyle Korumalar (Guardrails with WRONG vs. CORRECT Examples)

[assert|emphatic] KORUMA_SPESIFIKASYONU := {
  yanlis: "Asla testler olmadan dagitma.",
  dogru: {
    kural: "ASLA: CI/CD boru hatti gecmeden dagitma",
    neden: "Basarisiz testler = bozuk uretim",
    yanlis_ornek: "Testleri atla, dogrudan dagit: git push origin main",
    dogru_ornek: "CI/CD boru hatti testleri otomatik calistirir: git push origin main -> GitHub Actions bekle: Tum testler gecti -> SONRA dagit"
  },
  neden_daha_iyi: [
    "Somut ornekler (soyut kurallar degil)",
    "Sonuclari gosterir (NEDEN aciklamalari)",
    "%40-60 ihlal azaltmasi"
  ]
} [ground:witnessed:optimization-technique] [conf:0.92] [state:confirmed]

### 4. Tam Komutlarla Is Akisi Ornekleri (Workflow Examples with Exact Commands)

[assert|emphatic] IS_AKISI_ORNEGI := {
  yanlis: "1. Veri analiz et 2. Strateji olustur 3. Dagit",
  dogru: {
    adim_1: {
      isim: "Tarihi Veri Topla",
      komutlar: ["/file-read campaigns/q3-2024-performance.csv", "/memory-retrieve --key marketing/audience-personas"],
      cikti: "Segment basina tarihi ROAS, CAC, donusum oranlari",
      dogrulama: "Yeterli veri (3+ ay), tutarli izleme"
    },
    adim_2: {
      isim: "Hedef Kitle Segmentasyonu",
      komutlar: ["/audience-segment --criteria repeat-purchaser,high-ltv"],
      cikti: "LTV, CAC ile 3-5 hedef kitle segmenti",
      dogrulama: "Segmentler hedef kitlenin %80+'ini kapsiyor"
    }
  },
  neden_daha_iyi: [
    "Yurutulebilir (ajan komutlari kopyala-yapistir yapabilir)",
    "Test edilebilir (is akisi dogrulanabilir)",
    "%30-50 tutarlilik iyilestirmesi"
  ]
} [ground:witnessed:optimization-technique] [conf:0.92] [state:confirmed]

---

<!-- S3 UZMANLIK_KALIPLARI (Specialization Patterns) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Ajan Uzmanlik Kaliplari (Agent Specialization Patterns)

### Kalip 1: Analitik Ajanlar (Pattern 1: Analytical Agents)

[assert|neutral] ANALITIK_KALIP := {
  odak: "Kanit degerlendirme, veri kalitesi, dogrulama",
  faz_vurgulari: {
    faz_1: "Istatistiksel metodlar (A/B testi, anlam testleri), Veri kalitesi standartlari (tamliligi, dogruluk), Kanit hiyerarsisi",
    faz_2: "Analitik sezgisel kurallar ('Sonuclara varmadan once her zaman orneklem boyutunu dogrula'), Dogrulama cerceveleri (kontrol listesi tabanli)",
    faz_3: "Oz-tutarlilik kontrolu (cok acili dogrulama), Guven kalibrasyonu (belirsizligi nicelle)",
    faz_4: "Istatistiksel dogrulama kodu (anlam testleri, guc analizi), Hata tespit kaliplari (aykiri degerler, eksik veri)"
  },
  ornek_ajanlar: ["Veri Analisti", "Arastirma Analisti", "Kalite Denetcisi"]
} [ground:witnessed:pattern] [conf:0.88] [state:confirmed]

### Kalip 2: Uretici Ajanlar (Pattern 2: Generative Agents)

[assert|neutral] URETICI_KALIP := {
  odak: "Icerik olusturma, tasarim, sentez",
  faz_vurgulari: {
    faz_1: "Kalite kriterleri (okunabilirlik, etkilesim, dogruluk), Sablon kaliplari (kanitlanmis yapilar), Hedef kitle anlayisi",
    faz_2: "Yaratici sezgisel kurallar ('Anlatma, goster', 'Acamasizca duzenle'), Iyilestirme donguler (taslak -> inceleme -> revizyon)",
    faz_3: "Plan-ve-coz cerceveleri (anahat -> taslak -> cilalama), Gereksinim izleme (olmazsa olmazlar kontrol listesi)",
    faz_4: "Uretim kaliplari (sablonlar, ornekler), Kalite dogrulama kodu (okunabilirlik puanlari, intihal kontrolleri)"
  },
  ornek_ajanlar: ["Icerik Yazari", "Pazarlama Metin Yazari", "UI Tasarimci"]
} [ground:witnessed:pattern] [conf:0.88] [state:confirmed]

### Kalip 3: Teshis Ajanlari (Pattern 3: Diagnostic Agents)

[assert|neutral] TESHIS_KALIBI := {
  odak: "Problem tanimlama, hata ayiklama, kok neden analizi",
  faz_vurgulari: {
    faz_1: "Problem kaliplari (yaygin basarisizliklar), Hata ayiklama is akislari (sistematik sorun giderme), Teshis araclari (loglar, profiler'lar, debugger'lar)",
    faz_2: "Hipotez uretme ('X bozuksa, Y belirtileri gorulur'), Sistematik test (degiskenleri izole et)",
    faz_3: "Dusunce programi ayristirmasi (problemi alt-problemlere bol), Kanit izleme (ne elendi, ne onaylandi)",
    faz_4: "Tespit scriptleri (log ayristirma, hata kalip eslestirme), Kok neden analiz kaliplari (5 Neden, Balik Kilcigi diyagramlari)"
  },
  ornek_ajanlar: ["Hata Ayiklama Uzmani", "Performans Analizcisi", "Guvenlik Denetcisi"]
} [ground:witnessed:pattern] [conf:0.88] [state:confirmed]

### Kalip 4: Orkestrasyon Ajanlari (Pattern 4: Orchestration Agents)

[assert|neutral] ORKESTRASYON_KALIBI := {
  odak: "Is akisi koordinasyonu, ajan yonetimi, bagimlilik cozumleme",
  faz_vurgulari: {
    faz_1: "Is akisi kaliplari (sirasal, paralel, kosullu), Bagimlilik yonetimi (DAG'lar, kritik yollar), Hata kurtarma (yeniden dene, geri al, yukselt)",
    faz_2: "Koordinasyon sezgisel kurallari ('Bagimsiz gorevleri paralellestir'), Hata kurtarma cerceveleri (siniflandir -> yeniden dene/geri al)",
    faz_3: "Bagimlíliklarla plan-ve-coz (PERT grafikleri), Ilerleme izleme (kilometre taslari, saglik kontrolleri)",
    faz_4: "Orkestrasyon kodu (is akisi motorlari, DAG kutuphaneleri), Yeniden deneme mantigi (ustel geri cekilme, devre kesiciler), Yukseltme yollari (ne zaman insanlari dahil etmeli)"
  },
  ornek_ajanlar: ["DevOps Koordinatoru", "Proje Yonetici", "Is Akisi Orkestratoru"]
} [ground:witnessed:pattern] [conf:0.88] [state:confirmed]

---

<!-- S4 TEST_VE_DOGRULAMA (Testing & Validation) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Test ve Dogrulama En Iyi Uygulamalari (Testing & Validation Best Practices)

### Dogrulama Kontrol Listesi (Validation Checklist)

[assert|emphatic] DOGRULAMA_KONTROL_LISTESI := [
  "Kimlik: Ajan etkilesimler arasinda tutarli rolu suruyor",
  "Komutlar: Evrensel komutlari dogru kullaniyor (dosya islemleri, git, hafiza)",
  "Uzman Becerileri: Alan uzmanligi gosteriyor (genel yanitlar degil)",
  "MCP Entegrasyonu: Hafiza araciligiyla koordine ediyor, gerektiginde alt-ajanlar olusturuyor",
  "Korumalar: Tanimlanan basarisizlik modlarini onluyor (ornekler beklendig gibi calisiyor)",
  "Is Akislari: Is akisi orneklerini basariyla yurutuyor (kopyala-yapistir komutlari calisiyor)",
  "Metrikler: Performans verilerini izliyor (gorev tamamlama, kalite, verimlilik)",
  "Kod Kaliplari: Faz 4'ten tam kaliplari uyguluyor (kod parcalari calisiyor)",
  "Hata Isleme: Uygun sekilde yukseltiyor (ne zaman takildigini biliyor)",
  "Tutarlilik: Tekrarda kararli ciktilar uretiyor (rastgele degil)"
] [ground:witnessed:validation] [conf:0.95] [state:confirmed]

### Test Paketi Yapisi (Test Suite Structure)

[assert|neutral] TEST_PAKETI := {
  tipik_vakalar: {
    yuzde: "%80 kullanim",
    tanim: "Standart is akislari, yaygin girdiler, normal veri uzerinde beklenen davranis"
  },
  kenar_vakalari: {
    yuzde: "%15 kullanim",
    tanim: "Sinir kosullari, olagan disi girdiler, Bos veri, cok buyuk veri, bozuk veri"
  },
  hata_vakalari: {
    yuzde: "%5 kullanim",
    tanim: "Nazik basarisizlik, kurtarma, Eksik bagimlíliklar, gecersiz yapilandirmalar"
  },
  entegrasyon_vakalari: {
    tanim: "Diger ajanlarla uctan uca is akislari, Hafiza koordinasyonu, olay yayilimi"
  },
  performans_vakalari: {
    tanim: "Hiz (gecikme, verim), Verimlilik (token kullanimi, API cagrilari), Kaynak kullanimi (bellek, CPU)"
  }
} [ground:witnessed:test-structure] [conf:0.90] [state:confirmed]

### Izlenecek Metrikler (Metrics to Track)

[assert|neutral] IZLENECEK_METRIKLER := {
  gorev_tamamlama: ["Gun/hafta basina tamamlanan gorevler", "Gorev suresi (ort, p50, p95)", "Basari orani (tamamlanan / denenen)"],
  kalite: ["Dogrulama gecisleri (kontrol listesi ogeleri)", "Yukseltmeler (diger ajanlardan yardim gereken)", "Hata orani (basarisizliklar / denemeler)", "Oneri benimseme (kullanicilar/musteriler tarafindan)"],
  verimlilik: ["Gorev basina komut (ort)", "MCP arac kullanimi (siklik)", "Token kullanimi (gorev basina)", "API cagrilari (gorev basina)"],
  is_etkisi: ["Etkilenen gelir (pazarlama/satis ajanlari icin)", "Maliyet tasarrufu (optimizasyon ajanlari icin)", "Zaman tasarrufu (manuel ise karsi)", "Musteri memnuniyeti (NPS, CSAT puanlari)"]
} [ground:witnessed:metrics] [conf:0.88] [state:confirmed]

---

<!-- S5 SUREKLI_IYILESTIRME (Continuous Improvement) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Surekli Iyilestirme Dongusu (Continuous Improvement Cycle)

### 1. Haftalik Inceleme (Weekly Review)

[assert|neutral] HAFTALIK_INCELEME := {
  ne_incelenir: ["Performans metrikleri (gorev tamamlama, kalite, verimlilik)", "Basarisizlik vakalari (hatalar, yukseltmeler)", "Kullanici geri bildirimi (memnuniyet puanlari, sikayetler)"],
  eylemler: ["En onemli 3 basarisizlik modunu belirle", "Onlemek icin korumalari guncelle", "Yeni kod kaliplari ekle (kesfedilirse)"]
} [ground:witnessed:improvement-cycle] [conf:0.88] [state:confirmed]

### 2. Aylik Yineleme (Monthly Iteration)

[assert|neutral] AYLIK_YINELEME := {
  ne_guncellenir: ["Sistem prompt iyilestirmeleri (v2.1, v2.2, ...)", "Yeni is akisi ornekleri (basarili gorevlerden)", "Guncellenmis teknoloji yigini (yeni araclar, cerceveler)"],
  versiyon_kontrolu: {
    v1_0: "Faz 3'ten temel prompt",
    v1_x: "Testlerden kucuk iyilestirmeler",
    v2_0: "Faz 4 kaliplariyla gelistirilmis",
    v2_x: "Uretim yinelemeleri"
  }
} [ground:witnessed:improvement-cycle] [conf:0.88] [state:confirmed]

### 3. Ucaylik Buyuk Guncellemeler (Quarterly Major Updates)

[assert|neutral] UCAYLIK_GUNCELLEMELER := {
  ne_eklenir: ["Yeni yetenekler (alan kapsamini genislet)", "Yeni MCP sunuculariyla entegrasyon", "Gelismis koordinasyon kaliplari"],
  yeniden_dogrulama: ["Tam test paketini yeniden calistir", "Tum is akisi orneklerinin hala calistigini dogrula", "Dokumantasyonu guncelle"]
} [ground:witnessed:improvement-cycle] [conf:0.88] [state:confirmed]

---

<!-- S6 YAYGIN_TUZAKLAR (Common Pitfalls) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Yaygin Tuzaklar ve Nasil Kacinilir (Common Pitfalls & How to Avoid)

[assert|emphatic] TUZAKLAR := [
  {
    tuzak: "Yuzeysel Uzmanlik (Her Ise Kosar)",
    belirti: "Ajan genel tavsiyeler veriyor, alana ozgu icgorulardan yoksun",
    neden: "Faz 1 analizi cok genis, Faz 2 uzmanlik cikarimi eksik",
    duzeltme: "Faz 1 alan arastirmasina daha fazla zaman ayir (uzman bloglari, dokumantasyon oku), Faz 2'de 3-5 spesifik uzmanlik alani belirle (genel 'gelistirme' degil), 10+ alana ozgu sezgisel kural ekle (genel 'iyi kod yaz' degil)"
  },
  {
    tuzak: "Eksik Korumalar",
    belirti: "Ajan prompt'taki uyarilara ragmen hatalar yapiyor",
    neden: "Korumalar kurallar olarak belirtilmis (soyut) ornekler degil (somut)",
    duzeltme: "Her korumayi YANLIS vs. DOGRU ornegine donustur, NEDEN aciklamalari ekle (ihlalin sonuclari), Korumalari acikca test et (ihlali tetiklemeye calis)"
  },
  {
    tuzak: "Eksik Kod Kaliplari (Faz 4)",
    belirti: "Ajan dogru mantik uretiyor ama verimsiz/buglu kod",
    neden: "Faz 4 atlandi veya aceleci yapildi, tam kod kaliplari yok",
    duzeltme: "Kod tabanindan 3-5 kod kalibi cikar (dosya:satir referanslariyla), Kaliplara kenar vaka isleme dahil et, 'X gorursem, Y biliyorum' aciklamali yorumlar ekle"
  },
  {
    tuzak: "Zayif MCP Entegrasyonu",
    belirti: "Ajan diger ajanlarla koordine etmiyor, hafiza kullanmiyor",
    neden: "MCP entegrasyon kaliplari belirtilmemis, ad alani konvansiyonlari belirsiz",
    duzeltme: "Tam MCP arac kullanim kaliplari tanimla (kod ornekleriyle), Ad alani konvansiyonlarini belirt (orn. {ajan-rolu}/{gorev-id}/{veri-turu}), Hafiza depolama/alma gosteren is akisi ornekleri ekle"
  },
  {
    tuzak: "Performans Izleme Yok",
    belirti: "Ajan iyilestirmesi zaman icinde olculemiyor",
    neden: "Faz 4'te metrikler tanimlanmamis",
    duzeltme: "5-10 anahtar metrik tanimla (gorev tamamlama, kalite, verimlilik), Nasil izlenecegini belirt (hafiza depolama anahtarlari), Haftalik inceleme sureci kur"
  }
] [ground:witnessed:pitfalls] [conf:0.92] [state:confirmed]

---

<!-- S7 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonuc (Summary)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[assert|confident] TEMEL_CIKARIMLAR := [
  "Tum ajanlarda kanit-tabanli teknikler kullan (oz-tutarlilik, PoT, plan-ve-coz)",
  "Sistem promptlarini spesifik uzmanlik, tam komutlar, somut orneklerle optimize et",
  "Ajan kalibini alana esle (analitik, uretici, teshis, orkestrasyon)",
  "Uretimden once tam kontrol listesiyle kapsamli dogrula",
  "Metrikleri izle ve surekli yinele (haftalik incelemeler, aylik guncellemeler)"
] [ground:witnessed:summary] [conf:0.95] [state:confirmed]

[assert|emphatic] KACINILACAK_TUZAKLAR := [
  "Yuzeysel uzmanlik (Faz 1+2 alan analizine zaman ayir)",
  "Soyut korumalar (YANLIS vs. DOGRU ornekleri kullan)",
  "Eksik kod kaliplari (Faz 4'te tam kaliplari cikar)",
  "Zayif MCP entegrasyonu (tam arac kullanimini belirt)",
  "Metrik yok (performansi tanimla ve izle)"
] [ground:witnessed:summary] [conf:0.95] [state:confirmed]

[assert|confident] SONUC := "Derinlemesine gomulu uzmanlik, saglam korumalar ve olculebilir performansli uretime hazir ajanlar" [ground:witnessed:summary] [conf:0.95] [state:confirmed]

---

<promise>BEST_PRACTICES_VCL_VERIX_COMPLIANT</promise>
