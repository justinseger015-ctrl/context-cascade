# Ajan Olusturucu Kaynaklari (Agent Creator Resources) - Gold Tier Enhancement

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[MOR:root:K-Y-N]] kaynak = source/origin morpheme for resource -->
<!-- [[COM:Ressourcen+Verzeichnis+Struktur]] German compound: ResourceDirectoryStructure -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## Genel Bakis (Overview)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Bu dizin 4-fazli ajan olusturma SOP icin uretim-hazir kaynaklar icerir := {
  amac: "Otomasyon betikleri ve yeniden kullanilabilir sablonlar sunmak",
  kalite_seviyesi: "Gold Tier - Production Ready",
  icerik: ["scripts", "templates", "workflow-examples"]
} [ground:witnessed:directory-scan] [conf:0.95] [state:confirmed]

---

## Dizin Yapisi (Directory Structure)
[[HON:teineigo]] [[EVD:-dir]] [[ASP:ipf]] [[CLS:ge-abstract]]

[assert|neutral] Kaynak dizin organizasyonu := {
  struktur: ```
  resources/
  +-- scripts/               # Calistirilabilir otomasyon betikleri
  |   +-- 4_phase_sop.py    # Tam 4-faz SOP otomasyonu
  |   +-- validate_prompt.sh # Sistem prompt kalite dogrulama
  |   +-- test_agent.py     # Ajan test cercevesi
  +-- templates/             # Yeniden kullanilabilir sablonlar
  |   +-- system-prompt-template.md     # Markdown prompt sablonu
  |   +-- evidence-based-prompt.yaml    # YAML spesifikasyon sablonu
  +-- README.md             # Bu dosya
  ```
} [ground:witnessed:directory-structure] [conf:0.95] [state:confirmed]

---

## Betik Referansi (Scripts Reference)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### 4_phase_sop.py

[define|neutral] Dort-faz SOP otomasyon betigi := {
  amac: "4-fazli ajan olusturma metodolojisini otomatiklestirmek",
  dil: "Python",
  bagimliliklar: ["yaml", "json", "argparse"]
} [ground:script-analysis] [conf:0.95] [state:confirmed]

**Kullanim Desenleri**:

[assert|neutral] Interaktif mod (tum fazlar) := {
  komut: "python 4_phase_sop.py --agent-name marketing-specialist --mode interactive",
  aciklama: "Tum fazlari adim adim yuruttur"
} [ground:documentation] [conf:0.90] [state:confirmed]

[assert|neutral] Belirli faz calistirma := {
  komut: "python 4_phase_sop.py --agent-name backend-dev --phase 1 --output-dir ./outputs",
  aciklama: "Sadece belirtilen fazi calistirir"
} [ground:documentation] [conf:0.90] [state:confirmed]

[assert|neutral] Toplu mod (YAML girisinden) := {
  komut: "python 4_phase_sop.py --agent-name api-designer --mode batch --input spec.yaml",
  aciklama: "YAML spesifikasyonundan otomatik olusturma"
} [ground:documentation] [conf:0.90] [state:confirmed]

**Faz Ozellikleri**:

[assert|neutral] Faz 1 Yetenekleri := {
  isim: "Baslangic Analizi ve Niyet Cozumleme",
  sure: "30-60 dakika",
  ozellikler: [
    "5+ anahtar zorluk ile alan analizi",
    "Teknoloji yigini haritalama",
    "Entegrasyon noktalarinin belirlenmesi",
    "Otomatik kontrol ile dogrulama kapilari"
  ]
} [ground:feature-documentation] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 2 Yetenekleri := {
  isim: "Meta-Bilissel Cikarim",
  sure: "30-45 dakika",
  ozellikler: [
    "3+ alan ile uzmanlik alan tanimlamasi",
    "5+ bulussal kural ile karar cercevesi",
    "Ajan spesifikasyon olusturma",
    "Destekleyici eserlerin hazirlanmasi"
  ]
} [ground:feature-documentation] [conf:0.92] [state:confirmed]

