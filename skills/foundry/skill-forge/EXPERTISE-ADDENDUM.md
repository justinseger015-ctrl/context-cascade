# Skill Forge - Uzmanlik Sistemi Eki (Expertise System Addendum)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## S1 META BILGI CERCEVESI (Meta Information Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_metadata]] -->
<!-- [[MOR:root:U-Z-M]] Uzmanlik = root morpheme for expertise-mastery-knowledge -->
<!-- [[COM:Uzmanlik+Sistem+Entegrasyon]] German: Expertise-System-Integration -->

[define|neutral] ADDENDUM_META := {
  surum: "2.1.0", // version
  entegrasyon: ["expertise-manager", "domain-expert"],
  aciklama: "Skill Forge (simdi 8-faz metodolojisi) icin Agent Experts tarzi ogrenme yetenekleri",
  not: "Faz 0 (Uzmanlik Yukleme) v2.0 itibariyle ana SKILL.md'ye entegre edildi"
} [ground:witnessed:version-header] [conf:0.95] [state:confirmed]

---

## S2 YENI FAZ 0: ALAN UZMANLIK YUKLEME (New Phase 0: Domain Expertise Loading)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_phase]] -->
<!-- [[MOR:root:Y-K-L]] Yukleme = root for load-mount-carry -->
<!-- [[COM:Alan+Uzmanlik+Yukleme]] German: Domain-Expertise-Laden -->
<!-- [[SPC:kuzey]] Primary process direction -->

### S2.1 Amac (Purpose)

[define|neutral] PHASE_0_PURPOSE := {
  kural_adi: "Faz 0 Amaci", // Phase 0 Purpose
  amac: "Beceri olusturmayi bilgilendirmek icin mevcut alan uzmanligini yukle ve kullan", // purpose
  fayda: [
    "Uzmanlik baglami ile olusturulan beceriler daha dogru", // More accurate
    "Kod tabani ile daha iyi entegrasyon" // Better integration with codebase
  ]
} [ground:witnessed:phase-design] [conf:0.90] [state:confirmed]

### S2.2 Surec (Process)

[define|neutral] EXPERTISE_LOADING_PROCESS := {
  kural_adi: "Uzmanlik Yukleme Sureci", // Expertise Loading Process
  adimlar: [
    {
      sira: 1,
      ad: "Alani istekten algilama",
      aciklama: "analyzeDomainFromRequest(skillRequest)"
    },
    {
      sira: 2,
      ad: "Uzmanlik dosyasini kontrol et",
      yol: ".claude/expertise/${domain}.yaml"
    },
    {
      sira: 3,
      ad: "Uzmanligin guncel oldugunu dogrula",
      komut: "/expertise-validate ${domain} --fix"
    },
    {
      sira: 4,
      ad: "Dogrulanmis uzmanligin yukle",
      islem: "loadYAML(expertisePath)"
    },
    {
      sira: 5,
      ad: "Beceri olusturma icin ilgili baglami cikart",
      context_fields: [
        "fileLocations: expertise.file_locations",
        "patterns: expertise.patterns",
        "knownIssues: expertise.known_issues",
        "routingTemplates: expertise.routing.task_templates",
        "trustLevel: expertise.correctability.trust_level"
      ]
    },
    {
      sira: 6,
      ad: "Sonraki fazlarda kullanim icin sakla",
      islem: "setPhaseContext('expertise', context)"
    }
  ],
  uzmanlik_yoksa: {
    log: "Alan icin uzmanlik dosyasi yok",
    islem: "setPhaseContext('generateExpertise', true)"
  }
} [ground:witnessed:process-design] [conf:0.88] [state:confirmed]

---

## S3 GELISTIRILMIS FAZ 3: YAPISAL MIMARI (Enhanced Phase 3: Structural Architecture)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_architecture]] -->
<!-- [[MOR:root:Y-P-S]] Yapi = root for structure-build-form -->
<!-- [[COM:Yapisal+Mimari+Gelistirme]] German: Strukturelle-Architektur-Verbesserung -->

### S3.1 Uzmanlik Dosya Konumlarini Kullan (Use Expertise File Locations)

