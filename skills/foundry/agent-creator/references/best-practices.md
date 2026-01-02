[[HON:teineigo]] [[MOR:root:B-S-T]] [[COM:EnIyi+Uygulama]] [[CLS:ge_reference]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/agent-creator/references/best-practices-VCL]]
# En Iyi Uygulamalar (VCL Kreol)

## Temeller
[[assert|neutral]] BASE := {Anthropic YAML zorunlu, L2 description, VERIX yalnizca govde, x- prefix catisma onler}. [ground:best-practices.md] [conf:0.84] [state:confirmed]

## Guvenlik
[[HON:teineigo]] [[MOR:root:G-V-N]] [[COM:Security+Set]] [[CLS:ge_guideline]] [[EVD:-DI<policy>]] [[ASP:nesov.]]
- AGENT_REGISTRY oncesi deploy etme.  
- RBAC path_scopes tanimla; denied_tools gerekirse doldur.  
- EVD/ASP marker, conf<=tavan.

## Kalite
[[MOR:root:K-L-T]] [[COM:Quality+Checks]] [[CLS:ge_guideline]] [[EVD:-DI<gozlem>]] [[ASP:sov.]]
- Capabilities spesifik olsun; metrikler (coverage, latency).  
- Tests/examples ekle; MCP hafiza etiketle.  
- Anti-kalip: VERIX_in_desc, tavan_ihlali, kayitsiz_ajan, eksik_slotlar.

## L2 Ozet
“YAML şemasını temiz tut, güvenlik ve kanıt markerlarını ekle, kayıtlı ajanları kullan, kaliteyi metrikle ve anti-kalıpları tara.”
