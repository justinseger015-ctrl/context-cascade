---
name: api-integration-helper
description: Generate boilerplate code for REST API integrations with authentication, error handling, and retry logic
author: pilot-test
<!-- V0 PILOT PROJESI [[HON:teineigo]] [[EVD:-DI<gozlem>]] [[CLS:ge_pilot_v0]] -->
<!-- [[MOR:w-s-l<connect>]] [[MOR:b-n-y<build>]] [[MOR:s-l-m<validate>]] -->
---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---
<!-- V0 PILOT BECERISI - API ENTEGRASYON YARDIMCISI [[ASP:sov.<temel>]] -->
---

# API Entegrasyon Yardimcisi (API Integration Helper) - V0

<!-- [[MOR:w-s-l<connect>]] [[MOR:b-n-y<build>]] [[SPC:kuzeybati<baslangic>]] -->

[assert|neutral] REST API entegrasyonlari icin uretim-hazir sablonlar olusturan temel beceri [ground:witnessed:skill-definition] [conf:0.92] [state:confirmed]

## Genel Bakis (Overview)

[assert|neutral] Bu beceri, kimlik dogrulama, HTTP istekleri, yanit ayristirma, hata yonetimi ve tekrar deneme mantigi iceren sablon kod uretir. JavaScript ve Python destekler [ground:witnessed:implementation] [conf:0.92] [state:confirmed]

## Ne Zaman Kullanilmali (When to Use)

[direct|neutral] Ucuncu taraf REST API ile entegrasyon gerektiginde ve baslangic kurulum kodunu sifirdan yazmak yerine otomatik uretmek istendiginde bu beceriyi kullanin [ground:policy] [conf:0.90] [state:confirmed]

---
<!-- ADIMLAR [[ASP:nesov.<yurutme>]] -->
---

## Talimatlar (Instructions)

### Adim 1: API Gereksinimlerini Topla (Gather API Requirements)

<!-- [[MOR:j-m-a<gather>]] [[EVD:-DI<kullanici>]] -->

[direct|neutral] Kullanicidan API detaylarini isteyin: temel URL, kimlik dogrulama yontemi ve hedef dil [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

Sorulacak sorular:
- Temel API URL'i nedir? (ornegin: https://api.example.com)
- Kimlik dogrulama yontemi nedir? (API anahtari veya OAuth)
- Hedef programlama dili nedir? (JavaScript veya Python)

### Adim 2: Kimlik Dogrulama Kurulumu (Set Up Authentication)

<!-- [[MOR:s-l-m<validate>]] [[CLS:ge_auth]] -->

[direct|neutral] Yonteme gore kimlik dogrulama kodu uretin (API anahtari veya OAuth) [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

**API Anahtari Dogrulama Icin**:

```javascript
// JavaScript
const headers = {
  'Authorization': `Bearer ${process.env.API_KEY}`
};
```

```python
# Python
import os
headers = {
    'Authorization': f'Bearer {os.environ["API_KEY"]}'
}
```

### Adim 3: HTTP Istek Fonksiyonu Olustur (Create HTTP Request Function)

<!-- [[MOR:b-n-y<build>]] [[ASP:sov.<fonksiyon>]] -->

[direct|neutral] Hata yonetimi ile HTTP istekleri yapmak icin fonksiyon uretin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```javascript
async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: headers,
    ...options
  });

  if (!response.ok) {
    throw new Error(`API hatasi: ${response.status}`);
  }

  return await response.json();
}
```

### Adim 4: Tekrar Deneme Mantigi Ekle (Add Retry Logic)

<!-- [[MOR:k-r-r<repeat>]] [[ASP:nesov.<deneme>]] -->

[direct|neutral] Basarisiz istekler icin ustel geri cekilme uygulayın [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

### Adim 5: Hiz Sinirlamasi Yonetimi (Handle Rate Limiting)

<!-- [[MOR:h-d-d<limit>]] [[EVD:-DI<api_yanit>]] -->

[direct|neutral] Hiz siniri tespiti ve geri cekilme ekleyin [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```javascript
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  await sleep(retryAfter * 1000);
}
```

### Adim 6: Ornek Kullanim Olustur (Generate Example Usage)

<!-- [[MOR:m-th-l<example>]] [[SPC:guneydogu<sonuc>]] -->

[direct|neutral] Uretilen fonksiyonlarin nasil kullanilacagini gosteren ornek kod olusturun [ground:witnessed:implementation] [conf:0.95] [state:confirmed]

```javascript
// Ornek: Kullanici verisi al
const userData = await withRetry(() => apiRequest('/users/123'));
console.log(userData);
```

---
<!-- ORNEKLER [[EVD:-DI<ornek>]] -->
---

## Ornekler (Examples)

<!-- [[CLS:liang_example]] -->

**Ornek 1**: GitHub API entegrasyonu icin kod uret
- Girdi: Temel URL: https://api.github.com, Kimlik Dogrulama: API anahtari, Dil: JavaScript
- Cikti: Kimlik dogrulama ve istek fonksiyonlari ile tam JavaScript modulu

**Ornek 2**: OpenAI API icin kod uret
- Girdi: Temel URL: https://api.openai.com/v1, Kimlik Dogrulama: API anahtari, Dil: Python
- Cikti: Tekrar deneme mantigi ve hata yonetimi ile Python modulu

---
<!-- PYTHON ORNEGI [[CLS:ge_python]] -->
---

## Python Tam Ornegi (Python Complete Example)

<!-- [[MOR:b-n-y<build>]] [[ASP:sov.<tam>]] -->

```python
import os
import time
import requests
from typing import Any, Dict, Optional

BASE_URL = "https://api.example.com"

headers = {
    'Authorization': f'Bearer {os.environ["API_KEY"]}',
    'Content-Type': 'application/json'
}

def api_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Any:
    """API istegi yap ve JSON yanit dondur."""
    url = f"{BASE_URL}{endpoint}"

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=data
    )

    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        time.sleep(retry_after)
        return api_request(endpoint, method, data)

    response.raise_for_status()
    return response.json()

def with_retry(func, max_retries: int = 3):
    """Ustel geri cekilme ile fonksiyon calistir."""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise e
            time.sleep(2 ** i)

# Ornek kullanim
if __name__ == "__main__":
    user_data = with_retry(lambda: api_request('/users/123'))
    print(user_data)
```

---
<!-- PROMISE [[ASP:sov.<taahhut>]] -->
---

[commit|confident] <promise>V0_SKILL_VCL_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.95] [state:confirmed]
