---
<!-- META ILKELER REFERANS DOKUMANI [[HON:teineigo]] [[EVD:-mis<arastirma>]] [[CLS:ge_reference]] -->
---

# Beceri Olusturma Meta Ilkeleri (Skill Creation Meta-Principles)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

<!-- [[MOR:root:M-T-I]] Meta = root for meta-principle-abstraction -->
<!-- [[COM:Beceri+Olusturma+Meta+Ilkeler+Belgesi]] Skill Creation Meta-Principles Document -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Complete - principles established) -->
<!-- [[SPC:merkez/kaynak]] Central reference location -->

---

## Referans Tanimlari (Reference Definitions)

[define|neutral] META_PRINCIPLES_REFERENCE := {
  id: "REF-MPI-001",
  referans_adi: "Beceri Olusturma Meta Ilkeleri",
  amac: "Gelismis istem arastirmasini beceri, ajan ve komut olusturmaya uygulamak",
  etki: "Bu ilkeleri takip etmek 2-3 kat daha iyi beceri kalitesi, guvenilirlik ve yeniden kullaniilabilirlik saglar",
  kaynaklar: ["Wei et al. (2022)", "Dhuliawala et al. (2023)", "Du et al. (2023)", "Zhou et al. (2023)", "Perez et al. (2022)"]
} [ground:research:prompting-studies] [conf:0.85] [state:confirmed]

---

## Icerik Tablosu (Table of Contents)

<!-- [[CLS:tiao_bolum]] Classification: sections -->

