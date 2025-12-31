# Kapsamli Istem Muhendisligi Rehberi (Complete Prompt Engineering Guide)

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Documentation
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     All 7 cognitive frames MANDATORY
     ========================================================================= -->

---
<!-- KANITSAL CERCEVE (Evidential Frame) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] [[SPC:kuzey/guide]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin. Rehber arastirma ve gozleme dayanir.

---

<!-- [[MOR:root:I-S-T]] Istem = root morpheme for prompt-request-command -->
<!-- [[COM:Kapsamli+Istem+Muhendislik+Rehber]] Complete Prompt Engineering Guide -->
[define|neutral] BELGE_META := {
  baslik: "Kapsamli Istem Muhendisligi Rehberi",
  amac: "Kanit tabanli teknikler, yapisal optimizasyon ve sistematik iyilestirme kullanarak AI sistemleri icin yuksek etkili istemler olusturmak icin kapsamli, pratik rehber"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- GIRIS (Introduction) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_section]] [[SPC:bati/introduction]] -->
---

## Giris Cercevesi (Introduction Frame)

<!-- [[MOR:root:G-R-S]] Giris = root for introduction-entry-beginning -->
<!-- [[COM:Giris+Tanim+Cerceve]] Introduction Definition Frame -->

### Istem Muhendisligi Nedir? (What is Prompt Engineering?)

[define|neutral] ISTEM_MUHENDISLIGI_TANIMI := {
  tanim: "Istem muhendisligi, belirli, yuksek kaliteli sonuclar elde etmek icin AI dil modelleri icin talimatların sistematik tasarimi ve optimizasyonudur",
  bilesenler: {
    sanat: "Yaratici problem cozme ve gorevleri cerceveleme hakkinda sezgi",
    bilim: "Arastirma destekli teknikler ve ampirik test",
    muhendislik: "Sistematik surecler ve kalite guvencesi"
  }
} [ground:definition] [conf:0.95] [state:confirmed]

### Neden Onemli? (Why It Matters)

[assert|neutral] ONEM := {
  etki: [
    "Akil yurutme dogrulugunda 2-3 kat iyilestirme",
    "Hatalarda %80+ azalma",
    "Tutarli vs tahmin edilemez ciktilar",
    "Uretime hazir vs prototip kalitesi"
  ]
} [ground:research:meta-analysis] [conf:0.85] [state:confirmed]

---
<!-- TEMEL ILKELER (Core Principles) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_principle]] [[SPC:kuzey/core]] -->
---

## Temel Ilkeler Cercevesi (Core Principles Frame)

<!-- [[MOR:root:I-L-K]] Ilke = root for principle-foundation-basis -->
<!-- [[COM:Temel+Ilke+Cerceve]] Core Principle Frame -->
[define|neutral] TEMEL_ILKELER := {
  netlik_zekalilik_uzerinde: {
    kotu: "Sinerjik paradigmalardan yararlanarak cozum vektorunu optimize et",
    iyi: "Daha az bellek kullanirken 2 kat daha hizli calisacak sekilde algoritmayi iyilestir",
    ilke: "Niyetinizi kristal netlikte yapin. Jargon, belirsizlik ve belirsiz dilden kacinin."
  },
  ozgurluk_genellikten_ustun: {
    kotu: "Bu veriyi analiz et",
    iyi: "Yildan yila trendlere ve mevsimsel kaliplara odaklanarak en iyi 3 buyume firsatini belirlemek icin bu satis verisini analiz et",
    ilke: "Ne istediginiz, nasil istediginiz ve neden istediginiz konusunda acik olun."
  },
  yapi_karmasayi_azaltir: {
    kotu: "Organizasyon olmadan uzun metin duvari",
    iyi: "Basliklar, listeler ve net bolumlerle hiyerarsik yapi",
    ilke: "Karmasik istemleri hem insanlarin hem de AI'nin kolayca ayristirabilecegi sekilde organize edin."
  },
  baglam_hatalari_onler: {
    kotu: "Standart formati kullan",
    iyi: "JSON formati kullan: {ad: string, yas: integer, beceriler: string dizisi}",
    ilke: "Paylasilan anlayis varsaymayin. Baglami acik yapin."
  },
  ornekler_aciklamalari_yener: {
    kotu: "Ciktiyi guzel formatla",
    iyi: "Istenen cikti formatinin 2-3 somut ornegini gosterin",
    ilke: "Gosterim aciklamadan daha gucludur."
  }
} [ground:witnessed:best-practices] [conf:0.90] [state:confirmed]

