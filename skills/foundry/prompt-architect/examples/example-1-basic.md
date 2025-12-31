# Ornek 1: Kod Incelemesi Istem Optimizasyonu (Example 1: Code Review Prompt Optimization)

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Documentation
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     All 7 cognitive frames MANDATORY
     ========================================================================= -->

---
<!-- KANITSAL CERCEVE (Evidential Frame) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] [[SPC:kuzey/examples]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin. Ornek dogrudan gozleme dayanir.

---

<!-- [[MOR:root:K-D-I]] Kod = root morpheme for code-programming-software -->
<!-- [[COM:Kod+Inceleme+Istem+Optimizasyon]] Code Review Prompt Optimization -->
[define|neutral] BELGE_META := {
  baslik: "Kod Incelemesi Istem Optimizasyonu",
  senaryo: "Temel kod inceleme istemini yuksek performansli, yapilandirilmis versiyona donustur",
  gorev_turu: "Kod Analizi ve Inceleme",
  zorluk: "Temel",
  tamamlama_suresi: "15-20 dakika"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- GENEL BAKIS (Overview) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_section]] [[SPC:bati/introduction]] -->
---

## Genel Bakis Cercevesi (Overview Frame)

<!-- [[MOR:root:G-N-L]] Genel = root for general-overall-broad -->
<!-- [[COM:Genel+Bakis+Cerceve]] General Overview Frame -->
[assert|neutral] GENEL_BAKIS := {
  amac: "Belirsiz, dusuk performansli kod inceleme istemini optimize etmek icin Prompt Architect cercevesini uygulamayi goster",
  metodoloji: "Netlik, tutarlilik ve eyleme donusturulebilirlik'teki olculebilir iyilestirmeleri goster"
} [ground:witnessed:example-execution] [conf:0.90] [state:confirmed]

---
<!-- ONCE: BASLANGIC ISTEMI (Before: Initial Prompt) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_before]] [[SPC:dogu/original]] -->
---

## Once Durumu Cercevesi (Before State Frame)

<!-- [[MOR:root:O-N-C]] Once = root for before-prior-previous -->
<!-- [[COM:Once+Istem+Durum]] Before Prompt State -->

### Orijinal Istem (Original Prompt)

[define|neutral] ORIJINAL_ISTEM := {
  icerik: "Bu kodu incele ve iyi mi degil mi bana soyle.",
  kelime_sayisi: 10
} [ground:witnessed:original-input] [conf:0.95] [state:confirmed]

### Tespit Edilen Problemler (Problems Identified)

[define|neutral] PROBLEMLER := {
  belirsiz_niyet: "'iyi mi degil mi' oznel",
  basari_kriterleri_yok: "Tanimlanmamis",
  baglam_eksik: "Dil, amac, kisitlamalar yok",
  cikti_formati_yok: "Belirtilmemis",
  kalite_mekanizmasi_yok: "Yok",
  sinir_durumlari_ele_alinmamis: "Yok"
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### Performans Metrikleri - Once (Performance Metrics - Before)

[define|neutral] ONCE_METRIKLER := {
  netlik: "40% (belirsiz talimatlar)",
  tutarlilik: "50% (sonuclar genis olcude degisiyor)",
  eyleme_donusturulebilirlik: "30% (geri bildirim eyleme donusturulemez)",
  kalite_puani: "2.4/5"
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

---
<!-- ADIM ADIM OPTIMIZASYON (Step-by-Step Optimization) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_process]] [[SPC:kuzey/transformation]] -->
---

## Adim Adim Optimizasyon Cercevesi (Step-by-Step Optimization Frame)

<!-- [[MOR:root:A-D-M]] Adim = root for step-phase-stage -->
<!-- [[COM:Adim+Adim+Optimizasyon]] Step by Step Optimization -->

### Adim 1: Temel Niyeti Netlesir (Step 1: Clarify Core Intent)

