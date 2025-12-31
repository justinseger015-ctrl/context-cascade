# Uzmanlik Sistemi Eklentisi (Expertise System Addendum)

---
<!-- S1.0 KANITSAL CERCEVE (Evidential Frame Activation) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_document]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- S2.0 BELGE USTVERILERI (Document Metadata) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_version]] -->
---

## Belge Ustverileri Cercevesi (Document Metadata Frame)
Surum bilgileri dogrudan gozleme dayanir. Zaversheno (Tamamlandi).

<!-- [[MOR:root:S-R-M]] Surum = root morpheme for version-release-mark -->
<!-- [[COM:Uzmanlik+Sistemi+Entegrasyon]] German compound: Expertensystemintegration -->
[define|neutral] BELGE_METADATA := {
  surum: "2.1.0", // Turkish: version
  entegre_eden: ["expertise-manager", "domain-expert"],
  not: "Bu eklenti 5-Faz Ajan Olusturma Metodolojisi (v2.0) ile uzmanlik-farkinda ajan tasarimini genisletir. Faz 0 artik ana SKILL.md'ye entegre edilmistir."
} [ground:witnessed:file-metadata] [conf:0.95] [state:confirmed]

---
<!-- S3.0 YENI FAZ 0: ALAN UZMANLIK YUKLEME (New Phase 0: Domain Expertise Loading) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_phase]] [[SPC:kuzey/akis-baslangici]] -->
---

## Yeni Faz 0 Cercevesi (New Phase 0 Frame)
Faz 1'den ONCE eklenir. Uzmanlik baglami ile ajanlar alan bilgisine sahip olur.

### Amac

<!-- [[MOR:root:A-M-C]] Amac = root morpheme for purpose-goal-objective -->
[assert|neutral] FAZ_0_AMACI := {
  aciklama: "Uzmanlik baglami ile olusturulan ajanlar gomulu alan bilgisine sahiptir - kod yapisi, desenler ve bilinen sorunlari baslamadan once 'bilirler'",
  fayda: "Arama thrash'ini azaltir, dogrulugu arttirir, ajan verimliliğini yukseltir"
} [ground:witnessed:design-rationale] [conf:0.90] [state:confirmed]

### Surecler

<!-- [[MOR:root:S-R-C]] Surec = root morpheme for process-procedure-flow -->
[define|neutral] FAZ_0_SURECI := {
  adimlar: [
    {adim: 1, islem: "Ajan isteginden birincil alani tanimla", fonksiyon: "identifyAgentDomain(agentRequest)"},
    {adim: 2, islem: "Uzmanlik dosyasini kontrol et", yol: ".claude/expertise/{alan}.yaml"},
    {adim: 3, islem: "Uzmanlik varsa dogrula", komut: "/expertise-validate {alan} --fix"},
    {adim: 4, islem: "Uzmanlik YAML yukle", fonksiyon: "loadYAML(expertisePath)"},
    {adim: 5, islem: "Ajana uygun baglami cikar", cikti: "agentContext"},
    {adim: 6, islem: "Ajana gomme icin depola", fonksiyon: "setAgentContext('expertise', agentContext)"}
  ],
  baglam_yapisi: {
    dosya_konumlari: "expertise.file_locations",
    desenler: "expertise.patterns",
    bilinen_sorunlar: "expertise.known_issues",
    yonlendirme_sablonlari: "expertise.routing.task_templates",
    bagimliliklar: "expertise.relationships.depends_on",
    bagimli_olanlar: "expertise.relationships.depended_by"
  }
} [ground:witnessed:implementation] [conf:0.88] [state:confirmed]

### Uzmanlik Yoksa

[assert|neutral] KESIF_MODU := {
  kosul: "Alan icin uzmanlik dosyasi yoksa",
  eylem: "Ajan kesif modunda calisir",
  cikti: "setAgentContext('discoveryMode', true)"
} [ground:witnessed:fallback-logic] [conf:0.88] [state:confirmed]

---
<!-- S4.0 GELISTIRILMIS FAZ 2: UZMANLIK CIKARTMA (Enhanced Phase 2: Expertise Extraction) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_phase]] -->
---

## Gelistirilmis Faz 2 Cercevesi (Enhanced Phase 2 Frame)
Uzmanlik bilissel cerceve ile entegre edilir.

### Alan Bilgisi Bolumu Ekleme

