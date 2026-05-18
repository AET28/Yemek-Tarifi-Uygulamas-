"""Mutfak Defteri — Yemek Tarif Platformu."""
import sys
import os

# Proje kökünü Python yoluna ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from backend.auth import AuthYoneticisi
from backend.veri_yoneticisi import VeriYoneticisi
from backend.seed import seed_yukle
from frontend.tema import ANA_STIL
from frontend.login import LoginPenceresi
from frontend.ana_pencere import AnaPencere


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(ANA_STIL)

    # Fontları yükle (sistemde varsa)
    for font in ("Playfair Display", "Inter"):
        QFontDatabase.addApplicationFont(font)

    # Veri yöneticisi
    veri_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    vy = VeriYoneticisi(veri_klasoru)

    # Seed verisi (ilk çalıştırmada)
    seed_yukle(vy)

    # Auth
    auth_dosya = os.path.join(veri_klasoru, "auth.json")
    auth = AuthYoneticisi(auth_dosya)
    if not auth.kullanici_var_mi():
        auth.varsayilan_kullanici_olustur()

    # Login
    login = LoginPenceresi(auth)
    if login.exec_() != LoginPenceresi.Accepted:
        sys.exit(0)

    # Ana pencere
    pencere = AnaPencere(vy, login.dogrulanan_kullanici)
    pencere.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