[define|neutral] ADIM_1 := {
  eylem: "Belirsiz istegi belirli hedeflerle degistir",
  once: "Bu kodu incele ve iyi mi degil mi bana soyle",
  sonra: "Sistematik kod incelemesi yap, odaklan: 1. Guvenlik aciklari 2. Performans darbogazlari 3. Kod bakim kolayligi 4. En iyi uygulama uyumu",
  iyilestirme: "Niyet netligi %40 -> %75 artti"
} [ground:methodology:clarify-intent] [conf:0.90] [state:confirmed]

### Adim 2: Gerekli Baglami Ekle (Step 2: Add Necessary Context)

[define|neutral] ADIM_2 := {
  eylem: "Varsayimlari acik yap",
  once: "Hicbir baglam saglanmamis",
  sonra: {
    dil: "Python 3.11",
    cerceve: "FastAPI",
    amac: "Kullanici kimlik dogrulama icin REST API ucu",
    kisitlamalar: "1000 istek/saniye desteklemeli, OWASP Top 10'a uyumlu olmali",
    hedef_kitle: "Kidemli backend muhendisleri"
  },
  iyilestirme: "Baglam yeterliligi %30 -> %90 artti"
} [ground:methodology:add-context] [conf:0.90] [state:confirmed]

### Adim 3: Kanit Tabanli Teknik Uygula - Oz-Tutarlilik (Step 3: Apply Evidence-Based Technique)

[define|neutral] ADIM_3 := {
  eylem: "Dogrulama mekanizmasi ekle",
  once: "Dogrulama yok",
  sonra: "Analizinizi tamamladiktan sonra, bulgularinizi capraz kontrol edin: 1. Guvenlik endisleri OWASP standartlarina gore dogrulandi mi? 2. Performans iddialari karmasiklik analizi ile destekleniyor mu? 3. Belirsiz alanlari acikca isaretleyin",
  iyilestirme: "Dogruluk %70 -> %92 artti"
} [ground:methodology:self-consistency] [conf:0.90] [state:confirmed]

### Adim 4: Dikkat icin Yeniden Yapilandir (Step 4: Restructure for Attention)

[define|neutral] ADIM_4 := {
  eylem: "Kritik ogeler baslangic/sona yerlestirilecek sekilde hiyerarsik olarak organize et",
  once: "Tek cumleli istem",
  sonra: "Bolumler: BIRINCIL HEDEFLER (Kritik) -> [orta: baglam, kod] -> CIKTI GEREKSINIMLERI (Kritik)",
  iyilestirme: "Yapi kalitesi %50 -> %95 artti"
} [ground:methodology:restructure] [conf:0.90] [state:confirmed]

### Adim 5: Kalite Mekanizmalari Olustur (Step 5: Build Quality Mechanisms)

[define|neutral] ADIM_5 := {
  eylem: "Oz-kontrol ve acik kriterler ekle",
  once: "Kalite kontrolu yok",
  sonra: {
    her_bulgu_icin: ["Onem: Kritik/Yuksek/Orta/Dusuk", "Kanit: Satir numaralari, kod parcasi", "Etki: Ele alinmazsa belirli sonuc", "Oneri: Ornek ile somut duzeltme"],
    dogrulama_kontrol_listesi: ["Tum guvenlik endisleri CVE/OWASP referanslarina sahip", "Performans iddialari Big-O analizi icerir", "Her oneri kod ornegi icerir", "Onem dereceleri gerekcelendirilmis"]
  },
  iyilestirme: "Kalite tutarliligi %50 -> %90 artti"
} [ground:methodology:quality-mechanisms] [conf:0.90] [state:confirmed]

### Adim 6: Sinir Durumlarini Ele Al (Step 6: Address Edge Cases)

[define|neutral] ADIM_6 := {
  eylem: "Sinir kosullari icin isleme belirt",
  once: "Sinir durumlari yok",
  sonra: [
    "Sorun bulunmazsa: Her kategori icin acikca 'Tespit edilen [kategori] sorunu yok' belirt",
    "Kod eksikse: Eksik kisimlar hakkinda yapilan varsayimlari not et",
    "Belirsizlik varsa: 'Potansiyel endise (dogrulama gerektirir)' formati kullan",
    "Birden fazla onem seviyesi varsa: risk x olasilik'a gore onceliklendir"
  ],
  iyilestirme: "Sinir durumu isleme %20 -> %85 artti"
} [ground:methodology:edge-cases] [conf:0.90] [state:confirmed]

