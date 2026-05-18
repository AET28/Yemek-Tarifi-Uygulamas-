"""Dashboard — 4 metrik kart + son eklenen 6 tarif."""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QGridLayout, QFrame, QPushButton, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend.veri_yoneticisi import VeriYoneticisi
from frontend.widgets.bilesenler import (
    MetrikKart, EditorialHeader, Kart, YildizGoster, Rozet,
)


class TarifMiniKart(QFrame):
    """Son eklenen tarif mini kartı."""
    tiklandi = pyqtSignal(int)

    def __init__(self, tarif, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.tarif_id = tarif.tarif_id
        self.setObjectName("Kart")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(160)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        # Kategori tag
        kat = QLabel(tarif.kategori.upper())
        kat.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 9px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(kat)

        # Tarif adı
        ad = QLabel(tarif.tarif_adi)
        ad.setStyleSheet(
            "color: #2c2420; font-family: 'Merriweather', 'Georgia', serif; "
            "font-size: 16px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        ad.setWordWrap(True)
        layout.addWidget(ad)

        layout.addStretch()

        # Alt satır: süre + malzeme sayısı + puan
        alt = QHBoxLayout()
        alt.setSpacing(12)

        sure = QLabel(f"{tarif.hazirlama_suresi} dk")
        sure.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; background: transparent; border: none;"
        )
        alt.addWidget(sure)

        malz = QLabel(f"{len(tarif.malzemeler)} malzeme")
        malz.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; background: transparent; border: none;"
        )
        alt.addWidget(malz)

        ort = vy.tarif_ortalama_puan(tarif.tarif_id)
        if ort > 0:
            yildiz = YildizGoster(ort, boyut=12)
            alt.addWidget(yildiz)
            puan_lbl = QLabel(f"{ort:.1f}")
            puan_lbl.setStyleSheet(
                "color: #2c2420; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                "font-size: 11px; font-weight: 700; "
                "background: transparent; border: none;"
            )
            alt.addWidget(puan_lbl)

        alt.addStretch()
        layout.addLayout(alt)

    def mousePressEvent(self, e):
        self.tiklandi.emit(self.tarif_id)


class DashboardSayfasi(QWidget):
    tarif_secildi = pyqtSignal(int)

    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        icerik = QWidget()
        self.icerik_layout = QVBoxLayout(icerik)
        self.icerik_layout.setContentsMargins(48, 36, 48, 48)
        self.icerik_layout.setSpacing(32)

        # Header
        self.header = EditorialHeader(
            kategori="GENEL BAKIŞ",
            baslik="Dashboard",
            altyazi="Mutfak Defteri istatistikleri ve son eklenen tarifler.",
            sag_etiket="MUTFAK DEFTERİ",
        )
        self.icerik_layout.addWidget(self.header)

        # Metrik kartlar
        self.metrik_layout = QHBoxLayout()
        self.metrik_layout.setSpacing(16)

        self.mk_tarif = MetrikKart("Toplam Tarif", accent=True)
        self.mk_kullanici = MetrikKart("Kayıtlı Kullanıcı")
        self.mk_degerlendirme = MetrikKart("Toplam Değerlendirme")
        self.mk_ortalama = MetrikKart("Ortalama Puan", accent=True)

        self.metrik_layout.addWidget(self.mk_tarif)
        self.metrik_layout.addWidget(self.mk_kullanici)
        self.metrik_layout.addWidget(self.mk_degerlendirme)
        self.metrik_layout.addWidget(self.mk_ortalama)

        self.icerik_layout.addLayout(self.metrik_layout)

        # Son eklenen tarifler başlığı
        son_baslik = QLabel("SON EKLENEN TARİFLER")
        son_baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        self.icerik_layout.addWidget(son_baslik)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(16)
        self.icerik_layout.addLayout(self.grid_layout)

        self.icerik_layout.addStretch()

        scroll.setWidget(icerik)
        ana.addWidget(scroll)

    def yenile(self):
        self.mk_tarif.deger_ayarla(str(len(self.vy.tarifler)))
        self.mk_kullanici.deger_ayarla(str(len(self.vy.kullanicilar)))
        self.mk_degerlendirme.deger_ayarla(str(len(self.vy.degerlendirmeler)))
        ort = self.vy.genel_ortalama_puan()
        self.mk_ortalama.deger_ayarla(f"{ort:.1f}" if ort > 0 else "—")

        # Grid temizle
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Son 6 tarif
        son_tarifler = sorted(
            self.vy.tarifler,
            key=lambda t: t.eklenme_tarihi,
            reverse=True,
        )[:6]

        for i, tarif in enumerate(son_tarifler):
            kart = TarifMiniKart(tarif, self.vy)
            kart.tiklandi.connect(self.tarif_secildi.emit)
            self.grid_layout.addWidget(kart, i // 3, i % 3)