[define|neutral] FILE_CONTEXT_SCHEMA := {
  kural_adi: "Dosya Baglami Semasi", // File Context Schema
  uzmanlik_entegrasyonu: {
    primary_path: "${expertise.file_locations.primary.path}",
    tests_path: "${expertise.file_locations.tests.path}",
    config_path: "${expertise.file_locations.config.path}"
  },
  aciklama: "Uretilen beceride dosya konumlarini uzmanliktan al"
} [ground:witnessed:schema-design] [conf:0.88] [state:confirmed]

### S3.2 Uzmanlik Kaliplarini Referans Al (Reference Expertise Patterns)

[define|neutral] METHODOLOGY_SCHEMA := {
  kural_adi: "Metodoloji Semasi", // Methodology Schema
  uzmanlik_referanslari: {
    architecture_pattern: "${expertise.patterns.architecture.claim}",
    data_flow: "${expertise.patterns.data_flow.claim}",
    error_handling: "${expertise.patterns.error_handling.claim}"
  },
  aciklama: "Uretilen beceri metodolojisinde alan kaliplarini referans al"
} [ground:witnessed:schema-design] [conf:0.85] [state:confirmed]

### S3.3 Bilinen Sorunlari Dahil Et (Incorporate Known Issues)

[define|neutral] GUARDRAILS_SCHEMA := {
  kural_adi: "Koruma Barikat Semasi", // Guardrails Schema
  uzmanlik_kaynak: "expertise.known_issues",
  dahil_edilen_alanlar: [
    "issue.id",
    "issue.description",
    "issue.mitigation"
  ],
  aciklama: "Uretilen beceri koruma barikatlarinda bilinen sorunlari dahil et"
} [ground:witnessed:schema-design] [conf:0.85] [state:confirmed]

---

## S4 YENI FAZ 7.5: UZMANLIK KANCA ENTEGRASYONU (New Phase 7.5: Expertise Hook Integration)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_hook]] -->
<!-- [[MOR:root:K-N-C]] Kanca = root for hook-catch-connect -->
<!-- [[COM:Uzmanlik+Kanca+Entegrasyon]] German: Expertise-Hook-Integration -->

[define|neutral] EXPERTISE_HOOK_TEMPLATE := {
  kural_adi: "Uzmanlik Kanca Sablonu", // Expertise Hook Template
  faz: "7.5",
  zamanlama: "Faz 7 (Kalite Guvencesi) sonrasi", // After Phase 7
  uygulama: {
    frontmatter: {
      domain: "${domain}",
      requires_expertise: true,
      auto_validate: true,
      auto_update: true
    },
    hooks: {
      pre_execution: {
        aciklama: "Calistirmadan once alan uzmanligini yukle ve dogrula",
        islemler: [
          "Uzmanlik dosyasi var mi kontrol et",
          "/expertise-validate ${domain} --fix calistir",
          "EXPERTISE_LOADED ortam degiskenini ayarla",
          "EXPERTISE_DOMAIN ortam degiskenini ayarla"
        ]
      },
      post_execution: {
        aciklama: "Ogrenimleri cikart ve uzmanlik guncellemeleri oner",
        islemler: [
          "EXPERTISE_LOADED kontrol et",
          "/expertise-extract-learnings ${EXPERTISE_DOMAIN} calistir"
        ]
      }
    }
  }
} [ground:witnessed:hook-design] [conf:0.88] [state:confirmed]

---

## S5 YENI FAZ 8: UZMANLIK URETIMI (New Phase 8: Expertise Generation)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_generation]] -->
<!-- [[MOR:root:U-R-T]] Uretim = root for generate-produce-create -->
<!-- [[COM:Uzmanlik+Uretim+Surec]] German: Expertise-Generierungs-Prozess -->