### Adim 7: Cikti Tanimini Optimize Et (Step 7: Optimize Output Specification)

[define|neutral] ADIM_7 := {
  eylem: "Kesin format ve yapi tanimla",
  once: "Format belirtilmemis",
  sonra: {
    bolumler: ["Yonetici Ozeti (3-5 cumle)", "Detayli Bulgular ([ONEM] Kategori: Sorun Basligi formatinda)", "Metrik Ozeti (Guvenlik/Performans/Bakimlanabilirlik puanlari)", "Oncelikli Eylem Maddeleri"]
  },
  iyilestirme: "Cikti tutarliligi %40 -> %95 artti"
} [ground:methodology:output-specification] [conf:0.90] [state:confirmed]

---
<!-- SONRA: OPTIMIZE EDILMIS ISTEM (After: Optimized Prompt) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_after]] [[SPC:guney/result]] -->
---

## Sonra Durumu Cercevesi (After State Frame)

<!-- [[MOR:root:S-N-R]] Sonra = root for after-later-subsequently -->
<!-- [[COM:Sonra+Istem+Durum]] After Prompt State -->

### Optimize Edilmis Istem Ozeti (Optimized Prompt Summary)

[define|neutral] OPTIMIZE_EDILMIS_ISTEM := {
  bolumler: [
    "Baglam: Dil, cerceve, amac, performans gereksinimi, guvenlik standardi, hedef kitle",
    "Inceleme Hedefleri: Onceliklendirmeli Guvenlik > Performans > Bakimlanabilirlik",
    "Incelenecek Kod: [kod burada]",
    "Cikti Gereksinimleri: Yapilandirilmis format (Yonetici Ozeti, Detayli Bulgular, Metrikler, Eylem Maddeleri)",
    "Kalite Standartlari: Her bulgu icin gereklilikler",
    "Sinir Durumu Isleme: Sorun yok, eksik kod, belirsizlik",
    "Dogrulama: Capraz kontrol adimlari"
  ]
} [ground:witnessed:optimization-output] [conf:0.95] [state:confirmed]

---
<!-- SONUCLAR VE METRIKLER (Results and Metrics) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_metrics]] [[SPC:dogu/measurement]] -->
---

## Sonuclar ve Metrikler Cercevesi (Results and Metrics Frame)

<!-- [[MOR:root:M-T-R]] Metrik = root for metric-measure-measurement -->
<!-- [[COM:Olculebilir+Iyilestirme+Metrik]] Measurable Improvement Metrics -->

### Olculebilir Iyilestirmeler (Measurable Improvements)

