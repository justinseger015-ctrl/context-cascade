# Skill Forge - Ozyineleme Iyilestirme Eki (Recursive Improvement Addendum)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_document]] -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## S1 AMAC CERCEVESI (Purpose Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_purpose]] -->
<!-- [[MOR:root:A-M-C]] Amac = root morpheme for purpose-goal-objective -->
<!-- [[COM:Ozyineleme+Iyilestirme+Sistem]] German: Rekursives-Verbesserungs-System -->

[define|neutral] ADDENDUM_PURPOSE := {
  amac: "Skill-forge ile Ozyineleme Kendini-Iyilestirme Sistemi baglantisi", // purpose
  yetenekler: [
    "Skill Forge kendini iyilestirme", // Skill Forge improving itself
    "Prompt Forge tarafindan iyilestirme", // Being improved by Prompt Forge
    "Diger becerilere iyilestirme uygulama" // Applying improvements to other skills
  ],
  surum: "1.0.0",
  son_guncelleme: "2025-12-15"
} [ground:witnessed:purpose-definition] [conf:0.92] [state:confirmed]

---

## S2 OZYINELEME DONGUSU ROL CERCEVESI (Role in Recursive Loop Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_role]] -->
<!-- [[MOR:root:D-N-G]] Dongu = root for loop-cycle-iteration -->
<!-- [[COM:Ozyineleme+Dongu+Rol]] German: Rekursive-Schleifen-Rolle -->
<!-- [[SPC:kuzey]] Primary flow direction -->

[define|neutral] RECURSIVE_LOOP_ARCHITECTURE := {
  kural_adi: "Ozyineleme Dongusu Mimarisi", // Recursive Loop Architecture
  akis: {
    kaynak: "PROMPT FORGE",
    kaynak_islev: "Oneriler uretir", // Generates proposals
    hedef: "SKILL FORGE",
    hedef_islev: "Onerileri uygular", // Applies proposals
    son_hedef: "TUM BECERILER",
    son_hedef_islev: "Iyilestirme hedefleri" // Improvement targets
  },
  modlar: [
    {
      ad: "Hedef Modu", // Target Mode
      tanim: "Prompt Forge tarafindan iyilestiriliyor" // Being improved by Prompt Forge
    },
    {
      ad: "Uygulayici Modu", // Applier Mode
      tanim: "Diger becerilere (kendisi dahil) iyilestirme uygular" // Applying improvements to other skills
    }
  ]
} [ground:witnessed:loop-design] [conf:0.90] [state:confirmed]

---

## S3 ENTEGRASYON NOKTALARI CERCEVESI (Integration Points Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_integration]] -->
<!-- [[MOR:root:N-T-G]] Entegrasyon = root for integrate-combine-connect -->
<!-- [[COM:Entegrasyon+Nokta+Tanimlama]] German: Integrations-Punkt-Definition -->

### S3.1 Iyilestirme Hedefi Olarak (As Improvement Target)

[define|neutral] TARGET_INTEGRATION := {
  kural_adi: "Hedef Entegrasyonu", // Target Integration
  auditor: "skill-auditor",
  evaluator: "eval-harness",
  benchmarks: ["skill-generation-benchmark-v1"],
  regressions: ["skill-forge-regression-v1"],
  iyilestirme_alanlari: [
    {
      alan: "phase_structure",
      mevcut: "8-faz (Faz 0-7)",
      durum: "TAMAMLANDI - Faz 0 uzmanlik yukleme v2.0'da eklendi"
    },
    {
      alan: "contract_compliance",
      mevcut: "Faz 5",
      potansiyel: "Daha kati sema dogrulamasi"
    },
    {
      alan: "failure_handling",
      mevcut: "Faz 6",
      potansiyel: "Zaman asimi varsayilanlari ekle"
    }
  ]
} [ground:witnessed:integration-spec] [conf:0.88] [state:confirmed]

### S3.2 Iyilestirme Uygulayicisi Olarak (As Improvement Applier)

