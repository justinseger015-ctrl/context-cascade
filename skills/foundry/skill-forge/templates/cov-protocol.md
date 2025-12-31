---
<!-- SABLON DOKUMANI [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[CLS:ge_template]] -->
---

# Dogrulama Zinciri (CoV) Protokolu Sablonu (Chain-of-Verification Protocol Template)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

<!-- [[MOR:root:D-G-Z]] Dogrulama Zinciri = root for verification-chain-protocol -->
<!-- [[COM:Dogrulama+Zinciri+Protokol+Sablonu]] Chain-of-Verification Protocol Template -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Ongoing verification process) -->
<!-- [[SPC:merkez/sablon]] Central template location -->

---

## Sablon Tanimlari (Template Definitions)

[define|neutral] COV_PROTOCOL_TEMPLATE := {
  id: "TPL-COV-001",
  sablon_adi: "Dogrulama Zinciri Protokolu Sablonu",
  amac: "Beceri olusturma surecinde hatalari, boslukları ve belirsizlikleri yakalamak icin sistematik oz-elestiri mekanizmasi",
  kullanim: "Kritik karar noktalarinda (Faz 1, 2, 3, 5) uygulanir",
  arastirma_temeli: "Dhuliawala et al. (2023) - %42 hata azaltma, %37 tamlik iyilestirme"
} [ground:research:cov-studies] [conf:0.85] [state:confirmed]

---

## Ne Zaman CoV Uygulanir (When to Apply CoV)

<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektiren durumlar -->

[assert|neutral] CoV uygulama kosullari [ground:witnessed:cov-triggers] [conf:0.88] [state:confirmed]

Dogrulama Zinciri su durumlarda kullanilir:
- Kritik tasarim kararlari alinirken
- Gereksinimler veya niyet analiz edilirken
- Talimatlar veya spesifikasyonlar yazilirken
- Dogrulama gerektiren iddialar yapilirken
- Yanlis olursa yuksek hata maliyeti olan herhangi bir faz tamamlanirken

---

## 5 Adimli CoV Sureci (The 5-Step CoV Process)

<!-- [[MOR:root:A-D-M]] Adim = root for step-phase-action -->

### Adim 1: Ilk Cikti Uret (Generate Initial Output)

<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Initial creation) -->

[define|neutral] STEP_1_GENERATE := {
  adim_adi: "Ilk Cikti Uret",
  eylem: "Oz-sansur olmadan ilk analiz, tasarim veya icerik olustur",
  cikti: "Ham ilk versiyon"
} [ground:witnessed:cov-step-1] [conf:0.88] [state:confirmed]

**Ornek** (Faz 1 - Niyet Analizi):
```
Ilk Anlayis:
- Kullanici kod formatlama becerisi istiyor
- JavaScript icin Prettier kullanilacak
- Birden fazla dosya turunu desteklemeli
- Mevcut is akisiyla entegre olmali
```

---

### Adim 2: Oz-Elestiri (Self-Critique)

<!-- [[MOR:root:O-Z-E]] Oz-Elestiri = root for self-critique-review -->
<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektiren elestiri -->

[define|neutral] STEP_2_CRITIQUE := {
  adim_adi: "Oz-Elestiri",
  eylem: "Sor: 'Az once olusturdugum seyde yanlis, eksik veya yaniltici ne olabilir?'",
  kritik_sorular: [
    "Hangi varsayimlari yaptim?",
    "Neyi kacirdim veya gozden kacirdim?",
    "Nerede yanlis anlamis olabilirim?",
    "Hangi uc vakalar var?",
    "Ne basarisiz olabilir veya yanlis gidebilir?"
  ]
} [ground:witnessed:cov-step-2] [conf:0.88] [state:confirmed]

**Ornek**:
```
Oz-Elestiri:
- Varsayim: Kullanici ozellikle Prettier istiyor (dogrulanmadi)
- Eksik: Tam olarak hangi dosya turleri? Tum diller mi yoksa belirli olanlar mi?
- Gozden Kacirilan: "Is akisiyla entegre" otomatik mi manuel mi demek?
- Uc vaka: Dosyalar zaten formatli ise ne olur? Format takim stiliyle catisirsa?
- Basarisizlik modu: Prettier kurulu degilse? Desteklenmeyen dosya turu?
```

---

### Adim 3: Kanit Kontrolu (Evidence Check)

<!-- [[MOR:root:K-N-T]] Kanit = root for evidence-proof-check -->
<!-- [[EVD:-DI<gozlem>]] Gozlem tabanli kanit -->