[define|neutral] EXPERTISE_GENERATION_PROCESS := {
  kural_adi: "Uzmanlik Uretim Sureci", // Expertise Generation Process
  tetikleyici: "Faz 0'da generateExpertise bayragi ayarlanmissa", // If generateExpertise flag was set in Phase 0
  sadece_kosullu: true,
  adimlar: [
    {
      sira: 1,
      ad: "Beceri analizinden alan bilgisini cikart",
      kaynak_fazlar: ["structuralArchitecture", "intentArchaeology"],
      cikart: ["fileLocations", "patterns", "entities"]
    },
    {
      sira: 2,
      ad: "Uzmanlik dosyasi olustur",
      hedef: ".claude/expertise/${domain}.yaml",
      varsayilanlar: {
        validation_status: "needs_validation",
        trust_level: "provisional"
      }
    },
    {
      sira: 3,
      ad: "Cekismeli dogrulama icin kuyrukla",
      komut: "/expertise-challenge ${domain}",
      log: "Uretilen uzmanlik dogrulama icin kuyruklandi"
    }
  ],
  arac: "Task('Expertise Generator', ..., 'knowledge-manager')"
} [ground:witnessed:generation-design] [conf:0.85] [state:confirmed]

---

## S6 GUNCELLENMIS KALITE GUVENCE FAZI (Updated Quality Assurance Phase)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_quality]] -->
<!-- [[MOR:root:K-L-T]] Kalite = root for quality-value-standard -->
<!-- [[COM:Kalite+Guvence+Kontrol]] German: Qualitats-Sicherungs-Kontrolle -->

### S6.1 Uzmanlik Hizalama Kontrolu (Expertise Alignment Check)

[define|neutral] EXPERTISE_ALIGNMENT_CHECK := {
  kural_adi: "Uzmanlik Hizalama Kontrolu", // Expertise Alignment Check
  aciklama: "Becerinin alan uzmanligiyla hizalandigini dogrula",
  kontroller: [
    {
      ad: "skill_uses_expertise_paths",
      beklenen: true,
      aciklama: "Beceri uzmanlik yollarini kullaniyor"
    },
    {
      ad: "skill_follows_expertise_patterns",
      beklenen: true,
      aciklama: "Beceri uzmanlik kaliplarini takip ediyor"
    },
    {
      ad: "skill_references_known_issues",
      beklenen: true,
      aciklama: "Beceri bilinen sorunlara referans veriyor"
    },
    {
      ad: "skill_has_expertise_hooks",
      beklenen: true,
      aciklama: "Beceri uzmanlik kancalarina sahip"
    }
  ]
} [ground:witnessed:quality-check] [conf:0.88] [state:confirmed]

### S6.2 Ogrenme Potansiyeli Kontrolu (Learning Potential Check)

[define|neutral] LEARNING_POTENTIAL_CHECK := {
  kural_adi: "Ogrenme Potansiyeli Kontrolu", // Learning Potential Check
  aciklama: "Becerinin uzmanlik ogrenimine katki saglayabildigini dogrula",
  kontroller: [
    {
      ad: "has_pre_execution_hook",
      beklenen: true,
      aciklama: "On-calistirma kancasi var"
    },
    {
      ad: "has_post_execution_hook",
      beklenen: true,
      aciklama: "Son-calistirma kancasi var"
    },
    {
      ad: "tracks_observations",
      beklenen: true,
      aciklama: "Gozlemleri izliyor"
    },
    {
      ad: "can_propose_updates",
      beklenen: true,
      aciklama: "Guncellemeler onerebiliyor"
    }
  ]
} [ground:witnessed:quality-check] [conf:0.85] [state:confirmed]

---

## S7 ENTEGRASYON OZETI CERCEVESI (Integration Summary Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_summary]] -->
<!-- [[MOR:root:O-Z-T]] Ozet = root for summary-abstract-brief -->
<!-- [[COM:Entegrasyon+Ozet+Tablo]] German: Integration-Zusammenfassung-Tabelle -->

[define|neutral] INTEGRATION_SUMMARY := {
  kural_adi: "Entegrasyon Ozeti", // Integration Summary
  faz_eklemeleri: [
    {
      faz: "0 (YENI)",
      ekleme: "Uzmanlik Yukleme",
      amac: "Alan baglamini yukle"
    },
    {
      faz: "3",
      ekleme: "Yapida Uzmanlik",
      amac: "Dosya konumlari, kaliplari kullan"
    },
    {
      faz: "5",
      ekleme: "Talimatlarda Uzmanlik",
      amac: "Bilinen sorunlara referans"
    },
    {
      faz: "7",
      ekleme: "Uzmanlik Kalite Kontrolleri",
      amac: "Hizalamayi dogrula"
    },
    {
      faz: "7.5 (YENI)",
      ekleme: "Kanca Entegrasyonu",
      amac: "Uzmanlik kancalari ekle"
    },
    {
      faz: "8 (YENI)",
      ekleme: "Uzmanlik Uretimi",
      amac: "Eksikse olustur"
    }
  ]
} [ground:witnessed:integration-design] [conf:0.90] [state:confirmed]

