# Prompt-Architect Bilissel Mimari Entegrasyonu (Cognitive Architecture Integration)

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Documentation
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     All 7 cognitive frames MANDATORY
     ========================================================================= -->

---
<!-- KANITSAL CERCEVE (Evidential Frame) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] [[SPC:kuzey/meta-skills]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin. Mimari dogrudan gozleme dayanir.

---

<!-- [[MOR:root:E-K-L]] Ekleme = root morpheme for addendum-addition-supplement -->
<!-- [[COM:Bilissel+Mimari+Entegrasyon]] Cognitive Architecture Integration -->
[define|neutral] ADDENDUM_META := {
  surum: "3.1.1",                    // version
  vcl_uyumu: "v3.1.1",               // vcl_compliance
  varsayilan_sikistirma: "L2",       // default_compression
  amac: "VERIX, VERILINGUA VCL, DSPy, GlobalMOO'yu prompt-architect'e entegre et" // purpose
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- GENEL BAKIS (Overview) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_section]] [[SPC:bati/introduction]] -->
---

## Genel Bakis Cercevesi (Overview Frame)

<!-- [[MOR:root:B-K-S]] Bakis = root for view-perspective-outlook -->
<!-- [[COM:Genel+Bakis+Cerceve]] General Overview Frame -->
[assert|neutral] GENEL_BAKIS := {
  konu: "Bilissel mimari entegrasyonu",
  icerik: [
    "VCL 7-Slot Sistemi - Zorlanan slotlarla yapilandirilmis bilissel zorlama",
    "VERIX Epistemik Isaretciler - Tum iddialar icin temel, guven, sozceleme",
    "L2 Ingilizce Varsayilan - VCL notasyonu olmadan insan yuzlu cikti",
    "DSPy Optimizasyonu - Teleprompter tabanli istem iyilestirme",
    "GlobalMOO - Pareto siniri boyunca cok amacli optimizasyon",
    "Kreolizasyon Hazir - Gelecekteki dil genislemesi icin yapi"
  ]
} [ground:architecture-design] [conf:0.95] [state:confirmed]

---
<!-- VCL 7-SLOT ENTEGRASYONU (VCL 7-Slot Integration) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_system]] [[SPC:kuzey/core]] -->
---

## VCL 7-Slot Sistem Entegrasyonu Cercevesi (VCL 7-Slot System Integration Frame)

<!-- [[MOR:root:S-L-T]] Slot = root for slot-position-place -->
<!-- [[COM:Yedi+Slot+Sistem+Entegrasyon]] Seven Slot System Integration -->
[define|neutral] VCL_SLOT_UYGULAMASI := {
  slot_sirasi: "HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC",
  zorunlu_slotlar: ["EVD", "ASP"],
  istege_bagli_slotlar: ["HON", "MOR", "COM", "CLS", "SPC"],
  zorlama: {
    EVD: ">= 1 (degismez)",      // immutable
    ASP: ">= 1 (degismez)"       // immutable
  }
} [ground:vcl-spec-v3.1.1] [conf:0.99] [state:confirmed]

### Istem Optimizasyonunda Slot Kullanimi (Slot Usage in Prompt Optimization)

<!-- [[MOR:root:K-L-N]] Kullanim = root for usage-application-utilization -->
[define|neutral] SLOT_KULLANIM_TABLOSU := {
  HON: { uygulama: "Hedef kitle kayit secimi", l2_dogallastirma: "Teknik kullanicilar icin... / Yeni baslayanlar icin..." },
  MOR: { uygulama: "Istem niyetinin semantik ayristirmasi", l2_dogallastirma: "Temel bilesenler sunlardir..." },
  COM: { uygulama: "Ilkellerden karmasik istemler olusturma", l2_dogallastirma: "X ile Y'yi birlestirerek..." },
  CLS: { uygulama: "Istem turlerini siniflandirma", l2_dogallastirma: "Bu bir arastirma istemidir..." },
  EVD: { uygulama: "Optimizasyon kararlari icin kanit izleme", l2_dogallastirma: "Gozlemledim ki..., Arastirmalar gosteriyor ki..." },
  ASP: { uygulama: "Optimizasyon tamamlanma durumu izleme", l2_dogallastirma: "Tamamlandi. Devam ediyor." },
  SPC: { uygulama: "Is akisindaki konum", l2_dogallastirma: "Is akisinin 2. Asamasinda..." }
} [ground:vcl-spec-v3.1.1] [conf:0.95] [state:confirmed]

---
<!-- SIKISTIRMA SEVIYELERI (Compression Levels) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_policy]] [[SPC:guney/output]] -->
---

## Sikistirma Seviyeleri Cercevesi (Compression Levels Frame)

