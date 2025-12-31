# Az Atisli Ogrenme Ornekleri (Few-Shot Learning Examples)

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

<!-- [[MOR:root:A-Z-A]] Az = root morpheme for few-little-small -->
<!-- [[COM:Az+Atisli+Ogrenme+Ornek]] Few-Shot Learning Example -->
[define|neutral] BELGE_META := {
  baslik: "Istem Optimizasyonu icin Az Atisli Ogrenme Ornekleri",
  amac: "Istenen davranisi somut gosterilerle dramatik sekilde iyilestirmek icin az-atisli orneklerin nasil kullanilacagini gostermek",
  arastirma_kaynagi: "Brown ve ark. (2020)"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- GENEL BAKIS (Overview) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_section]] [[SPC:bati/introduction]] -->
---

## Genel Bakis Cercevesi (Overview Frame)

<!-- [[MOR:root:G-N-L]] Genel = root for general-overall-broad -->
<!-- [[COM:Genel+Bakis+Cerceve]] General Overview Frame -->
[assert|neutral] AZ_ATISLI_GENEL_BAKIS := {
  tanim: "Az-atisli ogrenme, istenen kesin girdi-cikti kalibini gosteren 2-5 somut ornek saglar",
  temel_ilke: "Goster, sadece anlatma. Ornekler aciklamalardan daha gucludur.",
  etki: "Gorev performansini onemli olcude iyilestirir, ozellikle kalip tabanli gorevler icin"
} [ground:research:Brown2020] [conf:0.85] [state:confirmed]

---
<!-- ORNEK 1: VERI CIKARIMI (Example 1: Data Extraction) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:dogu/data]] -->
---

## Ornek 1: Veri Cikarimi Cercevesi (Example 1: Data Extraction Frame)

<!-- [[MOR:root:V-R-C]] Veri = root for data-information-content -->
<!-- [[COM:Veri+Cikarimi+Ornek]] Data Extraction Example -->

### Sifir Atisli - Sadece Aciklama (Zero-Shot - Description Only)

