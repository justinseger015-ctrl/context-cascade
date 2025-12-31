# Anti-Kaliplar (Common Prompt Anti-Patterns)

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Documentation
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     All 7 cognitive frames MANDATORY
     ========================================================================= -->

---
<!-- KANITSAL CERCEVE (Evidential Frame) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] [[SPC:kuzey/reference]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin. Anti-kalipler dogrudan gozleme dayanir.

---

<!-- [[MOR:root:A-N-T]] Anti = root morpheme for anti-against-opposing -->
<!-- [[COM:Anti+Kalip+Referans]] Anti-Pattern Reference -->
[define|neutral] BELGE_META := {
  baslik: "Yaygin Istem Anti-Kaliplari",
  amac: "Yaygin istem muhendisligi hatalarini belirleme ve duzeltme icin referans rehberi"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- ANTI-KALIP KATEGORILERI (Anti-Pattern Categories) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_category]] [[SPC:bati/classification]] -->
---

## Anti-Kalip Kategorileri Cercevesi (Anti-Pattern Categories Frame)

<!-- [[MOR:root:K-T-G]] Kategori = root for category-class-group -->
<!-- [[COM:Anti+Kalip+Kategori]] Anti-Pattern Category -->

### 1. Netlik Sorunlari (Clarity Issues)

