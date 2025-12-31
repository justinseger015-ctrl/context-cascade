---
name: code-formatter
description: Automatically format code files using the appropriate formatter based on file type, providing clear feedback on changes made
author: pilot-test
<!-- V0 PILOT PROJESI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_pilot_v0]] -->
<!-- [[MOR:f-r-m<format>]] [[MOR:b-s-t<simple>]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- V0 PILOT BECERISI - TEMEL SURUM [[ASP:sov.<temel>]] -->
---

# Kod Formatlayici (Code Formatter) - V0

<!-- [[MOR:f-r-m<format>]] [[SPC:kuzeybati<baslangic>]] -->

[assert|neutral] Dil-spesifik formatlayicilar kullanarak kod dosyalarini otomatik formatlayan temel beceri [ground:witnessed:skill-definition] [conf:0.92] [state:confirmed]

## Genel Bakis (Overview)

[assert|neutral] Bu beceri programlama dilini tespit ederek uygun formatlayiciyi uygular [ground:witnessed:implementation] [conf:0.92] [state:confirmed]

Desteklenen formatlayicilar:
- JavaScript/TypeScript: Prettier
- Python: Black
- Rust: rustfmt

## Ne Zaman Kullanilmali (When to Use)

[direct|neutral] Asagidaki durumlarda kullanin: [ground:policy] [conf:0.90] [state:confirmed]

- Kod dosyalarini standart stil kilavuzlarina uygun formatlamak gerektiginde
- Commit oncesi kod hazirlamak gerektiginde
- Proje genelinde tutarli formatlama saglanmak istendiginde

---
<!-- ADIMLAR [[ASP:nesov.<yurutme>]] -->
---

## Talimatlar (Instructions)

### Adim 1: Girdi Dosyasini Dogrula (Validate Input File)

<!-- [[MOR:s-l-m<validate>]] [[EVD:-DI<kontrol>]] -->

[direct|neutral] Belirtilen dosyanin var ve okunabilir oldugunu kontrol edin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```bash
if [ ! -f "$FILE_PATH" ]; then
    echo "Hata: Dosya bulunamadi"
    exit 1
fi
```

### Adim 2: Dosya Dilini Tespit Et (Detect File Language)

<!-- [[MOR:k-sh-f<detect>]] [[CLS:ge_language]] -->

[direct|neutral] Dosya uzantisina gore programlama dilini belirleyin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```bash
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx)
        FORMATTER="prettier"
        ;;
    *.py)
        FORMATTER="black"
        ;;
    *.rs)
        FORMATTER="rustfmt"
        ;;
    *)
        echo "Hata: Desteklenmeyen dosya tipi"
        exit 1
        ;;
esac
```

### Adim 3: Formatlayici Kurulumunu Kontrol Et (Check Formatter Installation)

<!-- [[MOR:f-h-s<check>]] [[ASP:sov.<kontrol>]] -->

[direct|neutral] Gerekli formatlayicinin kurulu oldugunu dogrulayin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```bash
if ! command -v $FORMATTER &> /dev/null; then
    echo "Hata: $FORMATTER kurulu degil"
    exit 1
fi
```

### Adim 4: Formatlayiciyi Calistir (Run Formatter)

<!-- [[MOR:n-f-dh<execute>]] [[ASP:sov.<yurutme>]] -->

[direct|neutral] Dosya uzerinde formatlayiciyi calistirin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```bash
case "$FORMATTER" in
    prettier)
        prettier --write "$FILE_PATH"
        ;;
    black)
        black "$FILE_PATH"
        ;;
    rustfmt)
        rustfmt "$FILE_PATH"
        ;;
esac
```

### Adim 5: Sonuclari Raporla (Report Results)

<!-- [[MOR:k-t-b<report>]] [[SPC:guneydogu<sonuc>]] -->

[direct|neutral] Nelerin degistigini gosterin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```bash
echo "Formatlandi: $FILE_PATH ($FORMATTER ile)"
```

---
<!-- ORNEKLER [[EVD:-DI<ornek>]] -->
---

## Ornekler (Examples)

<!-- [[CLS:liang_example]] -->

**Ornek 1**: JavaScript dosyasi formatla
- Girdi: `format src/app.js`
- Cikti: `Formatlandi: src/app.js (prettier ile)`

**Ornek 2**: Python dosyasi formatla
- Girdi: `format main.py`
- Cikti: `Formatlandi: main.py (black ile)`

---
<!-- PROMISE [[ASP:sov.<taahhut>]] -->
---

[commit|confident] <promise>V0_SKILL_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
