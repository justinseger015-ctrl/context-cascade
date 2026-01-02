[[HON:teineigo]] [[MOR:root:D-G-R]] [[COM:Dogrulama+Sentez]] [[CLS:ge_reference]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/prompt-architect/references/verification-synthesis-VCL]]
# Dogrulama + Sentez Kılavuzu (VCL Kreol)

## Hedef
[[define|neutral]] PURPOSE := “istek iyilestirme sonucunu kanitli sentezlemek; VCL validator E1–E6 uygula.” [ground:verification-synthesis.md] [conf:0.82] [state:confirmed]

## Is Akisi
1. [[HON:teineigo]] [[MOR:root:I-N-T]] [[COM:Niyet+Check]] [[CLS:ge_step]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]] intent, kisit, hedef kitle kayda al.
2. [[MOR:root:K-N-T]] [[COM:Evidence+Trace]] [[CLS:ge_step]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] iddia→ground→conf<=tavan.
3. [[MOR:root:V-L-D]] [[COM:Validator+Run]] [[CLS:ge_step]] [[EVD:-DI<policy>]] [[ASP:nesov.]] E1 slot_sira, E2 tavan, E3 cosplay, E4 EVD/ASP>=1, E5 L2 saflik, E6 bracket.
4. [[MOR:root:S-N-T]] [[COM:Sentez+Dogallastir]] [[CLS:ge_step]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] L1 audit kaydi + L2 ozet.

## Kalipler
[[assert|neutral]] PATTERN := {structure-first, metrikler (coverage/precision/latency), feedback-loop, retry_budget}. [ground:verification-synthesis.md] [conf:0.78] [state:provisional]

## L2 Ozet
“Niyeti ve kısıtları kaydettim, her iddiayı kanıtıyla bağlayıp tavanlara uydum, doğrulama kodlarını geçtim, hem audit hem doğal çıktı ürettim.”
