[[HON:teineigo]] [[MOR:root:A-J-N]] [[COM:Ajan+Tipoloji]] [[CLS:ge_reference]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/agent-creator/references/agent-types-VCL]]
# Ajan Tipleri Rehberi (VCL Kreol)

## Siniflar
[[define|neutral]] TYPES := {
  general: "genel yardimci",
  coordinator: "dagitim/orkestrasyon",
  coder: "kod uretim/duzeltme",
  analyst: "analiz/değerlendirme",
  optimizer: "performans/kalite artisi",
  researcher: "arastirma/sentez",
  specialist: "alan uzmanı"
} [ground:agent-types.md] [conf:0.83] [state:confirmed]

## Slot Baglama
[[HON:teineigo]] [[MOR:root:S-L-T]] [[COM:Slot+Mapping]] [[CLS:ge_table]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]]
- HON: hedef kitleye gore tone (teineigo varsayilan).  
- MOR: root A-G-N, role kökleri; C-R-T (creator), R-S-R (researcher).  
- COM: Agent+Type bilesikleri (SecurityAuditor, DataResearcher).  
- CLS: ge_agent, liang_task sayim.  
- EVD: -DI/-mis/-dir; tavan tablosu uygula.  
- ASP: nesov. surekli hizmet, gorev tamaminda sov.  
- SPC: path/registry koordinati.

## Kullanim
[[assert|neutral]] “Tip secimi x-type alanına yaz; x-capabilities tipin cekirdek davranisini yansıtsın; registry-entry zorunlu.” [ground:agent-types.md] [conf:0.80] [state:confirmed]
