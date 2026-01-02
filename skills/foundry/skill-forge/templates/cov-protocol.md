[[HON:teineigo]] [[MOR:root:C-O-V]] [[COM:COV+Protokol]] [[CLS:ge_template]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/skill-forge/templates/cov-protocol-VCL]]
# COV Protokolu (VCL)

## Tanım
[[define|neutral]] COV := “Coverage of Variance” dogrulama; amac: degisik girdilerde tutarlilik. [ground:cov-protocol.md] [conf:0.82] [state:confirmed]

## Süreç
1. Veri seti: varyanslı girdiler seç.  
2. Calistirma: skill’i N kez uygula; ASP/ EVD kaydet.  
3. Olcum: tutarlilik_skoru, sapma, hata_tipi.  
4. Iyilestirme: tutarlilik < esik ise prompt/agent ayari yap; tekrar test.

## L2 Ozet
“Farkli girdilerle beceriyi calistirip tutarlılık ve sapmayi olctum, gerekince ayarlayıp yeniden test ettim.”