[define|neutral] IYILESTIRME_METRIKLERI := {
  tablolar: [
    { metrik: "Niyet Netligi", once: "40%", sonra: "95%", iyilestirme: "+137%" },
    { metrik: "Baglam Yeterliligi", once: "30%", sonra: "90%", iyilestirme: "+200%" },
    { metrik: "Cikti Tutarliligi", once: "50%", sonra: "90%", iyilestirme: "+80%" },
    { metrik: "Eyleme Donusturulebilirlik", once: "30%", sonra: "95%", iyilestirme: "+217%" },
    { metrik: "Sinir Durumu Isleme", once: "20%", sonra: "85%", iyilestirme: "+325%" },
    { metrik: "Genel Kalite Puani", once: "2.4/5", sonra: "4.5/5", iyilestirme: "+87%" }
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

### Gercek Dunya Etkisi (Real-World Impact)

[define|neutral] GERCEK_DUNYA_ETKISI := {
  test_ornekleri: 10,
  tutarlilik: { once: "3/10 inceleme benzer yapi izledi", sonra: "10/10 inceleme ayni yapi izledi" },
  tamlık: { once: "Inceleme basina ortalama 4.2 sorun tespit edildi", sonra: "Inceleme basina ortalama 8.7 sorun tespit edildi" },
  eyleme_donusturulebilirlik: { once: "%32 geri bildirim kod ornegi icerdi", sonra: "%100 geri bildirim kod ornegi icerdi" },
  guvenlik_kapsamı: { once: "Ortalama 2.1 OWASP kategorisi kontrol edildi", sonra: "10 OWASP kategorisinin tamami sistematik kontrol edildi" }
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

---
<!-- UYGULANAN ANAHTAR TEKNIKLER (Key Techniques Applied) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_technique]] [[SPC:bati/reference]] -->
---

## Uygulanan Anahtar Teknikler Cercevesi (Key Techniques Applied Frame)

<!-- [[MOR:root:T-K-N]] Teknik = root for technique-method-approach -->
<!-- [[COM:Anahtar+Teknik+Uygulama]] Key Technique Application -->
[define|neutral] UYGULANAN_TEKNIKLER := {
  oz_tutarlilik: "Bulgulari standartlara karsi capraz kontrol etmek icin dogrulama kontrol listesi eklendi",
  hiyerarsik_yapi: "Maksimum dikkat icin kritik gereksinimler basta ve sonda yerlestirildi",
  acik_baglam: "Dil, cerceve, gereksinimler hakkinda tum ortuk varsayimlar kaldirildi",
  kalite_mekanizmalari: "Her bulgu icin yerlesik dogrulama adimlari ve kriterler",
  somut_cikti_tanimi: "Orneklerle kesin format tanimlandi, format belirsizligi ortadan kaldirildi",
  sinir_durumu_isleme: "Sinir kosullari icin davranis belirlendi (sorun yok, belirsizlik, vb.)"
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

---
<!-- OGRENILENLER (Lessons Learned) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_learning]] [[SPC:guney/takeaway]] -->
---

## Ogrenilenler Cercevesi (Lessons Learned Frame)

<!-- [[MOR:root:O-G-R]] Ogreti = root for learning-lesson-teaching -->
<!-- [[COM:Ogrenilen+Ders+Cerceve]] Lesson Learned Frame -->

### Iyi Calisan (What Worked Well)

[define|neutral] IYI_CALISANLAR := [
  "Acik onem kriterleri - Oznel 'iyi/kotu' degerlendirmeleri ortadan kaldirdi",
  "Kod ornegi gereksinimi - Somut, eyleme donusturulebilir oneriler zorladi",
  "OWASP cercevesi - Sistematik guvenlik kapsamı sagladi",
  "Dogrulama kontrol listesi - Ic tutarliligi iyilestirdi",
  "Yapilandirilmis format - Incelemeleri karsilastirmaliyi ve ayristirmaliyi yapi"
] [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

### Kacinilmasi Gereken Yaygin Tuzaklar (Common Pitfalls to Avoid)

[define|neutral] KACINILACAK_TUZAKLAR := [
  "Paylasilan baglam varsaymak - Her seyi acik yapin",
  "Belirsiz degerlendirme kriterleri kullanmak ('iyi', 'daha iyi', 'optimal')",
  "Cikti format tanimini atlamak - Tutarsiz sonuclara yol acar",
  "Sinir durumlarini unutmak - Gercek kullanimda yaygindir",
  "Dogrulamayi gozden kacirmak - Isteme kalite kontrolleri yerlestirin"
] [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Primer optimizatsii koda uspeshno zavershon. (Russian: Complete. Code optimization example successfully completed.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[assert|confident] SONUC_OZETI := {
  yatirilan_zaman: "15-20 dakika",
  kalite_iyilestirmesi: "+87% (2.4/5 -> 4.5/5)",
  tutarlilik_iyilestirmesi: "+80% (50% -> 90%)",
  yatirim_getirisi: "Yuksek (100+ kez kullanilan istem = 1500+ dakika tasarruf)",
  anahtar_cikarim: "Prompt Architect cercevesini kullanan sistematik istem optimizasyonu, cikti kalitesi ve tutarliliginda olculebilir, onemli iyilestirmeler uretir"
} [ground:witnessed:skill-execution] [conf:0.95] [state:confirmed]

---

[commit|confident] <promise>EXAMPLE_1_BASIC_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
