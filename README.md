# 🐍 Python-Benzeri Dil İçin Gerçek Zamanlı Sözdizimi Vurgulayıcı ve Denetleyici

Bu proje, **Python benzeri söz dizimine sahip özel bir dil** için geliştirilmiş **gerçek zamanlı sözdizimi analizörüdür**. Kullanıcının yazdığı kod, her tuş vuruşunda hem **leksik** hem de **sözdizimsel** olarak analiz edilir, hatalar satır ve sütun bilgisiyle birlikte anında kullanıcıya gösterilir.  

## 🎯 Amaç

- Eğitim ortamlarında öğrencilerin sözdizimi hatalarını anlık görerek öğrenmelerini kolaylaştırmak
- Özel dil tasarımı veya DSL (Domain Specific Language) geliştirme süreçlerinde temel analiz altyapısı sunmak

---

## 📦 Proje Bileşenleri

| Dosya                | Açıklama                                                                 |
|---------------------|--------------------------------------------------------------------------|
| `lexical_analyzer.py` | Gelişmiş leksik analizör (tokenize işlemi, girinti takibi, yorum ayrıştırma) |
| `parser.py`           | Rekürsif çıkışlı sözdizim ayrıştırıcısı (recursive descent parser)      |
| `gui.py`              | Tkinter tabanlı canlı editör ve vurgulayıcı arayüz                     |

---

## 🚀 Temel Özellikler

✅ **Gerçek Zamanlı Analiz**  
Her tuşa basıldığında kod yeniden analiz edilir ve hata varsa anında gösterilir.

✅ **Satır-Sütun Tabanlı Hata Mesajları**  
Syntax hatalarında kullanıcıya satır ve sütun bilgisiyle uyarı verilir.

✅ **Zengin Sözdizimi Vurgulama**  
| Öğe Türü       | Renk    |
|----------------|---------|
| Anahtar Kelimeler (`if`, `def`, `return` vb.) | Mavi |
| Sayılar         | Mor     |
| Operatörler     | Turuncu |
| Yorumlar        | Yeşil   |

✅ **Blok Yapısı İçin Girinti Tespiti**  
Girintiye dayalı yapı tanıma (INDENT / DEDENT tokenları).

✅ **Fonksiyonel Sözdizim Denetimi**  
`if/elif/else`, `for`, `while`, `def`, `return`, atama ve ifadeler desteklenir.

---

## 💻 Ekran Görüntüsü

![Ekran görüntüsü 2025-05-26 200854](https://github.com/user-attachments/assets/6acbca3f-8c10-45be-9244-381daaa5f2a4)


---

## 📄 Desteklenen Yapılar

**Kontrol Akışı:**
```python
if x > 0:
    return x
elif x == 0:
    return 0
else:
    return -x
```

**Döngüler:**
```python
while i < 10:
    i = i + 1

for i in range(5):
    print(i)
```

**Fonksiyonlar:**
```python
def kare(x):
    return x * x
```

**İfadeler:**
- Aritmetik: `+`, `-`, `*`, `/`
- Karşılaştırma: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Fonksiyon çağrısı: `f(x, y)`
- Parantezli ifadeler: `(a + b) * c`

---

## 🔧 Kurulum ve Çalıştırma

1. Python 3 kurulu olduğundan emin olun.
2. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici-adi/proje-adi.git
cd proje-adi
```
3. Uygulamayı başlatın:
```bash
python gui.py
```

---

## 📚 Teknik Mimarinin Özeti

### 🧠 `lexical_analyzer.py`

- Token türleri: `KEYWORD`, `ID`, `NUMBER`, `OP`, `ASSIGN`, `COMMENT`, `INDENT`, `DEDENT`, `EOF`...
- Girinti (indentation) analiz edilerek blok yapıları tespit edilir.
- Yorumlar `#` ile tanınır, diğer analizler etkilenmeden ayrıştırılır.

### 🧩 `parser.py`

- Recursive descent yaklaşımı kullanır.
- Her yapı için ayrı metodlar: `if_statement`, `while_statement`, `function_def`, `expression`...
- Hatalar `ParseError` ile detaylı verilir (örnek: `Satır 3, sütun 5: Beklenen ')'`)

### 🖼️ `gui.py`

- `tk.Text` aracı ile kod yazım alanı
- Token'lara göre renkli vurgulama (`text.tag_add`)
- `status` etiketi ile anlık hata bilgisi
- Tüm analiz işlemi `on_key_release` fonksiyonu ile tetiklenir

---

## 📽️ Demo

🎬 [Demo Videosunu İzle](https://www.youtube.com/watch?v=4dztHVLFQJ8)

---

## 📘 Detaylı Makale

📄 [Teknik Makaleye Git](https://example.com/makale)

---
