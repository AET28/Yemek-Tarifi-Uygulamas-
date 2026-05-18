# Mutfak Defteri — Yemek Tarifi Platformu

Kullanıcıların lezzetli yemek tariflerini, malzemeleri, hazırlanış aşamalarını ve mutfak sırlarını merkezi olarak organize edip keşfedebildiği modern ve minimalist bir masaüstü tarif yönetim otomasyonudur. PyQt5 altyapısı üzerinde kurumsal ve editorial tasarım yönergeleri (Playfair Display & Inter font hiyerarşisi) ve Nesne Yönelimli Programlama (OOP) prensipleri kullanılarak, güvenli katmanlı mimari (Frontend/Backend) modeliyle geliştirilmiştir.

---

### 🚀 Teknolojiler

* **Python 3** - Temel programlama dili
* **PyQt5 (>=5.15.0)** - Masaüstü GUI (Grafik Kullanıcı Arayüzü) framework'ü
* **JSON** - Veri kalıcılığı ve yerel ilişkisel tarif veritabanı yönetimi
* **Typography Integration** - Playfair Display (Başlıklar için şık serif) ve Inter (Okunabilirlik için sans-serif) font entegrasyonu

---

### 📂 Proje Yapısı

```text
mutfak_defteri/
├── main.py                          # Uygulamanın ana giriş noktası ve başlatıcı
├── requirements.txt                 # Üçüncü parti kütüphane bağımlılıkları (PyQt5)
├── fix.py                           # Arayüz dosyalarındaki hatalı CSS letter-spacing dizilimlerini temizleyen betik
├── data/                            # JSON formatında yerel veritabanı dosyaları (Otomatik oluşturulur)
│   ├── auth.json                    # Sistem yetkilileri ve kimlik doğrulama verileri
│   └── [veri_dosyalari].json        # Yemek tarifleri, kategoriler ve malzeme listeleri
├── backend/
│   ├── __init__.py
│   ├── veri_yoneticisi.py           # Tarif iş mantığı, CRUD işlemleri ve arama-filtreleme motoru
│   ├── auth.py                      # Kullanıcı oturum yönetimi ve yetkilendirme modülü
│   └── seed.py                      # Veritabanı boşsa devreye giren gurme örnek tarif yükleyici
└── frontend/
    ├── __init__.py
    ├── ana_pencere.py               # Ana kontrol paneli, tarif listeleri, kartlar ve navigasyon
    ├── login.py                     # Şef / Kullanıcı giriş ekranı (QDialog)
    └── tema.py                      # Editorial renk paleti, tipografi ayarları ve UI stil şablonları (ANA_STIL)

🧠 Ana Yapı ve İş Mantığı Katmanları
🔐 Kimlik Doğrulama Yönetimi (backend/auth.py -> AuthYoneticisi)

    Özellikler: auth.json dosya yolu üzerinden şef ve kullanıcı hesaplarının yönetimi.

    Metodlar: kullanici_var_mi(), varsayilan_kullanici_olustur(), kullanici_dogrula(ad, sifre).

⚙️ Mutfak Veri Merkezi (backend/veri_yoneticisi.py -> VeriYoneticisi)

    Özellikler: data/ klasör referansı, tarif adları, hazırlık süreleri, porsiyon bilgileri ve malzeme veri kümeleri.

    Metodlar: seed_yukle() ve tarif yönetim fonksiyonları.

🎨 Grafik Arayüz Yönetimi (frontend/)

    LoginPenceresi (login.py): Uygulama güvenliğini sağlayan, ana tarif defteri açılmadan önce çalışan ve kullanıcının profilini doğrulayan modal giriş ekranı.

    AnaPencere (ana_pencere.py): Çift font destekli (Playfair Display & Inter), tarif detaylarını, kategorileri ve şef notlarını listeleyen görsel dashboard ekranı.

✨ Temel Özellikler

    Gurme Tasarım Paneli (Dashboard): Özenle seçilmiş yazı tipi hiyerarşisiyle tarifleri, pişirme sürelerini ve zorluk derecelerini şık kartlar halinde listeleyen modern arayüz.

    Katmanlı Güvenlik Kapısı (Auth Gate): Sistem geçerli bir kullanıcı veya şef oturumu (dogrulanan_kullanici) almadan ana tarif defterinin açılmasını kesin olarak engelleyen güvenli mimari.

    Otomatik Tarif Besleyici (Auto-Seed): Sistem ilk kez çalıştırıldığında yerel veri klasörü boşsa, uygulamanın gurme arayüzünü test edebilmek için veritabanını popüler örnek yemek tarifleriyle otomatik olarak dolduran mekanizma.

    Gelişmiş CSS Temizleyici (fix.py): Kodlama sürecinde arayüz bileşenlerinde oluşabilecek istenmeyen veya biçimsiz CSS yerleşim hatalarını (letter-spacing varyasyonları) Regex (re) kullanarak otomatik olarak tarayan ve temizleyen geliştirici aracı.

🛠️ Kurulum ve Çalıştırma

Gerekli bağımlılıkları yüklemek ve Mutfak Defteri uygulamasını başlatmak için terminalinizde sırasıyla şu komutları çalıştırın:
Bash

pip install -r requirements.txt
python main.py

🔒 Varsayılan Giriş Bilgileri

Sistem ilk kez çalıştırıldığında varsayılan yönetici/şef profili otomatik olarak arka planda oluşturulur:

    Kullanıcı Adı: admin

    Şifre: admin123

🌱 Otomatik Yüklenen Örnek Veriler (Seed)

Eğer yerel data/ klasörünüz boşsa, sistem ilk açılışta platformun görsel yeteneklerinin simüle edilebilmesi için veri tabanını otomatik olarak popüle eder ve şu verileri hazır hale getirir:

    Örnek Yemek Tarifleri (Malzemeler, Ölçüler ve Hazırlanış Adımları)

    Pişirme ve Hazırlama Süreleri

    Kategori Bazlı Ayrıştırma Verileri (Çorbalar, Ana Yemekler, Tatlılar vb.)