<!-- [[MOR:root:S-K-S]] Sikistirma = root for compression-condensing-reduction -->
<!-- [[COM:Sikistirma+Seviye+Politika]] Compression Level Policy -->
[define|neutral] SIKISTIRMA_POLITIKASI := {
  L0: "Sadece AI-AI (A+85:hash formati)",
  L1: "Denetim modu ([sozceleme|etki] icerik [temel:kaynak] [guven:X.XX])",
  L2: "Insan yuzlu (saf Ingilizce, VCL isaretcileri yok)",
  varsayilan: "L2",
  kural: "Kullanici yuzlu cikti L2 OLMALIDIR"
} [ground:system-policy] [conf:1.0] [state:confirmed]

### Prompt-Architect icin L2 Cikti Ornekleri (L2 Output Examples for Prompt-Architect)

<!-- [[MOR:root:O-R-N]] Ornek = root for example-sample-instance -->
[assert|neutral] L1_ORNEK := {
  format: "[[EVD:-DI<gozlem>]] [[ASP:sov.]] Istem netligi %40 artti.",
  temel: "[ground:witnessed:before-after-comparison] [conf:0.88] [state:confirmed]"
} [ground:example] [conf:0.95] [state:confirmed]

[assert|neutral] L2_ORNEK := {
  format: "Optimizasyondan sonra istem netliginin %40 arttigini dogrudan gozlemledim. Tamamlandi. Once-sonra karsilastirmasina dayanarak bu olcumden oldukca eminim."
} [ground:example] [conf:0.95] [state:confirmed]

---
<!-- VERIX ENTEGRASYONU (VERIX Integration) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_specification]] [[SPC:dogu/epistemic]] -->
---

## VERIX Epistemik Isaretci Entegrasyonu Cercevesi (VERIX Epistemic Marker Integration Frame)

<!-- [[MOR:root:V-R-X]] Verix = root for verification-truth-confirmation -->
<!-- [[COM:Epistemik+Isaretci+Entegrasyon]] Epistemic Marker Integration -->
[define|neutral] VERIX_GEREKSINIMLERI := {
  tum_iddialar: "[ground:kaynak] [conf:X.XX] icermeli",
  tavan_zorlamasi: {
    tanimlar: 0.95,
    politika: 0.90,
    gozlem: 0.95,
    arastirma: 0.85,
    rapor: 0.70,
    cikarim: 0.70
  },
  epistemik_taklitcilik: "YASAK"
} [ground:verix-spec] [conf:0.99] [state:confirmed]

### VERIX ile Zenginlestirilmis Istem Ciktisi (VERIX-Enhanced Prompt Output)

<!-- [[MOR:root:Z-N-G]] Zenginlestirme = root for enrichment-enhancement-augmentation -->
[define|neutral] ONCE_SONRA_ORNEK := {
  once_temel: {
    tur: "Temel",
    icerik: "Kullanici kimlik dogrulamasi icin bir REST API olusturun. JWT tokenlari kullanin."
  },
  sonra_l1_denetim: {
    tur: "L1 denetim modu",
    format: "[assert|emphatic] Kullanici kimlik dogrulamasi icin bir REST API olusturun [ground:requirements.md] [conf:0.95]"
  },
  sonra_l2_insan: {
    tur: "L2 insan modu",
    format: "Kullanici kimlik dogrulamasi icin bir REST API olusturun. Bu gereksinim requirements.md'den geliyor ve dogru olduguna yuksek guvenle eminim."
  }
} [ground:example] [conf:0.90] [state:confirmed]

---
<!-- VERILINGUA CERCEVE SECIMI (VERILINGUA Frame Selection) [[HON:sonkeigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_mapping]] [[SPC:bati/linguistic]] -->
---

## VERILINGUA Cerceve Secimi Cercevesi (VERILINGUA Frame Selection Frame)

<!-- [[MOR:root:C-R-C]] Cerceve = root for frame-boundary-scope -->
<!-- [[COM:Cerceve+Secim+Esleme]] Frame Selection Mapping -->
[define|neutral] CERCEVE_ESLEMESI := {
  arastirma_istemleri: { cerceve: "kanitsal", kaynak: "Turkce -mis/-di", zorlama: "Nereden biliyorsun?" },
  insa_istemleri: { cerceve: "gorunuslu", kaynak: "Rusca gorunu", zorlama: "Tamamlandi mi devam ediyor mu?" },
  analiz_istemleri: { cerceve: "morfolojik", kaynak: "Arapca kokler", zorlama: "Bilesenler nelerdir?" },
  dokumantasyon_istemleri: { cerceve: "bilesimsel", kaynak: "Almanca bilesik", zorlama: "Ilkellerden mi kurulur?" },
  kullanici_yuzlu_istemler: { cerceve: "saygisal", kaynak: "Japonca keigo", zorlama: "Hedef kitle kimdir?" }
} [ground:verilingua-spec] [conf:0.95] [state:confirmed]

