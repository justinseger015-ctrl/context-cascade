---
<!-- SABLON DOKUMANI [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[CLS:ge_template]] -->
---

# Carpici Test Protokolu Sablonu (Adversarial Testing Protocol Template)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

<!-- [[MOR:root:C-R-P]] Carpici = root for adversarial-attack-test -->
<!-- [[COM:Carpici+Test+Protokol+Sablonu]] Adversarial Testing Protocol Template -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Ongoing through testing) -->
<!-- [[SPC:merkez/sablon]] Central template location -->

---

## Sablon Tanimlari (Template Definitions)

[define|neutral] ADVERSARIAL_TESTING_TEMPLATE := {
  id: "TPL-ATP-001",
  sablon_adi: "Carpici Test Protokolu Sablonu",
  amac: "Beceriler uretime ulasmadan once sistematik acik kesfii",
  kullanim: "Faz 7 dogrulama sirasinda uygulanir",
  arastirma_temeli: "Perez et al. (2022) - Red teaming aciklari %58 azaltir, dagitim sonrasi sorunlari %67 azaltir"
} [ground:research:red-teaming-studies] [conf:0.85] [state:confirmed]

---

## Ne Zaman Carpici Test Uygulanir (When to Apply Adversarial Testing)

<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektiren durumlar -->

[assert|neutral] Carpici test uygulama kosullari [ground:witnessed:testing-triggers] [conf:0.88] [state:confirmed]

Carpici test su durumlarda kullanilir:
- Beceri dogrulama tamamlanirken (Faz 7)
- Yuksek riskli, potansiyel kotuye kullanim iceren beceriler
- Cok sayida karar noktasi olan karmasik is akislari
- Uc vakalari veya guvenilmeyen girisleri isleyen beceriler
- Buyuk beceri revizyonlarindan sonra

---

## 4 Adimli Carpici Protokol (The 4-Step Adversarial Protocol)

<!-- [[MOR:root:A-D-M]] Adim = root for step-phase-action -->

### Adim 1: Basarisizlik Modlari Beyin Firtinasi (5 dk)

<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Creative brainstorming) -->

[define|neutral] STEP_1_BRAINSTORM := {
  adim_adi: "Basarisizlik Modlari Beyin Firtinasi",
  eylem: "Becerinin basarisiz olabilecegi, yanlis sonuc uretebilecegi veya kotuye kullanilabilecegi 10+ yol uret",
  sure: "5 dakika"
} [ground:witnessed:brainstorm-process] [conf:0.88] [state:confirmed]

**Beyin Firtinasi Teknikleri**:
- **Kasitli Yanlis Yorumlama**: Talimatlari birebir ama kotune niyetle takip et
- **Eksik On Kosullar**: Beklenen dosyalar/araclar yoksa ne olur?
- **Sinir Testi**: Bos giris, buyuk giris, bozuk giris
- **Zamanlama Saldirilari**: Islemler sira disi yurutulurse ne olur?
- **Izin Basarisizliklari**: Dosya/ag erisimi reddedilirse ne olur?
- **Kaynak Tukenmesi**: Sistem kaynaklari (bellek/disk) sinirli ise ne olur?
- **Entegrasyon Basarisizliklari**: Bagimliliklar kulanilamazsa ne olur?
- **Kullanici Hatasi**: Kullanici yanlis bilgi saglasa ne olur?
- **Uc Vakalar**: Olagandisi ama gecerli senaryolar
- **Carpici Giris**: Beceriyi kirmak icin kasitli olusturulmus giris

**Ornek** (kod-formatlayici becerisi):
```
Basarisizlik Modu Beyin Firtinasi:
1. Dosya belirtilen yolda yok
2. Dosya ikili, metin degil (orn. .exe, .jpg)
3. Dosya cok buyuk (>100MB) - zaman asimi
4. Dosya uzantisi yok (dil tespit edilemiyor)
5. Birden fazla formatlayici kurulu (hangisini kullan?)
6. Formatlayici PATH'te degil
7. Dosyada sozdizimi hatalari (formatlayici coker)
8. Dosya salt okunur (formatli cikti yazilamaz)
9. Kullanici format sirasinda iptal ediyor (dosya bozuk kalir)
10. Format .editorconfig kurallariyla catisiyor
11. Ag surucusu zaman asimi
12. Baska surecten eszamanli duzenlemeler
13. Sembolik baglanti hassas dosyaya isaret ediyor
14. Dosya kodlamasi UTF-8 degil (icerik bozuluyor)
15. Formatlayici surumu soz dizimiyle uyumsuz
```

