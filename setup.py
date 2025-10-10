"""
TIR Yükleme Optimizasyon Sistemi Kurulum Scripti
"""
import subprocess
import sys
import os


def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 8):
        print("❌ Hata: Python 3.8 veya üzeri gereklidir!")
        print(f"Mevcut versiyon: {sys.version}")
        return False
    print(f"✅ Python versiyonu uygun: {sys.version.split()[0]}")
    return True


def create_virtual_environment():
    """Sanal ortam oluştur"""
    print("\n📦 Sanal ortam oluşturuluyor...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Sanal ortam başarıyla oluşturuldu!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Sanal ortam oluşturulamadı!")
        return False


def install_requirements():
    """Gerekli kütüphaneleri yükle"""
    print("\n📚 Gerekli kütüphaneler yükleniyor...")

    # Pip'i güncelle
    print("  ⏳ pip güncelleniyor...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                   stdout=subprocess.DEVNULL)

    # Requirements'ları yükle
    print("  ⏳ Kütüphaneler yükleniyor...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                       check=True, stdout=subprocess.DEVNULL)
        print("✅ Tüm kütüphaneler başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Kütüphaneler yüklenemedi!")
        return False


def create_directories():
    """Gerekli dizinleri oluştur"""
    print("\n📁 Dizinler kontrol ediliyor...")
    directories = ['core', 'gui']

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  ✅ {directory}/ dizini oluşturuldu")
        else:
            print(f"  ✓ {directory}/ dizini mevcut")

    return True


def create_init_files():
    """__init__.py dosyalarını oluştur"""
    print("\n📝 Init dosyaları kontrol ediliyor...")

    init_files = {
        'core/__init__.py': '''"""
Core modülü - TIR yükleme optimizasyon mantığı
"""
from .truck_loader import Box, TruckArea, TruckLoader

__all__ = ['Box', 'TruckArea', 'TruckLoader']
''',
        'gui/__init__.py': '''"""
GUI modülü - PyQt6 arayüz bileşenleri
"""
from .main_window import MainWindow

__all__ = ['MainWindow']
''',
        '__init__.py': '''"""
TIR Yükleme Optimizasyon Sistemi
Versiyon: 2.0
"""
__version__ = "2.0"
__author__ = "EDGIN"
'''
    }

    for filepath, content in init_files.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} oluşturuldu")
        else:
            print(f"  ✓ {filepath} mevcut")

    return True


def verify_installation():
    """Kurulumu doğrula"""
    print("\n🔍 Kurulum doğrulanıyor...")

    required_modules = ['PyQt6', 'pandas', 'openpyxl', 'matplotlib']
    all_ok = True

    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} yüklü")
        except ImportError:
            print(f"  ❌ {module} yüklenemedi!")
            all_ok = False

    return all_ok


def main():
    """Ana kurulum fonksiyonu"""
    print("=" * 60)
    print("TIR YÜKLEME OPTİMİZASYON SİSTEMİ - KURULUM")
    print("=" * 60)

    steps = [
        ("Python versiyonu kontrolü", check_python_version),
        ("Dizin yapısı oluşturma", create_directories),
        ("Init dosyaları oluşturma", create_init_files),
        ("Gerekli kütüphaneleri yükleme", install_requirements),
        ("Kurulum doğrulama", verify_installation)
    ]

    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Kurulum başarısız: {step_name}")
            print("\nLütfen hataları düzeltin ve tekrar deneyin.")
            return False

    print("\n" + "=" * 60)
    print("✅ KURULUM BAŞARIYLA TAMAMLANDI!")
    print("=" * 60)
    print("\nUygulamayı başlatmak için:")
    print("  python main.py")
    print("\nVeya sanal ortamı aktifleştirip çalıştırın:")
    print("  Windows: venv\\Scripts\\activate")
    print("  Linux/Mac: source venv/bin/activate")
    print("  python main.py")
    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)