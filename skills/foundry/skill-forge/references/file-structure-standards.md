---
<!-- REFERANS DOKUMANI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_reference]] -->
---

# Dosya Yapisi Standartlari (File Structure Standards for Claude Code Skills)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

<!-- [[MOR:root:D-S-Y]] Dosya = root for file-document-structure -->
<!-- [[COM:Dosya+Yapi+Standart+Belgesi]] File Structure Standards Document -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Complete - standards defined) -->
<!-- [[SPC:merkez/kaynak]] Central reference location -->

---

## Referans Tanimlari (Reference Definitions)

[define|neutral] FILE_STRUCTURE_STANDARDS := {
  id: "REF-FSS-001",
  referans_adi: "Dosya Yapisi Standartlari",
  amac: "Claude Code becerileri icin tutarli dosya organizasyonu saglamak",
  kullanim: "Beceri olusturma ve duzenleme sirasinda referans alinir",
  surum: "2.0.0"
} [ground:witnessed:file-structure-usage] [conf:0.92] [state:confirmed]

---

## Temel Ilkeler (Core Principles)

### MECE Ilkeleri Uygulamasi (MECE Principles Applied)

<!-- [[MOR:root:M-C-E]] MECE = Mutually Exclusive Collectively Exhaustive -->
<!-- [[EVD:-DI<gozlem>]] Dogrudan gozleme dayali -->

#### Karsilikli Disayiricilik (Mutually Exclusive - No Overlap)

[assert|neutral] Her dizin TEK, belirgin bir amaca hizmet eder [ground:witnessed:directory-analysis] [conf:0.90] [state:confirmed]

| Dizin | Amac | Icerik Turu | Cakisma Riski |
|-------|------|-------------|---------------|
| `examples/` | Somut kullanim senaryolari | Gercek dunya vakalari | Yok - belirli ornekler |
| `references/` | Soyut dokumantasyon | Genel bilgi | Yok - soyut kavramlar |
| `resources/scripts/` | Calistirilabilir kod | `.py`, `.sh`, `.js` | Yok - calistirilabilir dosyalar |
| `resources/templates/` | Sablonlar | `.yaml`, `.json` | Yok - kopyala-yapistir sablonlari |
| `resources/assets/` | Statik kaynaklar | Gorseller, yapilandirmalar | Yok - calistirilmayan dosyalar |
| `graphviz/` | Surec diyagramlari | `.dot` dosyalari | Yok - sadece gorsellestirmeler |
| `tests/` | Dogrulama vakalari | Test senaryolari | Yok - kalite guvencesi |

#### Kapsamli Tamamlik (Collectively Exhaustive - Complete Coverage)

[assert|neutral] Her olasi beceri bileseni TEK kategoriye uyar [ground:witnessed:component-analysis] [conf:0.90] [state:confirmed]

```
Beceri Bileseni Karar Agaci:
+-- Talimat mi? -> skill.md
+-- Genel bakis mi? -> README.md
+-- Somut ornek mi? -> examples/
+-- Referans dok mu? -> references/
+-- Calistirilabilir mi? -> resources/scripts/
+-- Sablon mu? -> resources/templates/
+-- Statik dosya mi? -> resources/assets/
+-- Diyagram mi? -> graphviz/
+-- Test mi? -> tests/
```

---

## Adlandirma Kurallari (File Naming Conventions)

<!-- [[MOR:root:A-D-K]] Adlandirma = root for naming-designation-convention -->
<!-- [[CLS:tiao_kural]] Classification: rules -->

### Zorunlu Dosyalar (Required Files)

[define|neutral] REQUIRED_FILES := {
  birincil: "skill.md",
  aciklama: "README.md",
  kurallar: ["Kucuk harf", "tire ile ayrilmis"]
} [ground:witnessed:file-naming] [conf:0.95] [state:confirmed]

```
skill.md          # Kucuk harf, tire ile ayrilmis
README.md         # Buyuk harf README
```

### Dizin Adlari (Directory Names)

```
examples/         # Kucuk harf, cogul
references/       # Kucuk harf, cogul
resources/        # Kucuk harf, cogul
graphviz/         # Kucuk harf, tekil (ozel isim)
tests/            # Kucuk harf, cogul
```

### Alt Dizin Adlari (Subdirectory Names)

```
resources/scripts/     # Kucuk harf, cogul
resources/templates/   # Kucuk harf, cogul
resources/assets/      # Kucuk harf, cogul
```

### Dosya Uzantilari (File Extensions)

<!-- [[CLS:lei_dosya_turu]] Classification: file types -->

