# Test 1: Temel Ajan Olusturma (Basic Agent Creation)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[MOR:root:T-S-T]] test = examination/trial morpheme for validation -->
<!-- [[COM:Basis+Agent+Erstellungs+Test]] German compound: BasicAgentCreationTest -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## Test Hedefi (Test Objective)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Test amaci := {
  hedef: "4-faz SOP'nin minimal karmasiklikla temel ajan olusturabildigini dogrulamak",
  kapsam: "Mutlu yol senaryosu",
  onem: "Daha karmasik senaryolari test etmeden once temel islevselligin dogrulanmasi"
} [ground:test-specification] [conf:0.95] [state:confirmed]

---

## Test Ajani (Test Agent)
[[HON:teineigo]] [[EVD:-dir]] [[ASP:ipf]] [[CLS:ge-abstract]]

[define|neutral] Test ajani spesifikasyonu := {
  isim: "file-organizer",
  alan: "Dosya sistemi islemleri ve organizasyonu",
  karmasiklik: "Dusuk (tek alan, basit komutlar)"
} [ground:agent-specification] [conf:0.95] [state:confirmed]

---

## Test Senaryosu (Test Scenario)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

### Faz 1: Baslangic Analizi ve Niyet Cozumleme (Initial Analysis)

[assert|neutral] Faz 1 beklenen girisler := {
  problem: "Dosyalari ture, tarihe veya ozel kurallara gore dizinlerde organize etmek",
  anahtar_zorluklar: [
    "Birden fazla dosya turunu isleme",
    "Dosya catismalarindan kacinma",
    "Dosya meta verilerini koruma",
    "Sembolik baglantilari isleme",
    "Buyuk dizinlerle basima"
  ],
  teknoloji_yigini: ["Python", "os", "shutil", "pathlib"],
  mcp_sunuculari: ["Claude Flow (koordinasyon icin)"]
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 1 beklenen ciktilar := {
  ciktilar: [
    "Alan analizi belgesi",
    "Teknoloji yigini envanteri",
    "Entegrasyon gereksinimleri"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 1 dogrulama kontrolleri := {
  kontroller: [
    "Tum Faz 1 dogrulama kapilari gecti",
    "5+ anahtar zorluk belirlendi",
    "Teknoloji yigini kapsamli"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 2: Meta-Bilissel Cikarim (Meta-Cognitive Extraction)

[assert|neutral] Faz 2 beklenen girisler := {
  uzmanlik_alanlari: ["Dosya sistemleri", "Desen eslestirme", "Hata isleme"],
  karar_cerceveleri: [
    "Dosya varsa, ustune yazmadan once catismalari kontrol et",
    "Her zaman zaman damgalari ve izinleri koru",
    "Onay almadan asla silme"
  ],
  kalite_standartlari: "Sifir veri kaybi, ongordulabilir organizasyon"
} [ground:test-input] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 beklenen ciktilar := {
  ciktilar: [
    "Ajan spesifikasyon belgesi",
    "Iyi/kotu ornekler",
    "Kenar durumlar (bos dosyalar, ozel karakterler, vb.)"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 dogrulama kontrolleri := {
  kontroller: [
    "3+ uzmanlik alani belirlendi",
    "5+ karar bulussal kurali belgelendi",
    "Ornekler kalite standartlarini gosteriyor"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 3: Ajan Mimari Tasarimi (Agent Architecture Design)

[assert|neutral] Faz 3 beklenen ciktilar := {
  temel_prompt_icerikleri: [
    "Cekirdek Kimlik bolumu",
    "Evrensel komutlar (file-read, file-write, glob, grep)",
    "Uzman komutlari (/organize, /classify, /batch-move)",
    "Bilissel cerceve (oz-tutarlilik kontrolleri)",
    "Koruma raylari (yedeksiz ustune yazma yok)",
    "2+ is akisi ornegi"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 3 dogrulama kontrolleri := {
  kontroller: [
    "Sistem prompti sablon yapisini takip ediyor",
    "Kanit-tabanli teknikler entegre edilmis",
    "Is akisi ornekleri tam komutlar iceriyor"
  ]
} [ground:validation-gate] [conf:0.90] [state:confirmed]

### Faz 4: Teknik Gelistirme (Bu test icin manuel)

[assert|neutral] Faz 4 beklenen ciktilar := {
  gelistirilmis_prompt_v2_icerikleri: [
    "Tam dosya isleme desenleri",
    "Hata tespit kodu",
    "MCP entegrasyon ornekleri",
    "Performans metrikleri izleme"
  ]
} [ground:expected-output] [conf:0.92] [state:confirmed]

---

## Test Yurutme (Test Execution)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### Kurulum

[assert|neutral] Test kurulum komutu := {
  komut: "python 4_phase_sop.py --agent-name file-organizer --mode interactive --phase 1",
  calisma_dizini: "C:\\Users\\17175\\claude-code-plugins\\ruv-sparc-three-loop-system\\skills\\agent-creator\\resources\\scripts"
} [ground:test-setup] [conf:0.90] [state:confirmed]

### Faz 1 Yurutme

[direct|neutral] Faz 1 testi := {
  islem: "Faz 1'i hazirlanmis girislerle calistir",
  dogrulama: "Cikti dosyalarinin var oldugunu ve beklenen yapida icerdiklerini dogrula"
} [ground:test-step] [conf:0.88] [state:confirmed]

### Faz 2 Yurutme

[assert|neutral] Faz 2 komutu := {
  komut: "python 4_phase_sop.py --agent-name file-organizer --mode interactive --phase 2",
  dogrulama: "Spesifikasyon belgesi kalitesini dogrula"
} [ground:test-step] [conf:0.88] [state:confirmed]

### Faz 3 Yurutme

[assert|neutral] Faz 3 komutu := {
  komut: "python 4_phase_sop.py --agent-name file-organizer --mode interactive --phase 3",
  dogrulama: "Temel prompti sablona karsi dogrula"
} [ground:test-step] [conf:0.88] [state:confirmed]

### Dogrulama

[assert|neutral] Dogrulama komutu := {
  komut: "bash ../scripts/validate_prompt.sh agent-outputs/file-organizer/file-organizer-base-prompt-v1.md",
  beklenen: "Skor >= 70%"
} [ground:validation-step] [conf:0.90] [state:confirmed]

### Test

[assert|neutral] Test komutu := {
  komut: "python ../scripts/test_agent.py --agent file-organizer --test-suite basic",
  beklenen: "80%+ testler gecti"
} [ground:test-step] [conf:0.90] [state:confirmed]

---

## Basari Kriterleri (Success Criteria)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Basari kontrol listesi := {
  kriterler: [
    "Tum 3 faz hatasiz tamamlandi",
    "Faz 1 dogrulama kapilari gecti",
    "Faz 2 dogrulama kapilari gecti",
    "Faz 3 prompt dogrulama skoru >= 70%",
    "Temel test paketi >= 80% gecti",
    "Cikti dosyalari duzgun yapilandirilmis",
    "Ajan spesifikasyonu acik ve tam",
    "Sistem prompti sablonu takip ediyor"
  ]
} [ground:acceptance-criteria] [conf:0.92] [state:confirmed]

---

## Beklenen Sure (Expected Duration)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Sure tahmini := {
  faz_1: "15-20 dakika (basitlestirilmis alan)",
  faz_2: "15-20 dakika",
  faz_3: "10-15 dakika",
  toplam: "40-55 dakika"
} [ground:time-estimate] [conf:0.85] [state:confirmed]

---

## Notlar (Notes)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

[assert|neutral] Test notu := {
  aciklama: "Bu test, net sinirlari ve iyi tanimlanmis islemleri olan basit bir ajanla 'mutlu yolu' dogrular",
  amac: "Daha karmasik senaryolari test etmeden once 4-faz SOP'nin temel durumlar icin calistigini gostermek"
} [ground:test-documentation] [conf:0.88] [state:confirmed]

---

<promise>TEST_1_BASIC_AGENT_VCL_V3.1.1_VERIX_COMPLIANT</promise>