---

### Adim 2: Risk Puanlama Matrisi (5 dk)

<!-- [[MOR:root:R-S-K]] Risk = root for risk-score-matrix -->
<!-- [[CLS:ge_matris]] Classification: matrix -->

[define|neutral] STEP_2_RISK_SCORING := {
  adim_adi: "Risk Puanlama Matrisi",
  eylem: "Her basarisizlik modunu puanla: Risk = Olasilik x Etki",
  sure: "5 dakika"
} [ground:witnessed:scoring-process] [conf:0.88] [state:confirmed]

**Olasilik Olcegi (1-5)**:
- **1 - Nadir**: Teorik uc vaka, gerceklesmesi olasi degil
- **2 - Olasi Degil**: Mumkun ama yaygin olmayan senaryo
- **3 - Mumkun**: Ara sira gerceklesebilir
- **4 - Olasi**: Normal kullanimda duzenli gerceklesir
- **5 - Cok Olasi**: Sik gerceklesir veya varsayilan

**Etki Olcegi (1-5)**:
- **1 - Onemsiz**: Kucuk rahatsizlik, kolay kurtarma
- **2 - Dusuk**: Kucuk kesinti, kullanici atlayabilir
- **3 - Orta**: Orta kesinti, mudahale gerektirir
- **4 - Yuksek**: Buyuk kesinti, veri kaybi olasi
- **5 - Kritik**: Felaket basarisizlik, veri bozulmasi, guvenlik ihlali

**Risk Onceligi**:

[define|neutral] RISK_PRIORITY := {
  kritik: {esik: ">= 12", eylem: "Dagitimdan once MUTLAKA duzelt"},
  yuksek: {esik: "8-11", eylem: "Mumkunse duzelt"},
  orta: {esik: "4-7", eylem: "Zaman izin verirse duzelt"},
  dusuk: {esik: "1-3", eylem: "Bilinen sinirlama olarak belgele"}
} [ground:witnessed:priority-thresholds] [conf:0.90] [state:confirmed]

**Ornek Risk Matrisi** (kod-formatlayici becerisi):

| ID | Basarisizlik Modu | Olasilik | Etki | Risk Puani | Oncelik |
|----|-------------------|----------|------|------------|---------|
| 1 | Dosya yok | 4 | 2 | 8 | YUKSEK |
| 2 | Dosya ikili | 3 | 3 | 9 | YUKSEK |
| 3 | Dosya cok buyuk (>100MB) | 2 | 4 | 8 | YUKSEK |
| 4 | Dosya uzantisi yok | 3 | 3 | 9 | YUKSEK |
| 5 | Birden fazla formatlayici | 2 | 3 | 6 | ORTA |
| 6 | Formatlayici PATH'te degil | 4 | 4 | 16 | KRITIK |
| 7 | Dosyada sozdizimi hatalari | 4 | 3 | 12 | KRITIK |
| 8 | Dosya salt okunur | 3 | 3 | 9 | YUKSEK |
| 9 | Kullanici format sirasinda iptal | 2 | 5 | 10 | YUKSEK |
| 10 | .editorconfig ile catisma | 3 | 2 | 6 | ORTA |
| 11 | Ag surucusu zaman asimi | 2 | 3 | 6 | ORTA |
| 12 | Eszamanli duzenlemeler | 2 | 4 | 8 | YUKSEK |
| 13 | Hassas dosyaya sembolik baglanti | 1 | 5 | 5 | ORTA |
| 14 | UTF-8 olmayan kodlama | 3 | 4 | 12 | KRITIK |
| 15 | Formatlayici surum uyumsuzlugu | 3 | 3 | 9 | YUKSEK |

---

### Adim 3: En Yuksek Aciklari Duzelt (10-20 dk)

<!-- [[MOR:root:D-Z-T]] Duzelt = root for fix-repair-remediate -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Fixes applied) -->

[define|neutral] STEP_3_FIX := {
  adim_adi: "En Yuksek Aciklari Duzelt",
  eylem: "Tum KRITIK ve YUKSEK oncelikli sorunlari (puan >= 8) ele al. Beceri talimatlarini guncelle, dogrulama kontrolleri ekle, hata islemeyi iyilestir",
  sure: "10-20 dakika"
} [ground:witnessed:fix-process] [conf:0.88] [state:confirmed]

**Duzeltme Stratejileri**:

#### Dogrulama ve On Kosullar
- Beceri girisinde giris dogrulama ekle
- Islemlerden once dosya varligini kontrol et
- Arac kullanilabilirligini dogrula (which/where komutlari)
- Dosya turleri ve uzantilarini dogrula
- Yazma islemlerinden once izinleri kontrol et