[define|neutral] APPLIER_INTEGRATION := {
  kural_adi: "Uygulayici Entegrasyonu", // Applier Integration
  girisler: {
    proposal: "prompt-forge'dan", // From prompt-forge
    target: "Iyilestirilecek beceri yolu", // Path to skill to improve
    audit_report: "skill-auditor'dan" // From skill-auditor
  },
  surec: [
    "Oneri degisikliklerini ayristir", // Parse proposal changes
    "Hedef beceriye degisiklikleri uygula", // Apply changes to target skill
    "Yapi uyumunu dogrula", // Validate structure compliance
    "Yeni surum icin test vakalari olustur", // Generate test cases for new version
    "Aday surumu cikart" // Output candidate version
  ],
  ciktilar: {
    candidate_skill: "Degistirilmis beceri icerigi",
    validation_report: "Yapi uyum kontrolu",
    test_cases: "Eval harness icin"
  }
} [ground:witnessed:applier-design] [conf:0.88] [state:confirmed]

### S3.3 Kendini-Iyilestirme Modu (Self-Improvement Mode)

[define|neutral] SELF_IMPROVEMENT := {
  kural_adi: "Kendini-Iyilestirme Modu", // Self-Improvement Mode
  tetikleyici: "Bootstrap dongusu dongusu", // Bootstrap loop cycle
  guvenlik_onlemleri: [
    "ONCEKI surumu kullanir (degistirilmis degil)", // Uses PREVIOUS version
    "skill-generation-benchmark-v1 gecmeli", // Must pass benchmark
    "skill-forge-regression-v1 gecmeli", // Must pass regression
    "Uygulamadan once onceki surum arsivlenir", // Previous version archived
    "Kirici degisiklikler icin insan kapisi" // Human gate for breaking changes
  ],
  surec: [
    "skill-auditor mevcut skill-forge'u analiz eder",
    "prompt-forge iyilestirme onerileri uretir",
    "skill-forge (ONCEKI surum) onerileri uygular",
    "eval-harness yeni skill-forge'u test eder",
    "Iyilesmisse: commit. Gerilemisse: reddet."
  ],
  yasakli_degisiklikler: [
    "Guvenlik onlemlerini kaldirma", // Removing safeguards
    "Eval harness'i atlama", // Bypassing eval harness
    "Faz yapisini kaldirma", // Removing phase structure
    "Sozlesme gereksinimlerini zayiflatma" // Weakening contract requirements
  ]
} [ground:witnessed:self-improvement-design] [conf:0.92] [state:confirmed]

---

## S4 DEGISTIRILMIS IS AKISI CERCEVESI (Modified Workflow Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_workflow]] -->
<!-- [[MOR:root:I-S]] Is = root for work-operation-process -->
<!-- [[COM:Degistirilmis+Is+Akis]] German: Modifizierter-Arbeits-Fluss -->

[define|neutral] WORKFLOW_VARIANTS := {
  kural_adi: "Is Akisi Varyantlari", // Workflow Variants
  varyantlar: [
    {
      ad: "Standart Beceri Olusturma", // Standard Skill Creation
      akis: "Kullanici Istegi -> Skill Forge -> Yeni Beceri",
      durum: "degistirilmedi"
    },
    {
      ad: "Beceri Iyilestirme", // Skill Improvement
      akis: "Denetim Raporu -> Prompt Forge -> Oneri -> Skill Forge -> Iyilestirilmis Beceri -> Eval Harness -> KABUL/REDDET",
      durum: "yeni"
    },
    {
      ad: "Kendini-Iyilestirme", // Self-Improvement
      akis: "Denetim Raporu -> Prompt Forge -> Skill Forge Onerisi -> Skill Forge (ONCEKI) -> Iyilestirilmis Skill Forge -> Eval Harness -> KABUL/REDDET",
      durum: "yeni"
    }
  ]
} [ground:witnessed:workflow-design] [conf:0.90] [state:confirmed]

---

## S5 YENI ISLEMLER CERCEVESI (New Operations Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_operation]] -->
<!-- [[MOR:root:I-S-L]] Islem = root for operation-process-action -->
<!-- [[COM:Yeni+Islem+Tanimlama]] German: Neue-Operation-Definition -->

### S5.1 Islem: Iyilestirme Onerisini Uygula (Operation: Apply Improvement Proposal)

