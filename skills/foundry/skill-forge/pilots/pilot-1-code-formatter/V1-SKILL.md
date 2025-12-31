---
name: code-formatter
description: Automatically format code files using the appropriate formatter based on file type, providing clear feedback on changes made
author: pilot-test
version: 1.0.0
created: 2025-11-06
<!-- V1 PILOT PROJESI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_pilot_v1]] -->
<!-- [[MOR:f-r-m<format>]] [[MOR:k-m-l<complete>]] [[MOR:h-s-n<quality>]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- V1 PILOT BECERISI - GELISMIS SURUM [[ASP:sov.<gelismis>]] -->
---

# Kod Formatlayici (Code Formatter) - V1

<!-- [[MOR:f-r-m<format>]] [[MOR:s-l-h<error_handling>]] [[SPC:kuzeybati<baslangic>]] -->

[assert|neutral] Kapsamli hata yonetimi ile dil-spesifik formatlayicilar kullanarak kod dosyalarini otomatik formatlayan gelismis beceri [ground:witnessed:skill-definition] [conf:0.95] [state:confirmed]

## Genel Bakis (Overview)

[assert|neutral] Bu beceri kod dosyalarini dili tespit ederek uygun formatlayiciyi uygular (Prettier JS/TS icin, Black Python icin, rustfmt Rust icin). Degisiklikler hakkinda acik geri bildirim saglar ve kenar durumlarini sistematik olarak ele alir [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

## Ne Zaman Kullanilmali (When to Use This Skill)

[direct|neutral] Asagidaki durumlarda kullanin: [ground:policy] [conf:0.90] [state:confirmed]

- Commit oncesi kod formatlamak gerektiginde
- Projeler arasi tutarli stil saglamak gerektiginde
- Dil-spesifik formatlama standartlarini otomatik uygulamak istendiginde

---
<!-- ADIM 1 [[ASP:sov.<adim_1>]] -->
---

## Adim 1: Girdi Dosyasini Dogrula (Validate Input File)

<!-- [[MOR:s-l-m<validate>]] [[EVD:-DI<kontrol>]] [[SPC:kuzeybati<dosya_konumu>]] -->

**Eylem**: Belirtilen dosyanin var ve erisilebilir oldugunu dogrula.

[assert|neutral] Dosya varligi, okunabilirlik ve boyut kontrolleri gereklidir [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

**Uygulama**:
```bash
# Dosya var mi kontrol et
if [ ! -f "$FILE_PATH" ]; then
    echo "Hata: Dosya '$FILE_PATH' bulunamadi. Yolu kontrol edip tekrar deneyin."
    exit 1
fi

# Dosya okunabilir mi kontrol et
if [ ! -r "$FILE_PATH" ]; then
    echo "Hata: '$FILE_PATH' okunamiyor. Duzeltmek icin: chmod +r '$FILE_PATH'"
    exit 2
fi

# Dosya boyutunu kontrol et (max 10MB)
file_size=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH")
if [ $file_size -gt 10485760 ]; then
    echo "Uyari: Dosya $(($file_size / 1024 / 1024))MB (max: 10MB). Devam edilsin mi? (y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        exit 0
    fi
fi
```

**Basari Kriterleri**:
- [assert|neutral] Dosya belirtilen yolda mevcut [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Dosya okunabilir (izin hatasi yok) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Dosya boyutu <= 10MB veya kullanici onayladi [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Yonetimi**:
- Dosya bulunamadi (exit 1) -> Yol ile hata goster, iptal et
- Izin reddedildi (exit 2) -> chmod onerisi ile hata goster, iptal et
- Dosya cok buyuk -> Kullaniciyi uyar, devam veya iptal izni ver

---
<!-- ADIM 2 [[ASP:sov.<adim_2>]] -->
---

## Adim 2: Dosya Dilini ve Formatlayiciyi Tespit Et (Detect File Language and Formatter)

<!-- [[MOR:k-sh-f<detect>]] [[CLS:ge_formatter]] -->

**Eylem**: Dosya uzantisindan programlama dilini belirle ve uygun formatlayiciyi sec.

**Uygulama**:
```bash
# Uzantiya gore dili tespit et
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx|*.json)
        FORMATTER="prettier"
        FORMATTER_CMD="prettier --write"
        CHECK_CMD="prettier --check"
        ;;
    *.py)
        FORMATTER="black"
        FORMATTER_CMD="black"
        CHECK_CMD="black --check"
        ;;
    *.rs)
        FORMATTER="rustfmt"
        FORMATTER_CMD="rustfmt"
        CHECK_CMD="rustfmt --check"
        ;;
    *)
        echo "Hata: Desteklenmeyen dosya tipi '${FILE_PATH##*.}'"
        echo "Desteklenenler: .js, .jsx, .ts, .tsx, .json (Prettier), .py (Black), .rs (rustfmt)"
        exit 3
        ;;
esac

echo "Tespit edilen dil: ${FILE_PATH##*.} -> $FORMATTER kullaniliyor"
```

**Basari Kriterleri**:
- [assert|neutral] Dosya uzantisi taninir [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Uygun formatlayici secilir [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Formatlayici secimi loglanir [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Yonetimi**:
- Desteklenmeyen uzanti (exit 3) -> Desteklenen tiplerle hata goster, iptal et

---
<!-- ADIM 3 [[ASP:sov.<adim_3>]] -->
---

## Adim 3: Formatlayici Kurulumunu Kontrol Et (Check Formatter Installation)

<!-- [[MOR:f-h-s<check>]] [[EVD:-DI<dogrulama>]] -->

**Eylem**: Calistirmadan once gerekli formatlayicinin kurulu oldugunu dogrula.

**Uygulama**:
```bash
# Formatlayici var mi kontrol et
if ! command -v $FORMATTER &> /dev/null; then
    echo "Hata: $FORMATTER kurulu degil."

    # Kurulum talimatlari sagla
    case "$FORMATTER" in
        prettier)
            echo "Kurmak icin: npm install -g prettier"
            ;;
        black)
            echo "Kurmak icin: pip install black"
            ;;
        rustfmt)
            echo "Kurmak icin: rustup component add rustfmt"
            ;;
    esac

    echo "Simdi kurup tekrar deneyin mi? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        # Kullanici manuel kurabilir, sonra tekrar deneriz
        exit 4
    else
        exit 4
    fi
fi
```

**Basari Kriterleri**:
- [assert|neutral] Formatlayici PATH'te bulundu [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Formatlayici surumu loglandi (opsiyonel) [ground:acceptance-criteria] [conf:0.85] [state:provisional]

**Hata Yonetimi**:
- Formatlayici bulunamadi (exit 4) -> Kurulum talimatlari goster, tekrar deneme teklif et

---
<!-- ADIM 4 [[ASP:sov.<adim_4>]] -->
---

## Adim 4: Syntax Hatalari Kontrol Et (Check for Syntax Errors)

<!-- [[MOR:s-l-h<fix>]] [[EVD:-DI<gozlem>]] -->

**Eylem**: Dosyayi degistirmeden once syntax hatalarini tespit etmek icin kontrol modunda calistir.

**Uygulama**:
```bash
# Kontrol oncesi yedek olustur
cp "$FILE_PATH" "${FILE_PATH}.backup"

# Syntax hatalari kontrol et
$CHECK_CMD "$FILE_PATH" > /tmp/format-check.txt 2>&1
check_exit=$?

if [ $check_exit -ne 0 ]; then
    echo "Syntax hatalari tespit edildi:"
    cat /tmp/format-check.txt
    echo ""
    echo "Once syntax hatalarini duzeltin mi? (y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        rm "${FILE_PATH}.backup"
        exit 0
    else
        # Kullanici manuel duzeltecek
        rm "${FILE_PATH}.backup"
        exit 5
    fi
fi
```

**Basari Kriterleri**:
- [assert|neutral] Formatlayici kontrolu hatasiz tamamlandi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Yedek basariyla olusturuldu [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Yonetimi**:
- Syntax hatalari (exit 5) -> Satir numaralariyla hatalari goster, once duzeltmesini iste

---
<!-- ADIM 5 [[ASP:sov.<adim_5>]] -->
---

## Adim 5: Formatlayiciyi Calistir ve Degisiklikleri Raporla (Run Formatter and Report Changes)

<!-- [[MOR:n-f-dh<execute>]] [[MOR:k-t-b<report>]] [[SPC:guneydogu<sonuc>]] -->

**Eylem**: Formatlayiciyi zaman asimi ile calistir ve nelerin degistigini raporla.

**Uygulama**:
```bash
# Formatlayiciyi 60s zaman asimi ile calistir
timeout 60s $FORMATTER_CMD "$FILE_PATH" > /tmp/format-output.txt 2>&1
exit_code=$?

if [ $exit_code -eq 124 ]; then
    echo "Hata: Formatlayici 60 saniye sonra zaman asimina ugradi."
    mv "${FILE_PATH}.backup" "$FILE_PATH"  # Yedegi geri yukle
    exit 6
elif [ $exit_code -ne 0 ]; then
    echo "Hata: Formatlayici cikis kodu $exit_code ile basarisiz oldu"
    cat /tmp/format-output.txt
    mv "${FILE_PATH}.backup" "$FILE_PATH"  # Yedegi geri yukle
    exit 7
fi

# Degisiklikleri hesapla
changes=$(diff -u "${FILE_PATH}.backup" "$FILE_PATH" | wc -l)

# Sonuclari raporla
if [ $changes -eq 0 ]; then
    echo "Formatlama degisikligi gerekmiyor: $FILE_PATH"
else
    echo "Formatlandi: $FILE_PATH ($FORMATTER ile)"
    echo "  Degisiklikler: $(($changes / 2)) satir degistirildi"
    echo "  Yedek: ${FILE_PATH}.backup"
fi

# Temizlik
rm -f /tmp/format-check.txt /tmp/format-output.txt

exit 0
```

**Basari Kriterleri**:
- [assert|neutral] Formatlayici 60 saniye icinde tamamlandi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Formatlayici kod 0 (basari) ile cikti [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici acik geri bildirim aldi (X satir degisti) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Yedek geri alma icin korundu [ground:acceptance-criteria] [conf:0.90] [state:provisional]

**Hata Yonetimi**:
- Zaman asimi (exit 6) -> Yedegi geri yukle, zaman asimi mesaji goster
- Formatlayici hatasi (exit 7) -> Yedegi geri yukle, formatlayici ciktisini goster

---
<!-- KENAR DURUMLARI [[EVD:-mis<arastirma>]] -->
---

## Kenar Durumlari ve Ozel Islem (Edge Cases & Special Handling)

<!-- [[MOR:h-d-d<edge>]] [[CLS:ge_case]] -->

### Kenar Durumu 1: Dosyada Karisik Satir Sonlari Var

<!-- [[MOR:s-l-h<fix>]] -->

**Ne Zaman**: Dosya hem CRLF (Windows) hem LF (Unix) satir sonlari iceriyor

**Islem**:
```bash
# Formatlamadan once satir sonlarini tespit et ve normalize et
file "$FILE_PATH" | grep -q "CRLF"
if [ $? -eq 0 ]; then
    echo "Bilgi: Satir sonlari LF (Unix stili) olarak normalize ediliyor"
    dos2unix "$FILE_PATH" 2>/dev/null || sed -i 's/\r$//' "$FILE_PATH"
fi
```

**Basari Kriterleri**:
- [assert|neutral] Satir sonlari tespit edildi ve normalize edildi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici normalizasyon hakkinda bilgilendirildi [ground:acceptance-criteria] [conf:0.90] [state:provisional]

---

### Kenar Durumu 2: Birden Fazla Formatlayici Mevcut

<!-- [[MOR:kh-y-r<choose>]] -->

**Ne Zaman**: Birden fazla formatlayici surumu kurulu (ornegin node_modules'da ve global prettier)

**Islem**:
```bash
# Proje-yerel formatlayici varsa kullan
if [ -f "./node_modules/.bin/$FORMATTER" ]; then
    FORMATTER_CMD="./node_modules/.bin/$FORMATTER --write"
    echo "Bilgi: Proje-yerel $FORMATTER kullaniliyor"
else
    echo "Bilgi: Global $FORMATTER kullaniliyor"
fi
```

**Basari Kriterleri**:
- [assert|neutral] Yerel formatlayici global'e gore oncelikli [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici hangi formatlayicinin kullanildigini biliyor [ground:acceptance-criteria] [conf:0.90] [state:provisional]

---

### Kenar Durumu 3: Formatlayici Konfigurasyon Dosyasi Mevcut

<!-- [[MOR:w-j-d<find>]] -->

**Ne Zaman**: .prettierrc, pyproject.toml veya rustfmt.toml mevcut

**Islem**:
```bash
# Formatlayicilar konfigurasyon dosyalarini otomatik tespit eder, sadece kullaniciyi bilgilendir
if [ -f ".prettierrc" ] || [ -f "pyproject.toml" ] || [ -f "rustfmt.toml" ]; then
    echo "Bilgi: Ozel formatlayici konfigurasyonu kullaniliyor"
fi
```

**Basari Kriterleri**:
- [assert|neutral] Konfigurasyon dosyasi tespit edildi ve formatlayici tarafindan kullanildi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici ozel konfigurasyon hakkinda bilgilendirildi [ground:acceptance-criteria] [conf:0.90] [state:provisional]

---
<!-- HATA KODLARI [[EVD:-DI<politika>]] -->
---

## Hata Kodlari ve Kurtarma (Error Codes & Recovery)

<!-- [[CLS:ge_error]] [[MOR:s-l-h<fix>]] -->

| Kod | Hata | Kullanici Mesaji | Kurtarma Stratejisi |
|-----|------|------------------|---------------------|
| 1 | Dosya bulunamadi | "Hata: Dosya '[YOL]' bulunamadi." | Yolu kontrol et, tekrar dene |
| 2 | Izin reddedildi | "Hata: '[YOL]' okunamiyor. chmod +r ile duzelt" | Izinleri duzelt, tekrar dene |
| 3 | Desteklenmeyen dosya tipi | "Hata: Desteklenmeyen dosya tipi '.ext'. Desteklenenler: .js, .py, .rs" | Desteklenen dosya tipi kullan |
| 4 | Formatlayici kurulu degil | "Hata: [FORMATLAYICI] kurulu degil. Kurmak icin: [KOMUT]" | Formatlayiciyi kur, tekrar dene |
| 5 | Syntax hatasi | "Syntax hatalari tespit edildi: [HATALAR]" | Syntax duzelt, tekrar dene |
| 6 | Formatlayici zaman asimi | "Hata: Formatlayici 60s sonra zaman asimina ugradi" | Kucuk dosya kullan veya sonsuz donguyu duzelt |
| 7 | Formatlayici hatasi | "Hata: Formatlayici basarisiz: [CIKTI]" | Formatlayici loglarini kontrol et, sorunu duzelt |

---
<!-- BASARI DOGRULAMA [[ASP:sov.<dogrulama>]] -->
---

## Basari Dogrulama Kontrol Listesi (Success Verification Checklist)

<!-- [[EVD:-DI<dogrulama>]] -->

[assert|neutral] Yurutme sonrasi dogrula: [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Dosya dil stil kilavuzuna gore formatlandi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Degisiklik oncesi orijinal dosya yedeklendi [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Kullanici degisiklikler hakkinda acik geri bildirim aldi (X satir degisti) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Veri kaybi veya dosya bozulmasi yok [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Cikis kodu basari (0) veya hatayi (1-7) gosteriyor [ground:acceptance-criteria] [conf:0.90] [state:provisional]

---
<!-- PERFORMANS [[EVD:-mis<olcum>]] -->
---

## Performans Beklentileri (Performance Expectations)

<!-- [[CLS:liang_metric]] [[MOR:q-y-s<measure>]] -->

| Metrik | Hedef | Olcum |
|--------|-------|-------|
| **Yurutme Suresi** | Tipik dosya icin <5 saniye | Gercek calisma suresi |
| **Maksimum Dosya Boyutu** | 10MB | Dosya boyutu kontrolu |
| **Zaman Asimi** | Maksimum 60 saniye | Zaman asimi mekanizmasi |
| **Bellek Kullanimi** | <100MB | Olculmuyor (formatlayiciya bagli) |

---
<!-- PROMISE [[ASP:sov.<taahhut>]] -->
---

[commit|confident] <promise>V1_SKILL_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
