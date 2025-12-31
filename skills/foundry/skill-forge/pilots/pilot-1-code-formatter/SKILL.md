---
name: pilot-1-code-formatter
description: Automatically format code files using the appropriate formatter based on file type, providing clear feedback on changes made
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
<!-- PILOT PROJESI BECERI DOKUMANI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_pilot]] -->
<!-- [[MOR:k-t-b<format>]] [[MOR:s-l-m<validate>]] [[MOR:h-s-n<quality>]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- S0 META-IDENTITY [[ASP:sov.<tamamlandi>]] [[SPC:kuzeybati<temel>]] -->
---

[define|neutral] SKILL := {
  beceri_adi: "code-formatter",
  kategori: "foundry",
  surum: "1.0.0",
  katman: "L1",
  pilot_id: "PILOT-CF-001"
} [ground:given] [conf:1.0] [state:confirmed]

---
<!-- S1 COGNITIVE FRAME [[COM:Erkenntnisrahmen]] -->
---

[define|neutral] COGNITIVE_FRAME := {
  cerceve: "Compositional",
  kaynak: "German",
  bilissel_zorlama: "Build from primitives?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

---
<!-- S2 TRIGGER CONDITIONS [[EVD:-DI<tetikleme>]] -->
---

[define|neutral] TRIGGER_POSITIVE := {
  anahtar_kelimeler: ["code-formatter", "format code", "prettier", "black", "rustfmt"],
  baglamlar: ["user needs code formatting", "pre-commit formatting", "style consistency"]
} [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] TRIGGER_NEGATIVE := {
  anti_kaliplar: ["linting only", "syntax checking without format", "compile errors"],
  alternatif_beceriler: ["linter", "syntax-checker", "compiler-diagnostics"]
} [ground:inferred] [conf:0.85] [state:provisional]

---
<!-- S3 TEMEL ICERIK [[ASP:nesov.<devam_ediyor>]] -->
---

# Kod Formatlayici (Code Formatter)

<!-- [[MOR:f-r-m<format>]] [[MOR:k-sh-f<detect>]] [[MOR:s-l-h<fix>]] -->

[assert|neutral] Bu beceri kod dosyalarini dil-spesifik formatlayicilar kullanarak otomatik formatlar [ground:witnessed:skill-definition] [conf:0.95] [state:confirmed]

## Genel Bakis (Overview)

[assert|neutral] Beceri programlama dilini tespit eder ve uygun formatlayiciyi uygular (Prettier JS/TS icin, Black Python icin, rustfmt Rust icin) [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

## Ne Zaman Kullanilmali (When to Use)

[direct|neutral] Asagidaki durumlarda bu beceriyi kullanin: [ground:policy] [conf:0.90] [state:confirmed]

- Commit oncesi kod formatlama gerektiginde
- Projeler arasi tutarli stil saglanmasi gerektiginde
- Dil-spesifik formatlama standartlari otomatik uygulanmak istendiginde

## Ne Zaman KULLANILMAMALI (When NOT to Use)

[direct|emphatic] Asagidaki durumlarda alternatif beceriler tercih edin: [ground:policy] [conf:0.90] [state:confirmed]

- Sadece linting gerektiginde -> linter becerisi kullanin
- Syntax hatalari duzeltilecekse -> syntax-checker kullanin
- Derleme hatalari varsa -> once hatalari duzeltin

---
<!-- S3.1 ADIMLAR [[ASP:sov.<adim_adim>]] -->
---

## Adim 1: Girdi Dosyasini Dogrula (Validate Input File)

<!-- [[MOR:s-l-m<validate>]] [[SPC:kuzeybati<dosya_konumu>]] -->

**Eylem**: Belirtilen dosyanin var oldugunu ve erisilebilir oldugunu dogrula.

[assert|neutral] Dosya varligi, okunabilirlik ve boyut kontrolu yapilmalidir [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

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

# Dosya boyutu kontrol et (max 10MB)
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

## Adim 2: Dosya Dilini ve Formatlayiciyi Tespit Et (Detect Language and Formatter)

<!-- [[MOR:k-sh-f<detect>]] [[CLS:ge_formatter]] -->

**Eylem**: Dosya uzantisindan programlama dilini belirle ve uygun formatlayiciyi sec.

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

---

## Adim 3: Formatlayici Kurulumunu Kontrol Et (Check Formatter Installation)

<!-- [[MOR:f-h-s<check>]] [[ASP:sov.<kontrol>]] -->

**Eylem**: Gerekli formatlayicinin kurulu oldugunu dogrula.

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
    exit 4
fi
```

---

## Adim 4: Syntax Hatalari Kontrol Et (Check for Syntax Errors)

<!-- [[MOR:s-l-h<fix>]] [[EVD:-DI<gozlem>]] -->

**Eylem**: Dosyayi degistirmeden once syntax hatalarini tespit etmek icin kontrol modunda calistir.

```bash
# Kontrol oncesi yedek al
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
        rm "${FILE_PATH}.backup"
        exit 5
    fi
fi
```

---

## Adim 5: Formatlayiciyi Calistir ve Degisiklikleri Raporla (Run Formatter and Report)

<!-- [[MOR:k-t-b<write>]] [[ASP:sov.<tamamlandi>]] [[SPC:guneydogu<sonuc>]] -->

**Eylem**: Formatlayiciyi zaman asimi ile calistir ve nelerin degistigini raporla.

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

---
<!-- S4 BASARI KRITERLERI [[EVD:-DI<dogrulama>]] -->
---

[define|neutral] SUCCESS_CRITERIA := {
  birincil: "Formatlama basariyla tamamlandi",
  kalite: "Cikti dil stil kilavuzuna uygun",
  dogrulama: "Yedek olusturuldu ve degisiklik sayisi raporlandi"
} [ground:given] [conf:1.0] [state:confirmed]

## Hata Kodlari ve Kurtarma (Error Codes & Recovery)

| Kod | Hata | Kullanici Mesaji | Kurtarma Stratejisi |
|-----|------|------------------|---------------------|
| 1 | Dosya bulunamadi | "Hata: Dosya '[YOL]' bulunamadi." | Yolu kontrol et, tekrar dene |
| 2 | Izin reddedildi | "Hata: '[YOL]' okunamiyor. chmod +r ile duzelt" | Izinleri duzelt, tekrar dene |
| 3 | Desteklenmeyen tip | "Hata: Desteklenmeyen dosya tipi '.ext'" | Desteklenen tip kullan |
| 4 | Formatlayici kurulu degil | "Hata: [FORMATLAYICI] kurulu degil" | Formatlayiciyi kur, tekrar dene |
| 5 | Syntax hatasi | "Syntax hatalari tespit edildi: [HATALAR]" | Syntax duzelt, tekrar dene |
| 6 | Zaman asimi | "Hata: Formatlayici 60s sonra zaman asimina ugradi" | Kucuk dosya kullan |
| 7 | Formatlayici hatasi | "Hata: Formatlayici basarisiz: [CIKTI]" | Logları kontrol et |

---
<!-- S5 MCP ENTEGRASYONU [[EVD:-mis<konfigurasyon>]] -->
---

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Yurutme sonuclarini ve kaliplari sakla",
  araclar: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

---
<!-- S6 BELLEK AD ALANI [[SPC:merkez<depolama>]] -->
---

[define|neutral] MEMORY_NAMESPACE := {
  kalip: "skills/foundry/code-formatter/{project}/{timestamp}",
  sakla: ["executions", "decisions", "patterns"],
  getir: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  KIM: "code-formatter-{session_id}",
  NE_ZAMAN: "ISO8601_timestamp",
  PROJE: "{project_name}",
  NEDEN: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

---
<!-- S7 BECERI TAMAMLAMA DOGRULAMASI [[ASP:sov.<dogrulama>]] -->
---

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_olusturma: "Task() ile agent olustur",
  kayit_dogrulama: "Sadece kayitli agentlari kullan",
  todowrite_cagrildi: "TodoWrite ile ilerleme takip et",
  is_delegasyonu: "Uzman agentlara delege et"
} [ground:system-policy] [conf:1.0] [state:confirmed]

---
<!-- S8 MUTLAK KURALLAR [[EVD:-DI<politika>]] -->
---

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

---
<!-- PROMISE [[ASP:sov.<taahhut>]] -->
---

[commit|confident] <promise>PILOT_CODE_FORMATTER_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
