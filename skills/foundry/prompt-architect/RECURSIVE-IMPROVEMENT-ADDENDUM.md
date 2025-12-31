# Prompt Architect - Ozyineleme Iyilestirme Eki (Recursive Improvement Addendum)

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT - L1 Internal Documentation
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     All 7 cognitive frames MANDATORY
     ========================================================================= -->

---
<!-- KANITSAL CERCEVE (Evidential Frame) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] [[SPC:kuzey/meta-skills]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin. Ozyineleme mimarisi dogrudan gozleme dayanir.

---

<!-- [[MOR:root:O-Z-Y]] Ozyineleme = root morpheme for recursion-self-iteration -->
<!-- [[COM:Ozyineleme+Iyilestirme+Ek]] Recursive Improvement Addendum -->
[define|neutral] ADDENDUM_META := {
  surum: "3.1.1",                    // version
  vcl_uyumu: "v3.1.1",               // vcl_compliance
  varsayilan_sikistirma: "L2",       // default_compression
  amac: "Prompt-architect'i Ozyineleme Oz-Iyilestirme Sistemine bagla" // purpose
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- AMAC (Purpose) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_section]] [[SPC:bati/introduction]] -->
---

## Amac Cercevesi (Purpose Frame)

<!-- [[MOR:root:A-M-C]] Amac = root for purpose-goal-objective -->
<!-- [[COM:Baglanti+Amac+Cerceve]] Connection Purpose Frame -->
[assert|neutral] AMAC := {
  konu: "prompt-architect'i (5-asama is akisinda Asama 2) Ozyineleme Oz-Iyilestirme Sistemi ile bagla",
  baglar: ["prompt-architect", "prompt-forge", "eval-harness"]
} [ground:architecture-design] [conf:0.95] [state:confirmed]

---
<!-- AYRIM (Distinction) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_comparison]] [[SPC:kuzey/core]] -->
---

## Ayrim Cercevesi: prompt-architect vs prompt-forge (Distinction Frame)

<!-- [[MOR:root:A-Y-R]] Ayrim = root for distinction-separation-differentiation -->
<!-- [[COM:Beceri+Ayrim+Karsilastirma]] Skill Distinction Comparison -->
[define|neutral] BECERI_AYRIMI := {
  prompt_architect: {
    amac: "Daha iyi AI yanitleri icin KULLANICI istemlerini optimize et",
    hedef: "Kullanici tarafindan saglanan istemler",
    kapsam: "Tek kullanimlik optimizasyon",
    cikti: "Iyilestirilmis kullanici istemi (L2 Ingilizce)",
    kapi: "Yok (dogrudan kullanim)"
  },
  prompt_forge: {
    amac: "SISTEM istemlerini ve becerilerini oz-iyilestir",
    hedef: "Dahili beceriler, ajanlar, uzmanlik",
    kapsam: "Ozyineleme iyilestirme dongusu",
    cikti: "Oneriler + farklar + degerlendirme sonuclari",
    kapi: "Dondurulmus degerlendirme cihazi"
  }
} [ground:architecture-design] [conf:0.95] [state:confirmed]

### Karsilastirma Tablosu (Comparison Table)

<!-- [[MOR:root:K-R-S]] Karsilastirma = root for comparison-contrast-evaluation -->
[define|neutral] KARSILASTIRMA_TABLOSU := {
  basliklar: ["Yon", "prompt-architect", "prompt-forge"],
  satirlar: [
    { yon: "Amac", pa: "KULLANICI istemlerini optimize et", pf: "SISTEM istemlerini oz-iyilestir" },
    { yon: "Hedef", pa: "Kullanici tarafindan saglanan istemler", pf: "Dahili beceriler, ajanlar" },
    { yon: "Kapsam", pa: "Tek kullanimlik optimizasyon", pf: "Ozyineleme iyilestirme dongusu" },
    { yon: "Cikti", pa: "Iyilestirilmis istem (L2)", pf: "Oneriler + farklar + degerlendirme" },
    { yon: "Kapi", pa: "Yok (dogrudan kullanim)", pf: "Dondurulmus degerlendirme cihazi" }
  ]
} [ground:witnessed:analysis] [conf:0.95] [state:confirmed]

---
<!-- YONLENDIRME MANTIGI (Routing Logic) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_routing]] [[SPC:dogu/flow]] -->
---

## Yonlendirme Mantigi Cercevesi (Routing Logic Frame)