[define|neutral] APPLY_PROPOSAL_OPERATION := {
  kural_adi: "Iyilestirme Onerisini Uygula", // Apply Improvement Proposal
  girisler: {
    proposal_id: "prop-123",
    target_path: ".claude/skills/example/SKILL.md"
  },
  adimlar: [
    {
      ad: "Oneriyi bellekten yukle",
      memory_key: "improvement/proposals/{proposal_id}"
    },
    {
      ad: "Hedef beceriyi oku",
      dogrulama: "Dosya mevcut"
    },
    {
      ad: "Her degisikligi uygula",
      for_each: "proposal.changes",
      action: "onceki ile sonrakiyi degistir",
      dogrulama: "Onceki metin dosyada bulundu"
    },
    {
      ad: "Yapi uyumunu dogrula",
      kontroller: [
        "Tum 8 faz mevcut (0-7)",
        "Islemler icin sozlesmeler tanimli",
        "Hata isleme mevcut"
      ]
    },
    {
      ad: "Ciktiyi olustur",
      ciktilar: [
        "Degistirilmis beceri icerigi",
        "Dogrulama raporu",
        "Yeni test vakalari"
      ]
    }
  ],
  cikti: {
    candidate_content: "Degisikliklerle tam beceri",
    validation: {
      structure_compliant: "true|false",
      phases_present: "[0,1,2,3,4,5,6,7]",
      issues: "[]"
    },
    new_test_cases: "Degisiklik 1 icin test"
  }
} [ground:witnessed:operation-spec] [conf:0.88] [state:confirmed]

### S5.2 Islem: Kendini Yeniden Olustur (Operation: Rebuild Self)

[define|neutral] REBUILD_SELF_OPERATION := {
  kural_adi: "Kendini Yeniden Olustur", // Rebuild Self
  tetikleyici: "Bootstrap dongusu kendini-iyilestirme",
  guvenlik_onlemleri: [
    {
      kosul: "Sadece bootstrap-loop tarafindan tetiklenir",
      zorunlu: true
    },
    {
      kosul: "Arsivlenmis ONCEKI surumu kullanir",
      zorunlu: true
    },
    {
      kosul: "Kirici degisiklikler icin insan kapisi",
      zorunlu: true
    }
  ],
  adimlar: [
    {
      ad: "Onceki surum yolunu al",
      kaynak: ".claude/skills/skill-forge/.archive/SKILL-v{N-1}.md"
    },
    {
      ad: "Onceki Skill Forge'u yukle",
      dogrulama: "Arsiv mevcut"
    },
    {
      ad: "Mevcut Skill Forge icin oneriyi yukle",
      kaynak: "improvement/proposals/{proposal_id}"
    },
    {
      ad: "Oneriyi ONCEKI surum kullanarak uygula",
      not: "Bu sonsuz kendine-referansi onler"
    },
    {
      ad: "Adayi cikart",
      cikti: "skill-forge-v{N+1} adayi"
    }
  ],
  cikti: {
    candidate_path: ".claude/skills/skill-forge/SKILL-candidate.md",
    applied_with_version: "v{N-1}"
  }
} [ground:witnessed:rebuild-spec] [conf:0.90] [state:confirmed]

---

## S6 EVAL HARNESS ENTEGRASYONU CERCEVESI (Eval Harness Integration Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_test]] -->
<!-- [[MOR:root:D-G-R]] Degerlendirme = root for evaluate-assess-test -->
<!-- [[COM:Eval+Harness+Entegrasyon]] German: Eval-Harness-Integration -->

### S6.1 Benchmarklar (Benchmarks)

[define|neutral] SKILL_GENERATION_BENCHMARK := {
  kural_adi: "Beceri Uretim Benchmark", // Skill Generation Benchmark
  id: "skill-generation-benchmark-v1",
  testler: [
    {
      id: "sg-001",
      giris: "JSON dogrulama icin mikro-beceri olustur",
      beklenen: {
        has_7_phases: true,
        has_contracts: true,
        has_error_handling: true
      },
      puanlama: {
        functionality: "0.0-1.0",
        contract_compliance: "0.0-1.0",
        error_coverage: "0.0-1.0"
      }
    }
  ],
  minimum_gecme: {
    functionality: 0.75,
    contract_compliance: 0.80,
    error_coverage: 0.75
  }
} [ground:witnessed:benchmark-spec] [conf:0.88] [state:confirmed]