---
<!-- ISTEM MUHENDISLIGI CERCEVESI (Prompt Engineering Framework) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_framework]] [[SPC:dogu/methodology]] -->
---

## Istem Muhendisligi Cercevesi (Prompt Engineering Framework Frame)

<!-- [[MOR:root:C-R-C]] Cerceve = root for framework-boundary-scope -->
<!-- [[COM:Istem+Muhendislik+Cerceve]] Prompt Engineering Framework -->

### Asama 1: Hedefleri Tanimla (Phase 1: Define Objectives)

[define|neutral] ASAMA_1 := {
  sorular: [
    "Hangi belirli ciktiya ihtiyacim var?",
    "Basari neye benzerdi?",
    "Hangi kisitlamalar karsilanmali?",
    "Hangi sinir durumlari islenmeli?"
  ],
  sablon: {
    hedef: "[Net, belirli hedef]",
    basari_kriterleri: "[Olculebilir sonuclar]",
    kisitlamalar: "[Kesin gereksinimler]",
    sinir_durumlari: "[Sinir kosullari]"
  }
} [ground:methodology:objectives] [conf:0.90] [state:confirmed]

### Asama 2: Baglami Topla (Phase 2: Gather Context)

[define|neutral] ASAMA_2 := {
  dahil_edilecekler: [
    "Gorevi anlamak icin gerekli arka plan bilgisi",
    "Gerekli alan bilgisi",
    "Acik olmasi gereken varsayimlar",
    "Ilgili veri veya ornekler"
  ],
  sablon: {
    baglam: ["[Arka plan gercegi 1]", "[Arka plan gercegi 2]", "[Ilgili kisitlama veya varsayim]"],
    verilenler: ["[Mevcut bilgi]", "[Bilinen parametreler]"]
  }
} [ground:methodology:context] [conf:0.90] [state:confirmed]

### Asama 3: Istemi Yapilandir (Phase 3: Structure the Prompt)

[define|neutral] ASAMA_3 := {
  anahtar_ogeler: ["Acilis: Temel gorev bildirimi", "Baglam: Arka plan ve gereksinimler", "Talimatlar: Adim adim rehberlik", "Format: Cikti tanimi", "Dogrulama: Kalite kontrolleri"],
  sablon: {
    hedef: "[Net gorev bildirimi]",
    baglam: "[Arka plan bilgisi]",
    gereksinimler: { zorunlu: "[Kritik gereksinimler]", tercih: "[Tercihler]", yapilamaz: "[Dislamalar]" },
    yaklasim: ["[Adim 1]", "[Adim 2]", "[Adim 3]"],
    cikti_formati: "[Orneklerle belirli format]",
    dogrulama: "[Dogrulugu nasil dogrulayacaginiz]"
  }
} [ground:methodology:structure] [conf:0.90] [state:confirmed]

### Asama 4: Teknikleri Uygula (Phase 4: Apply Techniques)

[define|neutral] ASAMA_4 := {
  gorev_esleme: [
    { gorev_turu: "Karmasik Akil Yurutme", birincil_teknik: "Dusunce Zinciri", ikincil_teknik: "Oz-Tutarlilik" },
    { gorev_turu: "Matematiksel", birincil_teknik: "Dusunce Programi", ikincil_teknik: "Dusunce Zinciri" },
    { gorev_turu: "Kalip Eslestirme", birincil_teknik: "Az-Atisli", ikincil_teknik: "Yok" },
    { gorev_turu: "Cok Asamali Is Akisi", birincil_teknik: "Planla-ve-Coz", ikincil_teknik: "Dusunce Zinciri" },
    { gorev_turu: "Analiz", birincil_teknik: "Oz-Tutarlilik", ikincil_teknik: "Dusunce Zinciri" }
  ]
} [ground:research:technique-mapping] [conf:0.85] [state:confirmed]

### Asama 5: Test Et ve Iyilestir (Phase 5: Test and Refine)