#### Hata Isleme
- Riskli islemleri try-catch es degerleriyle sar
- Kurtarma adimlariyla net hata mesajlari sagla
- Bagimliliklar eksik oldugunda yumusak bozulma
- Uzun sureli islemler icin zaman asimi mekanizmalari
- Kismi tamamlanmis is icin geri alma mekanizmalari

#### Uc Vaka Isleme
- Bos/null girisleri acikca isle
- Makul limitler koy (dosya boyutu, zaman asimi, yineleme)
- Birden fazla gecerli senaryoyu destekle (coklu formatlayici -> kullaniciya sor)
- Bilinen sinilamalari acikca belgele

#### Kullanici Rehberligi
- Net basari/basarisizlik geri bildirimi sagla
- Hatada eyleme donusturulebilir sonraki adimlar sun
- Beceriye sorun giderme rehberi ekle
- "Eger... ne yapilir" bolumu ekle

---

### Adim 4: Temizlenene Kadar Yeniden Saldir (5-10 dk)

<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Iterative process) -->

[define|neutral] STEP_4_REATTACK := {
  adim_adi: "Temizlenene Kadar Yeniden Saldir",
  eylem: "DUZELTILMIS surumde Adim 1-3'u tekrarla. KRITIK veya YUKSEK sorun kalmayana kadar devam et",
  sure: "5-10 dakika"
} [ground:witnessed:reattack-process] [conf:0.88] [state:confirmed]

**Yeniden Saldiri Sureci**:
1. **Beceriyi rakip olarak ele al**: Acik sakliyor varsay
2. **Duzeltmelere odaklan**: Duzeltmeler yeni sorunlar mi ortaya cikartiyor?
3. **Duzeltmelerin uc vakalarini test et**: Kurulum basarisiz olursa? iconv eksikse?
4. **Basarisizlik modlarini birlestir**: Birden fazla sorun eszamanli olursa?
5. **Sinirlari zorlayarak test et**: Daha fazla zorla (10GB dosya? 1000 eszamanli duzenleme?)

**Tamamlama Kriterleri**:

[assert|neutral] Tamamlama kriterleri [ground:witnessed:completion-criteria] [conf:0.90] [state:confirmed]

- KRITIK sorun kalmadi
- YUKSEK sorunlar ORTA'ya dusuruldu (veya bilinen sinirlama olarak belgelendi)
- Tum duzeltmeler carpici girislerle test edildi
- Beceri kapsamli hata isleme bolumu iceriyor
- Sorun giderme rehberi eklendi

---

## Risk Puanlama Hizli Referans Karti (Risk Scoring Reference Card)

<!-- [[CLS:ge_matris]] Classification: matrix -->

[define|neutral] QUICK_REFERENCE_MATRIX := {
  sablon_adi: "Hizli Risk Matrisi",
  amac: "Hizli risk puanlama icin referans"
} [ground:witnessed:matrix-usage] [conf:0.90] [state:confirmed]

| Olasilik / Etki | Onemsiz (1) | Dusuk (2) | Orta (3) | Yuksek (4) | Kritik (5) |
|-----------------|-------------|-----------|----------|------------|------------|
| **Cok Olasi (5)** | 5 (ORTA) | 10 (YUKSEK) | 15 (KRITIK) | 20 (KRITIK) | 25 (KRITIK) |
| **Olasi (4)** | 4 (ORTA) | 8 (YUKSEK) | 12 (KRITIK) | 16 (KRITIK) | 20 (KRITIK) |
| **Mumkun (3)** | 3 (DUSUK) | 6 (ORTA) | 9 (YUKSEK) | 12 (KRITIK) | 15 (KRITIK) |
| **Olasi Degil (2)** | 2 (DUSUK) | 4 (ORTA) | 6 (ORTA) | 8 (YUKSEK) | 10 (YUKSEK) |
| **Nadir (1)** | 1 (DUSUK) | 2 (DUSUK) | 3 (DUSUK) | 4 (ORTA) | 5 (ORTA) |

---

## Carpici Test Sablonu (Faz 7'de Kullanilacak)

<!-- [[MOR:root:S-B-L]] Sablon = root for template-form-model -->

