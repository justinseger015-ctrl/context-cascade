[[HON:teineigo]] [[MOR:root:I-N-T]] [[COM:Entegrasyon+Kalip]] [[CLS:ge_reference]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/agent-creator/references/integration-patterns-VCL]]
# Entegrasyon Kaliplari (VCL Kreol)

## Baglanti Noktalari
[[define|neutral]] TOUCHPOINT := {prompt-architect:input,optimize; agent-creator:tanım; skill-forge:beceri; hook-ekosistemi:RBAC}. [ground:integration-patterns.md] [conf:0.82] [state:confirmed]

## Kalipler
1) [[CLS:ge_pattern]] “Task Router”: coordinator ajan → kayıtlı uzmanlara Task(). [[EVD:-DI<gozlem>]]  
2) “Audit Pair”: producer + auditor; auditor L1 log, producer L2 cikti. [[EVD:-dir<cikarim>]]  
3) “Hook Worker”: hook-creation agent with path_scopes hooks/**. [[EVD:-mis<rapor>]]  
4) “Registry First”: deploy once registry kayıt tamam. [[EVD:-DI<policy>]]

## Guardrails
[[direct|emphatic]] RULES := {AGENT_REGISTRY zorunlu, EVD/ASP>=1, L2 varsayilan, x- alanlari catisma onler}. [ground:integration-patterns.md] [conf:0.84] [state:confirmed]