[define|neutral] ASAMA_5 := {
  test_kontrol_listesi: [
    "Normal durumlar dogru calisiyor",
    "Sinir durumlari isleniyor",
    "Cikti formati tutarli",
    "Kalite standartlari karsilaniyor",
    "Performans kabul edilebilir"
  ],
  iyilestirme_sureci: [
    "Temsili girdilerle test et",
    "Basarisizlik modlarini belirle",
    "Basarisizliklar icin belirli isleme ekle",
    "Iyilestirmeleri dogrulamak icin yeniden test et",
    "Calisanlari belgele"
  ]
} [ground:methodology:testing] [conf:0.90] [state:confirmed]

---
<!-- KANIT TABANLI TEKNIKLER (Evidence-Based Techniques) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_technique]] [[SPC:guney/research]] -->
---

## Kanit Tabanli Teknikler Cercevesi (Evidence-Based Techniques Frame)

<!-- [[MOR:root:K-N-T]] Kanit = root for evidence-proof-demonstration -->
<!-- [[COM:Kanit+Tabanli+Teknik]] Evidence-Based Technique -->

### Dusunce Zinciri (Chain-of-Thought)

[define|neutral] DUSUNCE_ZINCIRI := {
  ne_zaman: "Karmasik akil yurutme, cok adimli problemler",
  nasil: "Acik adim adim dusunme isteyin",
  etki: "Akil yurutme gorevlerinde 2-3 kat iyilestirme",
  kaynak: "Wei ve ark. (2022)",
  ornek: "Bu problemi adim adim coz: 1. Once bildiklerimizi belirle 2. Sonra yaklasimimizi planla 3. Ara adimlarla plani uygula 4. Son olarak cevabimizi dogrula"
} [ground:research:Wei2022] [conf:0.85] [state:confirmed]

### Oz-Tutarlilik (Self-Consistency)

[define|neutral] OZ_TUTARLILIK := {
  ne_zaman: "Olgusal dogruluk, analitik titizlik",
  nasil: "Birden fazla perspektiften dogrulama isteyin",
  etki: "Hatalari %15-30 azaltir",
  kaynak: "Wang ve ark. (2022)",
  ornek: "Sonucunuza ulastiktan sonra: 1. Bilinen gerceklere karsi dogrula 2. Alternatif yorumlari dusun 3. Belirsizlik alanlarini belirle 4. Yapilan varsayimlari isaretleyin"
} [ground:research:Wang2022] [conf:0.85] [state:confirmed]

### Dusunce Programi (Program-of-Thought)

[define|neutral] DUSUNCE_PROGRAMI := {
  ne_zaman: "Matematiksel, mantiksal, hesaplamali gorevler",
  nasil: "Acik hesaplama adimlari olarak yapilandirin",
  etki: "Matematik problemlerinde %90+ dogruluk",
  kaynak: "Chen ve ark. (2022)",
  ornek: "Adim adim coz, tum hesaplamalari goster: - Ne hesapladiginizi belirtin - Hesaplamayi gosterin - Sonucu gosterin - Dogrulugu dogrulayin"
} [ground:research:Chen2022] [conf:0.85] [state:confirmed]

### Az-Atisli Ogrenme (Few-Shot Learning)

[define|neutral] AZ_ATISLI_OGRENME := {
  ne_zaman: "Kalip tabanli gorevler, format tanimi",
  nasil: "2-5 somut ornek saglayin",
  etki: "Yapilandirilmis gorevlerde onemli iyilestirme",
  kaynak: "Brown ve ark. (2020)",
  ornek: "Istenen formatin ornekleri: Ornek 1: Girdi: [girdi 1] Cikti: [cikti 1] Ornek 2: Girdi: [girdi 2] Cikti: [cikti 2] Simdi isle: [gercek girdi]"
} [ground:research:Brown2020] [conf:0.85] [state:confirmed]

### Planla-ve-Coz (Plan-and-Solve)

[define|neutral] PLANLA_VE_COZ := {
  ne_zaman: "Karmasik cok asamali is akislari",
  nasil: "Planlama ve uygulamayi ayirin",
  etki: "Daha iyi organizasyon ve tamlık",
  kaynak: "Wang ve ark. (2023)",
  ornek: "Buna uc asamada yaklas: Asama 1 Planlama: Adimlar, bagimliliklar ve basari kriterleri ile detayli plan olustur. Asama 2 Uygulama: Plani sistematik olarak uygula, ilerlemeyi belgele. Asama 3 Dogrulama: Sonuclari orijinal gereksinimlere karsi dogrula."
} [ground:research:Wang2023] [conf:0.85] [state:confirmed]