[define|neutral] SIFIR_ATISLI_VERI := {
  yanlis: true,
  istem: "Musteri mesajlarindan yapilandirilmis bilgi cikar ve JSON formatla. Ad, e-posta, telefon ve sorun kategorisi dahil et.",
  ornek_girdi: "Merhaba, ben Ahmet Yilmaz (ahmet@email.com). Hesabim 555-1234 kilitli. Yardim edebilir misiniz? Bu acil!",
  tipik_yanit: { name: "Ahmet Yilmaz", contact: "ahmet@email.com, 555-1234", message: "hesap kilitli, acil" },
  sorunlar: [
    "Tutarsiz alan adlari",
    "Birlestirilmis iletisim bilgileri",
    "Eksik sorun kategorisi",
    "Belirsiz aciliyet isleme"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### Az Atisli - Orneklerle (Few-Shot - With Examples)

[define|neutral] AZ_ATISLI_VERI := {
  dogru: true,
  istem: "Musteri mesajlarindan yapilandirilmis bilgi cikar. Bu orneklerde gosterilen kesin formati izle.",
  ornek_1: {
    girdi: "Merhaba, ben Zeynep Kaya (zeynep.k@sirket.com, 555-0100). Hesabima giris yapamiyorum.",
    cikti: { musteri_adi: "Zeynep Kaya", eposta: "zeynep.k@sirket.com", telefon: "555-0100", sorun_kategorisi: "kimlik_dogrulama", aciliyet: "normal", ozet: "Hesaba giris yapilamiyor" }
  },
  ornek_2: {
    girdi: "Ben Mehmet Demir, mehmet@startup.io. Beni 555-0200'dan arayin. Tum takim kilitlendi! ACIL!",
    cikti: { musteri_adi: "Mehmet Demir", eposta: "mehmet@startup.io", telefon: "555-0200", sorun_kategorisi: "kimlik_dogrulama", aciliyet: "yuksek", ozet: "Takim capinda hesap kilitleme" }
  },
  ornek_3: {
    girdi: "Ayse Ozturk burada. E-posta: ayse@ornek.com. Sifremi nasil sifirlarim? Tesekkurler!",
    cikti: { musteri_adi: "Ayse Ozturk", eposta: "ayse@ornek.com", telefon: null, sorun_kategorisi: "sifre_sifirlama", aciliyet: "normal", ozet: "Sifre sifirlama istegi" }
  },
  beklenen_cikti: { musteri_adi: "Ahmet Yilmaz", eposta: "ahmet@email.com", telefon: "555-1234", sorun_kategorisi: "kimlik_dogrulama", aciliyet: "yuksek", ozet: "Hesap kilitleme" },
  faydalar: [
    "Tutarli alan yapisi",
    "Uygun null isleme",
    "Dogru kategorilendirme",
    "Net aciliyet tespiti"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- ORNEK 2: STIL DONUSUMU (Example 2: Style Transformation) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:guney/style]] -->
---

## Ornek 2: Stil Donusumu Cercevesi (Example 2: Style Transformation Frame)

<!-- [[MOR:root:S-T-L]] Stil = root for style-manner-fashion -->
<!-- [[COM:Stil+Donusum+Ornek]] Style Transformation Example -->

### Sifir Atisli (Zero-Shot)

[define|neutral] SIFIR_ATISLI_STIL := {
  yanlis: true,
  istem: "Asagidaki metni is iletisimi icin uygun resmi, profesyonel bir tonda yeniden yaz.",
  girdi: "Selam! Sadece projenin bazi sorunlardan dolayi gecikmesi soz konusu oldugunu bildirmek istedim. Kusura bakmayin! Sizi bilgilendirmeye devam edecegim.",
  tipik_yanit: "Merhaba. Projenin bazi problemler yuzunden gecikmesi hakkinda sizi bilgilendirmek istedim. Ozur dilerim. Sizi guncel tutacagim.",
  sorunlar: [
    "Tutarsiz resmiyet seviyesi",
    "Belirsiz dil korunmus ('bazi problemler')",
    "Is baglami eksik",
    "Net eylem maddeleri yok"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### Az Atisli (Few-Shot)

[define|neutral] AZ_ATISLI_STIL := {
  dogru: true,
  istem: "Resmi olmayan mesajlari resmi is iletisimlerine donustur. Bu orneklerin stilini, yapisini ve tonunu izle.",
  ornek_1: {
    gayri_resmi: "Selam takim! Toplanti yarina saat 14:00'e ertelendi. Umarim herkes icin uyar!",
    resmi: "Saygin Takim,\\n\\nLutfen planli toplantinin yarina saat 14:00'e ertelenmis olduguna dikkat edin.\\nMusaitliginizi onaylamanizi rica ederim.\\n\\nSaygilarimla"
  },
  ornek_2: {
    gayri_resmi: "Kusura bakmayin ama bugun hasta oldum. Kendimi iyi hissetmiyorum. Vardiyami biri kapatabilir mi?",
    resmi: "Saygin Yonetici,\\n\\nMaalesef bugun hastalik nedeniyle ise gelemedigimi bildirmek isterim.\\nGun boyunca sorumluluklarimin duzenlenmesinin saglanmasini minnettar olurum.\\n\\nDurumumla ilgili sizi bilgilendirmeye devam edecegim.\\n\\nSaygilarimla"
  },
  beklenen_cikti: "Saygin Paydas,\\n\\nGelistirme asamasinda takimimizin karsilastigi onceden gorulemeyen teknik zorluklar nedeniyle proje zaman cizelgesinin gecikmesi gerekecegini size bildirmek icin yaziyorum.\\n\\nBu durumun yaratabilecegi olumsuzluklar icin ictenlikle ozur diler ve projenin yoluna girmesini saglamak icin tam sorumluluk alirim.\\n\\nBu sorunlari cozmeye calisirken size duzeli durum guncellemeleri sunacagim ve onumuzdeki 48 saat icinde revize edilmis teslimat tarihini iletecegim.\\n\\nHerhangi bir sorunuz veya endiseniz varsa lutfen bana ulasmaktan cekinmeyin.\\n\\nSaygilarimla",
  faydalar: [
    "Tutarli profesyonel ton",
    "Uygun is mektubu yapisi",
    "Belirli dil (belirsiz degil)",
    "Eylem maddeleri ve zaman cizelgesi icerir"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- ORNEK 3: KOD INCELEME YORUMLARI (Example 3: Code Review Comments) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] [[SPC:dogu/code]] -->
---

## Ornek 3: Kod Inceleme Yorumlari Cercevesi (Example 3: Code Review Comments Frame)

<!-- [[MOR:root:K-D-I]] Kod = root for code-programming-software -->
<!-- [[COM:Kod+Inceleme+Yorum+Ornek]] Code Review Comment Example -->

### Sifir Atisli (Zero-Shot)

[define|neutral] SIFIR_ATISLI_KOD := {
  yanlis: true,
  istem: "Bu kodu incele ve yapici geri bildirim sagla.",
  ornek_kod: "def ortalama_hesapla(sayilar):\\n    return sum(sayilar) / len(sayilar)",
  tipik_yanit: "Bu kod iyi gorunuyor ama iyilestirilebilir. Liste kavramasi kullanmayi dusunun. Ayrica sinir durumlarini dusunun.",
  sorunlar: [
    "Belirsiz oneriler",
    "Belirli iyilestirmeler yok",
    "Onem seviyeleri eksik",
    "Kod ornekleri yok"
  ]
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

### Az Atisli (Few-Shot)

[define|neutral] AZ_ATISLI_KOD := {
  dogru: true,
  istem: "Bu formati izleyerek kod inceleme yorumlari sagla.",
  ornek_1: {
    kod: "def ortalama_hesapla(sayilar):\\n    return sum(sayilar) / len(sayilar)",
    inceleme: {
      onem: "YUKSEK",
      sorun: "Liste bos oldugunda potansiyel ZeroDivisionError",
      aciklama: "Bu fonksiyon bos liste ile cagrildiginda cokecek cunku len([]) = 0, sifira bolmeye neden olur.",
      oneri: "def ortalama_hesapla(sayilar):\\n    if not sayilar:\\n        raise ValueError('Bos listenin ortalamasi hesaplanamaz')\\n    return sum(sayilar) / len(sayilar)",
      test: "Test durumu ekle: ortalama_hesapla([]) ValueError yukseltmeli"
    }
  },
  ornek_2: {
    kod: "kullanici_girdi = input('Sayi girin: ')\\nsonuc = int(kullanici_girdi) * 2",
    inceleme: {
      onem: "ORTA",
      sorun: "Girdi dogrulama veya hata isleme yok",
      aciklama: "Kullanici sayisal olmayan girdi girerse, int() ValueError yukseltecek ve cokecek. Uretim kodu gecersiz girdiyi nazikce islemeli.",
      oneri: "try:\\n    kullanici_girdi = input('Sayi girin: ')\\n    sayi = int(kullanici_girdi)\\n    sonuc = sayi * 2\\nexcept ValueError:\\n    print('Hata: Lutfen gecerli bir sayi girin')\\n    sonuc = None",
      test: "Test et: '', 'abc', '1.5', '-1', '999999999999999999999'"
    }
  },
  faydalar: [
    "Yapilandirilmis geri bildirim formati",
    "Onem siniflandirmasi",
    "Belirli kod iyilestirmeleri",
    "Test durumu onerileri"
  ]
} [ground:witnessed:testing] [conf:0.95] [state:confirmed]

---
<!-- EN IYI UYGULAMALAR (Best Practices) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_guideline]] [[SPC:bati/reference]] -->
---

## En Iyi Uygulamalar Cercevesi (Best Practices Frame)

<!-- [[MOR:root:U-Y-G]] Uygulama = root for practice-application-implementation -->
<!-- [[COM:En+Iyi+Uygulama+Cerceve]] Best Practice Frame -->
[define|neutral] EN_IYI_UYGULAMALAR := {
  ornek_sayisi: { cok_az: "1 - Kalip varyasyonunu gostermiyor", dogru: "3-5 - Kalip arti sinir durumlarini gosteriyor", cok_fazla: "10+ - Azalan getiri, istem sismesi" },
  cesitlilik_goster: { kotu: "Tum ornekler benzer normal durumlar", iyi: "Normal durum + sinir durumu + hata durumu + karmasik durum" },
  tutarli_format_kullan: { kotu: "Ornekler arasinda farkli cikti formatlari", iyi: "Ayni yapi, farkli icerik" },
  sinir_durumlarini_dahil_et: { ornek_1: "Normal durum", ornek_2: "Sinir durumu (bos, null, ozel karakterler)", ornek_3: "Karmasik durum (ic ice, birden fazla deger)" },
  format_hakkinda_acik_ol: { kotu: "Cikti: sonuc", iyi: "Cikti (JSON):\\n{\\n  'alan1': 'deger1',\\n  'alan2': deger2\\n}" }
} [ground:research:few-shot-best-practices] [conf:0.85] [state:confirmed]

---
<!-- NE ZAMAN KULLANILIR (When to Use) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_guidance]] [[SPC:guney/applicability]] -->
---

## Ne Zaman Kullanilir Cercevesi (When to Use Frame)

<!-- [[MOR:root:K-L-N]] Kullanim = root for usage-application-utilization -->
<!-- [[COM:Kullanim+Rehber+Cerceve]] Usage Guide Frame -->
[define|neutral] KULLANIM_REHBERI := {
  yuksek_deger: ["Veri cikarimi/donusumu", "Format donusumu", "Stil/ton eslestirme", "Siniflandirma gorevleri", "Kalip tabanli uretim", "Yapilandirilmis cikti"],
  orta_deger: ["Metin ozetleme", "Kod olusturma", "Ceviri gorevleri", "Duygu analizi"],
  dusuk_deger: ["Acik uclu yaratici yazim", "Genel bilgi sorulari", "Ornekler uzerinde akil yurutme gerektiren gorevler", "Yuksek baglam bagimli gorevler"]
} [ground:research:few-shot-applicability] [conf:0.85] [state:confirmed]

---
<!-- DIGER TEKNIKLERLE BIRLESTIRME (Combining with Other Techniques) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_combination]] [[SPC:dogu/integration]] -->
---