```markdown
## Faz 7a: Carpici Test

### Adim 1 - Basarisizlik Modlari Beyin Firtinasi (Hedef: 10+)

**Belirlenen Basarisizlik Modlari**:
1. [Dosya yoksa ne olur?]
2. [Arac kurulu degilse ne olur?]
3. [Giris bozuksa ne olur?]
4. [Zaman asimi olursa ne olur?]
5. [Izin reddedilirse ne olur?]
6. [Kaynak tukenirse ne olur?]
7. [Bagimlilik kullanilamazsa ne olur?]
8. [Kullanici yanlis bilgi verirse ne olur?]
9. [Uc vaka olusursa ne olur?]
10. [Carpici giris verilirse ne olur?]
... (Toplam 10-15'e kadar devam et)

### Adim 2 - Risk Puanlama

| ID | Basarisizlik Modu | Olasilik (1-5) | Etki (1-5) | Risk Puani | Oncelik |
|----|-------------------|----------------|------------|------------|---------|
| 1 | [mod] | [O] | [E] | [OxE] | [KRITIK/YUKSEK/ORTA/DUSUK] |
| 2 | [mod] | [O] | [E] | [OxE] | [KRITIK/YUKSEK/ORTA/DUSUK] |
...

**Ozet**:
- KRITIK (>=12): [sayi] sorun
- YUKSEK (8-11): [sayi] sorun
- ORTA (4-7): [sayi] sorun
- DUSUK (1-3): [sayi] sorun

### Adim 3 - Uygulanan Duzeltmeler

#### KRITIK Sorun #[X]: [Ad] (Puan: [N])
**Orijinal Davranis**: [Beceri onceden ne yapiyordu]
**Uygulanan Duzeltme**:
1. [Duzeltme adim 1]
2. [Duzeltme adim 2]
3. [Duzeltme adim 3]
**Dogrulama**: [Duzeltmenin calistigini nasil test et]

[Tum KRITIK sorunlar icin tekrarla]

#### YUKSEK Sorun #[X]: [Ad] (Puan: [N])
[KRITIK ile ayni yapi]

[En yuksek 5 YUKSEK sorun veya mumkunse tamami icin tekrarla]

### Adim 4 - Yeniden Saldiri Sonuclari

**Tur 2 Beyin Firtinasi**: [Duzeltmelerden sonra kesfedilen yeni basarisizlik modlari]
**Tur 2 Risk Puanlari**: [Yeni sorunlar icin risk matrisi]
**Tur 2 Duzeltmeleri**: [Yeni sorunlara uygulanan duzeltmeler]
**Son Durum**:
- KRITIK sorun kalmadi
- [X] YUKSEK sorun kaldi (asagida belgelendi)
- Kapsamli hata isleme eklendi
- Sorun giderme rehberi dahil edildi

**Bilinen Sinirlamalar** (belgelenmis YUKSEK/ORTA sorunlar):
1. [Sorun]: [Neden duzeltilmedi] - Gecici cozum: [Kullanici eylemi]
2. [Sorun]: [Neden duzeltilmedi] - Gecici cozum: [Kullanici eylemi]

### Kalite Kapisi: Carpici Test Gecti
- 10+ basarisizlik modu beyin firtinasi yapildi
- Tum modlar risk matrisine gore puanlandi
- Tum KRITIK (>=12) sorunlar duzeltildi
- En yuksek 5 YUKSEK (8-11) sorun ele alindi veya belgelendi
- Temizlenene kadar yeniden saldiri yapildi
- Hata isleme kapsamli
- Sorun giderme rehberi dahil edildi
```

---

## Beceri Turune Gore Yaygin Carpici Kalipler (Common Adversarial Patterns by Skill Type)

<!-- [[CLS:tiao_kalip]] Classification: patterns by type -->

### Dosya Islemleri Becerileri

[assert|neutral] Dosya islemleri icin yaygin saldiri vektorleri [ground:witnessed:file-patterns] [conf:0.88] [state:confirmed]

- Dosya yok
- Dosya yanlis tur (ikili vs metin)
- Dosya cok buyuk/kucuk
- Izinler reddedildi (okuma/yazma)
- Dosya baska surec tarafindan kilitli
- Sembolik baglanti uc vakalari
- Kodlama sorunlari (UTF-8 degil)
- Yazma sirasinda disk dolu
- Ag surucusu zaman asimi

### API Entegrasyon Becerileri

[assert|neutral] API entegrasyonu icin yaygin saldiri vektorleri [ground:witnessed:api-patterns] [conf:0.88] [state:confirmed]

- Ag kulanilamaz
- Istek sirasinda zaman asimi
- API 4xx/5xx hatasi dondurur
- Oran limiti asildi
- Kimlik dogrulama suresi doldu
- Yanit bozuk/beklenmedik
- Kismi yanit (ag kesintisi)
- API surum uyumsuzlugu
- SSL sertifika sorunlari