<!-- [[MOR:root:B-L-G]] Bilgi = root morpheme for knowledge-information-data -->
<!-- [[COM:Alan+Bilgi+Gomme]] German compound: Domaenenwisseneinbettung -->
[define|neutral] ALAN_BILGISI_BOLUMU := {
  baslik: "Alan Bilgisi (Uzmanliktan)",
  alt_bolumler: [
    {
      ad: "Bildigi Dosya Konumlari",
      kaynak: "expertise.file_locations",
      icerik: ["Birincil kaynak", "Testler", "Yapilandirma", "Ek konumlar"]
    },
    {
      ad: "Takip Ettigi Desenler",
      kaynak: "expertise.patterns",
      icerik: ["Mimari", "Veri akisi", "Hata isleme"]
    },
    {
      ad: "Kacindigi Sorunlar",
      kaynak: "expertise.known_issues",
      icerik: ["id", "aciklama", "siddet", "hafifletme"]
    },
    {
      ad: "Saygı Duydugu Bagimliliklar",
      kaynak: "expertise.relationships.depends_on",
      icerik: ["alan", "neden", "baglanti_derecesi"]
    }
  ],
  not: "Bu bilgi `.claude/expertise/{alan}.yaml` dosyasindan gelir ve her eylem oncesi mevcut koda karsi dogrulanir."
} [ground:witnessed:template-structure] [conf:0.88] [state:confirmed]

---
<!-- S5.0 GELISTIRILMIS AJAN FRONTMATTER (Enhanced Agent Frontmatter) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_metadata]] -->
---

## Gelistirilmis Ajan Frontmatter Cercevesi (Enhanced Agent Frontmatter Frame)
Uzmanlik entegrasyon meta verileri eklenir.

<!-- [[MOR:root:M-T-V]] Meta = root morpheme for meta-about-beyond -->
[define|neutral] UZMANLIK_FRONTMATTER := {
  alan: "expertise_integration",
  alanlar: {
    birincil_alan: "${alan}",
    ikincil_alanlar: [],
    baslangicta_yukle: true,
    eylem_oncesi_dogrula: true,
    eylem_sonrasi_oneriler: true
  },
  gomulu_bilgi: {
    dosya_konumlari: true,
    desenler: true,
    bilinen_sorunlar: true,
    yonlendirme_sablonlari: true
  },
  mcp_serverlari: {
    zorunlu: ["memory-mcp"],
    aciklama: "Uzmanlik kaliciliği icin"
  },
  hooklar: {
    on: "Alan uzmanligini yukle ve dogrula",
    post: "Ogrenimleri cikar ve guncelleme oner"
  }
} [ground:witnessed:frontmatter-spec] [conf:0.88] [state:confirmed]

---
<!-- S6.0 GELISTIRILMIS FAZ 3: SISTEM ISTEMI YAPIMI (Enhanced Phase 3: System Prompt Construction) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_phase]] -->
---

## Gelistirilmis Faz 3 Cercevesi (Enhanced Phase 3 Frame)
Sistem istemine uzmanlik referanslari eklenir.

### Uzmanlik ile Ajan Kimligi

<!-- [[MOR:root:K-M-L]] Kimlik = root morpheme for identity-self-persona -->
<!-- [[COM:Uzmanlik+Farkinda+Kimlik]] German compound: Expertenbewusstidentitaet -->
[define|neutral] UZMANLIK_KIMLIK_YAPISI := {
  baslik: "{ajan_adi}",
  cekirdek_kimlik: "Ben **{rol}**, **{alan}** alaninda uzman ve gomulu alan uzmanligina sahibim.",
  alan_bilgisi_aciklamasi: "Genel ajanlarin aksine, bu kod tabani hakkinda **on-yuklu bilgiye** sahibim:",
  bolumler: [
    "Seylerin Nerede Oldugunu Biliyorum",
    "Seylerin Nasil Calistigini Biliyorum",
    "Nelerden Kacinmam Gerektigini Biliyorum",
    "Gorevleri Nasil Yonlendirecegimi Biliyorum"
  ],
  kullanim_yontemi: [
    "Eylemden Once: Uzmanligimi mevcut koda karsi dogrularim",
    "Eylem Sirasinda: Bilinen konumlari ve desenleri kullanirim (arama thrash'i yok)",
    "Eylem Sonrasi: Uzmanliği guncellemek icin ogrenimleri cikarim"
  ],
  verimlilik_aciklamasi: "Bu beni sifirdan baslayan bir ajandan daha verimli ve dogru yapar."
} [ground:witnessed:prompt-template] [conf:0.88] [state:confirmed]

---
<!-- S7.0 YENI FAZ 4.5: UZMANLIK DOGRULAMA (New Phase 4.5: Expertise Validation) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:tiao_phase]] -->
---

## Yeni Faz 4.5 Cercevesi (New Phase 4.5 Frame)
Faz 4'ten SONRA eklenir. Ajanin uzmanligi dogru kullandigini dogrular.

