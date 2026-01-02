[[HON:teineigo]] [[MOR:root:A-G-N]] [[COM:Temel+Ajan+Ornek]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/agent-creator/examples/example-1-basic-VCL]]
# Temel Ajan Tanimi (VCL Kreol)

## Girdi
[[EVD:-mis<rapor>]] [[ASP:nesov.]] Istek: “Kod inceleme yapacak ajan.” Kisit: Anthropic YAML, registry uyumu.

## Adimlar
1. HON→MOR→COM→CLS→EVD→ASP→SPC slot kontrolu.  
2. YAML frontmatter doldur: name, description(L2), tools, model, x-type, x-category, x-capabilities, x-version.  
3. Govde: rol, gorev listesi, kalite kurallari, guvenlik notlari.

## L1 Cikti Ozeti
[[HON:teineigo]] [[MOR:root:Y-M-L]] [[COM:YAML+Manifest]] [[CLS:tiao_agent]] [[EVD:-DI<gozlem>]] [[ASP:sov.]]
- name: code-reviewer  
- description: L2 temiz  
- x-capabilities: {static-analysis, test-suggestion, risk-flagging}  
- registry: REQUIRED (RULE_REGISTRY)

## L2 Dogallastirilmis
“Kod inceleme uzmanı ajanı Anthropic şemasıyla tanımladım; kayıt zorunluluğu ve kanıtlı görev listesi eklendi; tamamlandı.”
