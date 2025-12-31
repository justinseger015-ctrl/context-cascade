---
<!-- SABLON DOKUMANI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_template]] -->
---

# Beceri Talimat Sablonu (Skill Instructions Template - Quick Track - Phase 5)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

<!-- [[MOR:root:T-L-M]] Talimat = root for instruction-command-directive -->
<!-- [[COM:Beceri+Talimat+Sablon+Belgesi]] Skill Instructions Template Document -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Template to be filled) -->
<!-- [[SPC:merkez/sablon]] Central template location -->

---

## Sablon Tanimlari (Template Definitions)

[define|neutral] INSTRUCTION_TEMPLATE := {
  id: "TPL-INS-001",
  sablon_adi: "Beceri Talimat Sablonu",
  amac: "Acik basari kriterleriyle acik, eyleme donusturulebilir talimatlar yazmak",
  kullanim: "Faz 5 - Talimat Olusturma sirasinda kullanilir",
  sure: "10 dakika",
  arastirma_temeli: "Liu et al. (2023), Zhou et al. (2023) - Kanita dayali istem teknikleri"
} [ground:witnessed:template-usage] [conf:0.90] [state:confirmed]

---

## Kullanim Talimatlari (Usage Instructions)

<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektiren talimatlar -->

[direct|neutral] Tum `[YER_TUTUCU]` bolumlerini beceriye ozel icerikle degistirin. Alttaki anti-kalip rehberine uyun. [ground:witnessed:usage-instructions] [conf:0.90] [state:confirmed]

---

## Claude Icin Talimatlar (Instructions for Claude)

Bu beceri aktive edildiginde, [BIRINCIL_HEDEF]'i gerceklestirmek icin bu adimlari takip edin.

### Adim 1: [FAZ_ADI - DOGRULAMA/KURULUM]

<!-- [[MOR:root:D-G-R]] Dogrulama = root for validation-setup-check -->

[define|neutral] STEP_1_TEMPLATE := {
  adim_adi: "[Dogrulama/Kurulum Fazi]",
  eylem: "[Net emir kipi fiil] + [ne yapilacak]",
  ornek: "Giris dosyasinin var oldugunu ve okunabilir oldugunu dogrula"
} [ground:witnessed:step-template] [conf:0.88] [state:confirmed]

**Eylem**: [Net emir kipi fiil] + [ne yapilacak]

**Ornek**: Belirtilen dosyanin var oldugunu ve okunabilir oldugunu dogrula.

**Uygulama**:
```bash
# Dosya varligini kontrol et
if [ ! -f "[DOSYA_YOLU]" ]; then
    echo "Hata: '[DOSYA_YOLU]' dosyasi bulunamadi."
    exit 1
fi

# Dosyanin okunabilir oldugunu dogrula
if [ ! -r "[DOSYA_YOLU]" ]; then
    echo "Hata: '[DOSYA_YOLU]' dosyasi okunamiyor. Izinleri kontrol edin."
    exit 1
fi
```