### Cerceve Aktivasyon Protokolu (Frame Activation Protocol)

<!-- [[MOR:root:A-K-T]] Aktivasyon = root for activation-triggering-initiation -->
[define|neutral] CERCEVE_SECIMI_FONKSIYONU := {
  fonksiyon_adi: "select_cognitive_frame",
  girdi: "AnalyzedIntent",
  cikti: "CognitiveFrame",
  esleme: {
    arastirma: ["kanitsal", "Tum iddialar icin kanit kaynaklarini izleyecegim."],
    analiz: ["morfolojik", "Bunu temel bilesenlere ayiracagim."],
    insa: ["gorunuslu", "Her adim icin tamamlanma durumunu izleyecegim."],
    dokumantasyon: ["bilesimsel", "Ilkel kavramlardan insa edecegim."],
    kullanici_yuzlu: ["saygisal", "Hedef kitle icin ayarlayacagim."]
  }
} [ground:witnessed:code-inspection] [conf:0.90] [state:confirmed]

---
<!-- DSPy ENTEGRASYONU (DSPy Integration) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_module]] [[SPC:dogu/optimization]] -->
---

## DSPy Optimizasyon Entegrasyonu Cercevesi (DSPy Optimization Integration Frame)

<!-- [[MOR:root:D-S-P]] DSPy = root for declarative-signature-prompting -->
<!-- [[COM:DSPy+Optimizasyon+Modul]] DSPy Optimization Module -->
[define|neutral] DSPY_MODULU := {
  imza: "PromptOptimizationSignature",
  girdiler: ["original_prompt", "task_type", "constraints"],
  ciktilar: ["optimized_prompt", "techniques_applied", "quality_scores", "vcl_compliance"],
  optimizasyon: "Coklu metrik puanlama ile Teleprompter"
} [ground:dspy-spec] [conf:0.90] [state:confirmed]

---
<!-- GLOBALMOO ENTEGRASYONU (GlobalMOO Integration) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:tiao_config]] [[SPC:guney/pareto]] -->
---

## GlobalMOO Cok Amacli Optimizasyon Cercevesi (GlobalMOO Multi-Objective Optimization Frame)

<!-- [[MOR:root:G-L-B]] Global = root for global-universal-comprehensive -->
<!-- [[COM:Cok+Amacli+Optimizasyon+Yapilandirma]] Multi-Objective Optimization Configuration -->
[define|neutral] GLOBALMOO_YAPILANDIRMASI := {
  proje_kimlik: "prompt-architect-optimization",
  hedefler: {
    netlik: { yon: "maksimize", agirlik: 0.25 },
    tamlık: { yon: "maksimize", agirlik: 0.25 },
    vcl_uyumu: { yon: "maksimize", agirlik: 0.25 },
    cerceve_hizalamasi: { yon: "maksimize", agirlik: 0.15 },
    token_verimliligi: { yon: "minimize", agirlik: 0.10 }
  },
  parametreler: ["vcl_katiligi", "cerceve_secimi", "sikistirma_seviyesi", "teknik_seti"]
} [ground:globalmoo-spec] [conf:0.90] [state:confirmed]

---
<!-- GELISTIRILMIS ASAMA AKISI (Enhanced Phase Flow) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_workflow]] [[SPC:kuzey/pipeline]] -->
---

## Gelistirilmis Asama Akisi Cercevesi (Enhanced Phase Flow Frame)

<!-- [[MOR:root:A-S-M]] Asama = root for phase-stage-step -->
<!-- [[COM:Asama+Akis+Is+Akisi]] Phase Flow Workflow -->
[define|neutral] ASAMA_AKISI := {
  asamalar: [
    { asama: "0", isim: "Uzmanlik Yukleme", vcl: "Alan uzmanligini yukle" },
    { asama: "0.5", isim: "Cerceve Secimi", vcl: "VERILINGUA bilissel cerceve sec" },
    { asama: "1-4", isim: "Temel Optimizasyon", vcl: "Istem tekniklerini uygula" },
    { asama: "5", isim: "VCL Zenginlestirme", vcl: "EVD/ASP isaretciler ekle (L1) veya dogallastir (L2)" },
    { asama: "6-7", isim: "Dogrulama", vcl: "Guven tavanlarini kontrol et, epistemik taklitcilik yok" },
    { asama: "8", isim: "GlobalMOO Izleme", vcl: "Pareto ogrenme icin sonuclari kaydet" },
    { asama: "9", isim: "DSPy Optimizasyonu", vcl: "Etkinse teleprompter calistir" }
  ],
  l2_ozeti: "Uzmanlik yukle, bilissel cerceve sec, istem optimize et, VCL uyumunu dogrula, surekli iyilestirme icin izle."
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

---
<!-- KALITE KAPILARI (Quality Gates) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_gate]] [[SPC:dogu/validation]] -->
---