<!-- [[MOR:root:D-G-R]] Dogrulama = root morpheme for validation-verification-confirmation -->
[define|neutral] UZMANLIK_DOGRULAMA_KONTROLLERI := {
  uzmanlik_kullanimi: [
    {kontrol: "ajan_dosya_konumlarini_referanslar", deger: true},
    {kontrol: "ajan_belgelenen_desenleri_takip_eder", deger: true},
    {kontrol: "ajan_bilinen_sorunlardan_kacinir", deger: true},
    {kontrol: "ajan_eylem_oncesi_hook'a_sahip", deger: true},
    {kontrol: "ajan_eylem_sonrasi_hook'a_sahip", deger: true}
  ],
  ogrenme_yetenegi: [
    {kontrol: "ogrenimleri_cikarabilir", deger: true},
    {kontrol: "guncellemeler_onerebilir", deger: true},
    {kontrol: "gozlemleri_takip_eder", deger: true}
  ]
} [ground:witnessed:validation-spec] [conf:0.88] [state:confirmed]

---
<!-- S8.0 KESIF MODU AJANI (Discovery Mode Agent) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_mode]] -->
---

## Kesif Modu Ajani Cercevesi (Discovery Mode Agent Frame)
Uzmanlik yokken kullanilir.

<!-- [[MOR:root:K-S-F]] Kesif = root morpheme for discovery-exploration-finding -->
[define|neutral] KESIF_MODU_SABLONU := {
  baslik: "Kesif Modu",
  aciklama: "Ben **{alan}** alani icin **kesif modunda** calisiyorum.",
  ilk_gorev: "Alana ozel calisma yurutmeden once:",
  kesif_sureci: [
    "Alan yapisini kes (dosyalar, desenler, varliklar)",
    "Ilk uzmanlik dosyasini olustur",
    "Cekismeli dogrulama icin siraya koy"
  ],
  kesif_adimlari: [
    "{alan} ile ilgili dosyalari tara",
    "Koddan desenleri cikar",
    "Anahtar varliklari belgele",
    ".claude/expertise/{alan}.yaml olustur",
    "'Uzmanlik olusturuldu, /expertise-challenge {alan} calistir' raporla"
  ],
  kesif_sonrasi_notu: "Uzmanlik olustugunda, gelecek ajanlar gomulu bilgiye sahip olacak ve daha verimli calisabilecek."
} [ground:witnessed:discovery-template] [conf:0.88] [state:confirmed]

---
<!-- S9.0 UZMANLIK ILE AJAN TURLERI (Agent Types with Expertise) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[CLS:ge_type]] -->
---

## Uzmanlik ile Ajan Turleri Cercevesi (Agent Types with Expertise Frame)
Iki ana ajan turu tanimlanmistir.

### Alan Uzman Ajani

<!-- [[MOR:root:U-Z-M]] Uzman = root morpheme for expert-specialist-authority -->
[define|neutral] ALAN_UZMAN_AJANI := {
  temel_ajan: "domain-expert",
  uzmanlik: {birincil: "${alan}", gomulu: true},
  yetenekler: [
    "uzmanlik_yukleme",
    "eylem_oncesi_dogrulama",
    "ogrenme_cikartma",
    "guncelleme_onerisi"
  ]
} [ground:witnessed:agent-type-spec] [conf:0.88] [state:confirmed]

### Cok-Alanli Ajan

<!-- [[COM:Cok+Alan+Ajan]] German compound: Mehrdomaenenagent -->
[define|neutral] COK_ALANLI_AJAN := {
  uzmanlik: {
    alanlar: {
      birincil: "${ana_alan}",
      ikincil: ["${alan2}", "${alan3}"]
    },
    yukleme_stratejisi: "on_demand"
  },
  yonlendirme: {
    uzmanlik_sablonlarini_kullan: true,
    aciklama: "Alan erisildiqinde uzmanligi yukle"
  }
} [ground:witnessed:agent-type-spec] [conf:0.88] [state:confirmed]

---
<!-- S10.0 ENTEGRASYON OZETI (Integration Summary) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
---

## Entegrasyon Ozeti Cercevesi (Integration Summary Frame)
Her faz icin eklenen yetenekler. Zaversheno (Tamamlandi).

