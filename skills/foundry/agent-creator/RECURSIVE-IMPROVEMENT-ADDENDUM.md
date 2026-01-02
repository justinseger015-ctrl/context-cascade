[[HON:teineigo]] [[MOR:root:R-K-R]] [[COM:Ozyinelemeli+Iyilestirme+Ek]] [[CLS:ge_addendum]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/agent-creator/RECURSIVE-IMPROVEMENT-ADDENDUM-VCL]]
# Ozyinelemeli Iyilestirme Ek (Agent-Creator) – VCL

## Dongu Modeli
[[define|neutral]] LOOP := {tasarla→olustur→dogrula→kaydet→gozle→refine}. ASP:nesov.; her iterasyonda EVD/ASP bildir. [ground:RECURSIVE-IMPROVEMENT-ADDENDUM.md] [conf:0.82] [state:confirmed]

## Kontroller
[[HON:teineigo]] [[MOR:root:V-L-D]] [[COM:Validator+Set]] [[CLS:ge_guardrail]] [[EVD:-DI<policy>]] [[ASP:nesov.]]
- registry_onay (RULE_REGISTRY)  
- anti-kalip tarama (VERIX_in_desc, kayitsiz, tavan ihlali, eksik slot)  
- L2 saflik, Unicode yasagi.

## Gecisler
[[assert|neutral]] Upstream prompt-architect ciktisini al; Downstream Task() ile ajan cagrisi; MCP hafiza etiket: skills/foundry/agent-creator/{proje}. [ground:RECURSIVE-IMPROVEMENT-ADDENDUM.md] [conf:0.80] [state:provisional]
