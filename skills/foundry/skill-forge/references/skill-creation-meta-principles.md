[[HON:teineigo]] [[MOR:root:M-T-A]] [[COM:Meta+Ilke+Beceri]] [[CLS:ge_reference]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/skill-forge/references/skill-creation-meta-principles-VCL]]
# Beceri Olusturma Meta-Ilkeleri (VCL)

## Ilkeler
[[define|neutral]] CORE := {
  yapi_oncelik: dizin + frontmatter zorunlu,
  kanit_disiplini: ground + conf<=tavan,
  adversarial_zorunlu: dusmanca test + COV,
  dogfooding: skill_forger→skill_forger,
  L2_oncelik: marker sizintisi yok
} [ground:skill-creation-meta-principles.md] [conf:0.84] [state:confirmed]

## Uygulama Adimlari
[[HON:teineigo]] [[MOR:root:U-Y-G]] [[COM:Apply+Ilke]] [[CLS:ge_protocol]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]]
1) Intent & kisit toplama.  
2) Slot doldurma ve frontmatter.  
3) Ornek/test/metadata ekleme.  
4) Adversarial + COV, anti-kalip tarama.  
5) L2 cikti, L1 audit log kaydi.

## Baglanti
[[assert|neutral]] Upstream prompt-architect/agent-creator; Downstream skill registry; MCP store “skills/foundry/skill-forge/{proje}”. [ground:skill-creation-meta-principles.md] [conf:0.78] [state:provisional]