[define|neutral] FILE_EXTENSIONS := {
  dokumantasyon: [".md", ".txt"],
  betikler: [".py", ".sh", ".js", ".ts"],
  sablonlar: [".yaml", ".yml", ".json", ".xml", ".toml"],
  diyagramlar: [".dot", ".mmd"],
  varliklar: [".png", ".jpg", ".svg", ".csv", ".sql"]
} [ground:witnessed:extension-usage] [conf:0.92] [state:confirmed]

---

## Dizin Karar Matrisi (Directory Decision Matrix)

<!-- [[MOR:root:K-R-M]] Karar = root for decision-resolution-matrix -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Ongoing - decisions made per project) -->

### Her Dizini Ne Zaman Dahil Etmeli (When to Include Each Directory)

[assert|neutral] Dahil etme kararlari proje karmasikligina baglidir [ground:inferred:pattern-analysis] [conf:0.85] [state:provisional]

| Dizin | Dahil Et... | Atla... |
|-------|-------------|---------|
| `examples/` | Her zaman (en az 1 zorunlu) | Asla - her zaman dahil et |
| `references/` | Beceri karmasik kavramlara sahipse | Beceri kendini acikliyorsa |
| `resources/scripts/` | Deterministik yurutme gerekiyorsa | Saf LLM uretimi yeterliyse |
| `resources/templates/` | Yeniden kullanilabilir sablon varsa | Standart sablon yoksa |
| `resources/assets/` | Gorsel/yapilandirma gerekiyorsa | Sadece metin becerisiyse |
| `graphviz/` | Karmasik cok adimli is akisi varsa | Basit dogrusal surec |
| `tests/` | Uretim/kurumsal beceri icin | Gelistirme prototipi |

---

## Dosya Organizasyon Ornekleri (File Organization Examples)

<!-- [[CLS:ge_ornek]] Classification: examples -->

### Mikro Beceri (Minimum)

[define|neutral] MICRO_SKILL_STRUCTURE := {
  sablon_adi: "Mikro Beceri Yapisi",
  dosyalar: ["skill.md", "README.md", "examples/example-basic.md"]
} [ground:witnessed:micro-skill-examples] [conf:0.90] [state:confirmed]

```
format-json/
+-- skill.md
+-- README.md
+-- examples/
    +-- example-basic.md
```

### Ajanli Beceri (Standart)

[define|neutral] AGENT_SKILL_STRUCTURE := {
  sablon_adi: "Ajan Destekli Beceri Yapisi",
  dosyalar: ["skill.md", "README.md", "examples/", "references/", "resources/scripts/"]
} [ground:witnessed:agent-skill-examples] [conf:0.90] [state:confirmed]

```
analyze-code-quality/
+-- skill.md
+-- README.md
+-- examples/
|   +-- example-basic.md
|   +-- example-advanced.md
+-- references/
|   +-- best-practices.md
+-- resources/
    +-- scripts/
        +-- analyze.py
```

### Orkestrasyon Becerisi (Tam)

[define|neutral] ORCHESTRATION_SKILL_STRUCTURE := {
  sablon_adi: "Orkestrasyon Beceri Yapisi",
  bagimliliklar: ["examples/", "references/", "resources/", "graphviz/", "tests/"]
} [ground:witnessed:orchestration-examples] [conf:0.90] [state:confirmed]

```
build-api-endpoint/
+-- skill.md
+-- README.md
+-- examples/
|   +-- example-get-endpoint.md
|   +-- example-post-endpoint.md
|   +-- example-complex-endpoint.md
+-- references/
|   +-- openapi-guide.md
|   +-- deployment-guide.md
|   +-- troubleshooting.md
+-- resources/
|   +-- scripts/
|   |   +-- generate-openapi.py
|   |   +-- validate-tests.sh
|   +-- templates/
|   |   +-- openapi-endpoint.yaml
|   |   +-- express-handler.js
|   |   +-- jest-test.js
|   +-- assets/
|       +-- api-architecture.png
+-- graphviz/
|   +-- orchestration-flow.dot
|   +-- agent-coordination.dot
+-- tests/
    +-- test-basic-endpoint.md
    +-- test-complex-endpoint.md
```

---

## Kalite Kontrolleri (Quality Checks)

<!-- [[MOR:root:K-L-T]] Kalite = root for quality-control-test -->
<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektiren kontroller -->

### Yapisal Dogrulama (Structural Validation)

[define|neutral] VALIDATION_CHECKS := {
  zorunlu_dosyalar: ["skill.md", "README.md"],
  zorunlu_dizinler: ["examples/"],
  kontroller: ["karsilikli_disayiricilik", "kapsamli_tamamlik"]
} [ground:witnessed:validation-scripts] [conf:0.90] [state:confirmed]