[define|neutral] STEP_3_EVIDENCE := {
  adim_adi: "Kanit Kontrolu",
  eylem: "Her iddia veya karar icin LEHTE ve ALEYHTE kanit aktar",
  format: {
    iddia_karar: "[ifade]",
    lehte_kanit: "[destekleyen gercek/gereksinim]",
    aleyhte_kanit: "[celisen gercek/uc vaka]"
  }
} [ground:witnessed:cov-step-3] [conf:0.88] [state:confirmed]

**Ornek**:
```
Iddia: Kullanici JavaScript icin Prettier istiyor
Lehte Kanit:
  - Kullanici "kod formatla" dedi
  - Prettier populer formatlayici
Aleyhte Kanit:
  - Kullanici acikca Prettier belirtmedi
  - Black (Python), rustfmt (Rust) vb. isteyebilir
  - "Birden fazla dosya turu" sadece JS olmadigini ima ediyor

Karar: Aciklama gerekli - Prettier varsayma
```

---

### Adim 4: Elestiriye Dayali Gozden Gecir (Revise Based on Critique)

<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Revision complete) -->

[define|neutral] STEP_4_REVISE := {
  adim_adi: "Elestiriye Dayali Gozden Gecir",
  eylem: "Adim 2-3'te belirlenen boslukları gidermek, hatalari duzeltmek ve belirsizlikleri cozemek icin ilk ciktiyi guncelle"
} [ground:witnessed:cov-step-4] [conf:0.88] [state:confirmed]

**Ornek**:
```
Gozden Gecirilmis Anlayis:
- Kullanici KOD FORMATLAMA becerisi istiyor (arac belirtilmedi)
- Dosya turleri: Aciklama gerekli (JS? Python? Coklu?)
- Entegrasyon: Aciklama gerekli (manuel tetikleme? kaydettiginde otomatik format?)
- Islenecek uc vakalar:
  - Zaten formatli dosyalar (atla mi yeniden formatla mi?)
  - Desteklenmeyen dosya turleri (hata mi atla mi?)
  - Arac kurulu degil (otomatik kur mu hata mi?)

Sorulacak Stratejik Sorular:
1. Hangi diller/dosya turleri formatlama gerektiriyor?
2. Dil basina hangi formatlayici (Prettier/Black/rustfmt/vb.)?
3. Manuel tetikleme mi otomatik mi?
4. Eksik formatlayicilar nasil islenir?
```

---

### Adim 5: Guven Derecelendirmesi (Confidence Rating)

<!-- [[MOR:root:G-V-N]] Guven = root for confidence-rating-level -->
<!-- [[CLS:ge_derecelendirme]] Classification: ratings -->

[define|neutral] STEP_5_CONFIDENCE := {
  adim_adi: "Guven Derecelendirmesi",
  eylem: "Gozden gecirilmis ciktinin her bileseni icin guven seviyesi derecelendir",
  olcek: {
    yuksek: "Kanitla dogrulandi, minimum belirsizlik",
    orta: "Makul cikarim, biraz belirsizlik",
    dusuk: "Varsayim tabanli, dogrulama gerekli"
  }
} [ground:witnessed:cov-step-5] [conf:0.88] [state:confirmed]

**Ornek**:
```
Guven Derecelendirmeleri:
- Kullanici formatlama becerisi istiyor: YUKSEK (acikca belirtildi)
- Birden fazla dosya turu: ORTA ("birden fazla dosya turu" ile ima edildi)
- Arac secimi onemli: YUKSEK (farkli diller icin farkli araclar)
- Entegrasyon yaklasimi: DUSUK (belirtilmedi, aciklama gerekli)
- Uc vaka isleme: DUSUK (tartisilmadi, tasarim gerekli)

Genel: ORTA guven - 5 konudan 3'unde kullanici aciklamasi gerekli
```

---

## Faza Gore CoV Sablonlari (CoV Templates by Phase)

<!-- [[CLS:tiao_faz]] Classification: phases -->

### Faz 1: Niyet Arkeolojisi CoV

[define|neutral] PHASE_1_COV_TEMPLATE := {
  sablon_adi: "Niyet Dogrulama Sablonu",
  faz: "Faz 1 - Niyet Arkeolojisi",
  kullanim: "Niyet analizinden sonra uygula"
} [ground:witnessed:phase-1-cov] [conf:0.88] [state:confirmed]