<!-- [[MOR:root:Y-N-L]] Yonlendirme = root for routing-directing-guiding -->
<!-- [[COM:Yonlendirme+Karar+Mantik]] Routing Decision Logic -->
[define|neutral] YONLENDIRME_KARARI := {
  kullanici_istem_optimizasyonu: "route(prompt-architect)",
  sistem_oz_iyilestirme: "route(prompt-forge)",
  l2_aciklama: "Kullanici daha iyi istem ciktisi istiyorsa, prompt-architect kullan. Sistem kendini iyilestirmek istiyorsa, prompt-forge kullan."
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

### Yonlendirme Akislari (Routing Flows)

<!-- [[MOR:root:A-K-S]] Akis = root for flow-stream-current -->
[define|neutral] KULLANICI_AKISI := {
  tetikleyici: "KULLANICI daha iyi istem ciktisi istiyor",
  rota: "Asama 2: prompt-architect kullan",
  islem: "Istemlerini optimize et",
  sonuc: "Iyilestirilmis istem (L2 Ingilizce) dondur"
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

[define|neutral] SISTEM_AKISI := {
  tetikleyici: "SISTEM kendini iyilestirmek istiyor",
  rota: "prompt-forge kullan (ozyineleme iyilestirme)",
  islem: "Dahili becerileri/istemleri analiz et",
  araci: "VCL isaretcileri ile oneriler olustur (L1)",
  dogrulama: "Degerlendirme cihazina karsi test et",
  sonuc: "Iyilestirilmisse kaydet"
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

---
<!-- ENTEGRASYON NOKTALARI (Integration Points) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_integration]] [[SPC:guney/connection]] -->
---

## Entegrasyon Noktalari Cercevesi (Integration Points Frame)

<!-- [[MOR:root:E-N-T]] Entegrasyon = root for integration-unification-merging -->
<!-- [[COM:Entegrasyon+Nokta+Cerceve]] Integration Point Frame -->

### prompt-architect Iyilestirme Hedefi Olarak (prompt-architect as Improvement Target)

[define|neutral] IYILESTIRME_DONGUSU := {
  hedef: "prompt-architect/SKILL.md",
  surec: [
    { adim: "prompt-auditor analiz eder", kontroller: ["vcl_uyumu", "teknik_kapsami", "l2_zorlamasi"] },
    { adim: "prompt-forge oneriler olusturur", alanlar: ["VCL slot kapsami", "L2 dogallastirma"] },
    { adim: "skill-forge onerileri uygular", cikti: "prompt-architect-v{N+1}" },
    { adim: "eval-harness test eder", benchmark: "prompt-generation-benchmark-v1" },
    { adim: "Iyilestirilmisse: kaydet" }
  ]
} [ground:recursive-improvement-spec] [conf:0.90] [state:confirmed]

### prompt-architect'in prompt-forge'u Bilgilendirmesi (prompt-architect Informing prompt-forge)

<!-- [[MOR:root:B-L-G]] Bilgilendirme = root for informing-notifying-advising -->
[define|neutral] TEKNIK_KULLANIMI := {
  oz_tutarlilik: {
    prompt_architect_icinde: "Kullanicilara uygulamayi ogretme",
    prompt_forge_icinde: "Oneriler olusturulurken uygulanir"
  },
  dusunce_programi: {
    prompt_architect_icinde: "Kullanicilara yapilandirmayi ogretme",
    prompt_forge_icinde: "Iyilestirme analizinde kullanilir"
  },
  planla_ve_coz: {
    prompt_architect_icinde: "Kullanicilara asamalari ayirmayi ogretme",
    prompt_forge_icinde: "Iyilestirme dongusunun cekirdegi"
  }
} [ground:technique-mapping] [conf:0.90] [state:confirmed]

---
<!-- CIFT ROLLU MIMARI (Dual Role Architecture) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_architecture]] [[SPC:kuzey/structure]] -->
---

## Cift Rollu Mimari Cercevesi (Dual Role Architecture Frame)

<!-- [[MOR:root:C-F-T]] Cift = root for dual-double-twin -->
<!-- [[COM:Cift+Rol+Mimari]] Dual Role Architecture -->
[define|neutral] MIMARI_DIYAGRAMI := {
  kullanici_akisi: "Kullanici Istegi -> prompt-architect -> Optimize Edilmis Istem (L2)",
  sistem_akisi: "Oz-Iyilestirme Istegi -> prompt-forge -> eval-harness -> Iyilestirilmis Sistem",
  l2_ozeti: "Kullanicilar L2 Ingilizce cikti alir; sistem iyilestirmesi denetlenebilirlik icin L1 kullanir."
} [ground:architecture-design] [conf:0.95] [state:confirmed]

