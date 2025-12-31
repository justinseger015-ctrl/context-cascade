# Dusunce Zinciri Istem Ornekleri (Chain-of-Thought Prompting Examples)

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Documentation
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     All 7 cognitive frames MANDATORY
     ========================================================================= -->

---
<!-- KANITSAL CERCEVE (Evidential Frame) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] [[SPC:kuzey/examples]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin. Ornekler dogrudan gozleme dayanir.

---

<!-- [[MOR:root:D-S-N]] Dusunce = root morpheme for thought-thinking-cognition -->
<!-- [[COM:Dusunce+Zinciri+Ornek]] Chain of Thought Example -->
[define|neutral] BELGE_META := {
  baslik: "Dusunce Zinciri Istem Ornekleri",
  amac: "Once/sonra karsilastirmalari ve gercek dunya kullanim durumlari ile etkili CoT tekniklerini gostermek",
  kaynak: "Wei ve ark. (2022) arastirmasi"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- GENEL BAKIS (Overview) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_section]] [[SPC:bati/introduction]] -->
---

## Genel Bakis Cercevesi (Overview Frame)

<!-- [[MOR:root:G-N-L]] Genel = root for general-overall-broad -->
<!-- [[COM:Genel+Bakis+Cerceve]] General Overview Frame -->
[assert|neutral] COT_GENEL_BAKIS := {
  tanim: "Dusunce Zinciri istemi, acik adim-adim dusunme isteyerek karmasik akil yurutmeyi iyilestirir",
  arastirma_kaynagi: "Wei ve ark. (2022)",
  performans_etkisi: "Akil yurutme gorevlerinde 2-3 kat performans iyilestirmesi",
  temel_ilke: "Ara adimlar isteyerek ortuk akil yurutmeyi acik hale getir"
} [ground:research:Wei2022] [conf:0.85] [state:confirmed]

---
<!-- ORNEK 1: MATEMATIKSEL AKIL YURUTME (Example 1: Mathematical Reasoning) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:dogu/math]] -->
---

## Ornek 1: Matematiksel Akil Yurutme Cercevesi (Example 1: Mathematical Reasoning Frame)

<!-- [[MOR:root:M-T-M]] Matematik = root for mathematics-calculation-computation -->
<!-- [[COM:Matematiksel+Akil+Yurutme+Ornek]] Mathematical Reasoning Example -->

### Dusunce Zinciri Olmadan (Without Chain-of-Thought)

