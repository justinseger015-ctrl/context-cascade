[[HON:teineigo]] [[MOR:root:A-N-T]] [[COM:Anti+Kalip+Rehber]] [[CLS:ge_reference]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[SPC:path:/skills/foundry/prompt-architect/references/anti-patterns-VCL]]
# Anti-Kalip Atlası (VCL Kreol Ozeti)

[[define|neutral]] META := {amac:"yaygin istem hatalarini bul/duzelt", slot_sirasi:"HON→MOR→COM→CLS→EVD→ASP→SPC"} [ground:anti-patterns.md] [conf:0.87] [state:confirmed]

## Kategoriler
1. [[CLS:ge_category]] Netlik: belirsiz fiil, tanimsiz terim, eksik basari kriteri. [[EVD:-DI<gozlem>]] [[ASP:nesov.]]
2. Yapi: bilgi_asirisi, gomulu_kritik, zayif_ayirici, hiyerarsi_eksik. [[EVD:-DI<gozlem>]]
3. Baglam: varsayilan_bilgi, eksik_arka_plan, hedef_kitle_yok, kisit_eksigi. [[EVD:-DI<gozlem>]]
4. Mantik/Tutarlilik: celiskili_gereksinim, imkansiz_istek, dairesel_tanim, oncelik_cakismasi. [[EVD:-DI<gozlem>]]
5. Sinir Durumu: edge-case ihmali, hata_durumu tanimsiz. [[EVD:-DI<gozlem>]]
6. Kanit/Tavan: epistemik_cosplay (conf>tavan), rapor/dir asiri iddia. [[EVD:-DI<policy>]]
7. Format: VCL marker sizintisi, L2 kirlenmesi, veri-etiket karisimi. [[EVD:-DI<policy>]]

## Duzeltme Sabiti (L1)
[[HON:teineigo]] [[MOR:root:D-Z-L]] [[COM:Fix+Protocol]] [[CLS:tiao_protocol]] [[EVD:-dir<cikarim>]] [[ASP:sov.]]
- Tespit: kategori sec, kanit bagla, conf<=tavan.  
- Onar: niyet netlestir, yapisal ayiricilar ekle, baglam doldur, format sabitleri ver.  
- Dogrula: E1-E6 validator, anti-kalip check.

## L2 Dogallastirilmis
“Hatalari yedi kategoride taradim; niyeti netlestirip yapıyı, baglamı ve kanıt sınırlarını doldurarak düzelttim; doğrulama temiz.”