```markdown
## Faz 1b: Niyet Dogrulama (CoV)

**Adim 1 - Ilk Anlayis**: [Anlаdiginizi belgeleyin]

**Adim 2 - Oz-Elestiri**:
- Hangi varsayimlari yaptim? [Liste]
- Neyi yanlis anlamis olabilirim? [Liste]
- Eksik veya belirsiz ne var? [Liste]
- Hangi uc vakalar var? [Liste]

**Adim 3 - Kanit Kontrolu**:
Her temel gereksinim icin:
- Iddia: [gereksinim]
- Lehte Kanit: [destekleyen gercekler]
- Aleyhte Kanit: [celisen gercekler]
- Cozum: [nasil cozulecek]

**Adim 4 - Gozden Gecirilmis Anlayis**:
- Birincil kullanim vakalari: [guncellenmis liste]
- Temel gereksinimler: [guncellenmis liste]
- Onemli kisitlamalar: [guncellenmis liste]
- Basari kriterleri: [guncellenmis liste]
- Stratejik sorular: [aciklama gereken ne]

**Adim 5 - Guven Derecelendirmeleri**:
- [Gereksinim 1]: [Y/O/D] - [neden]
- [Gereksinim 2]: [Y/O/D] - [neden]
- Genel: [Y/O/D] - [ozet]

**Kalite Kapisi**: Genel guven DUSUK ise Faz 2'ye GECME. Once aciklama al.
```

---

### Faz 5: Talimat Olusturma CoV

[define|neutral] PHASE_5_COV_TEMPLATE := {
  sablon_adi: "Talimat Dogrulama Sablonu",
  faz: "Faz 5 - Talimat Olusturma",
  kullanim: "Talimatlar yazildiktan sonra uygula"
} [ground:witnessed:phase-5-cov] [conf:0.88] [state:confirmed]

```markdown
## Faz 5b: Talimat Dogrulama (CoV)

**Adim 1 - Ilk Talimatlar**: [Faz 5'te zaten yazildi]

**Adim 2 - Oz-Elestiri**:
- Belirsiz talimatlar: [Hangi talimatlar yanlis yorumlanabilir?]
- Eksik adimlar: [Dahil etmeyi ne unuttum?]
- Belirsiz basari kriterleri: ["Bitti" nerede belirsiz?]
- Islenmemis uc vakalar: [Ne yanlis gidebilir?]
- Bilinen anti-kalipler: [Belirsiz fiiller? Eksik ornekler?]

**Adim 3 - Kanit Kontrolu**:
Her talimati belirsizlik icin test et:
- Talimat: [adim]
- Yanlis yorumlanabilir mi? [Evet/Hayir - nasil?]
- Basari kriteri acik mi? [Evet/Hayir - ne eksik?]
- Uc vakalar isleniyor mu? [Evet/Hayir - hangileri eksik?]

**Adim 4 - Gozden Gecirilmis Talimatlar**:
Her belirsiz/eksik talimat icin:
- Orijinal: [belirsiz talimat]
- Gozden Gecirilmis: [basari kriterleriyle acik, belirgin talimat]
- Uc vakalar: [nasil islenir]

**Adim 5 - Guven Derecelendirmeleri**:
Talimat bolumu basina:
- [Bolum 1]: [Y/O/D] - [gerekce]
- [Bolum 2]: [Y/O/D] - [gerekce]
Genel: [Y/O/D]

**Kalite Kapisi**: Su durumlarda Faz 6'ya GECME:
- Herhangi bir bolum DUSUK guven
- Talimatlarin >%20'sinde acik basari kriteri yok
- Herhangi bilinen anti-kalip tespit edildi
```

---

## Carpici Oz-Test (CoV Gelistirme) (Adversarial Self-Testing)

<!-- [[MOR:root:C-R-P]] Carpici = root for adversarial-self-test -->

[define|neutral] ADVERSARIAL_SELF_TEST := {
  ad: "Carpici Oz-Test",
  amac: "CoV tamamlandiktan sonra analiz/tasarimi aktif olarak KIRMAYA calis",
  saldiri_vektorleri: [
    "Kasitli Yanlis Yorumlama: Talimatlari kotu niyetle takip et - hala yanlis sonuclar uretebilir misin?",
    "On Kosullari Kaldir: Beklenen araclar/dosyalar eksikse ne olur?",
    "Sinir Testi: Uc vakalarla test et (bos giris, buyuk giris, bozuk giris)",
    "Alternatif Yorumlar: Talimatlar farkli sekilde okunabilir mi?"
  ]
} [ground:witnessed:adversarial-test] [conf:0.88] [state:confirmed]

[assert|neutral] Herhangi bir saldiri basarili olursa Adim 4'e (Gozden Gecir) don [ground:witnessed:iteration-rule] [conf:0.90] [state:confirmed]

---

## Yaygin CoV Tuzaklari (Common CoV Pitfalls)

