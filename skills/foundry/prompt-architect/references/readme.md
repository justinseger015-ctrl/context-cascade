[[HON:teineigo]] [[MOR:root:P-R-M]] [[COM:Istem+Mimar+Referenz]] [[CLS:ge_reference]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/prompt-architect/references/readme-VCL]]
# Istem Mimarisi Rehberi (VCL Kreol Ozeti)

## Belge Kimligi
[[define|neutral]] README_VCL := {tur:"L1 teknik", surum:"1.0.0", kapsam:"prompt-architect cercevesi"} [ground:readme.md] [conf:0.86] [state:confirmed]

## Beceri Tanimi
[[HON:teineigo]] [[MOR:root:S-K-L]] [[COM:Prompt+Architekt+Rahmen]] [[CLS:ge_skill]] [[EVD:-DI<rapor>]] [[ASP:nesov.]]
- Amac: Yuksek-performansli istemler icin analiz + optimizasyon + anti-kalip tespiti.
- Bilesen: 6-boyut analiz, 7-adim iyilestirme, kanit-temelli teknikler, anti-kalip kutuphane.

## Kullanım Senaryolari
[[assert|neutral]] SENARYO := {tekrar_kullanilan_istemler, performans_artisi, kutuphane_kurulumu, egitim, yuksek_risk, debug}. Her biri oncelik=High/Mid/Critical. [ground:readme.md] [conf:0.82] [state:confirmed]

## Hizli Baslangic
[[HON:teineigo]] [[MOR:root:H-Z-L]] [[COM:Schnell+Start]] [[CLS:ge_workflow]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]]
1) Analiz: niyet, yapi, baglam, teknik, risk, format.  
2) Iyilestirme: 7-adim (niyet netlestir, yapilandir, baglam ekle, teknik uygula, riskleri kapat, metrik koy, dogrula).  
3) Dogrulama: anti-kalip tarama + guven tavan kontrolu.

## Teknikler
[[define|neutral]] TEKNIK := {self-consistency, chain-of-thought, role priming, format saplama, guardrails}. [[EVD:-mis<arastirma>]] [[ASP:nesov.]]

## Anti-Kaliplar
[[assert|emphatic]] ANTI := {epistemik_taklitcilik, eksik_baglam, format_sizintisi, erken_optimizasyon, guven_sisirmesi}. [[EVD:-DI<gozlem>]] [[ASP:sov.]]

## Cikti Stilleri
[[HON:teineigo]] [[MOR:root:O-Z-T]] [[COM:Output+Layer]] [[CLS:tiao_format]] [[EVD:-DI<policy>]] [[ASP:nesov.]]
- L1: VCL slotlari + VERIX.  
- L2: Dogallastirilmis Ingilizce, marker yok; varsayilan.

## Baglanti
[[assert|neutral]] Upstream: intent analizi; Downstream: agent-creator, skill-forge. [[SPC:upstream:/analysis]] [[SPC:downstream:/foundry]] [ground:readme.md] [conf:0.80] [state:confirmed]
