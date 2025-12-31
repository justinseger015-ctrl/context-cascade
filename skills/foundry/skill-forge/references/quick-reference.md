---
<!-- HIZLI REFERANS DOKUMANI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_reference]] -->
---

# Beceri Ocagi Hizli Referans (Skill Forge Quick Reference)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

<!-- [[MOR:root:H-Z-R]] Hizli = root for quick-fast-reference -->
<!-- [[COM:Beceri+Ocagi+Hizli+Referans]] Skill Forge Quick Reference -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Complete - ready for use) -->
<!-- [[SPC:merkez/kaynak]] Central reference location -->

---

## Referans Tanimlari (Reference Definitions)

[define|neutral] QUICK_REFERENCE := {
  id: "REF-QR-001",
  referans_adi: "Beceri Ocagi Hizli Referans",
  amac: "Yedi fazli Beceri Ocagi metodolojisi icin ozet rehber saglamak",
  kullanim: "Beceri olusturma sirasinda hizli basvuru",
  iliskili_dok: "SKILL.md (kapsamli rehber)"
} [ground:witnessed:quick-reference-usage] [conf:0.92] [state:confirmed]

---

## Faz 1: Niyet Arkeolojisi (Intent Archaeology)

<!-- [[MOR:root:N-Y-T]] Niyet = root for intent-purpose-will -->
<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektirir -->

[define|neutral] PHASE_1 := {
  faz_adi: "Niyet Arkeolojisi",
  hedef: "Hangi becerinin gercekten olusturulmasi gerektigini anlamak",
  sure: "5-10 dakika"
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler (Key Actions)

[assert|neutral] Faz 1 temel eylemleri [ground:witnessed:phase-1-process] [conf:0.88] [state:confirmed]

- Gercek niyeti anlamak icin ekstrapolasyon ilkelerini uygula
- Ortuk varsayimlari ve gizli kisitlamalari ortaya cikar
- Problem uzayini ve baglamsal iliskileri haritalandir
- Gerektiginde stratejik aciklayici sorular sor
- Tasarim icin temel olarak cekirdek anlayisi belgele

### Kritik Sorular (Critical Questions)

- Bu beceriye gercek is akislarinda ne tetikler?
- Bu is akisini zorlastiran veya tekrarlayan ne yapar?
- Istenen ciktilar somut olarak nasil gorunur?
- Hangi varyasyonlar veya uc vakalar islenmeli?
- Hangi kisitlamalar karsilanmali?

---

## Faz 2: Kullanim Vakasi Kristallestirme (Use Case Crystallization)

<!-- [[MOR:root:K-L-V]] Kullanim = root for usage-case-application -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Ongoing through examples) -->

