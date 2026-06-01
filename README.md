# PromptHub — Yapay Zeka Prompt Paylaşım Platformu

Yapay zeka meraklılarının en iyi promptlarını paylaşabileceği, beğenebileceği ve yorumlaşabileceği bir sosyal platform. ChatGPT, Gemini, Midjourney ve diğer AI araçları için etkili promptları keşfedin, koleksiyonunuzu oluşturun ve toplulukla etkileşime geçin.

## Kurulum

### 1. Depoyu Klonla

```bash
git clone https://github.com/kullanici/prompthub.git
cd prompthub
```

### 2. Sanal Ortam Oluştur ve Aktifleştir

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Yapılandır

`.env.example` dosyasını kopyalayıp `.env` olarak kaydet ve değerleri düzenle:

```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS / Linux
```

`.env` dosyasındaki `SECRET_KEY` değerini güvenli bir rastgele değerle değiştir:

```
SECRET_KEY=buraya-guclu-bir-anahtar-yaz
DATABASE_URL=sqlite:///app.db
```

### 5. Veritabanını Başlat

```bash
flask db init
flask db migrate -m "ilk migrasyon"
flask db upgrade
```

## Geliştirme

### Uygulamayı Çalıştır

```bash
flask run
```

Tarayıcıda `http://127.0.0.1:5000` adresine git.

### Veritabanı İşlemleri

```bash
# Model değişikliklerinden sonra yeni migrasyon oluştur
flask db migrate -m "degisiklik aciklamasi"

# Migrasyonları veritabanına uygula
flask db upgrade

# Son migrasyonu geri al
flask db downgrade
```

### Test Çalıştır

```bash
python -m pytest tests/
```

## Teknolojiler

| Teknoloji | Kullanım Amacı |
|-----------|---------------|
| **Flask 3.x** | Web framework |
| **Flask-SQLAlchemy** | ORM ve veritabanı yönetimi |
| **Flask-Migrate** | Veritabanı migrasyonları (Alembic) |
| **Flask-Login** | Kullanıcı oturum yönetimi |
| **Flask-WTF** | Form doğrulama ve CSRF koruması |
| **python-dotenv** | Ortam değişkenleri yönetimi |
| **SQLite** | Geliştirme veritabanı |

## Proje Yapısı

```
├── app/
│   ├── __init__.py      # Application Factory
│   ├── models.py        # Veritabanı modelleri
│   ├── main/            # Ana sayfa, prompt listeleme
│   ├── auth/            # Kayıt, giriş, profil
│   ├── errors/          # Hata sayfaları (404, 500)
│   ├── templates/       # Jinja2 şablonları
│   └── static/          # CSS, JS, görseller
├── migrations/          # Veritabanı migrasyonları
├── tests/               # Birim ve entegrasyon testleri
├── config.py            # Uygulama yapılandırması
├── run.py               # Giriş noktası
├── .env.example         # Örnek ortam değişkenleri
└── requirements.txt     # Python bağımlılıkları
```