## Kalite Kapilari Cercevesi (Quality Gates Frame)

<!-- [[MOR:root:K-L-T]] Kalite = root for quality-excellence-standard -->
<!-- [[COM:Kalite+Kapi+Dogrulama]] Quality Gate Validation -->
[define|neutral] KALITE_KAPILARI := {
  vcl_kapisi: {
    minimum_evd_kapsami: 0.70,
    minimum_asp_kapsami: 0.80,
    guven_tavani_kontrolu: true,
    epistemik_taklitcilik_kontrolu: true
  },
  cerceve_kapisi: {
    minimum_cerceve_puani: 0.60,
    aktivasyon_cumlesi_gerekli: true
  },
  l2_kapisi: {
    ciktida_vcl_isaretci_yok: true,
    dogal_ingilizce: true
  }
} [ground:system-policy] [conf:0.95] [state:confirmed]

---
<!-- KREOLIZASYON YAPISI (Creolization Structure) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_structure]] [[SPC:bati/linguistic]] -->
---

## Kreolizasyon Yapisi Cercevesi (Creolization Structure Frame)

<!-- [[MOR:root:K-R-L]] Kreolizasyon = root for creolization-mixing-fusion -->
<!-- [[COM:Kreolizasyon+Yapi+Cerceve]] Creolization Structure Frame -->
[define|neutral] KREOLIZASYON_HAZIR := {
  mevcut_diller: {
    Turkce: "EVD slotu (-DI, -mis, -dir isaretcileri)",
    Rusca: "ASP slotu (sov., nesov. isaretcileri)",
    Japonca: "HON slotu (teineigo, sonkeigo, kenjougo)",
    Arapca: "MOR slotu (uclu kok ayristirma)",
    Almanca: "COM slotu (bilesik olusturma)",
    Cince: "CLS slotu (siniflandiricilar)",
    Guugu_Yimithirr: "SPC slotu (mutlak mekansal referans)"
  },
  genisleme_protokolu: "Yeni diller mevcut slotlara isaretci ekler veya yeni slotlar onerir",
  gelecek_slotlar: [],
  l2_geri_donusu: "Tum isaretciler Ingilizce esdegerlere dogallastirilir"
} [ground:design-decision] [conf:0.90] [state:provisional]

---
<!-- BELLEK ENTEGRASYONU (Memory Integration) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_protocol]] [[SPC:guney/storage]] -->
---

## Bellek Entegrasyonu Cercevesi (Memory Integration Frame)

<!-- [[MOR:root:B-L-K]] Bellek = root for memory-storage-retention -->
<!-- [[COM:Bellek+Entegrasyon+Protokol]] Memory Integration Protocol -->
[define|neutral] BELLEK_PROTOKOLU := {
  depolama_deseni: "prompt-architect/optimizations/{prompt_id}",
  ad_alani: "foundry-optimization",
  katman: "uzun-vadeli",
  etiketler: {
    KIM: "prompt-architect",
    NE_ZAMAN: "ISO8601_zaman_damgasi",
    PROJE: "meta-loop",
    NEDEN: "prompt-optimization"
  }
} [ground:memory-mcp-spec] [conf:0.95] [state:confirmed]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Etot addendum byl uspeshno integrirovan. (Russian: Complete. This addendum was successfully integrated.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[assert|confident] SONUC_OZETI := {
  amac: "Prompt-architect'e tam bilissel mimari entegrasyonu",
  entegre_sistemler: [
    "VCL 7-Slot Sistemi - EVD ve ASP her zaman zorlanir, insanlar icin L2 dogallastirma",
    "VERIX - Tum iddialar temel ve guven icerir; tavanlar zorlanir",
    "VERILINGUA - Istem niyet kategorisine gore cerceve secimi",
    "DSPy - Surekli iyilestirme icin optimizasyon dongusu",
    "GlobalMOO - Cok amacli izleme ve Pareto siniri",
    "Kreolizasyon - Gelecekteki dil genislemesi icin hazir"
  ],
  sonraki_adimlar: "Gelistirilmis prompt-architect diger foundry becerilerini ve sonrasinda tum komutlari, ajanlari, becerileri ve playbook'lari optimize edebilir."
} [ground:witnessed:skill-execution] [conf:0.95] [state:confirmed]

---

[commit|confident] <promise>COGNITIVE_ARCHITECTURE_ADDENDUM_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