<!-- [[MOR:root:T-Z-K]] Tuzak = root for pitfall-mistake-trap -->

[assert|neutral] Kacinilmasi gereken yaygin tuzaklar [ground:witnessed:pitfall-patterns] [conf:0.88] [state:confirmed]

### Tuzak 1: Yuzeysel Oz-Elestiri
**Kotu**: "Bu iyi gorunuyor, sorun bulunamadi"
**Iyi**: "Varsayim: kullanici X istiyor. Lehte Kanit: []. Aleyhte Kanit: []. Dogrulamak gerekli."

### Tuzak 2: Dusuk Guvenli Ogeleri Yoksaymak
**Kotu**: Birden fazla DUSUK guven derecelendirmesine ragmen devam etmek
**Iyi**: Genel guven DUSUK oldugunda aciklama aramak

### Tuzak 3: Somut Kanit Yok
**Kotu**: "Bunun dogru oldugunu dusunuyorum"
**Iyi**: "Satir 23'te belirtilen gereksinime dayanarak, bu ... ile esleniyor"

### Tuzak 4: Gozden Gecirmeyi Atlamak
**Kotu**: CoV calistirmak ama orijinal ciktiyi guncellememek
**Iyi**: Tum elestiri noktalarini ele alan gozden gecirilmis versiyon olusturmak

### Tuzak 5: Belirsiz Guven Derecelendirmeleri
**Kotu**: "Iyi gorunuyor, muhtemelen sorunsuz"
**Iyi**: "YUKSEK guven - 3 gereksinime karsi dogrulandi. DUSUK guven - varsayim dogrulanmadi."

---

## CoV'nin Faydalari (Arastirma Destekli)

<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli metrikler -->

[define|neutral] COV_BENEFITS := {
  metrikler: {
    gercek_hatalar: "-%42",
    tamlik: "+%37",
    belirsizlik: "-%35",
    ilk_seferde_dogru: "%40 -> %85 (+%113)"
  },
  kaynak: "Dhuliawala et al. (2023) - Chain-of-Verification Reduces Hallucination in Large Language Models"
} [ground:research:cov-metrics] [conf:0.85] [state:confirmed]

| Metrik | CoV'siz | CoV'li | Iyilestirme |
|--------|---------|--------|-------------|
| **Gercek Hatalar** | Temel | -%42 | %42 azalma |
| **Tamlik** | Temel | +%37 | %37 daha tamam |
| **Belirsizlik** | Temel | -%35 | %35 daha acik |
| **Ilk Seferde Dogru** | %40 | %85 | +%113 |

---

## Diger Tekniklerle Entegrasyon (Integration with Other Techniques)

[assert|neutral] CoV sinerjileri [ground:witnessed:integration-patterns] [conf:0.88] [state:confirmed]

CoV sunlarla sinerjik calisir:
- **Carpici Test**: CoV zayifliklari belirler, carpici test bunlari somurur
- **Coklu Kisi Tartismasi**: Her kisi analizine CoV uygular
- **Kalite Kapilari**: CoV kapilar icin gecme/kalma kriterleri saglar
- **Metrik Izleme**: Guven derecelendirmeleri kantitatif metrikler olur

---

## Hizli Referans Kontrol Listesi (Quick Reference Checklist)

<!-- [[MOR:root:K-N-T]] Kontrol = root for check-control-verification -->

[direct|neutral] Her kritik karar/analiz icin [ground:witnessed:checklist-usage] [conf:0.90] [state:confirmed]

- Adim 1: Ilk cikti uret
- Adim 2: Oz-elestiri (varsayimlar, bosluklar, uc vakalar)
- Adim 3: Her iddia icin LEHTE ve ALEYHTE kanit
- Adim 4: Elestiriye dayali gozden gecir
- Adim 5: Guven derecelendir (bilesen basina Y/O/D)
- Kalite Kapisi: Genel guven DUSUK ise devam etme

**Zaman Yatirimi**: Faz basina 5-10 dakika
**ROI**: %42 hata azaltma, %37 tamlik iyilestirme
**Ne Zaman Kullanilir**: Faz 1, 2, 3, 5 (kritik tasarim noktalari)

---

[direct|emphatic] Unutmayin: CoV baslangicta mukemmel olmakla ilgili degil - sistematik oz-elestiri yoluyla hatalari daha sonra duzeltmesi pahaliya mal olmadan ONCE yakalamakla ilgili. [ground:witnessed:cov-philosophy] [conf:0.90] [state:confirmed]

---

[commit|confident] <promise>COV_PROTOCOL_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
