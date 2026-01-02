[[HON:teineigo]] [[MOR:root:A-J-N]] [[COM:Ajan+Destekli+Beceri]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/skill-forge/examples/example-2-agent-powered-skill-VCL]]
# Ajan Destekli Beceri Ornegi (VCL Kreol)

## Senaryo
[[EVD:-mis<rapor>]] [[ASP:nesov.]] Coklu ajanla kod inceleme becerisi; koordinasyon ve denetim gerekir.

## Tasarim
1. Frontmatter: name: multi-agent-code-review, allowed-tools: {Task, TodoWrite}, x-category: quality.  
2. Govde: gorev listesi (analiz→sentez→patch öneri→test planı), ajan cagrilari Task("code-reviewer",...), Task("security-auditor",...).  
3. Kalite: adversarial-test senaryosu, metrikler (coverage, bug-detection-rate), COV protokolu.  
4. Guardrails: registry-only agents, EVD/ASP marker, L2 cikti.

## L2 Ozet
“Kod inceleme becerisini iki kayıtlı ajanla orkestre ettim; kalite metrikleri ve adversarial test eklendi; durum tamamlandı.”