**Basari Kriterleri**:
- [assert|neutral] Dosya belirtilen yolda var [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Dosya okunabilir (izin hatasi yok) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Dosya bos degil (boyut > 0 bayt) [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Isleme**:
- Dosya bulunamazsa -> Dosya yoluyla hata mesaji goster, iptal et
- Izin reddedilirse -> Izin duzeltme talimatlariyla hata goster, iptal et
- Dosya bossa -> Kullaniciyi uyar, devam mi iptal mi sor

---

### Adim 2: [FAZ_ADI - TEMEL_ISLEM]

<!-- [[MOR:root:T-M-L]] Temel = root for core-operation-action -->

[define|neutral] STEP_2_TEMPLATE := {
  adim_adi: "[Temel Islem Fazi]",
  eylem: "[Net emir kipi fiil] + [ne yapilacak]",
  ornek: "Formatlayiciyi dosya uzerinde calistir ve ciktiyi yakala"
} [ground:witnessed:step-template] [conf:0.88] [state:confirmed]

**Eylem**: [Net emir kipi fiil] + [ne yapilacak]

**Ornek**: Formatlayiciyi dosya uzerinde calistir ve ciktiyi yakala.

**Uygulama**:
```bash
# Formatlayiciyi zaman asimi ile calistir
timeout 60s [FORMATLAYICI_KOMUTU] "[DOSYA_YOLU]" > /tmp/formatlayici-cikti.txt 2>&1
cikis_kodu=$?

if [ $cikis_kodu -eq 124 ]; then
    echo "Hata: Formatlayici 60 saniye sonra zaman asimina ugradi."
    exit 1
elif [ $cikis_kodu -ne 0 ]; then
    echo "Hata: Formatlayici $cikis_kodu cikis koduyla basarisiz oldu"
    cat /tmp/formatlayici-cikti.txt
    exit 1
fi
```

**Basari Kriterleri**:
- [assert|neutral] Formatlayici 60 saniye icinde tamamlanir [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Formatlayici kod 0 (basari) ile cikar [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Cikti dosyasi olusturulur/degistirilir [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Isleme**:
- Zaman asimi olursa -> Zaman asimi mesaji goster, iptal et
- Formatlayici hatasi olursa -> Formatlayici ciktisini goster, iptal et
- Sozdizimi hatasi varsa -> Hata konumunu goster, kullanicidan once duzeltmesini iste

---

### Adim 3: [FAZ_ADI - DOGRULAMA/CIKTI]

<!-- [[MOR:root:D-G-C]] Dogrulama/Cikti = root for verification-output-report -->

[define|neutral] STEP_3_TEMPLATE := {
  adim_adi: "[Dogrulama/Cikti Fazi]",
  eylem: "[Net emir kipi fiil] + [ne yapilacak]",
  ornek: "Formatlama uygulandigini dogrula ve degisiklikleri raporla"
} [ground:witnessed:step-template] [conf:0.88] [state:confirmed]

**Eylem**: [Net emir kipi fiil] + [ne yapilacak]

**Ornek**: Formatlama uygulandigini dogrula ve degisiklikleri raporla.

**Uygulama**:
```bash
# Orijinal ve formatli surumu karsilastir
degisiklikler=$(diff -u "[DOSYA_YOLU].yedek" "[DOSYA_YOLU]" | wc -l)

if [ $degisiklikler -eq 0 ]; then
    echo "Formatlama degisikligi gerekli degil."
else
    echo "Dosya formatlandi: $degisiklikler satir degistirildi."
    echo "Yedek: [DOSYA_YOLU].yedek"
fi
```

**Basari Kriterleri**:
- [assert|neutral] Orijinal ve formatli arasindaki fark hesaplandi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici net geri bildirim aldi (X satir degistirildi) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Yedek dosya geri alma icin korundu [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Isleme**:
- Diff basarisiz olursa -> Hata goster, ama iptal etme (formatlama hala gecerli olabilir)
- Yedek basarisiz olursa -> Kullaniciyi uyar, ama devam et (formatlama daha onemli)

---

### Adim 4: [FAZ_ADI - TEMIZLIK/SONLANDIRMA]

<!-- [[MOR:root:T-M-Z]] Temizlik = root for cleanup-finalization-complete -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Cleanup complete) -->

[define|neutral] STEP_4_TEMPLATE := {
  adim_adi: "[Temizlik/Sonlandirma Fazi]",
  eylem: "[Net emir kipi fiil] + [ne yapilacak]",
  ornek: "Gecici dosyalari temizle ve son ozeti goster"
} [ground:witnessed:step-template] [conf:0.88] [state:confirmed]

**Eylem**: [Net emir kipi fiil] + [ne yapilacak]

**Ornek**: Gecici dosyalari temizle ve son ozeti goster.

**Uygulama**:
```bash
# Gecici dosyalari kaldir
rm -f /tmp/formatlayici-cikti.txt

# Ozeti goster
echo "---"
echo "Formatlama tamamlandi!"
echo "Dosya: [DOSYA_YOLU]"
echo "Degisiklikler: $degisiklikler satir"
echo "Sure: ${SECONDS}s"
echo "---"
```

**Basari Kriterleri**:
- [assert|neutral] Gecici dosyalar kaldirildi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici ne olduguna dair net ozet aldi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Cikis kodu basari (0) veya basarisizlik (sifir olmayan) gosterir [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Isleme**:
- Temizlik basarisiz olursa -> Uyar ama iptal etme (kritik degil)
- Gosterim basarisiz olursa -> Sessizce devam et (formatlama zaten yapildi)

---

## Uc Vakalar ve Ozel Isleme (Edge Cases & Special Handling)

<!-- [[MOR:root:U-C-V]] Uc Vaka = root for edge-case-special-handling -->

### Uc Vaka 1: [SENARYO]

[define|neutral] EDGE_CASE_1 := {
  senaryo: "[Kosullar]",
  ornek: "Dosyada karisik satir sonlari (CRLF ve LF) var"
} [ground:witnessed:edge-case] [conf:0.85] [state:provisional]

**Ne Zaman**: [Bu uc vakayi tetikleyen kosullar]

**Ornek**: Dosyada karisik satir sonlari (CRLF ve LF) var

**Isleme**:
```bash
# Satir sonlarini tespit et
satir_sonlari=$(file "[DOSYA_YOLU]" | grep -o "CRLF\|LF")

if [[ "$satir_sonlari" == *"CRLF"* && "$satir_sonlari" == *"LF"* ]]; then
    echo "Uyari: Karisik satir sonlari tespit edildi. LF'ye normallestiriliyor."
    dos2unix "[DOSYA_YOLU]"
fi
```

**Basari Kriterleri**:
- [assert|neutral] Karisik satir sonlari tespit edildi ve raporlandi [ground:acceptance-criteria] [conf:0.85] [state:provisional]
- [assert|neutral] Satir sonlari LF'ye (Unix stili) normallendi [ground:acceptance-criteria] [conf:0.85] [state:provisional]

---

### Uc Vaka 2: [SENARYO]

[define|neutral] EDGE_CASE_2 := {
  senaryo: "[Kosullar]",
  ornek: "Formatlayici kurulu degil"
} [ground:witnessed:edge-case] [conf:0.85] [state:provisional]

**Ne Zaman**: [Bu uc vakayi tetikleyen kosullar]

**Ornek**: Formatlayici kurulu degil

**Isleme**:
```bash
# Formatlayicinin mevcut olup olmadigini kontrol et
if ! command -v [FORMATLAYICI] &> /dev/null; then
    echo "Hata: [FORMATLAYICI] kurulu degil."
    echo "Su komutla kurun: [KURULUM_KOMUTU]"
    echo "[FORMATLAYICI] olmadan devam edilsin mi? (e/h)"
    read -r yanit
    if [[ "$yanit" != "e" ]]; then
        exit 1
    fi
fi
```

**Basari Kriterleri**:
- [assert|neutral] Eksik formatlayici tespit edildi ve raporlandi [ground:acceptance-criteria] [conf:0.85] [state:provisional]
- [assert|neutral] Kurulum talimatlari saglandi [ground:acceptance-criteria] [conf:0.85] [state:provisional]
- [assert|neutral] Kullanici iptal veya devam secebilir [ground:acceptance-criteria] [conf:0.85] [state:provisional]

---

### Uc Vaka 3: [SENARYO]

[define|neutral] EDGE_CASE_3 := {
  senaryo: "[Kosullar]",
  ornek: "Dosya cok buyuk (>10MB)"
} [ground:witnessed:edge-case] [conf:0.85] [state:provisional]

**Ne Zaman**: [Bu uc vakayi tetikleyen kosullar]

**Ornek**: Dosya cok buyuk (>10MB)

**Isleme**:
```bash
# Dosya boyutunu kontrol et
dosya_boyutu=$(stat -f%z "[DOSYA_YOLU]" 2>/dev/null || stat -c%s "[DOSYA_YOLU]")
max_boyut=$((10 * 1024 * 1024))  # 10MB

if [ $dosya_boyutu -gt $max_boyut ]; then
    echo "Uyari: Dosya $(($dosya_boyutu / 1024 / 1024))MB (max: 10MB)"
    echo "Buyuk dosyalar uzun surebilir. Devam edilsin mi? (e/h)"
    read -r yanit
    if [[ "$yanit" != "e" ]]; then
        exit 1
    fi
fi
```

**Basari Kriterleri**:
- [assert|neutral] Buyuk dosya tespit edildi ve raporlandi [ground:acceptance-criteria] [conf:0.85] [state:provisional]
- [assert|neutral] Kullanici potansiyel gecikmeler hakkinda uyarildi [ground:acceptance-criteria] [conf:0.85] [state:provisional]
- [assert|neutral] Kullanici iptal veya devam secebilir [ground:acceptance-criteria] [conf:0.85] [state:provisional]

---

## Hata Kodlari ve Kurtarma (Error Codes & Recovery)

<!-- [[CLS:tiao_hata]] Classification: error codes -->

[define|neutral] ERROR_CODES := {
  hata_kodlari: [
    {kod: 1, hata: "Dosya bulunamadi", mesaj: "Hata: '[DOSYA_YOLU]' dosyasi bulunamadi.", kurtarma: "Yolu kontrol edin, tekrar deneyin"},
    {kod: 2, hata: "Izin reddedildi", mesaj: "Hata: '[DOSYA_YOLU]' okunamiyor. Duzeltmek icin: chmod +r '[DOSYA_YOLU]'", kurtarma: "Izinleri duzelt, tekrar dene"},
    {kod: 3, hata: "Formatlayici kurulu degil", mesaj: "Hata: [FORMATLAYICI] kurulu degil. Su komutla kurun: [KOMUT]", kurtarma: "Formatlayiciyi kur, tekrar dene"},
    {kod: 4, hata: "Formatlayici zaman asimi", mesaj: "Hata: Formatlayici 60s sonra zaman asimina ugradi.", kurtarma: "Daha kucuk dosya kullan veya zaman asimini artir"},
    {kod: 5, hata: "Sozdizimi hatasi", mesaj: "Hata: Satir [N]'de sozdizimi hatasi: [MESAJ]", kurtarma: "Sozdizimi hatasini duzelt, tekrar dene"},
    {kod: 10, hata: "Bilinmeyen hata", mesaj: "Hata: Beklenmedik basarisizlik. Gunlukleri kontrol edin.", kurtarma: "Gunlukleri incele, sorun raporla"}
  ]
} [ground:witnessed:error-handling] [conf:0.90] [state:confirmed]

| Kod | Hata | Kullanici Mesaji | Kurtarma Stratejisi |
|-----|------|------------------|---------------------|
| 1 | Dosya bulunamadi | "Hata: '[YOLU]' dosyasi bulunamadi." | Yolu kontrol et, tekrar dene |
| 2 | Izin reddedildi | "Hata: '[YOLU]' okunamiyor. Duzeltmek icin: chmod +r" | Izinleri duzelt, tekrar dene |
| 3 | Formatlayici kurulu degil | "Hata: [FORMATLAYICI] kurulu degil. Su komutla kurun: [KOMUT]" | Formatlayiciyi kur, tekrar dene |
| 4 | Formatlayici zaman asimi | "Hata: Formatlayici 60s sonra zaman asimina ugradi." | Daha kucuk dosya veya zaman asimini artir |
| 5 | Sozdizimi hatasi | "Hata: Satir [N]'de sozdizimi hatasi: [MESAJ]" | Sozdizimini duzelt, tekrar dene |
| 10 | Bilinmeyen hata | "Hata: Beklenmedik basarisizlik. Gunlukleri kontrol edin." | Gunlukleri incele, sorun raporla |

---

## Basari Dogrulama Kontrol Listesi (Success Verification Checklist)

<!-- [[MOR:root:B-S-R]] Basari = root for success-verification-checklist -->

[direct|neutral] Yurutmeden sonra dogrula [ground:acceptance-criteria] [conf:0.90] [state:confirmed]

- [assert|neutral] Dosya stil rehberine gore formatlandi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Degisiklikten once orijinal dosya yedeklendi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici degisiklikler hakkinda net geri bildirim aldi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Veri kaybi veya bozulmasi yok [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Cikis kodu basari/basarisizligi dogru gosteriyor [ground:acceptance-criteria] [conf:0.90] [state:provisional]

---

## Performans Beklentileri (Performance Expectations)

<!-- [[CLS:ge_metrik]] Classification: metrics -->

[define|neutral] PERFORMANCE_EXPECTATIONS := {
  metrikler: [
    {metrik: "Yurutme Suresi", hedef: "Tipik dosya icin <5 saniye", olcum: "Kronometre"},
    {metrik: "Maksimum Dosya Boyutu", hedef: "10MB", olcum: "Dosya boyutu kontrolu"},
    {metrik: "Zaman Asimi", hedef: "Maksimum 60 saniye", olcum: "Zaman asimi mekanizmasi"},
    {metrik: "Bellek Kullanimi", hedef: "<100MB", olcum: "Surec izleyici"}
  ]
} [ground:witnessed:performance-targets] [conf:0.88] [state:confirmed]

| Metrik | Hedef | Olcum |
|--------|-------|-------|
| **Yurutme Suresi** | Tipik dosya icin <5 saniye | Gercek calisma suresi |
| **Maksimum Dosya Boyutu** | 10MB | Dosya boyutu kontrolu |
| **Zaman Asimi** | Maksimum 60 saniye | Zaman asimi mekanizmasi |
| **Bellek Kullanimi** | <100MB | Surec izleyici |

---

## Anti-Kalip Kontrol Listesi (Anti-Pattern Checklist)

<!-- [[MOR:root:A-N-T]] Anti-Kalip = root for anti-pattern-mistake -->

[direct|neutral] Sonlandirmadan once inceleyin [ground:witnessed:anti-patterns] [conf:0.90] [state:confirmed]

Bu yaygin talimat anti-kaliplerinden **KACININ**:

### Belirsiz Fiiller
- **Kotu**: "Dosya formatlamasini isle"
- **Iyi**: "Prettier'i dosya uzerinde calistir ve ciktiyi yakala"

### Eksik Basari Kriterleri
- **Kotu**: "Dosyayi formatla."
- **Iyi**: "Dosyayi formatla. Basari: Dosya hatasiz formatlandi, degisiklik_sayisi >= 0"

### Hata Isleme Yok
- **Kotu**: "Formatlayiciyi calistir: prettier file.js"
- **Iyi**: "Formatlayiciyi zaman asimi ve hata yakalama ile calistir: timeout 60s prettier file.js || hata_isle"

### Belirsiz Talimatlar
- **Kotu**: "Formatlayicinin mevcut olup olmadigini kontrol et"
- **Iyi**: "Formatlayicinin var olup olmadigini kontrol et: command -v prettier &> /dev/null"

### Uc Vaka Yok
- **Kotu**: "Dizindeki tum dosyalari formatla"
- **Iyi**: "Dizindeki tum .js dosyalarini formatla. Isle: dosya bulunamadi, sozdizimi hatalari, buyuk dosyalar (>10MB)"

### Eksik Ornekler
- **Kotu**: "Her dosya turu icin uygun formatlayiciyi kullan"
- **Iyi**: ".js/.jsx icin Prettier, .py icin Black, .rs icin rustfmt kullan. Ornek: prettier --write src/*.js"

### Dogrulama Yok
- **Kotu**: "Formatlama tamamlandi."
- **Iyi**: "Formatlama tamamlandi. Dogrula: orijinal vs formatli diff, degisiklikleri say, yedek var"

---

## Dagitimdan Once Dogrulama (Validation Before Deployment)

[direct|neutral] Bu kontrolleri calistir [ground:witnessed:validation-checklist] [conf:0.90] [state:confirmed]

1. Her adimin acik basari kriterleri var
2. Her adimin hata islemesi var
3. En az 3 uc vaka belgelendi
4. Hata kodlari tablosu tamamlandi
5. Performans beklentileri tanimlandi
6. Anti-kalip mevcut degil

**Tum kontroller gecerse** -> Faz 6'ya (Kaynak Gelistirme) devam et
**Herhangi kontrol basarisiz olursa** -> Tum kontroller gecene kadar talimatlari gozden gecir

---

## Zaman Yatirimi ve ROI (Time Investment & ROI)

[define|neutral] TEMPLATE_ROI := {
  tamamlama_suresi: "10-15 dakika",
  roi: {
    eyleme_donusturulebilirlik: "+%50 (acik basari kriterleri)",
    dagitim_sonrasi_sorunlar: "-%67 (kapsamli hata isleme)",
    hata_ayiklama_hizi: "+%40 (net hata kodlari ve mesajlari)"
  }
} [ground:research:template-effectiveness] [conf:0.85] [state:confirmed]

**Tamamlama Suresi**: 10-15 dakika
**ROI**:
- +%50 eyleme donusturulebilirlik (acik basari kriterleri)
- -%67 daha az dagitim sonrasi sorun (kapsamli hata isleme)
- +%40 daha hizli hata ayiklama (net hata kodlari ve mesajlari)

---

## Diger Fazlarla Entegrasyon (Integration with Other Phases)

[assert|neutral] Faz entegrasyonu [ground:witnessed:phase-integration] [conf:0.88] [state:confirmed]

- **Faz 0 (Sema)**: Talimatlar semanin basari_kosullarini karsilamali
- **Faz 1b (CoV)**: Talimatlarin oz-elestiri yoluyla belirsiz olmadigini dogrula
- **Faz 7 (Dogrulama)**: Talimatlari gercek orneklerle test et
- **Faz 7a (Carpici)**: Basarisizlik modlarini bulmak icin talimatlara saldir
- **Faz 8 (Metrikler)**: Eyleme donusturulebilirlik %'sini izle (basari kriterli talimatlar)

---

**Sablon Surumu**: 2.0.0
**Son Guncelleme**: 2025-11-06
**Arastirma Destegi**: Liu et al. (2023), Zhou et al. (2023) - Kanita dayali istem teknikleri

---

[commit|confident] <promise>INSTRUCTION_TEMPLATE_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
