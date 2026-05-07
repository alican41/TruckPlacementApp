TIR Yükleme Optimizasyon Sistemi
Modern ve kullanıcı dostu PyQt6 arayüzü ile TIR yükleme optimizasyonu yapan profesyonel bir uygulama.

Özellikler
Excel dosyalarından kutu verilerini okuma
32 alanlı TIR için otomatik optimizasyon
İlk 10 alan için özel ağırlık kontrolü (max 5000 kg)
Yükseklik dengesi tabanlı yerleşim
Gerçek zamanlı ilerleme göstergesi
PDF rapor oluşturma
Görsel istatistik paneli
Modern ve şık kullanıcı arayüzü

Proje Yapısı
truck_loader_app/
│
├── main.py                 # Ana uygulama başlatıcı
├── requirements.txt        # Gerekli kütüphaneler
├── README.md              # Bu dosya
│
├── core/                  # Core modülü
│   ├── __init__.py
│   └── truck_loader.py    # Optimizasyon mantığı
│
└── gui/                   # GUI modülü
    ├── __init__.py
    └── main_window.py     # Ana pencere
Kurulum
1. Python Kurulumu
Python 3.8 veya üzeri sürüm gereklidir. Python.org adresinden indirin.

2. Sanal Ortam Oluşturma (Önerilen)
bash
python -m venv venv

# Windows için:
venv\Scripts\activate

# macOS/Linux için:
source venv/bin/activate
3. Gerekli Kütüphaneleri Yükleme
bash
pip install -r requirements.txt
Kullanım
Uygulamayı Başlatma
bash
python main.py
Adım Adım Kullanım
Dosya Seçimi: "Dosya Seç" butonuna tıklayarak Excel dosyanızı seçin
Optimizasyon: "Optimizasyonu Başlat" butonuna tıklayın
Sonuçları İnceleme: Yükleme planını ve istatistikleri görüntüleyin
PDF Raporu: "PDF Dışa Aktar" ile görsel rapor oluşturun
Excel Dosya Formatı
Excel dosyanızda aşağıdaki sütunlar bulunmalıdır:

Sütun Adı	Açıklama
BOX NO	Kutu numarası (örn: B001)
BOYUT	Kutu boyutu (BÜYÜK, ORTA, KÜÇÜK, PALET, KATLI RAF, BATTAL BOY)
DOLU KG	Kutu ağırlığı (kg cinsinden)
Kutu Tipleri ve Yükseklikleri
Tip	Yükseklik
KÜÇÜK	1x
ORTA	2x
BÜYÜK	3x
PALET	3x
KATLI RAF (PROJECT)	6x
BATTAL BOY	7x
Optimizasyon Kuralları
32 Alan: TIR toplam 32 alana bölünmüştür
İlk 10 Alan: Maksimum 5000 kg (ağırlık merkezi için)
Maksimum Yükseklik: Her alan için 6x birim
Palet Kuralı: Her alanda maksimum 1 palet olabilir
Dengeli Dağılım: Yükseklik dengesi gözetilerek yerleşim yapılır
Özellik Detayları
Optimizasyon Algoritması
300 iterasyon ile en iyi yerleşimi bulur
Yükseklik dengesi öncelikli
Her alanda en az 1 kutu garantisi
Ağırlık limitlerine uyum
PDF Raporu
2 sayfalık detaylı görsel rapor
Her alan için kutu listesi ve toplam ağırlık
A4 boyutunda profesyonel çıktı
Kullanıcı Arayüzü
Modern ve şık tasarım
İlerleme göstergesi
Gerçek zamanlı istatistikler
Hata yönetimi ve bildirimler
Sorun Giderme
Uygulama Başlamıyor
bash
# Kütüphaneleri yeniden yükleyin
pip install --upgrade -r requirements.txt
Excel Dosyası Okunamıyor
Dosya formatının .xlsx veya .xls olduğundan emin olun
Gerekli sütunların (BOX NO, BOYUT, DOLU KG) bulunduğunu kontrol edin
Dosyanın başka bir program tarafından açık olmadığından emin olun
PDF Oluşturulamıyor
Matplotlib kütüphanesinin doğru yüklendiğinden emin olun
Kaydetmek istediğiniz klasöre yazma izniniz olduğunu kontrol edin
Teknik Destek
Sorularınız için: ali.can.dgru10@gmail.com

Versiyon Geçmişi
v2.0 (Mevcut)
PyQt6 modern arayüz
İyileştirilmiş optimizasyon algoritması
PDF rapor desteği
İlerleme göstergesi
İstatistik paneli
v1.0
Temel komut satırı uygulaması
Excel okuma ve optimizasyon
Lisans
© 2024 EDGIN - Tüm hakları saklıdır.

Ekran Görüntüleri
Ana Pencere
Modern ve kullanıcı dostu arayüz ile tüm işlemlerinizi kolayca yapabilirsiniz.

Optimizasyon Sonuçları
Detaylı yükleme planı ve istatistikler gerçek zamanlı olarak görüntülenir.

PDF Raporu
Profesyonel görünümlü, yazdırılabilir PDF raporları oluşturun.

Not: Bu uygulama Python 3.8+ gerektirir ve Windows, macOS ve Linux işletim sistemlerinde çalışır.