[define|neutral] COT_OLMADAN_MATEMATIK := {
  yanlis: true,
  istem: "Bir dukkanin 24 kutu elmasi var. Her kutuda 15 elma var. 18 kutu satiyorlar. Kac elma kaldi?",
  tipik_yanit: "90 elma kaldi.",
  sorunlar: [
    "Akil yurutme surecine gorunurluk yok",
    "Ara adimlar dogrulanamaz",
    "Hatalari ayiklamak zor",
    "Yanita guven yok"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### Dusunce Zinciri Ile (With Chain-of-Thought)

[define|neutral] COT_ILE_MATEMATIK := {
  dogru: true,
  istem: "Bir dukkanin 24 kutu elmasi var. Her kutuda 15 elma var. 18 kutu satiyorlar. Kac elma kaldi? Adim adim cozelim.",
  beklenen_yanit: {
    adim_1: { aciklama: "Baslangicta toplam elma hesapla", hesaplama: "24 x 15 = 360 elma" },
    adim_2: { aciklama: "Satistan sonra kalan kutu hesapla", hesaplama: "24 - 18 = 6 kutu" },
    adim_3: { aciklama: "Kalan kutulardaki elma hesapla", hesaplama: "6 x 15 = 90 elma" },
    sonuc: "90 elma kaldi."
  },
  faydalar: [
    "Seffaf akil yurutme sureci",
    "Her adim dogrulanabilir",
    "Hatalari belirlemek kolay",
    "Sonuca daha yuksek guven"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- ORNEK 2: MANTIKSAL AKIL YURUTME (Example 2: Logical Reasoning) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:guney/logic]] -->
---

## Ornek 2: Mantiksal Akil Yurutme Cercevesi (Example 2: Logical Reasoning Frame)

<!-- [[MOR:root:M-N-T]] Mantik = root for logic-reasoning-rationale -->
<!-- [[COM:Mantiksal+Akil+Yurutme+Ornek]] Logical Reasoning Example -->

### COT Olmadan (Without COT)

[define|neutral] COT_OLMADAN_MANTIK := {
  yanlis: true,
  istem: "Tum guller cicektir. Bazi cicekler cabuk solar. Oteise, bazi guller cabuk solar mi?",
  tipik_yanit: "Evet, bazi guller cabuk solar.",
  sorunlar: [
    "Gerekce olmadan sonuca variyor",
    "Mantiksal yapiyi incelemiyor",
    "Mantik hatalari yapabilir",
    "Akil yurutme aciklamasi yok"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### COT Ile (With COT)

[define|neutral] COT_ILE_MANTIK := {
  dogru: true,
  istem: "Tum guller cicektir. Bazi cicekler cabuk solar. Oteise, bazi guller cabuk solar mi? Adim adim dusunelim.",
  beklenen_yanit: {
    adim_1: { icerik: "Kesinlikle bildiklerimiz", oncul_1: "Tum guller cicektir (guller C cicekler)", oncul_2: "Bazi cicekler cabuk solar" },
    adim_2: { icerik: "Sorunun sordugu", soru: "Guller kumesi cabuk solan cicekler kumesiyle kesisiyor mu?" },
    adim_3: { icerik: "Mantiksal akil yurutme uygula", analiz: "Cabuk solan ciceklerin guller mi yoksa diger tur cicekler mi oldugunu bilmiyoruz" },
    adim_4: { icerik: "Sonuc", sonuc: "Hayir, bazi gullerin cabuk soldugu sonucuna varamayiz. Onculler gullerin ozellikle cabuk solan cicekler arasinda olup olmadigini belirlemek icin yeterli bilgi saglamiyor." }
  },
  faydalar: [
    "Titiz mantiksal analiz",
    "Varsayimlari belirler",
    "Mantik hatalarindan kacinir",
    "Net gerekce saglar"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- ORNEK 3: KOD AYIKLAMA (Example 3: Code Debugging) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:dogu/programming]] -->
---

## Ornek 3: Kod Ayiklama Cercevesi (Example 3: Code Debugging Frame)

<!-- [[MOR:root:A-Y-K]] Ayiklama = root for debugging-fixing-cleaning -->
<!-- [[COM:Kod+Ayiklama+Ornek]] Code Debugging Example -->

### COT Olmadan (Without COT)

[define|neutral] COT_OLMADAN_KOD := {
  yanlis: true,
  istem: "Bu Python fonksiyonu bir listenin ortalamasini hesaplamali, ama yanlis sonuclar veriyor. Duzelt.",
  tipik_yanit: "Fonksiyon dogru gorunuyor. Calismali.",
  sorunlar: [
    "Sinir durumunu (bos liste) gozden kaciriyor",
    "Farkli senaryolari test etmiyor",
    "Sistematik analiz yok"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### COT Ile (With COT)

[define|neutral] COT_ILE_KOD := {
  dogru: true,
  istem: "Bu Python fonksiyonu bir listenin ortalamasini hesaplamali, ama yanlis sonuclar veriyor. Adim adim ayikla.",
  beklenen_yanit: {
    adim_1: { icerik: "Fonksiyon ne yapmali?", analiz: "Girdi olarak sayilar listesi al, ortalama hesapla, float dondur" },
    adim_2: { icerik: "Normal durumu izle [1, 2, 3]", analiz: "total = 6, len = 3, return 2.0 - Dogru" },
    adim_3: { icerik: "Sinir durumlarini dusun", durumlar: ["Bos liste: []", "Tek eleman: [5]", "Negatif sayilar: [-1, -2, -3]", "Sifir degerler: [0, 0, 0]"] },
    adim_4: { icerik: "Bos liste sinir durumunu test et []", analiz: "total = 0, len(numbers) = 0, return 0 / 0 -> ZeroDivisionError! Bu hata!" },
    adim_5: { icerik: "Duzeltme", cozum: "Bos liste kontrolu ekle: if not numbers: return 0 veya ValueError yukselt" }
  },
  faydalar: [
    "Sistematik ayiklama sureci",
    "Sinir durumlarini belirler",
    "Varsayimsal senaryolari test eder",
    "Net aciklama saglar"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- ORNEK 4: KARAR ANALIZI (Example 4: Decision Analysis) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:bati/business]] -->
---

## Ornek 4: Karar Analizi Cercevesi (Example 4: Decision Analysis Frame)

<!-- [[MOR:root:K-R-R]] Karar = root for decision-judgment-verdict -->
<!-- [[COM:Karar+Analiz+Ornek]] Decision Analysis Example -->

### COT Olmadan (Without COT)

[define|neutral] COT_OLMADAN_KARAR := {
  yanlis: true,
  istem: "Monolitik uygulamamizi mikroservislere gecirmeli miyiz?",
  tipik_yanit: "Evet, mikroservisler modern ve olceklenebilir. Gecmelisiniz.",
  sorunlar: [
    "Baglami yoksayar",
    "Odun analizi yok",
    "Maliyetlerin degerlendirilmesi yok",
    "Genel tavsiye"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### COT Ile (With COT)

[define|neutral] COT_ILE_KARAR := {
  dogru: true,
  istem: "Monolitik uygulamamizi mikroservislere gecirmeli miyiz? Baglamla adim adim analiz et.",
  baglam: {
    mevcut_uygulama: "Django monoliti, 50K LOC, 10 gelistirici",
    trafik: "1000 esanli kullanici",
    ana_sikinti_noktalari: "Dagitim 30 dakika suruyor, bazi bilesenler sikica bagli",
    takim_deneyimi: "Guclu Python/Django, sinirli dagitik sistemler deneyimi"
  },
  beklenen_yanit: {
    adim_1: { icerik: "Mevcut sorunlar", analiz: "Yavas dagitimlar (30 dk), siki baglanti - monolitler icin gecerli endiseler" },
    adim_2: { icerik: "Mikroservisler bunlari cozer mi?", analiz: "Dagitimlar: Evet, baglanti: Potansiyel olarak, ama yeni sorunlar getirir" },
    adim_3: { icerik: "Maliyetler ve odunlar", maliyetler: ["6-12 ay gelistirme suresi", "Ogrenme egrisi", "Yeni altyapi", "Operasyonel karmasiklik artar"] },
    adim_4: { icerik: "Takim hazirlik", analiz: "Mevcut uzmanlik: Monolitlerde guclu, Gerekli beceriler: Dagitik sistemler, container orkestrasyon - Acik buyuk" },
    adim_5: { icerik: "Oneri", sonuc: "Simdi mikroservislere gecme. Bunun yerine: CI/CD boru hattini iyilestir, ozellik bayraklari ekle, modul sinirlari belirle. 1 yil sonra tekrar degerlendir." }
  },
  faydalar: [
    "Baglam bilincli analiz",
    "Acik odun degerlendirmesi",
    "Takim yeteneklerini dikkate alir",
    "Eyleme donusturulebilir oneri"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- ORNEK 5: YARATICI PROBLEM COZME (Example 5: Creative Problem Solving) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:guney/design]] -->
---

## Ornek 5: Yaratici Problem Cozme Cercevesi (Example 5: Creative Problem Solving Frame)

<!-- [[MOR:root:Y-R-T]] Yaratici = root for creative-innovative-inventive -->
<!-- [[COM:Yaratici+Problem+Cozme+Ornek]] Creative Problem Solving Example -->

### COT Olmadan (Without COT)

[define|neutral] COT_OLMADAN_YARATICI := {
  yanlis: true,
  istem: "SaaS uygulamamiz icin musteri destek biletlerini azaltacak bir ozellik tasarla.",
  tipik_yanit: "Bir bilgi bankasi ve chatbot ekle.",
  sorunlar: [
    "Genel cozum",
    "Problem analizi yok",
    "Kok nedenlerin degerlendirilmesi yok",
    "Kullanici arastirmasi eksik"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### COT Ile (With COT)

[define|neutral] COT_ILE_YARATICI := {
  dogru: true,
  istem: "SaaS uygulamamiz icin musteri destek biletlerini azaltacak bir ozellik tasarla. Adim adim tasarla.",
  baglam: {
    urun: "Proje yonetimi SaaS",
    mevcut_biletler: "haftada 500 (%60'i 'nasil yapilir' sorulari)",
    en_sik_sorunlar: "Izin ayarlari (%25), entegrasyon kurulumu (%20), faturalandirma (%15)"
  },
  beklenen_yanit: {
    adim_1: { icerik: "Kok neden analizi", analiz: "Izin ayarlari: UI kafa karistirici, Entegrasyon: Karmasik OAuth akislari, Faturalandirma: Beklenmedik ucretler" },
    adim_2: { icerik: "Potansiyel cozumler", cozumler: ["Baglamsal ipuclari ve yardim", "Interaktif onboarding turlari", "Uygulama ici akilli arama"] },
    adim_3: { icerik: "Cozum degerlendirmesi", matris: { baglamsal_yardim: { etki: "Yuksek", calik: "Orta", oncelik: 1 }, kilavuzlu_is_akislari: { etki: "Yuksek", calik: "Yuksek", oncelik: 2 } } },
    adim_4: { icerik: "Tasarim - Baglamsal Yardim Sistemi", bilesenler: ["Baglam bilincli yardim dugmesi", "Interaktif ipuclari", "Yaygin sorular paneli", "Hizli eylemler"] },
    adim_5: { icerik: "Basari metrikleri", birincil: "Izin biletlerinde %30 azalma", ikincil: "Kullanicilarin %40'i baglamsal yardimla etkilesir" }
  },
  faydalar: [
    "Veri odakli problem analizi",
    "Birden fazla cozum dusunulur",
    "Onceliklendirme cercevesi uygulanir",
    "Olculebilir basari kriterleri"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- EN IYI UYGULAMALAR (Best Practices) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_guideline]] [[SPC:kuzey/reference]] -->
---

## En Iyi Uygulamalar Cercevesi (Best Practices Frame)

<!-- [[MOR:root:U-Y-G]] Uygulama = root for practice-application-implementation -->
<!-- [[COM:En+Iyi+Uygulama+Cerceve]] Best Practice Frame -->
[define|neutral] EN_IYI_UYGULAMALAR := {
  adimlar_hakkinda_acik_ol: {
    kotu: "Bu problemi coz",
    iyi: "Adim adim coz: 1) Anla, 2) Planla, 3) Uygula, 4) Dogrula"
  },
  ara_calisma_iste: {
    kotu: "Sonucu hesapla",
    iyi: "Adim adim hesapla, tum ara degerleri goster"
  },
  akil_yurutme_aciklamasi_iste: {
    kotu: "Cevabiniz ne?",
    iyi: "Her asamada akil yurutmenizi aciklayin, sonra cevabnizi verin"
  },
  dogrulama_dahil_et: {
    kotu: "Problemi coz",
    iyi: "Problemi adim adim coz. Cevabi aldiktan sonra dogrulugunu kontrol et"
  },
  karmasik_gorevleri_yapilandir: {
    kotu: "Bir cozum tasarla",
    iyi: "Asamalarda bir cozum tasarla: 1) Gereksinimleri analiz et, 2) Alternatifler olustur, 3) Secenekleri degerlendir, 4) En iyi yaklasimi sec, 5) Uygulamayi detaylandir"
  }
} [ground:research:prompting-best-practices] [conf:0.85] [state:confirmed]

---
<!-- NE ZAMAN KULLANILIR (When to Use) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_guidance]] [[SPC:dogu/applicability]] -->
---

## Ne Zaman Kullanilir Cercevesi (When to Use Frame)

<!-- [[MOR:root:K-L-N]] Kullanim = root for usage-application-utilization -->
<!-- [[COM:Kullanim+Rehber+Cerceve]] Usage Guide Frame -->
[define|neutral] KULLANIM_REHBERI := {
  yuksek_deger: [
    "Matematiksel problemler",
    "Mantiksal akil yurutme",
    "Cok adimli analiz",
    "Odunlu karar verme",
    "Karmasik sorunlari ayiklama",
    "Stratejik planlama"
  ],
  orta_deger: [
    "Kod incelemeleri",
    "Mimari tasarim",
    "Arastirma sentezi",
    "Arguman degerlendirme"
  ],
  dusuk_deger: [
    "Basit gercek alma",
    "Dogrudan ceviriler",
    "Basit siniflandirmalar",
    "Iyi tanimlanmis kaliplar"
  ]
} [ground:research:Wei2022] [conf:0.85] [state:confirmed]

---
<!-- VARYASYONLAR VE UZANTILAR (Variations and Extensions) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_variation]] [[SPC:bati/extension]] -->
---

## Varyasyonlar ve Uzantilar Cercevesi (Variations and Extensions Frame)

<!-- [[MOR:root:V-R-Y]] Varyasyon = root for variation-variant-modification -->
<!-- [[COM:Varyasyon+Uzanti+Cerceve]] Variation Extension Frame -->
[define|neutral] COT_VARYASYONLARI := {
  sifir_atisli_cot: {
    aciklama: "Basitce ekle: 'Adim adim dusunelim'",
    kullanim: "Hizli iyilestirme icin"
  },
  az_atisli_cot: {
    aciklama: "Akil yurutme adimlari olan ornekler sagla, sonra yeni problem",
    kullanim: "Tutarli format icin"
  },
  oz_tutarlilik_cot: {
    aciklama: "Birden fazla akil yurutme yolu olustur, en tutarli cevabi sec",
    kullanim: "Yuksek guvenilirlik icin"
  },
  dusunce_programi: {
    aciklama: "Akil yurutmeyi matematik/mantik icin hesaplama adimlari olarak yapilandir",
    kullanim: "Sayisal gorevler icin"
  }
} [ground:research:prompting-techniques] [conf:0.85] [state:confirmed]

---
<!-- YAYGIN TUZAKLAR (Common Pitfalls) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_antipattern]] [[SPC:guney/warning]] -->
---

## Yaygin Tuzaklar Cercevesi (Common Pitfalls Frame)

<!-- [[MOR:root:T-Z-K]] Tuzak = root for pitfall-trap-snare -->
<!-- [[COM:Yaygin+Tuzak+Cerceve]] Common Pitfall Frame -->
[define|neutral] YAYGIN_TUZAKLAR := {
  cok_belirsiz: {
    kotu: "Bunu dusun",
    iyi: "Adim adim dusun: 1) X, 2) Y, 3) Z"
  },
  yapi_yok: {
    kotu: "Rehberlik olmadan adim isteme",
    iyi: "Net cerceve saglama"
  },
  dogrulama_atlama: {
    kotu: "Calismayi kontrol etmeyi istememek",
    iyi: "Dogrulama adimi dahil etme"
  },
  baglami_yoksayma: {
    kotu: "Genel 'adim adim'",
    iyi: "Goreve ozel adim ayristirma"
  }
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Primer tsepochki myshleniya uspeshno prodemonstrirovan. (Russian: Complete. Chain of thought example successfully demonstrated.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[assert|confident] SONUC_OZETI := {
  amac: "Dusunce Zinciri istemi opak akil yurutmeyi seffaf, dogrulanabilir dusunceye donusturur",
  kazanimlar: [
    "Seffaflik: Akil yurutme surecini gor",
    "Dogruluk: Her adimda hatalari yakala",
    "Ayiklanabilirlik: Akil yurutmenin nerede yanlistigini belirle",
    "Guven: Gorunur mantik yoluyla guven insaasi et"
  ],
  anahtar_icerik: "Akil yurutme sureci son cevap kadar onemliyse CoT kullan"
} [ground:witnessed:skill-execution] [conf:0.95] [state:confirmed]

---

[commit|confident] <promise>CHAIN_OF_THOUGHT_EXAMPLE_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