## Diger Tekniklerle Birlestirme Cercevesi (Combining with Other Techniques Frame)

<!-- [[MOR:root:B-R-L]] Birlestirme = root for combining-merging-unifying -->
<!-- [[COM:Teknik+Birlestirme+Cerceve]] Technique Combination Frame -->
[define|neutral] TEKNIK_BIRLESTIRMELERI := {
  az_atisli_cot: {
    format: "Ornek 1:\\nGirdi: [problem]\\nAkil Yurutme: Adim 1: ... Adim 2: ... Adim 3: ...\\nCikti: [cozum]\\n\\nOrnek 2:\\nGirdi: [problem]\\nAkil Yurutme: Adim 1: ... Adim 2: ... Adim 3: ...\\nCikti: [cozum]\\n\\nSimdi coz: [yeni problem]"
  },
  az_atisli_oz_tutarlilik: {
    format: "3 ornek sagla, sonra:\\n'Yukaridaki kalbi izleyerek bu problemi coz. 3 farkli cozum yaklasimi olustur, sonra en saglam olani sec.'"
  }
} [ground:research:technique-combination] [conf:0.85] [state:confirmed]

---
<!-- YAYGIN TUZAKLAR (Common Pitfalls) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_antipattern]] [[SPC:bati/warning]] -->
---