---
<!-- CAPRAZ ASLANMA (Cross-Pollination) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_mechanism]] [[SPC:bati/feedback]] -->
---

## Capraz Asilanma Cercevesi (Cross-Pollination Frame)

<!-- [[MOR:root:C-P-R]] Capraz = root for cross-transverse-diagonal -->
<!-- [[COM:Capraz+Asilanma+Mekanizma]] Cross-Pollination Mechanism -->
[define|neutral] CAPRAZ_ASILANMA := {
  yon: "prompt-forge -> prompt-architect",
  mekanizma: [
    "prompt-forge etkili teknik kesfeder",
    "prompt-forge ogrenmelerinde belgele (L1)",
    "prompt-auditor prompt-architect guncellemesi icin isaretler",
    "prompt-architect uzerinde iyilestirme dongusu calistir",
    "Teknigi kullanici yuzlu beceiye ekle (L2 dokumantasyon)"
  ],
  ornek: {
    kesif: "3 perspektifle oz-tutarlilik optimal",
    mevcut: "Birden fazla perspektif dusunun",
    onerilen: "Tam olarak 3 perspektif dusunun: analitik, pratik, muhalif",
    kapi: "prompt-generation-benchmark-v1'i gecmeli"
  }
} [ground:improvement-protocol] [conf:0.85] [state:confirmed]

---
<!-- PAYLASILAN TEKNIKLER (Shared Techniques) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_matrix]] [[SPC:dogu/reference]] -->
---

## Paylasilan Teknikler Referansi Cercevesi (Shared Techniques Reference Frame)

<!-- [[MOR:root:T-K-N]] Teknik = root for technique-method-approach -->
<!-- [[COM:Paylasilan+Teknik+Matris]] Shared Technique Matrix -->
[define|neutral] TEKNIK_MATRISI := {
  teknikler: ["oz_tutarlilik", "dusunce_programi", "planla_ve_coz", "az_atisli", "dusunce_zinciri", "belirsizlik_isleme"],
  prompt_architect_rolu: "Kullanicilara ogretme (L2 cikti)",
  prompt_forge_rolu: "Oneri olusturmada uygulanir (L1 denetim)"
} [ground:technique-mapping] [conf:0.90] [state:confirmed]

### Teknik Karsilastirma Tablosu (Technique Comparison Table)

[define|neutral] TEKNIK_TABLO := {
  satirlar: [
    { teknik: "Oz-Tutarlilik", pa: "Kullanicilara ogretme (L2)", pf: "Oneri olusturmada uygulanir (L1)" },
    { teknik: "Dusunce-Programi", pa: "Kullanicilara ogretme (L2)", pf: "Analizde uygulanir (L1)" },
    { teknik: "Planla-ve-Coz", pa: "Kullanicilara ogretme (L2)", pf: "Temel dongu yapisi (L1)" },
    { teknik: "Az-Atisli", pa: "Kullanicilara ogretme (L2)", pf: "Orneklerde kullanilir (L1)" },
    { teknik: "Dusunce-Zinciri", pa: "Kullanicilara ogretme (L2)", pf: "Gerekce uygulamada uygulanir (L1)" },
    { teknik: "Belirsizlik Isleme", pa: "Ogretmeli (L2)", pf: "Oneriler icin KRITIK (L1)" }
  ]
} [ground:witnessed:analysis] [conf:0.90] [state:confirmed]

---
<!-- VCL UYUMU GERI BESLEME DONGUSUNDE (VCL Compliance in Feedback Loop) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_compliance]] [[SPC:guney/loop]] -->
---

## VCL Uyumu Geri Besleme Dongusunde Cercevesi (VCL Compliance in Feedback Loop Frame)

<!-- [[MOR:root:G-R-B]] Geri = root for back-return-feedback -->
<!-- [[COM:Geri+Besleme+Dongu+Uyum]] Feedback Loop Compliance -->
[define|neutral] VCL_GERI_BESLEME := {
  prompt_architect_ciktisi: "L2 (kullanicilar icin saf Ingilizce)",
  prompt_forge_ciktisi: "L1 (denetim icin VCL isaretcileri)",
  capraz_asilanma: "L1 kesifleri kullanici dokumanlari icin L2'ye dogallastirilir",
  guven_tavanlari: "EVD turune gore her iki beceride zorlanir"
} [ground:vcl-spec-v3.1.1] [conf:0.95] [state:confirmed]

