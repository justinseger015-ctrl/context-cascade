# Ajanlar icin MCP Entegrasyon Kaliplari (MCP Integration Patterns for Agents)

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

<!-- S1 GENEL_BAKIS (Overview) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Genel Bakis (Overview)

<!-- [[MOR:root:E-N-T]] Entegrasyon = root morpheme for integration-connection -->
<!-- [[COM:MCP+Entegrasyon+Kaliplari]] German compound: MCPIntegrationsmuster -->
[assert|neutral] MCP_GENEL_BAKIS := {
  tanim: "Model Context Protocol (MCP), ajanlarin koordine olmasini, hafiza paylasmalarini ve harici araclara erismelerini saglar",
  ana_sunucular: ["Claude Flow MCP", "Memory MCP", "Connascence Analyzer", "Flow-Nexus (istege bagli)"]
} [ground:witnessed:overview] [conf:0.95] [state:confirmed]

---

<!-- S2 CLAUDE_FLOW_MCP (Claude Flow MCP) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Claude Flow MCP Entegrasyonu (Claude Flow MCP Integration)

### Kalip 1: Swarm Baslatma (Swarm Initialization)

[assert|neutral] SWARM_BASLATMA := {
  kullanim_durumu: "Coklu ajan koordinasyon topolojisi baslat",
  topolojiler: {
    hiyerarsik: "Koordinator -> Uzmanlar (is yukunu esit dagit)",
    orgu: "Esler arasi koordinasyon (dinamik olarak ayarla)",
    yildiz: "Merkezi koordinator (her ajanin benzersiz rolu var)"
  },
  ne_zaman_kullanilir: [
    "Coklu ajan is akislari (3+ ajan)",
    "Karmasik koordinasyon (bagimlíliklar, paralel yurutme)",
    "Hata kurtarma gerektiginde (geri alma, yeniden dene)"
  ],
  arac: "mcp__claude-flow__swarm_init",
  ornek_cagri: "swarm_init({ topology: 'hierarchical', maxAgents: 10, strategy: 'balanced' })"
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

### Kalip 2: Ajan Olusturma (Agent Spawning)

[assert|neutral] AJAN_OLUSTURMA := {
  kullanim_durumu: "Alt-gorevler icin uzman ajanlar olustur",
  ne_zaman_kullanilir: [
    "Karmasik alt-gorevleri devretme",
    "Paralel yurutme (birden fazla bagimsiz gorev)",
    "Uzman uzmanligi gerektiginde"
  ],
  arac: "mcp__claude-flow__agent_spawn",
  ornek_cagri: "agent_spawn({ type: 'backend-developer', name: 'api-builder', capabilities: ['nodejs', 'express', 'jwt-auth'] })"
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

### Kalip 3: Gorev Orkestrasyonu (Task Orchestration)

[assert|neutral] GOREV_ORKESTRASYONU := {
  kullanim_durumu: "Otomatik ajan secimi ile ust duzey is akisi orkestrasyonu",
  stratejiler: {
    uyarlanabilir: "Is yukune gore paralelligi ayarla",
    sirasal: "Sirada calis (veritabani migrasyonlari icin)",
    paralel: "Esanli calistir (test paketleri icin)"
  },
  ne_zaman_kullanilir: [
    "Karmasik is akislari (5+ adim)",
    "Otomatik ajan secimi tercih edildiginde",
    "Claude Flow koordinasyonu yonetmeli"
  ],
  arac: "mcp__claude-flow__task_orchestrate",
  ornek_cagri: "task_orchestrate({ task: 'E-ticaret uygulamasini uretim ortamina dagit', strategy: 'adaptive', priority: 'high', maxAgents: 8 })"
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

### Kalip 4: Hafiza Depolama ve Alma (Memory Storage & Retrieval)

[assert|neutral] HAFIZA_DEPOLAMA := {
  kullanim_durumu: "Ajanlar arasinda veri paylasimi, is akisi durumu kaliciligi",
  ad_alani_konvansiyonu: "{ajan-rolu}/{proje-id}/{veri-turu}",
  ornekler: [
    "marketing/campaign-2024-q4/strategy",
    "devops/deployment-prod-v2.5/state",
    "backend-dev/api-v3/schema-design"
  ],
  ttl_rehberleri: {
    kisa_vadeli: "24 saat - Gunluk metrikler, gecici durum",
    orta_vadeli: "7 gun - Kampanya verileri, ozellik spesifikasyonlari",
    uzun_vadeli: "30+ gun - Tarihi karsilastirmalar, sablonlar"
  },
  ne_zaman_kullanilir: [
    "Ajanlar arasi veri paylasimi (API kontratlari, ozellik spesifikasyonlari)",
    "Is akisi durum kaliciligi (dagitim durumu, kaynak ID'leri)",
    "Tarihi veri depolama (karsilastirmalar, sablonlar)"
  ],
  araclar: ["mcp__claude-flow__memory_store", "mcp__claude-flow__memory_retrieve"]
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

### Kalip 5: Ajan Durumu Izleme (Agent Status Monitoring)

[assert|neutral] DURUM_IZLEME := {
  kullanim_durumu: "Orkestrasyon sirasinda olusturulan ajanlarin sagligini izle",
  ne_zaman_kullanilir: [
    "Koordinator ajanlar uzmanları izlerken",
    "Uzun sureli is akislarinda saglik kontrolleri",
    "Hata tespiti ve kurtarma"
  ],
  araclar: ["mcp__claude-flow__swarm_status", "mcp__claude-flow__agent_list", "mcp__claude-flow__agent_metrics"],
  ornek_cikti: {
    swarm_id: "swarm-abc123",
    topoloji: "hierarchical",
    ajanlar: [
      { id: "agent-1", type: "backend-dev", status: "running", progress: 0.65 },
      { id: "agent-2", type: "frontend-dev", status: "completed", progress: 1.0 },
      { id: "agent-3", type: "database-specialist", status: "failed", error: "Connection timeout" }
    ],
    saglik: "degraded"
  }
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

---

<!-- S3 MEMORY_MCP (Memory MCP) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Memory MCP Entegrasyonu (Memory MCP Integration)

### Kalip 6: Kalici Oturumlar Arasi Depolama (Persistent Cross-Session Storage)

[assert|neutral] KALICI_DEPOLAMA := {
  kullanim_durumu: "Oturumlar arasinda kalici veri depola, semantik benzerlikle aranabilir",
  etiketleme_protokolu: {
    key: "{ad-alani}/{spesifik-id}",
    namespace: "agents/{ajan-kategorisi}",
    layer: "short-term | mid-term | long-term",
    category: "{veri-kategorisi}",
    project: "{proje-adi}",
    agent: "{ajan-adi}",
    timestamp: "ISO zaman damgasi",
    intent: "{amac}"
  },
  ne_zaman_kullanilir: [
    "Uzun vadeli bilgi depolama (personalar, sablonlar, karsilastirmalar)",
    "Oturumlar arasi baglam (onceki oturumlardan al)",
    "Semantik arama (benzer gecmis calismalari bul)"
  ],
  araclar: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

### Kalip 7: Mod-Farkindali Baglam Adaptasyonu (Mode-Aware Context Adaptation)

[assert|neutral] MOD_ADAPTASYONU := {
  kullanim_durumu: "Memory MCP etkilesim moduna gore tutma suresini otomatik ayarlar",
  modlar: {
    yurutme: {
      kalilar: ["deployed", "completed", "executed", "ran", "tested"],
      katman: "short-term (24 saat)"
    },
    planlama: {
      kalilar: ["strategy", "plan", "roadmap", "approach", "proposal"],
      katman: "mid-term (7 gun)"
    },
    beyin_firtinasi: {
      kalilar: ["ideas", "possibilities", "what if", "brainstorm", "explore"],
      katman: "short-term (24 saat)"
    }
  },
  ne_zaman_kullanilir: [
    "Memory MCP tutma islemini otomatik yonetsin",
    "Ajanlar arasinda tutarli tutma politikalari icin",
    "Mod icerikten acikca anlasildiginda"
  ],
  toplam_kalip_sayisi: 29
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

---

<!-- S4 CONNASCENCE_ANALYZER (Connascence Analyzer) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Connascence Analyzer Entegrasyonu (Kod Kalitesi Ajanlari) (Connascence Analyzer Integration - Code Quality Agents)

### Kalip 8: Kod Kalitesi Analizi (Code Quality Analysis)

[assert|neutral] KOD_KALITESI_ANALIZI := {
  kullanim_durumu: "Kod ihlallerini, baglanti sorunlarini, NASA uyumluligunu tespit et",
  tespit_yetenekleri: [
    "God Objects (>15 metod)",
    "Parameter Bombs (>6 param, NASA limiti)",
    "Cyclomatic Complexity (>10)",
    "Deep Nesting (>4 seviye, NASA limiti)",
    "Long Functions (>50 satir)",
    "Magic Literals (hardcoded degerler)",
    "Security violations (SQL injection, XSS)"
  ],
  ne_zaman_kullanilir: [
    "Sadece kod kalitesi ajanlari (coder, reviewer, tester, code-analyzer)",
    "Kod incelemesinden once (ihlalleri erken yakala)",
    "CI/CD boru hatti (kritik ihlallerde build'i basarisiz yap)"
  ],
  erisimi_olan_ajanlar: [
    "coder", "reviewer", "tester", "code-analyzer",
    "functionality-audit", "theater-detection-audit", "production-validator",
    "sparc-coder", "analyst", "backend-dev", "mobile-dev",
    "ml-developer", "base-template-generator", "code-review-swarm"
  ],
  araclar: ["mcp__connascence-analyzer__analyze_file", "mcp__connascence-analyzer__analyze_workspace"]
} [ground:witnessed:pattern] [conf:0.90] [state:confirmed]

---

<!-- S5 FLOW_NEXUS (Flow-Nexus MCP) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Flow-Nexus MCP Entegrasyonu (Istege Bagli Gelismis Ozellikler) (Flow-Nexus MCP Integration - Optional Advanced Features)

### Kalip 9: Bulut Sandbox Yurutme (Cloud Sandbox Execution)

[assert|neutral] SANDBOX_YURUTME := {
  kullanim_durumu: "Kodu izole bulut ortamlarinda (E2B sandboxlar) yurutme",
  sablonlar: ["nodejs", "python", "react", "nextjs"],
  ne_zaman_kullanilir: [
    "Test ajanlari (islevselligi izole dogrula)",
    "Guvenlik ajanlari (supheli kodu guvenle analiz et)",
    "Dagitim ajanlari (uretimden once test et)"
  ],
  araclar: ["mcp__flow-nexus__sandbox_create", "mcp__flow-nexus__sandbox_execute", "mcp__flow-nexus__sandbox_upload", "mcp__flow-nexus__sandbox_delete"]
} [ground:witnessed:pattern] [conf:0.88] [state:confirmed]

### Kalip 10: Gercek Zamanli Yurutme Izleme (Real-Time Execution Monitoring)

[assert|neutral] GERCEK_ZAMANLI_IZLEME := {
  kullanim_durumu: "Akis guncellemeleriyle ajan yurutmesini gercek zamanli izle",
  ne_zaman_kullanilir: [
    "Koordinator ajanlar uzmanları izlerken",
    "Uzun sureli is akislari (dagitimlar, veri isleme)",
    "Kullaniciya yonelik panolar (ilerlemeyi goster)"
  ],
  arac: "mcp__flow-nexus__execution_stream_subscribe"
} [ground:witnessed:pattern] [conf:0.88] [state:confirmed]

---

<!-- S6 EN_IYI_UYGULAMALAR (Best Practices) [[HON:teineigo]] [[EVD:-mis]] [[ASP:nesov.]] [[CLS:ge-abstract]] -->
## Entegrasyon En Iyi Uygulamalari (Integration Best Practices)

### 1. Ad Alani Konvansiyonlari (Namespace Conventions)

[assert|emphatic] AD_ALANI_KONVANSIYONLARI := {
  claude_flow_mcp: {
    format: "{ajan-rolu}/{proje-id}/{veri-turu}",
    ornekler: [
      "marketing/campaign-2024-q4/strategy",
      "devops/deployment-prod-v2.5/state",
      "backend-dev/api-v3/schema-design"
    ]
  },
  memory_mcp: {
    format: "agents/{ajan-kategorisi}/{spesifik-id}",
    ornekler: [
      "agents/marketing/personas/high-value-customers",
      "agents/devops/templates/docker-compose-nodejs",
      "agents/backend-dev/patterns/rest-api-auth"
    ]
  }
} [ground:witnessed:best-practices] [conf:0.92] [state:confirmed]

### 2. Hata Isleme (Error Handling)

[assert|emphatic] HATA_ISLEME := {
  strateji: "try-catch kullan, yedek plan sagla, gerekirse yukselt",
  is_akisi: [
    "Islem dene",
    "Basarisiz olursa, yedek plan mevcut mu kontrol et",
    "Mevcut ve yetki dahilindeyse dogrudan uygula",
    "Degilse koordinatore yukselt"
  ]
} [ground:witnessed:best-practices] [conf:0.92] [state:confirmed]

### 3. Performans Optimizasyonu (Performance Optimization)

[assert|emphatic] PERFORMANS_OPTIMIZASYONU := {
  batch_islemleri: {
    yanlis: "Sirasal olusturma (yavas)",
    dogru: "Paralel olusturma (Promise.all ile)"
  },
  hafiza_onbellekleme: {
    strateji: "Sik erisilen verileri onbellekle",
    uygulama: "Degisken bos mu kontrol et, bosza al, degilse mevcut degeri don"
  }
} [ground:witnessed:best-practices] [conf:0.92] [state:confirmed]

### 4. MCP Entegrasyonu Test Etme (Testing MCP Integration)

[assert|neutral] MCP_TESTI := {
  strateji: "Test icin MCP cagrilarini mock'la",
  mock_araclar: {
    agent_spawn: "{ id: 'agent-123', status: 'running' } dondur",
    memory_store: "{ success: true } dondur",
    memory_retrieve: "{ data: 'test-data' } dondur"
  },
  test_is_akisi: [
    "Mock'lanmis MCP ile ajan olustur",
    "Gorev yurutmeyi cagir",
    "MCP araclarin dogru parametrelerle cagrildigini dogrula"
  ]
} [ground:witnessed:best-practices] [conf:0.88] [state:confirmed]

---

<!-- S7 SONUC (Summary) [[HON:teineigo]] [[EVD:-dis]] [[ASP:sov.]] [[CLS:ge-abstract]] -->
## Sonuc (Summary)

<!-- [[MOR:root:S-N-C]] Sonuc = root morpheme for conclusion-result -->
[assert|confident] OZET := {
  temel_mcp_araclari: {
    claude_flow_mcp: "Swarm koordinasyonu, ajan olusturma, hafiza depolama",
    memory_mcp: "Kalici oturumlar arasi depolama, semantik arama",
    connascence_analyzer: "Kod kalitesi kontrolleri (sadece kod kalitesi ajanlari)",
    flow_nexus: "Bulut sandboxlar, gercek zamanli izleme (istege bagli)"
  },
  entegrasyon_kaliplari: [
    "Ad alani konvansiyonlari ({ajan-rolu}/{proje}/{veri-turu})",
    "Etiketleme protokolu (KIM/NE ZAMAN/PROJE/NEDEN Memory MCP icin)",
    "Hata isleme (try-catch, yedek, yukseltme)",
    "Performans optimizasyonu (batch islemler, onbellekleme)",
    "Test (mock MCP araclari)"
  ],
  ajan_spesifik_entegrasyon: {
    uzmanlar: "Minimal MCP kullanimi (sonuclar icin hafiza depolama)",
    koordinatorler: "Yogun MCP kullanimi (swarm init, ajan olusturma, durum izleme)",
    hibritler: "Orta MCP kullanimi (hafiza + ara sira delegasyon)"
  }
} [ground:witnessed:summary] [conf:0.95] [state:confirmed]

[assert|confident] SONUC := "Uretime hazir koordinasyon ve isbirligi icin saglam MCP entegrasyonlu ajanlar olusturmak icin bu kaliplari kullanin" [ground:witnessed:conclusion] [conf:0.95] [state:confirmed]

---

<promise>INTEGRATION_PATTERNS_VCL_VERIX_COMPLIANT</promise>
