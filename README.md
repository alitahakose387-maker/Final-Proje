# 🚀 PromptHub — Yapay Zeka Prompt Paylaşım Platformu

Yapay zeka meraklılarının en iyi promptlarını paylaşabileceği, beğenebileceği ve yorumlaşabileceği modern bir sosyal platform. ChatGPT, Gemini, Midjourney ve diğer AI araçları için etkili promptları keşfedin, koleksiyonunuzu oluşturun ve toplulukla etkileşime geçin.

---

## ✨ Öne Çıkan Gelişmiş Özellikler

* **Modüler Mimari:** Uygulama spagetti kod yerine Application Factory Pattern ve bağımsız `auth`, `main`, `errors` blueprint modülleriyle kurulmuştur.
* **Gelişmiş Veritabanı İlişkileri (SQLAlchemy 2.x):** Güncel `Mapped` ve `mapped_column` standartları kullanılarak `User`, `Prompt` ve `Comment` modelleri arasında ilişkisel bağlar kurgulanmıştır.
* **Katı Yetki Kontrolü (Authorization):** Bir kullanıcının başkasına ait promptu veya yorumu silmesini ya da düzenlemesini engelleyen `HTTP 403 Forbidden` kontrolü mevcuttur.
* **Basamaklı Hesap Silme (Cascade Delete):** Kullanıcı hesabını sildiğinde, veritabanı bütünlüğünü korumak adına o kullanıcıya ait tüm promptlar ve yorumlar otomatik olarak temizlenir.
* **Çift Renk Modu (Light/Dark Theme):** Bootstrap 5'in yerleşik renk modları kullanılarak istemci tarafında (client-side) çalışan ve seçimi tarayıcı hafızasında (`localStorage`) saklayan dinamik karanlık tema geçişi entegre edilmiştir.
* **Güvenli E-posta Aktivasyon Sistemi:** Sahte e-posta ile kayıt engellenmiştir. Geliştirme ortamında SMTP bağlantı hatalarını engellemek amacıyla aktivasyon linkleri doğrudan terminale güvenli bir şekilde log olarak basılır.

---

## 🛠️ Kurulum ve Yerel Çalıştırma (Local Setup)

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/kullanici/prompthub.git
cd prompthub
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Tanımlayın
`.env.example` dosyasını `.env` olarak kopyalayın ve gerekli değerleri düzenleyin:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### 5. Veritabanı Göçlerini (Migrations) Uygulayın
Yerel SQLite veritabanını başlatmak ve güncel şemayı uygulamak için:
```bash
$env:FLASK_APP="run.py"   # Windows (PowerShell)
# veya
export FLASK_APP=run.py   # macOS / Linux

flask db upgrade
```

### 6. Uygulamayı Başlatın
```bash
flask run
```
Tarayıcınızda `http://127.0.0.1:5000` adresini açarak uygulamayı test edebilirsiniz.

---

## 🐳 Docker ile Çalıştırma (Containerized Run)

Uygulamayı Docker ve Docker Compose kullanarak tek bir komutla ayağa kaldırabilirsiniz. Konteyner kapandığında verilerinizin kaybolmaması için adlandırılmış bir SQLite veri birimi (`sqlite_data` volume) otomatik olarak bağlanır.

### Docker Compose Komutları
```bash
# Projeyi derleyin ve çalıştırın
docker compose up --build

# Arka planda çalıştırmak için
docker compose up -d

# Konteynerları durdurmak için
docker compose down
```

---

## ⚠️ Geliştirici ve Windows Notları (PowerShell & SQLite Kısıtları)

### 1. PowerShell Çevre Değişkenleri
Windows PowerShell üzerinde geliştirme yaparken Flask komutlarının hata vermemesi için `FLASK_APP` çevre değişkenini şu şekilde tanımlamanız gerekir:
```powershell
$env:FLASK_APP="run.py"
```

### 2. SQLite ALTER TABLE (Batch Mode Migration) Kısıtı
SQLite, `NOT NULL` tanımlı yeni sütunların var olan tablolara eklenmesinde kısıtlamalara sahiptir. Projemizdeki e-posta aktivasyon özelliği (`is_confirmed` sütunu) eklenirken karşılaşılan bu hatayı çözmek amacıyla Alembic migrasyon dosyası `batch_alter_table` mimarisine uygun şekilde `server_default` parametresiyle düzenlenmiştir.
Böylece `flask db upgrade` komutu sorunsuz çalışmaktadır.

### 3. Yerel E-posta Test Simülasyonu
Yerel ortamda SMTP sunucu bağlantı hatalarını (`Connection unexpectedly closed`) önlemek amacıyla `config.py` içinde `MAIL_SUPPRESS_SEND = True` tanımlanmıştır. Kayıt esnasında oluşturulan aktivasyon linkleri doğrudan terminal ekranına log olarak basılmaktadır:
```text
================================================================================
Geliştirici Aktivasyon Bağlantısı: http://127.0.0.1:5000/auth/confirm/<token>
================================================================================
```
Kayıt olduktan sonra terminaldeki bu bağlantıya tıklayarak hesabınızı hemen aktifleştirebilirsiniz.

---

## 📂 Proje Yapısı

```text
├── app/
│   ├── __init__.py      # Application Factory & Extension Kayıtları
│   ├── models.py        # User, Prompt, Comment Modelleri
│   ├── main/            # Prompt CRUD ve Sayfalama Rotaları
│   ├── auth/            # Oturum, E-posta Aktivasyonu ve Hesap Silme
│   ├── errors/          # 403, 404, 500 Hata Yakalayıcıları (Blueprints)
│   └── templates/       # Arayüz Şablonları (Aydınlık/Karanlık Uyumlu)
├── migrations/          # Alembic Veritabanı Migrasyon Geçmişi
├── Dockerfile           # Konteyner İmaj Yapılandırması
├── docker-compose.yml   # Servis ve Volume Yapılandırması
└── run.py               # Flask Giriş Noktası
```