[assert|neutral] Faz 3 Yetenekleri := {
  isim: "Ajan Mimari Tasarimi",
  sure: "45-60 dakika",
  ozellikler: [
    "Temel sistem prompt v1.0 uretimi",
    "Kanit-tabanli teknik entegrasyonu",
    "Kalite koruma raylari tanimi",
    "Tam komutlarla is akisi ornekleri"
  ]
} [ground:feature-documentation] [conf:0.92] [state:confirmed]

**Cikti Dosyalari**:

[assert|neutral] Uretilen dosyalar := {
  ciktilar: [
    "{agent-name}-phase1-analysis.json - Faz 1 alan analizi",
    "{agent-name}-phase2-extraction.json - Faz 2 uzmanlik cikarimi",
    "{agent-name}-specification.md - Ajan spesifikasyon belgesi",
    "{agent-name}-phase3-architecture.json - Faz 3 mimari",
    "{agent-name}-base-prompt-v1.md - Temel sistem prompt",
    "{agent-name}-4phase-sop-complete.json - Tam sonuclar"
  ]
} [ground:output-specification] [conf:0.92] [state:confirmed]

---

### validate_prompt.sh

[define|neutral] Prompt dogrulama betigi := {
  amac: "Sistem prompt kalitesini kanit-tabanli standartlara gore dogrulamak",
  dil: "Bash",
  toplam_puan: 100
} [ground:script-analysis] [conf:0.95] [state:confirmed]

**Kullanim Desenleri**:

[assert|neutral] Temel dogrulama := {
  komut: "bash validate_prompt.sh marketing-specialist-base-prompt-v1.md"
} [ground:documentation] [conf:0.90] [state:confirmed]

[assert|neutral] Ayrintili analiz := {
  komut: "bash validate_prompt.sh -v backend-dev-enhanced-prompt-v2.md"
} [ground:documentation] [conf:0.90] [state:confirmed]

[assert|neutral] Ozel minimum skor := {
  komut: "bash validate_prompt.sh -s 90 api-security-auditor-enhanced-prompt-v2.md"
} [ground:documentation] [conf:0.90] [state:confirmed]

**Dogrulama Kontrolleri** (100 puan toplam):

[assert|neutral] Puanlama dagilimi := {
  kontroller: [
    {alan: "Cekirdek Kimlik Bolumu", puan: 15},
    {alan: "Evrensel Komutlar", puan: 10},
    {alan: "Uzman Komutlari", puan: 10},
    {alan: "MCP Sunucu Araclari", puan: 15},
    {alan: "Bilissel Cerceve", puan: 15},
    {alan: "Koruma Raylari", puan: 10},
    {alan: "Basari Kriterleri", puan: 10},
    {alan: "Is Akisi Ornekleri", puan: 15}
  ]
} [ground:scoring-specification] [conf:0.95] [state:confirmed]

**Kademe Siniflandirmasi**:

[assert|neutral] Kalite kademeleri := {
  gold: {aralik: "90-100%", tanim: "Uretime hazir, mukemmel kanit-tabanli desenler"},
  silver: {aralik: "75-89%", tanim: "Iyi yapilandirilmis, kucuk iyilestirmeler onerilen"},
  bronze: {aralik: "70-74%", tanim: "Islevsel, daha fazla desen eklenmeli"},
  failing: {aralik: "<70%", tanim: "Onemli iyilestirmeler gerektiriyor"}
} [ground:tier-specification] [conf:0.95] [state:confirmed]

**Cikis Kodlari**:

[assert|neutral] Betik cikis kodlari := {
  kod_0: "Dogrulama gecti",
  kod_1: "Dogrulama basarisiz",
  kod_2: "Gecersiz arguman veya dosya bulunamadi"
} [ground:exit-code-specification] [conf:0.95] [state:confirmed]