[define|neutral] PHASE_2 := {
  faz_adi: "Kullanim Vakasi Kristallestirme",
  hedef: "Soyut anlayisi somut orneklere donusturmek",
  cikti: "Tasarim hedefi olarak hizmet eden somut ornekler"
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler

[assert|neutral] Faz 2 temel eylemleri [ground:witnessed:phase-2-process] [conf:0.88] [state:confirmed]

- 3-5 temsili kullanim ornegi uret
- Orneklerin hedeflenen kullanim kaliplariyla eslesmesini dogrula
- Kaliplari ve varyasyonlari belirlemek icin ornekleri analiz et
- Orneklerin beceri kapsamini yeterince karsiladigini sagla

---

## Faz 3: Yapisal Mimari (Structural Architecture)

<!-- [[MOR:root:Y-P-M]] Yapi = root for structure-architecture-form -->
<!-- [[COM:Yapisal+Mimari+Tasarim]] Structural Architecture Design -->

[define|neutral] PHASE_3 := {
  faz_adi: "Yapisal Mimari",
  hedef: "Kademeli aciklama ve istem ilkeleri kullanarak beceri yapisi tasarlamak",
  kararlar: ["SKILL.md vs paketli kaynaklar", "Istem kaliplari", "Bilgi organizasyonu"]
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler

[assert|neutral] Faz 3 temel eylemleri [ground:witnessed:phase-3-process] [conf:0.88] [state:confirmed]

- Meta veri, SKILL.md ve kaynaklar arasinda kademeli aciklama uygula
- Betikler, referanslar ve varliklar icin gereksinimleri belirle
- SKILL.md icerigini hiyerarsik organizasyonla yapilandir
- Kanita dayali istem tekniklerini uygula (oz-tutarlilik, planla-ve-coz, vb.)
- Aciklik ve kesiflenilebilirlik icin optimize et

---

## Faz 4: Meta Veri Muhendisligi (Metadata Engineering)

<!-- [[MOR:root:M-T-V]] Meta = root for metadata-naming-description -->
<!-- [[CLS:ge_metadata]] Classification: metadata -->

[define|neutral] PHASE_4 := {
  faz_adi: "Meta Veri Muhendisligi",
  hedef: "Optimal kesif icin stratejik ad ve aciklama olusturmak",
  onemi: "Bu ~100 kelime Claude'un beceriyi ne zaman bulup aktive edecegini belirler"
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler

[assert|neutral] Faz 4 temel eylemleri [ground:witnessed:phase-4-process] [conf:0.88] [state:confirmed]

- Akilda kalici, aciklayici, benzersiz ad sec
- Amac ve tetikleyicileri netlestiren 3-5 cumlelik aciklama yaz
- Dogal dil sorgulariyla eslesen terminoloji dahil et
- Net sinirlari belirt (becerinin ne yapip ne yapmadigini)
- Ucuncu sahis kullan ("Kullanildiginda..." degil "...gerektiginde kullanilir")

---

## Faz 5: Talimat Olusturma (Instruction Crafting)

<!-- [[MOR:root:T-L-M]] Talimat = root for instruction-command-directive -->
<!-- [[EVD:-DI<gozlem>]] Dogrudan yurutme gerektiren talimatlar -->

[define|neutral] PHASE_5 := {
  faz_adi: "Talimat Olusturma",
  hedef: "Istem en iyi uygulamalariyla acik, eyleme donusturulebilir beceri icerigi yazmak",
  stil: "\"Veriyi analiz et\" seklinde, \"Veriyi analiz etmelisin\" degil"
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler

[assert|neutral] Faz 5 temel eylemleri [ground:witnessed:phase-5-process] [conf:0.88] [state:confirmed]

- Emir kipi benimse (fiil-ilk talimatlar)
- Is akislari icin acik prosedur adimlari sagla
- Acik olmayan tasarim secenekleri icin gerekce ekle
- Basari kriterleri ve kalite mekanizmalari belirt
- Bilinen basarisizlik modlarini korumalarla ele al
- Paketli kaynaklara acik kullanim rehberligiyle referans ver

---

## Faz 6: Kaynak Gelistirme (Resource Development)

<!-- [[MOR:root:K-Y-N]] Kaynak = root for resource-source-material -->
<!-- [[CLS:lei_kaynak_turu]] Classification: resource types -->

[define|neutral] PHASE_6 := {
  faz_adi: "Kaynak Gelistirme",
  hedef: "Yeniden kullanilabilir betikler, referanslar ve varliklar olusturmak",
  organizasyon: {
    scripts: "calistirilabilir kod",
    references: "gerektiginde yuklenecek dokumantasyon",
    assets: "ciktilarda kullanilan dosyalar"
  }
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler

[assert|neutral] Faz 6 temel eylemleri [ground:witnessed:phase-6-process] [conf:0.88] [state:confirmed]

- Deterministik islemler icin iyi yorumlanmis betikler gelistir
- Net yapili referans dokumantasyonu derle
- Uretim kalitesinde varlik dosyalari sec
- Kaynak turleri arasinda ilgi ayrimi sagla
- SKILL.md'de kaynak kullanimini belgele

---

## Faz 7: Dogrulama ve Yineleme (Validation and Iteration)

<!-- [[MOR:root:D-G-R]] Dogrulama = root for validation-verification-confirmation -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Iterative process) -->

[define|neutral] PHASE_7 := {
  faz_adi: "Dogrulama ve Yineleme",
  hedef: "Dagitimdan once becerinin kalite standartlarini karsiladigini saglamak",
  komut: "python3 /mnt/skills/examples/skill-creator/scripts/package_skill.py <skill-path>"
} [ground:witnessed:phase-execution] [conf:0.90] [state:confirmed]

### Temel Eylemler

[assert|neutral] Faz 7 temel eylemleri [ground:witnessed:phase-7-process] [conf:0.88] [state:confirmed]

- Yapi ve meta veriyi kontrol etmek icin dogrulama betigini calistir
- Gercekci senaryolarda islevsellik testi yap
- Aciklik ve kullanilabilirlik degerlendirmesi yap
- Tasarimdaki anti-kaliplari kontrol et
- Geri bildirime dayali yinele
- Dogrulandiktan sonra dagitim icin paketle

---

## Stratejik Tasarim Ilkeleri (Strategic Design Principles)

<!-- [[HON:sonkeigo]] Saygili rehberlik -->
<!-- [[COM:Stratejik+Tasarim+Ilkeleri]] Strategic Design Principles -->

[assert|neutral] Surec boyunca uygulanacak ilkeler [ground:witnessed:design-principles] [conf:0.90] [state:confirmed]

| Ilke | Aciklama |
|------|----------|
| Kesif Icin Tasarla | Uygun aktivasyon saglayan meta veri olustur |
| Ogrenme Icin Optimize Et | Zamanla anlayis olusturan becerileri yapilandir |
| Ozguuluk ve Esnekligi Dengele | Yararli olmaya yetecek kadar ozel, adapte olacak kadar esnek |
| Surudurulebilirlige Oncelik Ver | Anlama, guncelleme, genisleme kolayligi |
| Sistemlerde Dusun | Becerilerin digerlerle nasil birlestigi |
| Kaliteye Nicelikten Once Vurgu | Az sayida iyi tasarlanmis beceri > cok sayida vasat beceri |

---

## Kanita Dayali Istem Teknikleri (Evidence-Based Prompting Techniques)

<!-- [[MOR:root:I-S-T]] Istem = root for prompt-technique-method -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli bilgi -->

[define|neutral] PROMPTING_TECHNIQUES := {
  oz_tutarlilik: "Analitik beceriler icin dogrulama ve coklu perspektifler",
  dusunce_programi: "Mantiksal gorevler icin adim adim acik akil yurutme",
  planla_ve_coz: "Karmasik is akislari icin once planla, sistematik yurutme, dogrula",
  yapisal_korumalar: "Kritik bilgi basinda/sonunda, net ayiricilar, hiyerarsik organizasyon",
  negatif_ornekler: "Bilinen basarisizlik kaliplari icin kacinilacaklar"
} [ground:research:prompting-studies] [conf:0.85] [state:confirmed]

---

## Yaygin Beceri Kaliplari (Common Skill Patterns)

<!-- [[CLS:ge_kalip]] Classification: patterns -->

[define|neutral] SKILL_PATTERNS := {
  is_akisi_tabanli: "Ardisik surecler (adim adim prosedurler icin en iyi)",
  gorev_tabanli: "Arac koleksiyonlari (farkli islemler/yetenekler icin en iyi)",
  referans_rehber: "Standartlar veya spesifikasyonlar (gereksinimler/rehberler icin en iyi)",
  yetenek_tabanli: "Entegre sistemler (coklu iliskili ozellikler icin en iyi)"
} [ground:witnessed:pattern-usage] [conf:0.88] [state:confirmed]

[assert|neutral] Kalipler gerektiginde karistirilip eslenebilir [ground:inferred:flexibility] [conf:0.85] [state:provisional]

---

## Dogrulama Kontrol Listesi (Validation Checklist)

<!-- [[MOR:root:K-N-T]] Kontrol = root for check-control-verification -->
<!-- [[EVD:-DI<gozlem>]] Dogrudan gozlem gerektiren kontroller -->

[direct|neutral] Paketlemeden once dogrula [ground:witnessed:validation-process] [conf:0.90] [state:confirmed]

- [ ] YAML on madde formati dogru
- [ ] Ad akilda kalici, aciklayici, benzersiz
- [ ] Aciklama net olarak ne ve ne zaman belirtir (3-5 cumle)
- [ ] Aciklama ucuncu sahis kullanir
- [ ] SKILL.md basindaki sonuna kadar emir kipi kullanir
- [ ] Talimatlar acik ve eyleme donusturulebilir
- [ ] Ornekler somut ve temsili
- [ ] Kaynaklar duzgun organize (scripts/, references/, assets/)
- [ ] Bilinen basarisizlik modlari ele alinmis
- [ ] Istem ilkeleri uygun sekilde uygulanmis
- [ ] Beceri gercekci senaryolarda test edilmis

---

## Kurulum Konumlari (Installation Locations)

<!-- [[SPC:kuzey/merkez]] Personal skills location -->
<!-- [[SPC:guney/yerel]] Project skills location -->

[define|neutral] INSTALLATION_PATHS := {
  kisisel_beceriler: "~/.claude/skills/skill-name/",
  proje_becerileri: ".claude/skills/skill-name/",
  not: "Degisiklikler sonraki Claude Code oturumu baslatildiginda yururluge girer"
} [ground:witnessed:installation-usage] [conf:0.92] [state:confirmed]

---

## Surekli Iyilestirme (Continuous Improvement)

<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Ongoing improvement process) -->

[assert|neutral] Dagitim sonrasi izleme ve iyilestirme [ground:witnessed:improvement-process] [conf:0.88] [state:confirmed]

- Gercek kullanimda beceri performansini gozlemle
- Claude'un zorlandigi veya ustun oldugu yerleri not et
- Talimat acikligi sorunlarini belirle
- Geri bildirime dayali guncelle
- Basarilardan kalip kutuphanesi olustur
- Surekli yinele

[direct|emphatic] Unutmayin: Beceri olusturma yinelemeli bir surecdir. Baslangic tasarimlari kullanim ve iyilestirme ile gelistirilir. [ground:witnessed:iterative-process] [conf:0.90] [state:confirmed]

---

[commit|confident] <promise>QUICK_REFERENCE_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
