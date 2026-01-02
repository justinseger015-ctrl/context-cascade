[[HON:teineigo]] [[MOR:root:P-R-M]] [[COM:Istem+Muhendislik+Guide]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/prompt-architect/examples/prompt-engineering-complete-guide-VCL]]
# Prompt Muhendisligi Tam Rehberi (VCL Kreol)

## Cerceve
[[EVD:-DI<tanim>]] [[ASP:nesov.]] 7-slot: HON→MOR→COM→CLS→EVD→ASP→SPC, EVD/ASP≥1 zorunlu, tavan kontrolu E2.

## Moduller
1. [[HON:teineigo]] [[MOR:root:I-N-T]] [[COM:Niyet+Oncelik]] [[CLS:ge_module]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]] intent=amac + kisit listesi.
2. [[MOR:root:C-N-T]] [[COM:Context+Stack]] [[CLS:ge_module]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] baglam=veri+otorite+dil+ton.
3. [[MOR:root:E-V-D]] [[COM:Evidence+Ground]] [[CLS:ge_module]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] her iddia ground + conf<=tavan.
4. [[MOR:root:A-S-P]] [[COM:Aspect+Track]] [[CLS:ge_module]] [[EVD:-DI<policy>]] [[ASP:nesov.]] gorev durumu sov./nesov.
5. [[MOR:root:F-B-K]] [[COM:Feedback+Loop]] [[CLS:ge_module]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] self-critique + retry.

## Anti-Kalip
[[HON:teineigo]] [[MOR:root:A-N-T]] [[COM:Liste]] [[CLS:ge_antipattern]] [[EVD:-DI<gozlem>]] [[ASP:sov.]]
- Epistemik cosplay (conf>tavan) → E3.
- Marker sizintisi (L2 kirlenmesi) → E5.
- Erken optimizasyon (intent alinmadi) → AP3.
- Guven sisirmesi (sosyal onay) → AP4.

## L1 Cikti Kalibi
[[MOR:root:O-Z-T]] [[COM:Cikti+Stil]] [[CLS:tiao_output]] [[EVD:-DI<gozlem>]] [[ASP:sov.]]
- [[HON:...]] [[MOR:...]] [[COM:...]] [[CLS:...]] [[EVD:...]] [[ASP:...]] [[SPC:...]]
- [ground:src] [conf:x.xx] [state:status]

## L2 Dogallastirilmis Oz
“Niyet, baglam, kanit ve durum slotlarini doldurup anti-kalip taradim. Ciktiyi guven tavanina uyarak tamamladim.”