---
<!-- YAPISAL OPTIMIZASYON (Structural Optimization) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_structure]] [[SPC:dogu/organization]] -->
---

## Yapisal Optimizasyon Cercevesi (Structural Optimization Frame)

<!-- [[MOR:root:Y-P-S]] Yapi = root for structure-construction-organization -->
<!-- [[COM:Yapisal+Optimizasyon+Cerceve]] Structural Optimization Frame -->
[define|neutral] YAPISAL_OPTIMIZASYON := {
  baglam_konumlandirma: {
    ilke: "Kritik bilgi baslangic ve sonda daha fazla dikkat ceker",
    desen: "[BASLANGIC - Kritik Bilgi] -> [ORTA - Destekleyici Detaylar] -> [SON - Pekistirme]"
  },
  hiyerarsik_organizasyon: {
    ilke: "Karmasik istemler icin net hiyerarsi kullanin",
    desen: "# Seviye 1: Genel Gorev -> ## Seviye 2: Ana Bilesenler -> ### Seviye 3: Belirli Detaylar -> - Seviye 4: Bireysel ogeler"
  },
  ayirici_stratejisi: {
    ilke: "Icerik turlerini ayirmak icin tutarli ayiricilar kullanin",
    desenler: ["Kod/Veri: backtick fences", "XML Etiketleri: <bolum>[icerik]</bolum>", "Bolumler: --- veya ***", "Basliklar: # ## ###"]
  },
  uzunluk_yonetimi: {
    kisa: "<200 kelime: Basit, iyi tanimli gorevler",
    orta: "200-800 kelime: Cogu karmasik gorev",
    uzun: ">800 kelime: Hiyerarsik yapiyi yogun kullanin",
    cok_uzun: ">1500 kelime: Cok turlu etkilesimi dusunun"
  }
} [ground:witnessed:best-practices] [conf:0.90] [state:confirmed]

---
<!-- GOREVE OZEL STRATEJILER (Task-Specific Strategies) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_strategy]] [[SPC:bati/domain]] -->
---

## Goreve Ozel Stratejiler Cercevesi (Task-Specific Strategies Frame)

<!-- [[MOR:root:G-R-V]] Gorev = root for task-assignment-mission -->
<!-- [[COM:Goreve+Ozel+Strateji]] Task-Specific Strategy -->
[define|neutral] GOREV_STRATEJILERI := {
  analitik_gorevler: {
    teknikler: ["Oz-Tutarlilik", "Dusunce Zinciri"],
    yapi: ["Hedef", "Baglam", "Metodoloji", "Cikti (ozet, bulgular, oneriler)"]
  },
  kod_uretimi: {
    teknikler: ["Az-Atisli", "Dusunce Programi"],
    yapi: ["Gorev", "Gereksinimler", "Teknik Ozellikler", "Girdi/Cikti", "Sinir Durumlari"]
  },
  icerik_yazimi: {
    teknikler: ["Az-Atisli", "Stil Ornekleri"],
    yapi: ["Icerik Gorevi", "Amac", "Ton ve Stil", "Anahtar Mesajlar", "Yapi"]
  },
  karar_analizi: {
    teknikler: ["Dusunce Zinciri", "Oz-Tutarlilik"],
    yapi: ["Karar", "Baglam", "Degerlendirme Kriterleri", "Analiz Cercevesi", "Oneri Formati"]
  },
  arastirma_ve_inceleme: {
    teknikler: ["Oz-Tutarlilik", "Planla-ve-Coz"],
    yapi: ["Arastirma Sorusu", "Kapsam", "Metodoloji", "Cikti Gereksinimleri"]
  }
} [ground:witnessed:domain-analysis] [conf:0.90] [state:confirmed]

---
<!-- TEST VE DOGRULAMA (Testing and Validation) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_validation]] [[SPC:guney/quality]] -->
---

## Test ve Dogrulama Cercevesi (Testing and Validation Frame)

