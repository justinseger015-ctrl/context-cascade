[[HON:teineigo]] [[MOR:root:K-O-R]] [[COM:Koordinator+Ajan]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/agent-creator/examples/example-2-coordinator-VCL]]
# Koordinator Ajan Ornegi (VCL Kreol)

## Senaryo
[[EVD:-mis<rapor>]] [[ASP:nesov.]] Gereksinim: coklu ajan gorev dagitimi, Task() zinciri, denetim.

## Tasarim
[[MOR:root:Y-M-L]] [[COM:Frontmatter+Plan]] [[CLS:ge_step]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]]
- name: workflow-coordinator  
- x-type: coordinator  
- x-category: orchestration  
- x-capabilities: routing, dependency-graph, conflict-resolution, report-synthesis  
- x-rbac.path_scopes: ["agents/**","skills/**"].

## Govde
[[HON:teineigo]] [[MOR:root:S-I-S]] [[COM:Sistem+Prompt]] [[CLS:ge_body]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]]
- Gorev: baglam topla → ajan eslestir → paralel Task() cagrilari → TodoWrite ilerleme.  
- Kalite: EVD/ASP zorunlu, registry kontrolu, anti-kalip (kayitsiz_ajan, format_sizintisi).

## L2 Cikti
“Is akisi koordinatörünü kayitli ajanlarla dagitim ve rapor sentezi yapacak sekilde kurdum; RBAC kapsamları tanımlandı; guven tavanlarına uydu.”