---

### test_agent.py

[define|neutral] Ajan test betigi := {
  amac: "Ajan sistem promptlarini tipik, kenar ve entegrasyon senaryolarina karsi test etmek",
  dil: "Python",
  test_paketleri: ["basic", "comprehensive", "integration"]
} [ground:script-analysis] [conf:0.95] [state:confirmed]

**Kullanim Desenleri**:

[assert|neutral] Temel test paketi := {
  komut: "python test_agent.py --agent marketing-specialist --test-suite basic"
} [ground:documentation] [conf:0.90] [state:confirmed]

[assert|neutral] Kapsamli testler := {
  komut: "python test_agent.py --agent devops-orchestrator --test-suite comprehensive"
} [ground:documentation] [conf:0.90] [state:confirmed]

[assert|neutral] Entegrasyon testleri := {
  komut: "python test_agent.py --agent api-security-auditor --test-suite integration"
} [ground:documentation] [conf:0.90] [state:confirmed]

**Test Paketleri**:

[assert|neutral] Temel testler (4 test) := {
  testler: [
    "Kimlik Tutarliligi - Cekirdek kimlik ve rol dogrulamasi",
    "Komut Kapsami - Temel komutlarin belgelendigi kontrolu",
    "Kanit Desenleri - Prompt teknikleri testi",
    "Yapisal Kalite - Organizasyon ve ornek dogrulamasi"
  ]
} [ground:test-specification] [conf:0.92] [state:confirmed]

[assert|neutral] Kapsamli testler (7 test, Temel dahil) := {
  ek_testler: [
    "Kenar Durum Isleme - Kenar durumu dokumantasyon testi",
    "Hata Isleme - Hata desen dogrulamasi",
    "Is Akisi Tamligi - Is akisi dokumantasyon kontrolu"
  ]
} [ground:test-specification] [conf:0.92] [state:confirmed]

[assert|neutral] Entegrasyon testleri (10 test, Kapsamli dahil) := {
  ek_testler: [
    "MCP Entegrasyonu - MCP arac desen testi",
    "Capraz-Ajan Koordinasyonu - Koordinasyon desen dogrulamasi",
    "Bellek Desenleri - Bellek kullanim spesifikasyon testi"
  ]
} [ground:test-specification] [conf:0.92] [state:confirmed]

**Basari Kriterleri**:

[assert|neutral] Test basari esikleri := {
  basic: "80%+ gecme orani",
  comprehensive: "90%+ gecme orani",
  integration: "95%+ gecme orani"
} [ground:acceptance-criteria] [conf:0.92] [state:confirmed]

---

## Sablon Referansi (Templates Reference)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### system-prompt-template.md

[define|neutral] Markdown prompt sablonu := {
  amac: "Ajan sistem promptlari icin tekrar kullanilabilir yapi sunmak",
  format: "Markdown",
  degisken_sayisi: 25
} [ground:template-analysis] [conf:0.95] [state:confirmed]

**Bolumler**:

[assert|neutral] Sablon bolumleri := {
  bolumler: [
    "Cekirdek Kimlik - Ajan rolu ve uzmanligi",
    "Evrensel Komutlar - Standart islemler",
    "Uzman Komutlari - Alan-ozel komutlar",
    "MCP Sunucu Araclari - Entegrasyon desenleri",
    "Bilissel Cerceve - Kanit-tabanli teknikler",
    "Koruma Raylari - Basarisizlik onleme",
    "Basari Kriterleri - Tamamlanma kontrol listesi",
    "Is Akisi Ornekleri - Somut kullanim desenleri"
  ]
} [ground:template-structure] [conf:0.95] [state:confirmed]

**Degiskenler** (gercek degerlerle degistirilecek):