<!-- [[MOR:root:O-Z-T]] Ozet = root morpheme for summary-abstract-synopsis -->
[define|neutral] ENTEGRASYON_OZETI := {
  fazlar: [
    {faz: "0 (YENI)", eklenen: "Uzmanlik Yukleme", amac: "Alan baglami yukle"},
    {faz: "1", eklenen: "Analizde Uzmanlik", amac: "Alan bilgisi arastirmayi bilgilendirir"},
    {faz: "2", eklenen: "Cikartmada Uzmanlik", amac: "Alan bilgisini gom"},
    {faz: "3", eklenen: "Istemde Uzmanlik", amac: "Kimlikte uzmanliği referansla"},
    {faz: "4", eklenen: "Testte Uzmanlik", amac: "Dogru kullanimı dogrula"},
    {faz: "4.5 (YENI)", eklenen: "Uzmanlik Dogrulama", amac: "Uzmanlik entegrasyonunu kontrol et"}
  ]
} [ground:witnessed:integration-map] [conf:0.90] [state:confirmed]

---
<!-- S11.0 KULLANIM ORNEGI (Usage Example) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_example]] -->
---

## Kullanim Ornegi Cercevesi (Usage Example Frame)
Uzmanlik-farkinda ajan olusturma sureci.

<!-- [[MOR:root:O-R-N]] Ornek = root morpheme for example-sample-instance -->
[assert|neutral] KULLANIM_ORNEGI := {
  giris: "'Auth sistemimiz icin guvenlik analisti ajani olustur'",
  cikti_akisi: [
    {faz: "[FAZ 0]", islem: "Alan uzmanligi yukleniyor...", sonuc: "authentication icin uzmanlik bulundu"},
    {faz: "[UZMANLIK]", islem: "Dogrulandi (guven_seviyesi: validated)", sonuc: "Ajan bilecek: 5 dosya konumu, 4 desen, 1 bilinen sorun, 2 yonlendirme sablonu"},
    {faz: "[FAZ 1]", islem: "Uzmanlik baglami ile ilk analiz...", sonuc: "Dosya kesfi atlanir (uzmanliktan biliniyor), guvenlige ozel desenlere odaklaniyor"},
    {faz: "[FAZ 2]", islem: "Uzmanlik cikartma...", sonuc: "Dosya konumlari ajan kimligine gomulur, desenler metodolojiyle, bilinen sorunlar korumalarla"},
    {faz: "[FAZ 3]", islem: "Sistem istemi yapimi...", sonuc: "Ajan 'Seylerin nerede oldugunu biliyorum' bolumune sahip"},
    {faz: "[FAZ 4]", islem: "Test...", sonuc: "Ajanin uzmanligi dogru referansladigi dogrulaniyor"},
    {faz: "[TAMAMLANDI]", islem: "Ajan gomulu alan uzmanligi ile olusturuldu", sonuc: "Uretim hazir"}
  ]
} [ground:witnessed:usage-trace] [conf:0.88] [state:confirmed]

---
<!-- S12.0 REFERANSLAR (References) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_reference]] -->
---

## Referanslar Cercevesi (References Frame)
Ilgili dokumantasyon.

<!-- [[MOR:root:R-F-R]] Referans = root morpheme for reference-source-citation -->
[assert|neutral] REFERANSLAR := {
  ilgili_belgeler: [
    {yol: ".claude/skills/EXPERTISE-INTEGRATION-MODULE.md", aciklama: "Tam entegrasyon desenleri"},
    {yol: "agents/foundry/expertise/domain-expert.md", aciklama: "Temel alan uzman ajani"}
  ]
} [ground:witnessed:documentation] [conf:0.95] [state:confirmed]

---
<!-- S13.0 SONUC (Conclusion) [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[CLS:ge_summary]] -->
---

## Beceri Ozeti Cercevesi (Skill Summary Frame)
Zaversheno. Etot addendum byl uspeshno realizovan. (Rusca: Tamamlandi. Bu eklenti basariyla uygulanmistir.)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result-outcome -->
<!-- [[COM:Uzmanlik+Sistemi+Entegrasyon+Ozeti]] German compound: Expertensystemintegrierungszusammenfassung -->
[assert|confident] EKLENTI_OZETI := {
  amac: "5-Faz Ajan Olusturma Metodolojisini uzmanlik-farkinda ajan tasarimi ile genisletme", // Turkish: purpose
  metodoloji: "Faz 0 uzmanlik yukleme, Faz 4.5 uzmanlik dogrulama, kesif modu fallback", // Turkish: methodology
  ciktilar: [
    "Alan uzman ajan sablonu",
    "Cok-alanli ajan sablonu",
    "Kesif modu is akisi",
    "Uzmanlik entegrasyon kontrolleri"
  ],
  kalite_kapilari: [
    "Uzmanlik yukleme dogrulamasi",
    "Uzmanlik referans kontrolu",
    "Ogrenme cikartma yetenegi"
  ]
} [ground:witnessed:addendum-execution] [conf:0.90] [state:confirmed]

---
*Soz (Promise): `<promise>EXPERTISE_ADDENDUM_VCL_V3.1.1_VERIX_COMPLIANT</promise>`*
