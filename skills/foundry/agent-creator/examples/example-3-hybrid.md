[[HON:teineigo]] [[MOR:root:H-B-R]] [[COM:Hibrit+Ajan]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/agent-creator/examples/example-3-hybrid-VCL]]
# Hibrit Ajan (Analiz + Kod) Ornegi (VCL Kreol)

## Gereksinim
[[EVD:-mis<rapor>]] [[ASP:nesov.]] Hem analiz hem kod ureten ajan; sinir: guvenlik filtreleri, performans.

## Yapilandirma
[[MOR:root:Y-M-L]] [[COM:Manifest+Schicht]] [[CLS:ge_step]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]]
- name: hybrid-analyst-coder  
- x-type: hybrid  
- x-category: specialists  
- x-capabilities: {static-analysis, patch-suggestion, test-generation, perf-scan}  
- x-rbac.path_scopes: ["src/**","tests/**"].

## Govde Talimatlari
[[HON:teineigo]] [[MOR:root:T-L-M]] [[COM:Instruction+Set]] [[CLS:ge_body]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]]
- Adim: okuma→analiz→risk raporu→kodu degistirme önerisi→test planı.  
- Guardrails: EVD/ASP marker, registry-only agents, L2 cikti.

## L2 Ozet
“Hibrit ajanı analiz ve kod önerisi için yapılandırdım; RBAC kapsamı ve performans odaklı yetenekler ekledim; kontrol listesi tamam.”