### S6.2 Regresyonlar (Regressions)

[define|neutral] SKILL_FORGE_REGRESSION := {
  kural_adi: "Skill Forge Regresyon Testi", // Skill Forge Regression Test
  id: "skill-forge-regression-v1",
  testler: [
    {
      id: "sfr-001",
      ad: "8-faz yapisi korundu",
      beklenen: "Cikti tum 8 fazi (0-7) icerir",
      gecmeli: true
    },
    {
      id: "sfr-002",
      ad: "Sozlesme belirtimi mevcut",
      beklenen: "Cikti giris/cikis sozlesmelerini icerir",
      gecmeli: true
    },
    {
      id: "sfr-003",
      ad: "Hata isleme dahil",
      beklenen: "Cikti hata isleme bolumu icerir",
      gecmeli: true
    },
    {
      id: "sfr-004",
      ad: "Test vakalari uretildi",
      beklenen: "Cikti test vakalari icerir",
      gecmeli: true
    }
  ],
  basarisizlik_esigi: 0
} [ground:witnessed:regression-spec] [conf:0.90] [state:confirmed]

---

## S7 BELLEK ISIM ALANLARI CERCEVESI (Memory Namespaces Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_namespace]] -->
<!-- [[MOR:root:B-L-K]] Bellek = root for memory-store-retain -->
<!-- [[COM:Bellek+Isim+Alan]] German: Speicher-Namens-Raum -->

[define|neutral] MEMORY_NAMESPACES := {
  kural_adi: "Bellek Isim Alanlari", // Memory Namespaces
  isim_alanlari: [
    {
      yol: "skill-forge/generations/{id}",
      amac: "Skill Forge tarafindan olusturulan beceriler"
    },
    {
      yol: "skill-forge/improvements/{id}",
      amac: "Uygulanan iyilestirmeler"
    },
    {
      yol: "skill-forge/self-rebuilds/{id}",
      amac: "Kendini-iyilestirme donguleri"
    },
    {
      yol: "improvement/commits/skill-forge",
      amac: "Surum gecmisi"
    }
  ]
} [ground:witnessed:memory-design] [conf:0.92] [state:confirmed]

---

## S8 GUVENLIK KISITLAMALARI CERCEVESI (Safety Constraints Frame)
<!-- [[HON:sonkeigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:tiao_constraint]] -->
<!-- [[MOR:root:G-V-N]] Guvenlik = root for safety-security-trust -->
<!-- [[COM:Guvenlik+Kisitlama+Tanimlama]] German: Sicherheits-Einschrankung-Definition -->

### S8.1 Anti-Kaliplar: ASLA Yapilmamalilar (Anti-Patterns: NEVER Do)

[assert|emphatic] ANTI_PATTERNS_NEVER := {
  kural_adi: "Asla Yapilmamalilar", // NEVER Do
  yasaklar: [
    {
      hata_adi: "Eval Harness Atlama",
      belirti: "Kendini-iyilestirme sirasinda test olmadan degisiklik",
      yanlis: "Dogrulama olmadan degisiklikleri uygula",
      dogru: "Tum degisiklikler eval harness'dan gecmeli",
      onleme: "Zorunlu test kapisi"
    },
    {
      hata_adi: "Mevcut Surum Kullanimi",
      belirti: "Skill Forge kendini yeniden olusturmak icin kendini kullaniyor",
      yanlis: "Mevcut surumu kendini yeniden olusturmak icin kullan",
      dogru: "N-1 surumunu kullanmali",
      onleme: "Surum kontrolu zorunlu"
    },
    {
      hata_adi: "Insan Kapisi Olmadan Kirici Degisiklikler",
      belirti: "Onemli degisiklikler onaysiz uygulanir",
      yanlis: "Kirici degisiklikleri otomatik kabul et",
      dogru: "Insan kapisi gerektir",
      onleme: "Kirici degisiklik algilama"
    },
    {
      hata_adi: "Guvenlik Onlemlerini Kaldirma",
      belirti: "Iyilestirme guvenlik kontrollerini kaldirir",
      yanlis: "Guvenlik kontrollerini kaldiran degisikliklere izin ver",
      dogru: "Tum guvenlik onemleri korunmali",
      onleme: "Guvenlik kontrolu dogrulamasi"
    },
    {
      hata_adi: "Sozlesme Gereksinimlerini Zayiflatma",
      belirti: "Iyilestirme sozlesme katiliklarini azaltir",
      yanlis: "Sozlesme dogrulamasini gevset",
      dogru: "Sozlesme gereksinimleri zayiflatilmamali",
      onleme: "Sozlesme karsilastirma kontrolu"
    }
  ]
} [ground:witnessed:safety-policy] [conf:0.95] [state:confirmed]