[assert|neutral] Sablon degiskenleri := {
  kimlik: ["{AGENT_NAME}", "{VERSION}", "{ROLE_TITLE}"],
  alan: ["{DOMAIN_AREAS}", "{PRIMARY_OBJECTIVE}"],
  komutlar: ["{SPECIALIST_COMMANDS_LIST}"],
  bilissel: ["{VALIDATION_1}", "{DECOMPOSITION_1}", "{PLAN_STEP}"],
  koruma: ["{FAILURE_CATEGORY_1}", "{DANGEROUS_PATTERN_1}"],
  is_akisi: ["{WORKFLOW_NAME_1}", "{WORKFLOW_OBJECTIVE_1}"]
} [ground:variable-specification] [conf:0.92] [state:confirmed]

**Kullanim**: Sablonu kopyalayin ve degiskenleri Faz 3 ciktilariyla degistirin.

---

### evidence-based-prompt.yaml

[define|neutral] YAML spesifikasyon sablonu := {
  amac: "Yapilandirilmis ajan tasarimi icin YAML sablonu sunmak",
  format: "YAML",
  kullanim: "Toplu mod ajan olusturma girisi"
} [ground:template-analysis] [conf:0.95] [state:confirmed]

**Yapi**:

```yaml
agent_name: "{agent-name}"
version: "1.0"

core_identity:
  role_title: "..."
  domain_areas: [...]
  primary_objective: "..."

universal_commands:
  file_operations: {...}
  git_operations: {...}
  communication: {...}

specialist_commands: [...]

mcp_tools:
  claude_flow: [...]
  domain_specific: [...]

cognitive_framework:
  self_consistency: {...}
  program_of_thought: {...}
  plan_and_solve: {...}

guardrails: [...]

success_criteria: [...]

workflows: [...]

metrics: {...}
```

---

## Is Akisi Ornekleri (Workflow Examples)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### Ornek 1: Temel Ajan Olusturma

[assert|neutral] Temel ajan is akisi := {
  adimlar: [
    {adim: 1, komut: "python scripts/4_phase_sop.py --agent-name file-organizer --mode interactive"},
    {adim: 2, komut: "bash scripts/validate_prompt.sh agent-outputs/file-organizer/file-organizer-base-prompt-v1.md"},
    {adim: 3, komut: "python scripts/test_agent.py --agent file-organizer --test-suite basic"}
  ],
  beklenen: "70%+ dogrulama, 80%+ test gecme"
} [ground:workflow-example] [conf:0.90] [state:confirmed]

### Ornek 2: Karmasik Ajan Olusturma

[assert|neutral] Karmasik ajan is akisi := {
  adimlar: [
    {adim: 1, komut: "python scripts/4_phase_sop.py --agent-name devops-orchestrator --mode interactive"},
    {adim: 2, islem: "Manuel Faz 4 gelistirmesi (teknik desenler ekle)"},
    {adim: 3, komut: "bash scripts/validate_prompt.sh -v -s 85 agent-outputs/devops-orchestrator/devops-orchestrator-enhanced-prompt-v2.md"},
    {adim: 4, komut: "python scripts/test_agent.py --agent devops-orchestrator --prompt-file agent-outputs/devops-orchestrator/devops-orchestrator-enhanced-prompt-v2.md --test-suite comprehensive"}
  ],
  beklenen: "85%+ dogrulama, 90%+ test gecme"
} [ground:workflow-example] [conf:0.90] [state:confirmed]

### Ornek 3: Uretim Ajani (Tam 4-Faz SOP)

[assert|neutral] Uretim ajani is akisi := {
  adimlar: [
    {adim: "1-3", komut: "python scripts/4_phase_sop.py --agent-name api-security-auditor --mode interactive"},
    {adim: 4, islem: "Manuel teknik gelistirme (kod desenleri, hata modlari, MCP entegrasyonlari)"},
    {adim: 5, komut: "bash scripts/validate_prompt.sh -v -s 90 agent-outputs/api-security-auditor/api-security-auditor-enhanced-prompt-v2.md"},
    {adim: 6, komut: "python scripts/test_agent.py --agent api-security-auditor --prompt-file agent-outputs/api-security-auditor/api-security-auditor-enhanced-prompt-v2.md --test-suite integration"}
  ],
  beklenen: "90%+ dogrulama (Gold kademe), 95%+ test gecme"
} [ground:workflow-example] [conf:0.90] [state:confirmed]