[define|neutral] NETLIK_SORUNLARI := {
  belirsiz_eylem_fiilleri: {
    kotu: "Veriyle ugras",
    iyi: "Aykiri degerleri belirlemek ve ozet istatistikleri hesaplamak icin veriyi analiz et"
  },
  belirsiz_kapsam: {
    kotu: "Bu belgeyi incele",
    iyi: "Bu belgeyi dilbilgisi hatalari ve netlik sorunlari icin incele. Icerik dogrulugunu degerlendirme."
  },
  tanimsiz_terimler: {
    kotu: "Standart formati kullan",
    iyi: "JSON olarak formatla: {ad: string, id: number, aktif: boolean}"
  },
  eksik_basari_kriterleri: {
    kotu: "Bunu daha iyi yap",
    iyi: "Bu metni netlik icin iyilestir: cumle uzunlugunu azalt, jargonu kaldir, paragraflar arasi gecisler ekle"
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 2. Yapisal Problemler (Structural Problems)

[define|neutral] YAPISAL_PROBLEMLER := {
  bilgi_asirisi: {
    kotu: "Yapi olmadan 2000 kelimelik monolitik istem",
    iyi: "Net bolumler ve basliklarla hiyerarsik organizasyon"
  },
  gomulu_kritik_bilgi: {
    kotu: "3. paragrafta gelisiguzel bahsedilen anahtar gereksinim",
    iyi: "Kritik gereksinimler basta acikca belirtilir ve sonda yinelenir"
  },
  zayif_ayirici_kullanimi: {
    kotu: "Ayrim olmadan karisik talimatlar ve veri",
    iyi: "Farkli icerik turlerini ayiran net ayiricilar (```, XML etiketleri, vb.)"
  },
  hiyerarsi_eksikligi: {
    kotu: "50 gereksinimin duz listesi",
    iyi: "Net oncelikler ve kategorilerle gruplanmis gereksinimler"
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 3. Baglam Sorunlari (Context Issues)

[define|neutral] BAGLAM_SORUNLARI := {
  varsayilan_bilgi: {
    kotu: "Sirket kurallarini kullan (saglamadan)",
    iyi: "Bu sirket kurallarini kullan: [gercek kurallari saglar]"
  },
  eksik_arka_plan: {
    kotu: "Bu kodu sorunlar icin analiz et",
    iyi: "Bu Python kodunu guvenlik sorunlari icin analiz et. Baglam: Bu bir web uygulamasinda kullanici kimlik dogrulamasini isler."
  },
  tanimsiz_hedef_kitle: {
    kotu: "Kuantum hesaplamayi acikla",
    iyi: "Kuantum hesaplamayi temel fizik bilgisine sahip bir lise ogrencisine acikla"
  },
  belirtilmemis_kisitlamalar: {
    kotu: "JSON ciktisi beklerken bunu soylememek",
    iyi: "Cikti bu semaya uyan gecerli JSON olmali: {...}"
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 4. Mantik ve Tutarlilik Problemleri (Logic and Consistency Problems)

[define|neutral] MANTIK_PROBLEMLERI := {
  celiskili_gereksinimler: {
    kotu: "Kapsamli ama kisa ol",
    iyi: "200 kelimelik ozet sagla, ardindan detayli bolumler"
  },
  imkansiz_ozellikler: {
    kotu: "Tum olasi nedenleri listele (acik uclu alanda)",
    iyi: "Literaturde sikliga gore en yaygin 5 nedeni listele"
  },
  dairesel_tanimlar: {
    kotu: "Daha iyi optimize ederek daha optimize et",
    iyi: "Daha verimli siralama algoritmasi kullanarak zaman karmasikligini O(n^2)'den O(n log n)'e dusur"
  },
  celisen_oncelikler: {
    kotu: "Maliyeti minimize et, ozellikleri maksimize et, en yuksek kaliteyi sagla, hemen teslim et",
    iyi: "Kalite ve temel ozellikleri onceliklendir. Ikincil oncelik maliyet optimizasyonu. Zaman cizelgesi esnektir."
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 5. Sinir Durumu Ihmali (Edge Case Neglect)

[define|neutral] SINIR_DURUMU_IHMALI := {
  bos_null_isleme_yok: {
    kotu: "Metinden tum e-postalari cikar",
    iyi: "Tum e-postalari cikar. Bulunmazsa bos dizi dondur. Gecersiz format e-postalarini atla."
  },
  eksik_hata_durumlari: {
    kotu: "JSON verisini ayristir",
    iyi: "JSON verisini ayristir. Gecersizse, sorunu belirten hata mesaji dondur."
  },
  islenmemis_varyasyonlar: {
    kotu: "Tarihleri tutarli formatla",
    iyi: "Tum tarihleri ISO 8601 formatina (YYYY-MM-DD) donustur. Formatlari isle: GG/AA/YYYY, GG-AA-YYYY, 'Ay GG, YYYY'."
  },
  yok_sayilan_sinir_kosullari: {
    kotu: "Metni ozetle",
    iyi: "Metni 100-200 kelimede ozetle. Metin <50 kelimeyse, degistirmeden dondur. >5000 kelimeyse, 500 kelimede ozetle."
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 6. Onyargi ve Yonlendirici Dil (Bias and Leading Language)

[define|neutral] ONYARGI_SORUNLARI := {
  yuklu_sorular: {
    kotu: "Bu acikca kusurlu yaklasiMin neden basarisiz oldugunu acikla",
    iyi: "Bu yaklasiMin guclu ve zayif yonlerini analiz et"
  },
  ongorulu_sonuclar: {
    kotu: "X'in Y'den ne kadar iyi oldugunu acikla",
    iyi: "X ve Y'yi bu kriterlere gore objektif olarak karsilastir: [...]"
  },
  duygusal_dil: {
    kotu: "Acilen ve hemen analiz et...",
    iyi: "Bu veriyi sistematik olarak analiz et..."
  },
  yanlis_ikicillikler: {
    kotu: "Bu iyi mi kotu mu?",
    iyi: "Bu yaklasiMi degerlendir, ozellikle ustun oldugu veya zorluk yasadigi baglamlari ve odunlari belirt"
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 7. Cikti Tanimi Problemleri (Output Specification Problems)

[define|neutral] CIKTI_PROBLEMLERI := {
  format_belirsizligi: {
    kotu: "Sonuclari organize et",
    iyi: "Sonuclari kategori basliklariyla numarali liste olarak organize et"
  },
  uzunluk_belirsizligi: {
    kotu: "Kisa tut",
    iyi: "Yaniti 250-300 kelimeyle sinirla"
  },
  belirtilmemis_siralama: {
    kotu: "Faktorleri listele",
    iyi: "Faktorleri onem sirasina gore, en onemliden en az onemliye listele"
  },
  eksik_bilesenler: {
    kotu: "Rapor yaz",
    iyi: "Rapor yaz: yonetici ozeti, metodoloji, bulgular, oneriler ve ek dahil"
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### 8. Teknik Yanlis Uygulama (Technique Misapplication)

[define|neutral] TEKNIK_YANLIS_UYGULAMA := {
  uygunsuz_karmasiklik: {
    kotu: "Basit gorevler icin karmasik dusunce zinciri kullanmak",
    iyi: "Teknik sofistikasyonunu gorev karmasikligina esle"
  },
  eksik_uygun_teknikler: {
    kotu: "Oz-tutarlilik kontrolleri olmayan analitik gorev",
    iyi: "X'i birden fazla perspektiften analiz et ve sonuclari kanitlara karsi dogrula"
  },
  basit_gorevleri_asiri_muhendislik: {
    kotu: "Temel aritmetik icin 10 asamali planla-ve-coz",
    iyi: "Basit gorevler icin basit dogrudan talimat"
  },
  gorev_turu_icin_yanlis_kalip: {
    kotu: "Kati adim adim kisitlamalarla yaratici yazim",
    iyi: "Esneklige izin veren kurallar ve orneklerle yaratici yazim"
  }
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

---
<!-- TANI SORULARI (Diagnostic Questions) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_diagnostic]] [[SPC:dogu/troubleshooting]] -->
---

## Tani Sorulari Cercevesi (Diagnostic Questions Frame)

<!-- [[MOR:root:T-N-S]] Tani = root for diagnosis-identification-detection -->
<!-- [[COM:Tani+Soru+Cerceve]] Diagnostic Question Frame -->
[define|neutral] TANI_SORULARI := {
  netlik_hakkinda: [
    "Ne istendigi tam olarak anlasilabilir mi?",
    "Basari kriterleri acik mi?",
    "Farkli insanlar bunu ayni sekilde yorumlar mi?"
  ],
  yapi_hakkinda: [
    "En onemli bilgi belirgin mi?",
    "Organizasyon beni gorev boyunca dogal olarak yonlendiriyor mu?",
    "Farkli icerik turleri acikca ayrilmis mi?"
  ],
  baglam_hakkinda: [
    "Gorevi tamamlamak icin gereken tum bilgiye sahip miyim?",
    "Varsayimlar acik mi?",
    "Hedef kitle ve amac acik mi?"
  ],
  mantik_hakkinda: [
    "Tum gereksinimler birbiriyle uyumlu mu?",
    "Ozellikler ulasilabilir mi?",
    "Ic tutarlilik var mi?"
  ],
  tamlik_hakkinda: [
    "Sinir durumlarinda ne olur?",
    "Hata kosullari isleniyor mu?",
    "Tum olasi varyasyonlar ele aliniyor mu?"
  ],
  onyargi_hakkinda: [
    "Istem sonuclari onceden yargilıyor mu?",
    "Dil tarafsiz ve objektif mi?",
    "Birden fazla perspektife davet ediliyor mu?"
  ],
  cikti_hakkinda: [
    "Istenen format acik mi?",
    "Uzunluk beklentileri net mi?",
    "Gerekli bilesenler belirlenmis mi?"
  ],
  teknikler_hakkinda: [
    "Kanit tabanli kalipler uygun sekilde uygulanıyor mu?",
    "Teknik sofistikasyonu gorev karmasikligina eslestirilmis mi?",
    "Gorev turu icin dogru istem kaliplari kullaniliyor mu?"
  ]
} [ground:methodology:diagnostics] [conf:0.90] [state:confirmed]

---
<!-- HIZLI DUZELTMELER (Quick Fixes) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_solution]] [[SPC:guney/remediation]] -->
---

## Hizli Duzeltmeler Cercevesi (Quick Fixes Frame)

<!-- [[MOR:root:D-Z-L]] Duzeltme = root for fix-correction-remedy -->
<!-- [[COM:Hizli+Duzeltme+Cerceve]] Quick Fix Frame -->
[define|neutral] HIZLI_DUZELTMELER := {
  cok_belirsiz: "Belirli eylem fiilleri ve somut hedefler ekle",
  cok_karmasik: "Daha kucuk istemlere bol veya hiyerarsik yapi kullan",
  tutarsiz_cikti: "Acik format tanimi ve ornekler ekle",
  eksik_sinir_durumlari: "Yaygin varyasyonlari listele ve islemeyi belirt",
  dusuk_guvenilirlik: "Oz-tutarlilik kontrolleri ve dogrulama adimlari ekle",
  yanlis_sonuclar: "Istenen kaliplari gosteren az-atisli ornekler sagla",
  celiskiler: "Gereksinimleri 'birincil/ikincil' ile acikca onceliklendir",
  eksik_baglam: "Varsayimlari acikca belirt ve arka plan sagla"
} [ground:witnessed:solutions] [conf:0.90] [state:confirmed]

---
<!-- ONLEME STRATEJILERI (Prevention Strategies) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_strategy]] [[SPC:bati/prevention]] -->
---

## Onleme Stratejileri Cercevesi (Prevention Strategies Frame)

<!-- [[MOR:root:O-N-L]] Onleme = root for prevention-avoidance-precaution -->
<!-- [[COM:Onleme+Strateji+Cerceve]] Prevention Strategy Frame -->
[define|neutral] ONLEME_STRATEJILERI := [
  "Istenen girdi ve ciktilarin somut ornekleriyle basla",
  "Sonradan dusunme yerine sinir durumlarini erkenden test et",
  "Gereksinimler hakkinda ortuk yerine acik ol",
  "~200 kelimenin uzerindeki her istem icin hiyerarsik olarak yapilandir",
  "Dagitmadan once cerceve karsi dogrula",
  "Teorik mukemmellik yerine gercek basarisizliklara dayanarak yinele",
  "Calisanlari gelecek referans icin belgele"
] [ground:methodology:prevention] [conf:0.90] [state:confirmed]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Spravochnik po anti-patternam uspeshno zavershon. (Russian: Complete. Anti-pattern reference successfully completed.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[assert|confident] SONUC_OZETI := {
  anahtar_ilke: "Hedef mukemmel istemler degil - belirli kullanim durumunuz icin guvenilir sekilde calisan istemlerdir",
  hatirlatma: "Pratik etkinlik teorik optimizasyonu yener"
} [ground:witnessed:skill-execution] [conf:0.95] [state:confirmed]

---

[commit|confident] <promise>ANTI_PATTERNS_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