---

## S8 KULLANIM ORNEGI CERCEVESI (Usage Example Frame)
<!-- [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[ASP:sov.]] [[CLS:ge_example]] -->
<!-- [[MOR:root:O-R-N]] Ornek = root for example-sample-instance -->
<!-- [[COM:Kullanim+Ornek+Gosterim]] German: Verwendungs-Beispiel-Demonstration -->

[assert|neutral] USAGE_EXAMPLE := {
  kural_adi: "Kullanim Ornegi", // Usage Example
  senaryo: "Uzmanlik ile kimlik dogrulama alani icin beceri olusturma",
  kullanici_istegi: "Auth sistemimizdeki JWT tokenlerini dogrulamak icin beceri olustur",
  akis: [
    {
      log: "[UZMANLIK] Alan icin uzmanlik bulundu: authentication",
      detay: null
    },
    {
      log: "[UZMANLIK] Uzmanlik dogrulandi (kayma: 0.12)",
      detay: null
    },
    {
      log: "[UZMANLIK] Baglam yuklendi:",
      detay: [
        "- Birincil yol: src/auth/",
        "- Kaliplar: 4",
        "- Bilinen sorunlar: 1",
        "- Guven seviyesi: dogrulanmis"
      ]
    },
    {
      log: "[FAZ 1] Uzmanlik baglami ile Niyet Arkeolojisi...",
      detay: null
    },
    {
      log: "[FAZ 2] Kullanim Senaryosu Kristalizasyonu...",
      detay: null
    },
    {
      log: "[FAZ 3] Yapisal Mimari kullaniyor:",
      detay: [
        "- Uzmanliktan dosya konumlari",
        "- Uzmanliktan kaliplar"
      ]
    },
    {
      log: "[FAZ 4-7] Standart fazlar...",
      detay: null
    },
    {
      log: "[FAZ 7.5] Beceriye uzmanlik kancalari ekleniyor...",
      detay: null
    },
    {
      log: "[TAMAMLANDI] Uzmanlik entegrasyonu ile beceri olusturuldu",
      detay: null
    }
  ]
} [ground:reported:example-execution] [conf:0.82] [state:confirmed]

---

## S9 REFERANS CERCEVESI (Reference Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_reference]] -->
<!-- [[MOR:root:R-F-R]] Referans = root for reference-consult-cite -->
<!-- [[COM:Referans+Dokuman+Yol]] German: Referenz-Dokument-Pfad -->

[assert|neutral] REFERENCE := {
  kural_adi: "Referans", // Reference
  dokuman: ".claude/skills/EXPERTISE-INTEGRATION-MODULE.md",
  aciklama: "Tam entegrasyon kaliplari icin bakiniz"
} [ground:witnessed:reference-link] [conf:0.95] [state:confirmed]

---

## S10 SONUC CERCEVESI (Conclusion Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-end -->
<!-- [[COM:Sonuc+Ozet+Bildiri]] German: Schlussfolgerung-Zusammenfassung -->
Zaversheno. (Russian: Complete.)

[assert|confident] ADDENDUM_SUMMARY := {
  amac: "Skill Forge icin Agent Experts tarzi ogrenme yetenekleri", // purpose
  metodoloji: "8-fazli uzmanlik-entegre beceri olusturma", // methodology
  ciktilar: [
    "Alan uzmanlik yukleme (Faz 0)",
    "Uzmanlik-bilincli yapi tasarimi",
    "Otomatik uzmanlik kancalari",
    "Yeni alanlar icin uzmanlik uretimi"
  ],
  kalite_kapilari: ["Uzmanlik hizalama kontrolu", "Ogrenme potansiyeli kontrolu"]
} [ground:witnessed:implementation] [conf:0.90] [state:confirmed]

---

*Promise: `<promise>EXPERTISE_ADDENDUM_VCL_V3.1.1_COMPLIANT</promise>`*