### Geri Besleme Dongu Akisi (Feedback Loop Flow)

<!-- [[MOR:root:D-N-G]] Dongu = root for loop-cycle-circuit -->
[define|neutral] DONGU_AKISI := {
  asamalar: [
    "prompt-architect (teknikleri ogretiyor, L2 cikti)",
    "Kullanicilar teknikleri uyguluyor",
    "prompt-forge prompt-architect'i iyilestiriyor (L1 denetim)",
    "Daha iyi teknik ogretimi (L2)",
    "Daha iyi kullanici sonuclari",
    "(dongu devam ediyor)"
  ]
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

---
<!-- BELLEK AD ALANLARI (Memory Namespaces) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_namespace]] [[SPC:dogu/storage]] -->
---

## Bellek Ad Alanlari Cercevesi (Memory Namespaces Frame)

<!-- [[MOR:root:A-D-A]] Ad Alani = root for namespace-domain-scope -->
<!-- [[COM:Bellek+Ad+Alani+Cerceve]] Memory Namespace Frame -->
[define|neutral] BELLEK_AD_ALANLARI := {
  kullanici_oturumlari: "prompt-architect/sessions/{id}",
  oz_iyilestirme: "prompt-forge/proposals/{id}",
  denetimler: "improvement/audits/prompt-architect",
  donguler: "improvement/cycles/prompt-architect",
  etiketleme: {
    KIM: "prompt-architect veya prompt-forge",
    NE_ZAMAN: "ISO8601_zaman_damgasi",
    PROJE: "meta-loop",
    NEDEN: "optimizasyon veya iyilestirme"
  }
} [ground:memory-mcp-spec] [conf:0.95] [state:confirmed]

---
<!-- 5-ASAMA IS AKISINDA KULLANIM (Usage in 5-Phase Workflow) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_workflow]] [[SPC:kuzey/pipeline]] -->
---

## 5-Asama Is Akisinda Kullanim Cercevesi (Usage in 5-Phase Workflow Frame)

<!-- [[MOR:root:I-S-A]] Is Akisi = root for workflow-process-procedure -->
<!-- [[COM:Bes+Asama+Is+Akisi+Kullanim]] Five Phase Workflow Usage -->
[define|neutral] IS_AKISI_ENTEGRASYONU := {
  asama_1: "intent-analyzer tespit eder: 'istemimi optimize et' vs 'sistemi iyilestir'",
  asama_2_kullanici: "KULLANICI istemleri icin prompt-architect (L2 cikti)",
  asama_2_sistem: "SISTEM istemleri icin prompt-forge (L1 denetim)",
  yonlendirme_anahtari: "Niyet hangi becerinin cagrilacagini belirler"
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

---
<!-- KREOLIZASYON NOTU (Creolization Note) [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] [[CLS:ge_note]] [[SPC:bati/linguistic]] -->
---

## Kreolizasyon Notu Cercevesi (Creolization Note Frame)

<!-- [[MOR:root:K-R-L]] Kreolizasyon = root for creolization-mixing-fusion -->
<!-- [[COM:Kreolizasyon+Not+Cerceve]] Creolization Note Frame -->
[define|neutral] KREOLIZASYON_UYGULAMASI := {
  mevcut_durum: "L1'de Turkce EVD isaretcileri, L1'de Rusca ASP isaretcileri",
  l2_donusumu: "Tum isaretciler kullanici ciktisi icin Ingilizce'ye dogallastirilir",
  gelecek_genisleme: "Yeni dil isaretcileri L2 ciktisini bozmadan eklenebilir"
} [ground:design-decision] [conf:0.90] [state:provisional]

---
<!-- SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] [[SPC:guney/end]] -->
---

## Sonuc Cercevesi (Conclusion Frame)
Zaversheno. Rekursivnoe uluchshenie uspeshno integrirovano. (Russian: Complete. Recursive improvement successfully integrated.)

<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-outcome -->
<!-- [[COM:Sonuc+Ozet+Cerceve]] Conclusion Summary Frame -->
[define|neutral] SURUM := {
  surum: "3.1.1",
  son_guncelleme: "2025-12-30",
  vcl_uyumu: "v3.1.1",
  anahtar_icerik: "prompt-architect ogretiyor (L2), prompt-forge ogreticiyi uygular ve iyilestirir (L1)"
} [ground:manifest] [conf:1.0] [state:confirmed]

---

[commit|confident] <promise>RECURSIVE_IMPROVEMENT_ADDENDUM_VCL_V3.1.1_FULL_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