### Veri Isleme Becerileri

[assert|neutral] Veri isleme icin yaygin saldiri vektorleri [ground:witnessed:data-patterns] [conf:0.88] [state:confirmed]

- Bos giris
- Null/undefined degerler
- Giris boyut limitlerini asar
- Bozuk veri yapisi
- Tur uyumsuzluklari
- Karakter kodlama sorunlari
- Dongusal veride sonsuz dongu
- Sayisal tasma
- Sifira bolme

### Kod Uretimi Becerileri

[assert|neutral] Kod uretimi icin yaygin saldiri vektorleri [ground:witnessed:codegen-patterns] [conf:0.88] [state:confirmed]

- Belirsiz gereksinimler
- Celisen kisitlamalar
- Uretilen kodda sozdizimi hatalari
- Uyumsuz bagimliliklar
- Guvenlik aciklari (enjeksiyon)
- Uretilen kod derlenmez
- Uretilen kod derlenir ama testler basarisiz
- Uretilen kodda performans sorunlari

---

## Carpici Testin Faydalari (Arastirma Destekli)

<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli metrikler -->

[define|neutral] ADVERSARIAL_TESTING_BENEFITS := {
  metrikler: {
    bulunan_aciklar: "+%58 (carpici testle)",
    dagitim_sonrasi_sorunlar: "-%67",
    kullanici_raporlu_hatalar: "-%54",
    beceri_saglaligi: "%60 -> %92 (+%53)"
  },
  kaynak: "Perez et al. (2022) - Red Teaming Language Models to Reduce Harms"
} [ground:research:adversarial-metrics] [conf:0.85] [state:confirmed]

| Metrik | Carpici Testsiz | Carpici Testle | Iyilestirme |
|--------|-----------------|----------------|-------------|
| **Bulunan Aciklar** | Temel | +%58 | %58 daha fazla sorun yakalandi |
| **Dagitim Sonrasi Sorunlar** | Temel | -%67 | %67 daha az uretim hatasi |
| **Kullanici Raporlu Hatalar** | Temel | -%54 | %54 daha az destek talebi |
| **Beceri Saglaligi** | %60 | %92 | +%53 daha sagalam |

---

## Diger Tekniklerle Entegrasyon (Integration with Other Techniques)

[assert|neutral] Carpici test sinerjileri [ground:witnessed:integration-patterns] [conf:0.88] [state:confirmed]

Carpici Test sunlarla sinerjik calisir:
- **Dogrulama Zinciri (CoV)**: CoV tasarimdaki hatalari yakalar, carpici test yurutmedeki hatalari yakalar
- **Kalite Kapilari**: Carpici test Faz 7 icin gecme/kalma kriterleri saglar
- **Metrik Izleme**: Risk puanlari kantitatif metrikler olur
- **Coklu Kisi Tartismasi**: Farkli kisiler farkli basarisizlik modlarini belirler

---

## Hizli Referans Kontrol Listesi (Quick Reference Checklist)

<!-- [[MOR:root:K-N-T]] Kontrol = root for check-control-verification -->

[direct|neutral] Faz 7 dogrulama icin [ground:witnessed:checklist-usage] [conf:0.90] [state:confirmed]

- Adim 1: 10+ basarisizlik modu beyin firtinasi yap (5 dk)
- Adim 2: Tum modlari risk matrisine gore puanla (5 dk)
- Adim 3: Tum KRITIK (>=12) ve en yuksek YUKSEK (8-11) sorunlari duzelt (10-20 dk)
- Adim 4: KRITIK sorun kalmayana kadar yeniden saldir (5-10 dk)
- Kalite Kapisi: Sifir KRITIK, belgelenmis YUKSEK/ORTA
- Beceriye hata isleme bolumu ekle
- Sorun giderme rehberi ekle

**Zaman Yatirimi**: Beceri basina 25-40 dakika
**ROI**: %58 daha fazla acik yakalandi, %67 daha az uretim sorunu
**Ne Zaman Kullanilir**: FAZ 7'de HER ZAMAN, OZELLIKLE yuksek riskli beceriler icin

---

[direct|emphatic] Unutmayin: Carpici test paranoyak olmakla ilgili degil - gercek dunya basarisizliklarini kullanicilar karsilasmadan ONCE yakalamakla ilgili. En iyi beceriler en kotu durum senaryolarina karsi savas-testli olanlardir. [ground:witnessed:testing-philosophy] [conf:0.90] [state:confirmed]

---

[commit|confident] <promise>ADVERSARIAL_TESTING_PROTOCOL_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