### S8.2 En Iyi Uygulamalar: HER ZAMAN Yapilmalilar (Best Practices: ALWAYS Do)

[assert|emphatic] BEST_PRACTICES_ALWAYS := {
  kural_adi: "Her Zaman Yapilmalilar", // ALWAYS Do
  uygulamalar: [
    "Uygulamadan once arsivle", // Archive before apply
    "Tam regresyon suitini calistir", // Run full regression suite
    "Pozitif iyilestirme deltasi gerektir", // Require positive improvement delta
    "Tum kendini-iyilestirme girisimlerini kaydet", // Log all self-improvement attempts
    "Insan kapilarini dikkate al" // Respect human gates
  ]
} [ground:witnessed:best-practices] [conf:0.92] [state:confirmed]

---

## S9 SURUM KONTROLU CERCEVESI (Version Control Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_version]] -->
<!-- [[MOR:root:S-R-M]] Surum = root for version-edition-release -->
<!-- [[COM:Surum+Kontrol+Yapi]] German: Versions-Kontroll-Struktur -->

[define|neutral] VERSION_CONTROL_STRUCTURE := {
  kural_adi: "Surum Kontrol Yapisi", // Version Control Structure
  dizin_yapisi: {
    root: ".claude/skills/skill-forge/",
    dosyalar: [
      {
        yol: "SKILL.md",
        aciklama: "Mevcut surum"
      },
      {
        yol: "RECURSIVE-IMPROVEMENT-ADDENDUM.md",
        aciklama: "Bu dosya"
      },
      {
        yol: ".archive/SKILL-v1.0.0.md",
        aciklama: "Onceki surumler"
      },
      {
        yol: ".archive/SKILL-v1.1.0.md",
        aciklama: "Onceki surumler"
      },
      {
        yol: "CHANGELOG.md",
        aciklama: "Surum gecmisi"
      }
    ]
  }
} [ground:witnessed:version-structure] [conf:0.90] [state:confirmed]

---

## S10 SONUC CERCEVESI (Conclusion Frame)
<!-- [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
<!-- [[MOR:root:S-N-C]] Sonuc = root for conclusion-result-end -->
<!-- [[COM:Sonuc+Ozet+Bildiri]] German: Schlussfolgerung-Zusammenfassung -->
Zaversheno. (Russian: Complete.)

[assert|confident] ADDENDUM_SUMMARY := {
  amac: "Skill-forge ile ozyineleme iyilestirme sistemi entegrasyonu", // purpose
  metodoloji: "Guvenlik onlemli uc-modlu iyilestirme dongusu", // methodology
  ciktilar: [
    "Hedef modu entegrasyonu",
    "Uygulayici modu entegrasyonu",
    "Kendini-iyilestirme modu (guvenli)"
  ],
  anahtar_kisitlama: "Kendini-iyilestirme ONCEKI surumu kullanir, asla mevcutu degil",
  kalite_kapilari: ["Benchmark testi", "Regresyon testi", "Insan kapisi"]
} [ground:witnessed:implementation] [conf:0.90] [state:confirmed]

---

*Promise: `<promise>RECURSIVE_IMPROVEMENT_ADDENDUM_VCL_V3.1.1_COMPLIANT</promise>`*