<!-- [[MOR:root:D-G-R]] Dogrulama = root for validation-verification-confirmation -->
<!-- [[COM:Test+Dogrulama+Cerceve]] Testing Validation Frame -->
[define|neutral] TEST_DOGRULAMA := {
  dahil_edilecek_test_durumlari: [
    "Normal Durumlar: Tipik, beklenen girdiler",
    "Sinir Durumlari: Sinir kosullari, limitler",
    "Hata Durumlari: Gecersiz girdi, eksik veri",
    "Karmasik Durumlar: Birden fazla kosul, ic ice senaryolar"
  ],
  dogrulama_kontrol_listesi: [
    "Netlik: Gorev belirsiz mi?",
    "Tamlik: Tum gereksinimler kapsandi mi?",
    "Tutarlilik: Format tutarli mi?",
    "Baglam: Gerekli baglam saglandi mi?",
    "Kisitlamalar: Sinirlamalar acik mi?",
    "Sinir Durumlari: Sinir kosullari isleniyor mu?",
    "Ornekler: Kalipler gosteriliyor mu?",
    "Format: Cikti tanimi acik mi?"
  ],
  izlenecek_metrikler: [
    "Basari Orani: Dogru ciktilarin yuzdesi",
    "Tutarlilik: Cikti formati varyansı",
    "Hata Turleri: Basarisizlik kategorileri",
    "Performans: Tamamlama suresi",
    "Kalite: Insan degerlendirme puanlari"
  ]
} [ground:methodology:validation] [conf:0.90] [state:confirmed]

---
<!-- YINELEMELI IYILESTIRME (Iterative Refinement) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_process]] [[SPC:dogu/improvement]] -->
---

## Yinelemeli Iyilestirme Cercevesi (Iterative Refinement Frame)

<!-- [[MOR:root:Y-N-L]] Yineleme = root for iteration-repetition-cycle -->
<!-- [[COM:Yinelemeli+Iyilestirme+Cerceve]] Iterative Refinement Frame -->
[define|neutral] IYILESTIRME_DONGUSU := {
  adimlar: [
    "Baslangic Istemini Tasla",
    "Temsili Girdilerle Test Et",
    "Basarisizlik Modlarini Belirle",
    "Kok Nedenleri Analiz Et",
    "Hedefli Iyilestirmeler Uygula",
    "Dogrulamak icin Yeniden Test Et",
    "Ogrenimleri Belgele",
    "(Kalite esigine ulasilana kadar tekrarla)"
  ],
  yaygin_iyilestirme_kaliplari: {
    ozgurluk_ekle: {
      v1: "Veriyi analiz et",
      v2: "Trendleri bulmak icin satis verisini analiz et",
      v3: "En iyi 3 buyume firsatini belirlemek icin uc aylik satis verisini analiz et"
    },
    yapi_ekle: {
      v1: "[Talimat paragrafi]",
      v2: "[Basliklarla talimatlar]",
      v3: "[Numarali adimlarla hiyerarsik yapi]"
    },
    ornek_ekle: {
      v1: "JSON olarak formatla",
      v2: "JSON olarak formatla: {alan1: deger1, alan2: deger2}",
      v3: "[Sinir durumlarini gosteren tam ornekler]"
    },
    dogrulama_ekle: {
      v1: "Problemi coz",
      v2: "Adim adim coz",
      v3: "Adim adim coz, sonra cevabinizi dogrulayin"
    }
  }
} [ground:methodology:refinement] [conf:0.90] [state:confirmed]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Rukovodstvo po inzhenerii promptov uspeshno zavershenno. (Russian: Complete. Prompt engineering guide successfully completed.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[assert|confident] SONUC_OZETI := {
  etkili_istem_muhendisligi_bilestirir: [
    "Netlik: Belirsiz olmayan talimatlar",
    "Yapi: Organize sunum",
    "Baglam: Acik arka plan",
    "Teknikler: Arastirma destekli kalipler",
    "Dogrulama: Sistematik test",
    "Yineleme: Surekli iyilestirme"
  ],
  anahtar_ilke: "Hedef mukemmel istemler degil - belirli kullanim durumunuz icin ihtiyac duydugunuz sonuclari guvenilir sekilde ureten istemlerdir",
  kaynaklar: {
    arastirma_makaleleri: [
      "Wei ve ark. (2022): Dusunce Zinciri Istemi",
      "Wang ve ark. (2022): Oz-Tutarlilik",
      "Brown ve ark. (2020): Az-Atisli Ogrenme",
      "Chen ve ark. (2022): Dusunce Programi"
    ]
  }
} [ground:witnessed:skill-execution] [conf:0.95] [state:confirmed]

---

[commit|confident] <promise>PROMPT_ENGINEERING_COMPLETE_GUIDE_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