## Yaygin Tuzaklar Cercevesi (Common Pitfalls Frame)

<!-- [[MOR:root:T-Z-K]] Tuzak = root for pitfall-trap-snare -->
<!-- [[COM:Yaygin+Tuzak+Cerceve]] Common Pitfall Frame -->
[define|neutral] YAYGIN_TUZAKLAR := {
  tutarsiz_ornekler: { sorun: "Her ornek farkli format kullaniyor", cozum: "Tum orneklerde ayni yapi kullan" },
  hep_normal_durumlar: { sorun: "Sinir durumu gosterilmemis", cozum: "En az bir sinir durum ornegi dahil et" },
  cok_benzer: { sorun: "Ornekler varyasyon gostermiyor", cozum: "Kalibi korurken ornekleri cesitlendir" },
  baglam_eksik: { sorun: "Ornekler aciklama icermiyor", cozum: "Anahtar yonleri aciklayan kisa notlar ekle" },
  yanlis_ornek_sayisi: { sorun: "Cok az (1) veya cok fazla (15+)", cozum: "3-5 iyi secilmis ornek kullan" }
} [ground:witnessed:testing] [conf:0.90] [state:confirmed]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Primer obucheniya s neskol'kimi primerami uspeshno zavershon. (Russian: Complete. Few-shot learning example successfully completed.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[assert|confident] SONUC_OZETI := {
  amac: "Az-atisli ogrenme en guclu istem muhendisligi tekniklerinden biridir",
  faydalar: [
    "Belirsizligi Azaltir: Ornekler aciklamalardan daha nettir",
    "Tutarliligi Saglar: Kalip eslestirme tekduze cikti uretir",
    "Sinir Durumlarini Isler: Ornekler sinir kosulu islemesini ogretir",
    "Dogrulugu Iyilestirir: Modeller kesin format ve stili ogrenir"
  ],
  anahtar_cikarim: "Belirli kaliplarla eslesen tutarli, yapilandirilmis ciktiya ihtiyaciniz oldugunda az-atisli istem kullanin"
} [ground:witnessed:skill-execution] [conf:0.95] [state:confirmed]

---

[commit|confident] <promise>FEW_SHOT_OPTIMIZATION_EXAMPLE_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