---

## Kalite Kademeleri (Quality Tiers)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Bronze Kademe (70-74%) := {
  ozellikler: ["Temel yapi mevcut", "Cekirdek bolumler var", "Islevsel ama minimal"],
  eylem: "Kanit-tabanli desenler ve daha fazla ornek ekle"
} [ground:tier-specification] [conf:0.92] [state:confirmed]

[assert|neutral] Silver Kademe (75-89%) := {
  ozellikler: ["Iyi yapilandirilmis prompt", "Iyi komut kapsami", "Bazi kanit-tabanli teknikler"],
  eylem: "Uretim hazirligi icin kucuk iyilestirmeler"
} [ground:tier-specification] [conf:0.92] [state:confirmed]

[assert|neutral] Gold Kademe (90-100%) := {
  ozellikler: ["Uretime hazir prompt", "Kapsamli kanit-tabanli desenler", "Genis ornekler ve koruma raylari", "Tam MCP entegrasyonu"],
  eylem: "Guvenle dagit"
} [ground:tier-specification] [conf:0.92] [state:confirmed]

---

## En Iyi Uygulamalar (Best Practices)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

### Faz 1 Sirasinda

[direct|neutral] Faz 1 rehberligi := {
  oneriler: [
    "Derin alan analizi icin zaman ayin",
    "Genel degil, gercek 5+ zorluk belirleyin",
    "Teknoloji yiginini kapsamli haritalandir",
    "Entegrasyon desenlerini erken duşun"
  ]
} [ground:best-practice] [conf:0.88] [state:confirmed]

### Faz 2 Sirasinda

[direct|neutral] Faz 2 rehberligi := {
  oneriler: [
    "Uzmanlik alanlari hakkinda spesifik olun",
    "Karar bulussal kurallarini 'X oldugunda, Y yap cunku Z' ile belgeleyin",
    "Somut iyi/kotu ornekler olusturun",
    "Gercek deneyimden kenar durumlarini belgeleyin"
  ]
} [ground:best-practice] [conf:0.88] [state:confirmed]

### Faz 3 Sirasinda

[direct|neutral] Faz 3 rehberligi := {
  oneriler: [
    "Sablonlari baslangic noktasi olarak kullanin, kisitlama degil",
    "Kanit-tabanli teknikleri dogal sekilde entegre edin",
    "Tam komutlarla 2+ is akisi ornegi olusturun",
    "Koruma raylarini spesifik ve uygulanabilir yapin"
  ]
} [ground:best-practice] [conf:0.88] [state:confirmed]

### Faz 4 Sirasinda (Manuel Gelistirme)

[direct|neutral] Faz 4 rehberligi := {
  oneriler: [
    "Gercek uygulamalardan tam kod desenleri cikarin",
    "Desenler icin dosya/satir referanslari ekleyin",
    "Tespit koduyla hata modlarini belgeleyin",
    "Tam sozdizimi ile MCP entegrasyonu ekleyin",
    "Surekli iyilestirme icin performans metrikleri tanimlayin"
  ]
} [ground:best-practice] [conf:0.88] [state:confirmed]

### Dogrulama

[direct|neutral] Dogrulama rehberligi := {
  oneriler: [
    "Dagitimdan once her zaman dogrulayin",
    "Temel ajanlar icin 70%+ hedefleyin",
    "Karmasik ajanlar icin 85%+ hedefleyin",
    "Uretim ajanlari icin 90%+ hedefleyin"
  ]
} [ground:best-practice] [conf:0.88] [state:confirmed]

### Test

