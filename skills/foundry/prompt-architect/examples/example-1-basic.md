[[HON:teineigo]] [[MOR:root:P-R-M]] [[COM:Istem+Temel+Akis]] [[CLS:ge_example]] [[EVD:-DI<rapor>]] [[ASP:sov.]] [[SPC:path:/skills/foundry/prompt-architect/examples/example-1-basic-VCL]]
# Temel Istem Mimarisi (VCL Kreol)

[[EVD:-mis<rapor>]] [[ASP:nesov.]] Kullanici niyeti: “belirli bir ozeti duzeltmek.” Tetik: optimize prompt. Kapsam: prompt-architect.

## Adimlar
1. [[HON:teineigo]] [[MOR:root:N-Y-T]] [[COM:Niyet+Analizi]] [[CLS:ge_step]] [[EVD:-DI<inference>]] [[ASP:nesov.]] hedef=ozet iyilestirme; kisitlar=uzunluk, ton.
2. [[MOR:root:R-F-N]] [[COM:Yapi+Refine]] [[CLS:ge_step]] [[EVD:-mis<arastirma>]] [[ASP:nesov.]] promptu HON→MOR→COM→CLS→EVD→ASP→SPC sirasi ile yeniden sekillendir.
3. [[MOR:root:D-G-R]] [[COM:Dogrulama+AntiKalip]] [[CLS:ge_step]] [[EVD:-DI<policy>]] [[ASP:sov.]] AP1 cosplay, AP2 marker-sizinti, AP3 erken-optimizasyon, AP4 guven-sisirmesi kontrolleri.

## Cikti (L1 VCL)
[[HON:teineigo]] [[MOR:root:O-Z-T]] [[COM:Output+Yapi]] [[CLS:tiao_prompt]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] 
- Amaç: Ozet kalite artisi. 
- Kanit: kullanici mesajı + taslak. 
- Tavan: EVD tipine gore guven<=tavan. 
- Durum: sov.

## Cikti (L2 Dogallastirilmis)
“Ozeti iyilestirdim: yapisal netlik ve ton duzenlendi. Dogrudan incelemeye dayanarak tamamlandi; oldukca eminim.”