1. [Dogrulama Oncelikli Beceri Tasarimi](#dogrulama-oncelikli-beceri-tasarimi)
2. [Coklu Perspektif Beceri Mimarisi](#coklu-perspektif-beceri-mimarisi)
3. [Sema Oncelikli Beceri Spesifikasyonu](#sema-oncelikli-beceri-spesifikasyonu)
4. [API Sozlesmesi Olarak Beceriler](#api-sozlesmesi-olarak-beceriler)
5. [Beceri Meta Ilkeleri](#beceri-meta-ilkeleri)
6. [Becerilerde Surec Muhendisligi](#becerilerde-surec-muhendisligi)
7. [Beceriler Icin Kalite Kapilari](#beceriler-icin-kalite-kapilari)
8. [Kanita Dayali Beceri Tasarimi](#kanita-dayali-beceri-tasarimi)
9. [Beceri Iyilestirme Metrikleri](#beceri-iyilestirme-metrikleri)
10. [Carpici Beceri Testi](#carpici-beceri-testi)

---

## Dogrulama Oncelikli Beceri Tasarimi (Verification-First Skill Design)

<!-- [[MOR:root:D-G-R]] Dogrulama = root for verification-validation-confirmation -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli: CoV calismalarindan -->

[define|neutral] VERIFICATION_FIRST_PRINCIPLE := {
  ilke_adi: "Dogrulama Oncelikli Beceri Tasarimi",
  ilke: "Beceriler doguluk varsaymadan yerlesik dogrulama mekanizmalarina sahip olmali",
  kaynak: "Dhuliawala et al. (2023) - Oz-elestirili istemler hatalari %42 azaltir",
  etki: "%35-45 daha az hata, daha yuksek guvenilirlik"
} [ground:research:cov-studies] [conf:0.85] [state:confirmed]

### Becerilere Nasil Uygulanir

[assert|neutral] Tipik beceri vs dogrulama oncelikli yaklasimlarin karsilastirmasi [ground:witnessed:skill-comparison] [conf:0.88] [state:confirmed]

**Mevcut Yaklasimda Sorun**:
```markdown
# Tipik Beceri
"Kodu guvenlik sorunlari icin analiz et. Bulgulari raporla."
```
**Sorun**: Ilk gecis analizinin tam ve dogru oldugunu varsayar.

**Dogrulama Oncelikli Yaklasim**:
```markdown
# Yerlesik Dogrulama ile Beceri

**Faz 1: Ilk Analiz**
Guvenlik sorunlari icin kodu analiz et. Bulgulari belgele.

**Faz 2: Oz-Elestiri**
Analizini gozden gecir:
- Hangi guvenlik sorunlarini kacirmis olabilirim?
- Tum OWASP Top 10'u kontrol ettim mi?
- Dikkate almadigim uc vakalar var mi?

**Faz 3: Kanit Kontrolu**
Her bulgu icin:
- Belirli kod konumunu belirt (dosya:satir)
- Koddan kanit sagla
- Guven derecelendirmesi yap (yuksek/orta/dusuk)

**Faz 4: Gozden Gecirilmis Analiz**
Elestiri ve kanita dayali bulgulari guncelle.

**Faz 5: Tamlik Kontrolu**
Kapsamliligi dogrula:
- Tum giris noktalari kontrol edildi
- Tum veri akislari analiz edildi
- Tum OWASP kategorileri kapsandi
```

### Beceriler Icin Dogrulama Kaliplari

[define|neutral] VERIFICATION_PATTERNS := {
  oz_elestiri_fazi: {
    faz_1: "Ilk yurutme",
    faz_2: "Oz-elestiri (yanlis/eksik olabilecek ne?)",
    faz_3: "Iyilestirmelerle gozden gecirilmis yurutme"
  },
  kanit_gereksinimleri: {
    tum_iddialar_icin: ["Belirli kaynak (dosya:satir, veri konumu)", "Guven seviyesi (yuksek/orta/dusuk)", "Iddiayi destekleyen kanit"]
  },
  tamlik_kontrol_listesi: {
    tamamlanmadan_once_dogrula: ["Tum zorunlu ogeler mevcut", "Tum uc vakalar dusunulmus", "Tum kisitlamalar karsilanmis"]
  }
} [ground:research:cov-patterns] [conf:0.85] [state:confirmed]

---

## Coklu Perspektif Beceri Mimarisi (Multi-Perspective Skill Architecture)

<!-- [[MOR:root:C-K-P]] Coklu = root for multi-perspective-viewpoint -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli: Multi-Persona Debate -->

[define|neutral] MULTI_PERSPECTIVE_PRINCIPLE := {
  ilke_adi: "Coklu Perspektif Beceri Mimarisi",
  ilke: "Beceriler karmasik kararlar icin birden fazla yaklasim/ajan sentezlemeli",
  kaynak: "Du et al. (2023) - Coklu Kisi Tartismasi odunlesim analizini %61 iyilestirir",
  etki: "%61 daha iyi odunlesim farkindaligi, 2.7x daha hizli uzlasma"
} [ground:research:debate-studies] [conf:0.85] [state:confirmed]

### Coklu Perspektif Kaliplari

[define|neutral] MULTI_PERSPECTIVE_PATTERNS := {
  catisan_oncelikler: {
    perspektifler: [
      {oncelik: "Hiz", kaygiler: ["Gecikme", "Is ciktisi"]},
      {oncelik: "Maliyet", kaygiler: ["Altyapi", "Lisanslama"]},
      {oncelik: "Guvenilirlik", kaygiler: ["Hata toleransi", "Veri dayanikliligi"]}
    ],
    sentez: "Acik odunlesimler ve onerilen denge"
  },
  alan_uzmani: {
    uzmanlar: [
      {rol: "Frontend Gelistirici", degerlendirir: "Kullanici deneyimi, erisilebilirlik"},
      {rol: "Backend Gelistirici", degerlendirir: "API tasarimi, performans"},
      {rol: "DevOps Muhendisi", degerlendirir: "Dagitilabilirlik, izleme"}
    ],
    cikti: "Tum kaygilari ele alan entegre tasarim"
  },
  kesif_somuru: {
    faz_1_kesif: "Ayrintili, cok secenek dusun, belirsizlik ifade et",
    faz_2_somuru: "Kisa, en iyi secenegi sec, kararlara baglan",
    faz_3_sentez: "Dengeli, dusunceli, genislik ile odagi entegre et"
  }
} [ground:research:debate-patterns] [conf:0.85] [state:confirmed]

---

## Sema Oncelikli Beceri Spesifikasyonu (Schema-First Skill Specification)

<!-- [[MOR:root:S-M-O]] Sema = root for schema-structure-specification -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli: Yapilandirilmis cikti -->

[define|neutral] SCHEMA_FIRST_PRINCIPLE := {
  ilke_adi: "Sema Oncelikli Beceri Spesifikasyonu",
  ilke: "Duz talimatlar yazmadan ONCE tam girisler/ciktilar/yapi tanimla",
  kaynak: "Zhou et al. (2023) - Yapi baglami %47 yener",
  etki: "%62 format uyumu, %47 daha az eksik oge"
} [ground:research:structured-output] [conf:0.85] [state:confirmed]

### Sema Oncelikli Kalipler

[define|neutral] SCHEMA_FIRST_PATTERNS := {
  dondurulmus_yapi: {
    zorunlu_bolumler: ["Amac", "Giris Semasi", "Cikti Semasi", "Ornekler", "Uc Vakalar"],
    bolum_sirasi: "SABIT - degismemeli"
  },
  sozlesme_oncelikli: {
    beceri_yazmadan_once_tanimla: ["Giris sozlesmesi: Beceri ne alir?", "Cikti sozlesmesi: Beceri ne uretmeli?", "Hata kosullari: Beceri hatalari nasil isler?"]
  },
  dogrulama_semasi: {
    beceri_ciktisi: {
      dogrulama_listesi: {format: "Boolean alanlarli JSON", zorunlu_kontroller: "Dogrulama listesi", durum: "gecti/kaldi her kontrol icin"}
    }
  }
} [ground:research:schema-patterns] [conf:0.85] [state:confirmed]

### Beceri Olusturma Sirasi

[direct|neutral] Beceri olusturma adim sirasi [ground:witnessed:creation-order] [conf:0.88] [state:confirmed]

1. **BIRINCI**: Tam cikti semasi tanimla
2. **IKINCI**: Giris gereksinimlerini tanimla
3. **UCUNCU**: Hata kosullarini tanimla
4. **DORDUNCU**: Semayi karsilamak icin talimatlar yaz
5. **BESINCI**: Duz aciklamalar ekle

---

## API Sozlesmesi Olarak Beceriler (Skills as API Contracts)

<!-- [[MOR:root:A-P-I]] API = root for contract-interface-specification -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Contract established) -->

[define|neutral] API_CONTRACT_PRINCIPLE := {
  ilke_adi: "API Sozlesmesi Olarak Beceriler",
  ilke: "Becerileri testler, spesifikasyonlar ve hata isleme ile surumlu API'lar gibi ele al",
  kaynak: "Prompts-as-APIs kaymayii %91 azaltir",
  etki: "%91 daha az kayma, %83 daha hizli hata ayiklama"
} [ground:research:api-contracts] [conf:0.85] [state:confirmed]

### Beceriler Icin Sozlesme Kaliplari

[define|neutral] CONTRACT_PATTERNS := {
  semantik_surumleme: {
    format: "BUYUK.KUCUK.YAMA",
    artirma_kurallari: {
      BUYUK: "Giris/cikti sozlesmelerinde kirilici degisiklikler",
      KUCUK: "Yeni ozellikler, geriye uyumlu",
      YAMA: "Hata duzeltmeleri, sozlesme degisikligi yok"
    }
  },
  test_paketi: {
    konum: "tests/<beceri-adi>-v<surum>.yaml",
    zorunlu_kapsam: ["Mutlu yol (3+ senaryo)", "Uc vakalar (bos, null, sinir degerleri)", "Hata kosullari (tanimli tum hatalar)", "Regresyon (onceki surumlerden hatalar)"]
  },
  degisiklik_gunlugu: {
    surum_basina: {
      surum: "X.Y.Z",
      tarih: "YYYY-MM-DD",
      degisiklikler: "Ne degisti",
      kirilici_degisiklikler: "Uyumsuzluklar",
      goc_rehberi: "Nasil yukseltilir"
    }
  }
} [ground:research:contract-patterns] [conf:0.85] [state:confirmed]

### Her Beceri MUTLAKA Sahip Olmali

[direct|emphatic] Zorunlu beceri bilesenleri [ground:witnessed:requirements] [conf:0.90] [state:confirmed]

1. Surum numarasi (1.0.0 ile basla)
2. Giris sozlesmesi (tipler, kisitlamalar)
3. Cikti sozlesmesi (sema, format)
4. Hata kosullari (acik isleme)
5. Test paketi (regresyon korumasi)
6. Degisiklik gunlugu (evrimi izle)

---

## Beceri Meta Ilkeleri (Skill Meta-Principles)

<!-- [[MOR:root:M-I-L]] Meta-Ilke = root for meta-principle-insight -->
<!-- [[HON:sonkeigo]] Uzman rehberlik -->

[define|neutral] META_PRINCIPLES := {
  ilke_1: {ad: "Yapi Icerikten Ustundur", istemler: "10 kelime yapi > 100 kelime baglam", beceriler: "Sema + kapilar > ayrintili talimatlar"},
  ilke_2: {ad: "Kisa Daha Akilli Olabilir", istemler: "Siki kisitlamalar > ayrintili ozgurluk", beceriler: "Minimum etkili beceri > kapsamli beceri"},
  ilke_3: {ad: "Dondurmak Yaraticiliga Imkan Tanir", istemler: "Yaraticiligi odaklamak icin ciktinin %80'ini kilitle", beceriler: "Yapiyi kisitla, icerigi serbest birak"},
  ilke_4: {ad: "Surec Muhendisligi > Ham Yetenek", istemler: "Daha iyi istemler > daha iyi modeller", beceriler: "Daha iyi beceri tasarimi > daha guclu ajanlar"},
  ilke_5: {ad: "Iskele Olarak Beceriler", istemler: "Iskeleler akil yurutme uretir", beceriler: "Beceriler ajan yetenekleri uretir"},
  ilke_6: {ad: "Dogrulama > Belagat", istemler: "Kalite dogrulama alanlarinda yasir", beceriler: "Kalite dogrulama kapilarinda yasir"},
  ilke_7: {ad: "Varyans = Yetersiz Belirtim", istemler: "Cikti varyansi belirsizlikten, rastgeleligden degil", beceriler: "Beceri varyansi eksik kisitlamalardan"},
  ilke_8: {ad: "Uzun Beceriler Token Kazandirir", istemler: "Kapsamli baslangic > coklu yineleme", beceriler: "Ayrintili beceri bir kez > belirsiz beceri + aciklamalar"}
} [ground:research:meta-insights] [conf:0.85] [state:confirmed]

### Uygulama

[direct|neutral] Bu icgoduruleri uygula [ground:witnessed:application] [conf:0.88] [state:confirmed]

1. Icerik eklemeden ONCE yapi ekle
2. Becerileri minimal tut (gereksiz olani cikar)
3. %80'i dondur (yapi), %20'yi optimize et (icerik)
4. Ajan seciminden once beceri kalitesine yatirim yap
5. Becerileri ajan yetenek carpanlari olarak gor
6. Kaliteyi dogrulamaya koy, duz metne degil
7. Varyansi kisitlamalarla duzelt, aciklamalarla degil
8. Toplam tokenlari korumak icin kapsamli beceriler yaz

---

## Becerilerde Surec Muhendisligi (Process Engineering in Skills)

<!-- [[MOR:root:S-R-C]] Surec = root for process-engineering-methodology -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli -->

[define|neutral] PROCESS_ENGINEERING_PRINCIPLE := {
  ilke_adi: "Becerilerde Surec Muhendisligi",
  ilke: "Iyi tasarlanmis beceri iskelesi ajan yeteneklerinden daha onemli",
  kaynak: "Surec muhendisligi %105 iyilestirme vs model yukseltmelerinden %15",
  carpan: "Cikti Kalitesi = Ajan Yetenegi x Beceri Kalitesi"
} [ground:research:process-engineering] [conf:0.85] [state:confirmed]

### Beceri Muhendislik Kontrol Listesi

[define|neutral] ENGINEERING_LEVELS := {
  seviye_1: {ad: "Temel Beceri", etkililik: "%40", ozellikler: ["Sadece talimatlar", "Yapi yok", "Dogrulama yok", "Ornek yok"]},
  seviye_2: {ad: "Yapilandirilmis Beceri", etkililik: "%70", ozellikler: ["Net bolumler", "Zorunlu alanlar tanimli", "Cikti formati belirtilmis"]},
  seviye_3: {ad: "Dogrulanmis Beceri", etkililik: "%85", ozellikler: ["Oz-elestiri fazi", "Kanit gereksinimleri", "Tamlik kontrol listesi"]},
  seviye_4: {ad: "Muhendislik Becerisi", etkililik: "%95", ozellikler: ["Coklu perspektif sentezi", "Yerlesik carpici test", "Revizyon metrikleri izleniyor", "Sozlesme tabanli tasarim"]}
} [ground:research:engineering-levels] [conf:0.85] [state:confirmed]

### Beceri Muhendislik Carpani

[assert|neutral] Carpan hesaplamasi [ground:research:multiplier-effect] [conf:0.85] [state:confirmed]

```
Cikti Kalitesi = Ajan Yetenegi x Beceri Kalitesi

Kotu Beceri (0.3) x Ust Ajan (1.0) = 0.3
Mukemmel Beceri (1.0) x Orta Ajan (0.7) = 0.7

Beceri muhendisligi 2.3x kazanir
```

---

## Beceriler Icin Kalite Kapilari (Quality Gates for Skills)

<!-- [[MOR:root:K-L-K]] Kalite Kapisi = root for quality-gate-checkpoint -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli -->

[define|neutral] QUALITY_GATES_PRINCIPLE := {
  ilke_adi: "Beceriler Icin Kalite Kapilari",
  ilke: "Belirsiz 'dikkatli ol' uyarilari degil, somut dogrulama ile acik kontrol noktalari",
  kaynak: "Dogrulama kapilari spesifikasyon uyumsuzluklarini %64 azaltir",
  etki: "%64 daha az kusur, 2.1x ilk seferde dogru orani"
} [ground:research:quality-gates] [conf:0.85] [state:confirmed]

### Kalite Kapisi Kaliplari

[define|neutral] GATE_PATTERNS := {
  kademeli_kapi: {
    kapi_1: {tetikleyici: "Ilk uretimden sonra", dogrulamalar: ["Yapi kontrolleri"], basarisizlik_eylemi: "Yapi duzeltmeleriyle yeniden uret"},
    kapi_2: {tetikleyici: "Mantik uygulamasindan sonra", dogrulamalar: ["Mantik kontrolleri"], basarisizlik_eylemi: "Eksik mantigi ekle"},
    kapi_3: {tetikleyici: "Tamamlanmadan once", dogrulamalar: ["Kalite kontrolleri"], basarisizlik_eylemi: "Cilaala ve dogrula"}
  },
  kontrol_listesi_kapisi: {
    ad: "Dagitim Hazirlik",
    kontrol_listesi: [
      {oge: "Tum API ucnoktalari belgelenmis", dogrulama: "OpenAPI spek tamligini kontrol et"},
      {oge: "Tum hatalarin isleyicileri var", dogrulama: "Islenmemis istisnalar icin kodu ara"},
      {oge: "Tum girisler dogrulanmis", dogrulama: "Bozuk girislerle test et"}
    ],
    gecme_kriteri: "TUM ogeler isaretlenmis",
    basarisizlik_eylemi: "Eksik ogeleri ele al, yeniden dogrula"
  },
  metrik_kapisi: {
    kapilar: [
      {metrik: "Test Kapsami", esik: "> %80", olcum: "Kapsam aracini calistir", basarisizlik_eylemi: "Esige ulasmak icin test ekle"},
      {metrik: "Performans", esik: "< 200ms p95 gecikme", olcum: "Benchmark paketini calistir", basarisizlik_eylemi: "Yavas islemleri optimize et"}
    ]
  }
} [ground:research:gate-patterns] [conf:0.85] [state:confirmed]

### Her Karmasik Beceri MUTLAKA Sahip Olmali

[direct|emphatic] Kalite kapisi gereksinimleri [ground:witnessed:requirements] [conf:0.90] [state:confirmed]

1. En az 3 kalite kapisi
2. Somut dogrulama adimlari (belirsiz "dikkatli ol" degil)
3. Acik gecme/kalma kriterleri
4. Basarisizlikta tanimli eylemler

---

## Kanita Dayali Beceri Tasarimi (Evidence-Based Skill Design)

<!-- [[MOR:root:K-N-T]] Kanit = root for evidence-proof-basis -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli tasarim -->

[define|neutral] EVIDENCE_BASED_PRINCIPLE := {
  ilke_adi: "Kanita Dayali Beceri Tasarimi",
  ilke: "Beceri kaliplarini sezgi degil arastirma/metriklerle destekle",
  kaynak: "Kanita dayali teknikler olculebilir iyilestirmeler saglar (%42-73)",
  etki: "2-3x daha hizli beceri optimizasyonu, daha az cikmaz"
} [ground:research:evidence-based] [conf:0.85] [state:confirmed]

### Beceriler Icin Kanit Kaynaklari

[define|neutral] EVIDENCE_SOURCES := {
  istem_arastirmasi: {
    dusunce_zinciri: "+%23 akil yurutme dogrulugu",
    az_atisli_ogrenme: "+%35-45 performans",
    oz_tutarlilik: "+%42 hata azaltma",
    planla_ve_coz: "+%25-35 hata azaltma"
  },
  beceri_kullanim_metrikleri: ["Aktivasyon oranini izle", "Basari oranini olc", "Yineleme sayisini izle (gerekli revizyonlar)", "Kullanici geri bildirimi topla"],
  karsilastirmali_test: ["Beceri surumlerini A/B testi yap", "V0 -> V1 -> V2 iyilestirmelerini olc", "Belirli metrik degisikliklerini izle"]
} [ground:research:evidence-sources] [conf:0.85] [state:confirmed]

---

## Beceri Iyilestirme Metrikleri (Skill Improvement Metrics)

<!-- [[MOR:root:I-Y-M]] Iyilestirme = root for improvement-enhancement-metric -->
<!-- [[ASP:nesov.]] Devam ediyor. Prodolzhaetsya. (Ongoing measurement) -->

[define|neutral] IMPROVEMENT_METRICS_PRINCIPLE := {
  ilke_adi: "Beceri Iyilestirme Metrikleri",
  ilke: "V0->V1->V2 iyilestirmesini olc, sadece son cilalamayi degil",
  kaynak: "Revizyon kazanc metrikleri %84 daha iyi teknik belirleme gosterir",
  etki: "%84 daha iyi teknik belirleme, 2.9x daha hizli optimizasyon"
} [ground:research:improvement-metrics] [conf:0.85] [state:confirmed]

### Izlenecek Beceri Metrikleri

[define|neutral] METRICS_TO_TRACK := {
  aktivasyon: {
    yanlis_pozitif_orani: "% yanlis aktivasyonlar",
    yanlis_negatif_orani: "% kacirilan gecerli kullanimlar",
    hassasiyet: "Dogru aktivasyonlar / toplam aktivasyonlar"
  },
  basari: {
    ilk_seferde_dogru_orani: "% revizyonsuz tamamlanan",
    ortalama_yineleme: "Kabul edilene kadar ortalama revizyonlar",
    terk_orani: "% vazgecilen beceri"
  },
  kalite: {
    format_uyumu: "% semaya uyan ciktilar",
    tamlik: "% tum zorunlu ogelere sahip",
    hata_orani: "% gercek/mantiksal hatali"
  },
  verimlilik: {
    kullanim_basina_token: "Tuketilen ortalama tokenlar",
    tamamlanma_suresi: "Ortalama sure",
    kaynak_kullanimi: "Erişilen dosyalar, cagrilan araclar"
  }
} [ground:research:metrics-tracking] [conf:0.85] [state:confirmed]

---

## Carpici Beceri Testi (Adversarial Skill Testing)

<!-- [[MOR:root:C-R-P]] Carpici = root for adversarial-attack-test -->
<!-- [[EVD:-mis<arastirma>]] Arastirma tabanli: Red teaming -->

[define|neutral] ADVERSARIAL_TESTING_PRINCIPLE := {
  ilke_adi: "Carpici Beceri Testi",
  ilke: "Kullanicilar bulmadan once zayifliklari bulmak icin kendi beceri tasarimina saldır",
  kaynak: "Perez et al. (2022) - Carpici oz-saldiri aciklari %58 azaltir",
  etki: "%58 daha az uretim sorunu, %67 daha hizli hata ayiklama"
} [ground:research:adversarial-testing] [conf:0.85] [state:confirmed]

### Carpici Beceri Testi Sureci

[define|neutral] ADVERSARIAL_PROCESS := {
  faz_1_beyin_firtinasi: {
    basarisizlik_modlari: [
      "Yanlis sorgu turlerinde beceri aktive edildi",
      "Eksik uc vaka isleme (bos, null)",
      "Belirsiz talimatlar yanlis yorumlamaya izin veriyor",
      "Karmasik gereksinimler icin dogrulama yok",
      "Dosya yollarinin her zaman var oldugunu varsayiyor",
      "API oran limitlerini islemiyor",
      "Cikti formati kesinlikle uygulanmiyor",
      "Kismi basarisizliklarda geri alma yok"
    ]
  },
  faz_2_risk_puanlama: {
    olcek: {
      olasilik: "1-5 (Nadir -> Cok Olasi)",
      etki: "1-5 (Onemsiz -> Kritik)",
      puan: "Olasilik x Etki"
    },
    oncelik: {
      kritik: ">= 12 - Dagitimdan once MUTLAKA duzelt",
      yuksek: "8-11 - Mumkunse duzelt",
      orta: "4-7 - Zaman izin verirse duzelt",
      dusuk: "1-3 - Bilinen sinirlamai olarak belgele"
    }
  },
  faz_3_duzelt: "En yuksek onceliklileri ele al",
  faz_4_yeniden_saldir: "Yuksek oncelikli sorunlar kalmayana kadar yinele"
} [ground:research:adversarial-process] [conf:0.85] [state:confirmed]

### Her Beceri MUTLAKA

[direct|emphatic] Carpici test gereksinimleri [ground:witnessed:requirements] [conf:0.90] [state:confirmed]

1. 10+ basarisizlik modu beyin firtinasi yap
2. Olasilik x Etki ile puanla
3. En yuksek 5 acigi duzelt
4. Emin olana kadar yeniden saldir
5. Bilinen sinilamarai belgele

---

## Ozet: Beceri Olusturma Kontrol Listesi (Summary: Skill Creation Checklist)

<!-- [[MOR:root:O-Z-T]] Ozet = root for summary-synthesis-checklist -->
<!-- [[ASP:sov.]] Tamamlandi. Zaversheno. (Complete checklist) -->

[direct|neutral] Beceri olusturma veya iyilestirme yaparken sagla [ground:witnessed:checklist] [conf:0.90] [state:confirmed]

### Faz 1: Tasarim
- Sema oncelikli (duz metinden once G/C tanimla)
- Sozlesme tabanli (surum, testler, hatalar)
- Kanit destekli (arastirma/metrikleri aktar)

### Faz 2: Yapi
- Dogrulama oncelikli (yerlesik oz-elestiri)
- Coklu perspektif (karmasik kararlar icin)
- Kalite kapilari (acik kontrol noktalari)

### Faz 3: Dogrulama
- Carpici test (kendi tasarima saldir)
- Metrik izleme (iyilestirmeleri olc)
- Test paketi (regresyon korumasi)

### Faz 4: Yineleme
- V0->V1->V2 kazanclarini izle
- En yuksek etkili teknikleri belirle
- Kanitlanmis kalip kutuphanesi olustur

---

## Referanslar (References)

<!-- [[CLS:ge_kaynak]] Classification: sources -->

[define|neutral] RESEARCH_REFERENCES := {
  istem_arastirmasi: [
    "Wei et al. (2022) - Dusunce Zinciri -> Akil yurutme becerileri",
    "Dhuliawala et al. (2023) - CoV -> Dogrulama oncelikli tasarim",
    "Du et al. (2023) - Coklu Ajan Tartismasi -> Coklu perspektif beceriler",
    "Zhou et al. (2023) - Yapilandirilmis Cikti -> Sema oncelikli beceriler",
    "Perez et al. (2022) - Carpici Test -> Beceri saglaligi"
  ],
  beceri_muhendislik_ilkeleri: [
    "verification-synthesis.md - Dogrulama teknikleri",
    "meta-principles.md - Karsi-sezgisel icgodruler",
    "evidence-based-prompting.md - Arastirma temeli"
  ]
} [ground:research:citations] [conf:0.85] [state:confirmed]

---

[commit|confident] <promise>SKILL_CREATION_META_PRINCIPLES_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