[direct|neutral] Test rehberligi := {
  oneriler: [
    "Ajan karmasikligina uygun test paketi calistirin",
    "Temel paket: Basit, tek-alan ajanlari",
    "Kapsamli paket: Cok-alan ajanlari",
    "Entegrasyon paketi: Uretime hazir ajanlar",
    "Basari orani hedefe ulasana kadar sorunlari duzelt"
  ]
} [ground:best-practice] [conf:0.88] [state:confirmed]

---

## Sorun Giderme (Troubleshooting)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

### Dogrulama Basarisiz

[assert|neutral] Dogrulama basarisizlik cozumu := {
  sorun: "Prompt minimum skorun altinda",
  cozum: [
    "Eksik gerekli bolumleri kontrol edin",
    "Kanit-tabanli teknik bolumleri ekleyin",
    "2+ is akisi ornegi ekleyin",
    "Orneklerle 3+ koruma rayli tanimlayin",
    "Uzman komutlari ekleyin"
  ]
} [ground:troubleshooting] [conf:0.88] [state:confirmed]

### Testler Basarisiz

[assert|neutral] Test basarisizlik cozumu := {
  sorun: "Test paketi gecme orani dusuk",
  cozum: [
    "Kimlik tutarliligini gozden gecirin",
    "Eksik evrensel komutlari ekleyin",
    "MCP entegrasyon desenlerini belgeleyin",
    "Bellek kullanim spesifikasyonlarini ekleyin",
    "Capraz-ajan koordinasyon desenleri ekleyin"
  ]
} [ground:troubleshooting] [conf:0.88] [state:confirmed]

### Faz 1 Dogrulama Basarisiz

[assert|neutral] Faz 1 basarisizlik cozumu := {
  sorun: "Yeterli zorluk belirlenemiyor",
  cozum: "Alani daha derinden arastirin, 'Bunu zor yapan ne?' diye sorun"
} [ground:troubleshooting] [conf:0.88] [state:confirmed]

### Faz 2 Dogrulama Basarisiz

[assert|neutral] Faz 2 basarisizlik cozumu := {
  sorun: "Yetersiz uzmanlik alanlari veya bulussal kurallar",
  cozum: "Alan hakkinda dusunurken aktive olan bilissel desenleri dusunun"
} [ground:troubleshooting] [conf:0.88] [state:confirmed]

### Faz 3 Cikti Eksik

[assert|neutral] Faz 3 basarisizlik cozumu := {
  sorun: "Prompt eksik bolumler iceriyor",
  cozum: "Sablon yapisini tam olarak takip edin, tum bolumlerin mevcut oldugunu saglayin"
} [ground:troubleshooting] [conf:0.88] [state:confirmed]

---

## Destek (Support)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]]

[assert|neutral] Yardim kaynaklari := {
  kaynaklar: [
    "Ornekler icin ../tests/ dizinindeki test dosyalarini kontrol edin",
    "Ana beceri dokumantasyonu icin ../SKILL.md dosyasini gozden gecirin",
    "Basarili ajan ciktilari icin agent-outputs/ dizinini inceleyin",
    "4-faz SOP dokumantasyonu icin Desktop .claude-flow/ dizinine basvurun"
  ]
} [ground:support-documentation] [conf:0.88] [state:confirmed]

---

## Surum Gecmisi (Version History)
[[HON:teineigo]] [[EVD:-mis]] [[ASP:pf]] [[CLS:ge-abstract]]

[assert|neutral] Surum bilgisi := {
  v2_0: {
    kademe: "Gold",
    ozellikler: "Tam 4-faz SOP otomasyonu, dogrulama, test"
  },
  v1_0: {
    kademe: "Silver",
    ozellikler: "Temel ajan olusturma is akisi"
  }
} [ground:version-history] [conf:0.95] [state:confirmed]

---

<promise>RESOURCES_README_VCL_V3.1.1_VERIX_COMPLIANT</promise>