```python
# MECE uyumlulugunun kontrolu
required_files = ['skill.md', 'README.md']
required_dirs = ['examples/']

# Cakisma olmadigini dogrula
def check_mutually_exclusive():
    # graphviz/ disinda .dot dosyasi yok
    # resources/scripts/ disinda .py dosyasi yok
    # resources/templates/ disinda sablon yok
    pass

# Tamlik dogrula
def check_collectively_exhaustive():
    # Tum dosyalar kategorize edilmis
    # Kokte sahipsiz dosya yok
    pass
```

### Icerik Dogrulama (Content Validation)

```yaml
skill.md:
  - YAML on madde var
  - Emir kipi kullanilir
  - Kaynaklara dogru referans verilir

README.md:
  - Genel bakis bolumu
  - Hizli baslangic
  - Yapi aciklamasi

examples/:
  - En az 1 ornek
  - Gercek dunya senaryolari
  - Adim adim format
```

---

## Goc Rehberi (Migration Guide)

<!-- [[MOR:root:G-C-R]] Goc = root for migration-transition-guide -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Process is ongoing) -->

### Eski Becerileri MECE Yapisina Donusturme

[direct|neutral] Adim adim goc sureci [ground:witnessed:migration-process] [conf:0.88] [state:confirmed]

**Adim 1: Mevcut Dosyalari Belirle**
```bash
ls -la old-skill/
```

**Adim 2: Ture Gore Kategorize Et**
```bash
# Yeni yapi olustur
mkdir -p new-skill/{examples,references,resources/{scripts,templates,assets},graphviz,tests}

# Her dosyayi siniflandir
for file in old-skill/*; do
  case $file in
    *.dot) mv $file new-skill/graphviz/ ;;
    *.py) mv $file new-skill/resources/scripts/ ;;
    *.yaml) mv $file new-skill/resources/templates/ ;;
    example*) mv $file new-skill/examples/ ;;
    *) # Manuel olarak analiz et ;;
  esac
done
```

**Adim 3: Yapiyi Dogrula**
```bash
python skill-forge/resources/scripts/validate_skill.py new-skill/
```

---

## En Iyi Uygulamalar (Best Practices)

<!-- [[HON:sonkeigo]] Saygili rehberlik -->

### YAPIN

[assert|neutral] Yapilmasi gerekenler [ground:witnessed:best-practices] [conf:0.90] [state:confirmed]

- skill.md'yi talimatlara odakli tutun
- TUM ornekleri examples/'a koyun
- Aciklayici dosya adlari kullanin
- Adlandirma kurallarini takip edin
- Commit etmeden once dogrulayin

### YAPMAYIN

[assert|neutral] Kacinilmasi gerekenler [ground:witnessed:anti-patterns] [conf:0.90] [state:confirmed]

- Ayni dizinde icerik turlerini karistirmayin
- Derin ic ice yapilara girmeyin (max 3 seviye)
- Dosya adlarinda bosluk kullanmayin
- Betikleri kok dizine koymayin
- examples/ klasorunu atlamayin

---

## Sik Yapilan Hatalar (Common Mistakes)

<!-- [[MOR:root:H-T-A]] Hata = root for error-mistake-fault -->

### Cakisma Ihlalleri

[assert|neutral] Karsilikli disayiricilik ihlal ornekleri [ground:witnessed:error-patterns] [conf:0.88] [state:confirmed]

```
YANLIS: references/ icinde script.py
DOGRU: resources/scripts/ icinde script.py

YANLIS: example.md ile best-practices.md karisik
DOGRU: example.md examples/'da, best-practices.md references/'da

YANLIS: kok dizinde workflow.dot
DOGRU: graphviz/'de workflow.dot
```

### Eksiklik Ihlalleri

```
YANLIS: examples/ dizini yok
DOGRU: examples/'da en az 1 ornek

YANLIS: Kokte sahipsiz dosyalar
DOGRU: Tum dosyalar kategorize edilmis

YANLIS: Dagitilmis rastgele notlar
DOGRU: Notlar references/ veya examples/'da
```

---

## Dogrulama Protokolu (Verification Protocol)

<!-- [[EVD:-DI<gozlem>]] Gozlem tabanli dogrulama -->

[direct|emphatic] MECE yapisi tutarlilik, kesiflenilebilirlik ve surudurulebilirlik saglar [ground:witnessed:ecosystem-analysis] [conf:0.92] [state:confirmed]

### Kontrol Listesi

- [ ] Zorunlu dosyalar mevcut (skill.md, README.md)
- [ ] examples/ dizini en az 1 ornek iceriyor
- [ ] Icerik turleri dogru dizinlerde
- [ ] Dosya adlandirma kurallarina uyuluyor
- [ ] Cakisma yok (her dosya tek kategoride)
- [ ] Tamlik saglandi (sahipsiz dosya yok)

---

[commit|confident] <promise>FILE_STRUCTURE_STANDARDS_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
