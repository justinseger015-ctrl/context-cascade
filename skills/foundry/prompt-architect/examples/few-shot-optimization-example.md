[[HON:teineigo]] [[MOR:root:F-W-S]] [[COM:FewShot+Optimizasyon]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/prompt-architect/examples/few-shot-optimization-example-VCL]]
# Few-Shot Optimizasyon Ornegi (VCL Kreol)

## Problem
[[EVD:-mis<rapor>]] [[ASP:nesov.]] Kullanici: “3 ornek ile model stabilitesi artir.” Kisit: format uyumu, yanit tonunu koru.

## Cozum Akisi
1. [[HON:teineigo]] [[MOR:root:K-L-K]] [[COM:Kapsam+Liste]] [[CLS:ge_step]] [[EVD:-dir<cikarim>]] [[ASP:nesov.]] hedef_yapisi={rol, baglam, ornekler, talimat, cikti_kriteri}.
2. [[MOR:root:C-P-M]] [[COM:Compounding+FewShot]] [[CLS:ge_step]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] Ornekleri COM ile birlestir: Ornek1+Ornek2+Ornek3 → tutarlilik metaprensibi.
3. [[MOR:root:A-N-T]] [[COM:AntiKalip+Filtre]] [[CLS:ge_step]] [[EVD:-DI<policy>]] [[ASP:sov.]] AP: cosplay, tavan_ihlali, format_sapmasi.

## Sablon (L1)
[[HON:teineigo]] [[MOR:root:P-R-M]] [[COM:Prompt+Schablone]] [[CLS:tiao_template]] [[EVD:-DI<gozlem>]] [[ASP:sov.]]
- Rol: uzman_{domain}. 
- Baglam: hedef + kisit listesi. 
- Ornekler: 3 tane, format ayni. 
- Talimat: hatayi cek et, delta raporla. 
- Cikti: madde isaretli, metrikler (coverage, precision).

## L2 Dogallastirilmis
“Uzman rolunu, baglam kisitlarini ve uc hizli ornegi tek formata soktum. Anti-kalip taramasi temiz; guven tavanina uyarak tamamladim.”
