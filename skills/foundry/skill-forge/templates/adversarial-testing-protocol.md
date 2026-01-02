[[HON:teineigo]] [[MOR:root:D-S-M]] [[COM:Dusmanca+Test+Protokol]] [[CLS:ge_template]] [[EVD:-DI<rapor>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/skill-forge/templates/adversarial-testing-protocol-VCL]]
# Dusmanca Test Protokolu (VCL)

## Hedef
[[define|neutral]] PURPOSE := “becerinin sinir durumlarda kirilmasini onlemek, COV saglamak.” [ground:adversarial-testing-protocol.md] [conf:0.83] [state:confirmed]

## Adimlar
1. Tehdit modeli: input manip, prompt injection, performans tuzaklari.  
2. Senaryolar: en az 5 edge-case; etiketle (CLS:ge_case).  
3. Calistir: Task() veya manuel; EVD/ASP kaydet.  
4. Degerlendir: metrikler (pass_rate, severity), conf<=tavan.  
5. Iyilestir: zayif noktaları optimize, yeniden test et.

## L2 Ozet
“Tehditleri belirledim, sinir senaryoları calistirdim, kanıt ve durumla raporladım, zayıf alanları onardım.”
