"""Tarifler — kart grid, filtreler, arama."""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QGridLayout, QFrame, QPushButton, QLineEdit, QComboBox,
    QSpinBox, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend.veri_yoneticisi import VeriYoneticisi, KATEGORILER
from frontend.widgets.bilesenler import (
    EditorialHeader, YildizGoster, Rozet,
)


class TarifKart(QFrame):
    """Tarif grid kartı."""
    tiklandi = pyqtSignal(int)

    def __init__(self, tarif, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.tarif_id = tarif.tarif_id
        self.setObjectName("Kart")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

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
            "font-size: 18px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        ad.setWordWrap(True)
        layout.addWidget(ad)

        # Yazar
        yazar_adi = vy.kullanici_adi(tarif.yazar_id)
        yazar = QLabel(f"— {yazar_adi}")
        yazar.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; font-style: italic; "
            "background: transparent; border: none;"
        )
        layout.addWidget(yazar)

        layout.addStretch()

        # Alt satır
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


class TariflerSayfasi(QWidget):
    tarif_secildi = pyqtSignal(int)
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
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
        self.icerik_layout.setSpacing(24)

        # Header
        self.header = EditorialHeader(
            kategori="KOLEKSİYON",
            baslik="Tarifler",
            altyazi="Tüm tarifler — filtrele, ara, keşfet.",
            sag_etiket="MUTFAK DEFTERİ",
        )
        self.icerik_layout.addWidget(self.header)

        # Filtre satırı
        filtre = QHBoxLayout()
        filtre.setSpacing(12)

        self.arama_input = QLineEdit()
        self.arama_input.setObjectName("AramaInput")
        self.arama_input.setPlaceholderText("Tarif ara...")
        self.arama_input.setFixedHeight(38)
        self.arama_input.textChanged.connect(self._filtrele)
        filtre.addWidget(self.arama_input)

        self.kategori_combo = QComboBox()
        self.kategori_combo.setFixedHeight(38)
        self.kategori_combo.addItem("Tüm Kategoriler")
        for k in KATEGORILER:
            self.kategori_combo.addItem(k)
        self.kategori_combo.currentTextChanged.connect(self._filtrele)
        filtre.addWidget(self.kategori_combo)

        sure_lbl = QLabel("Max Süre:")
        sure_lbl.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; background: transparent; border: none;"
        )
        filtre.addWidget(sure_lbl)

        self.sure_spin = QSpinBox()
        self.sure_spin.setFixedHeight(38)
        self.sure_spin.setRange(0, 999)
        self.sure_spin.setValue(0)
        self.sure_spin.setSuffix(" dk")
        self.sure_spin.setSpecialValueText("Hepsi")
        self.sure_spin.valueChanged.connect(self._filtrele)
        filtre.addWidget(self.sure_spin)

        self.ekle_btn = QPushButton("YENİ TARİF")
        self.ekle_btn.setObjectName("PrimaryButon")
        self.ekle_btn.setStyleSheet("background-color: #c4623a; color: #ffffff; border: none; font-weight: bold; border-radius: 4px;")
        self.ekle_btn.setFixedHeight(40)
        self.ekle_btn.setMinimumWidth(140)
        self.ekle_btn.setCursor(Qt.PointingHandCursor)
        self.ekle_btn.clicked.connect(self._tarif_ekle)
        filtre.addWidget(self.ekle_btn)

        self.icerik_layout.addLayout(filtre)

        # Sonuç sayısı
        self.sonuc_lbl = QLabel()
        self.sonuc_lbl.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; font-style: italic; "
            "background: transparent; border: none;"
        )
        self.icerik_layout.addWidget(self.sonuc_lbl)

        # Grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)
        self.icerik_layout.addWidget(self.grid_widget)

        self.icerik_layout.addStretch()

        scroll.setWidget(icerik)
        ana.addWidget(scroll)

    def _filtrele(self):
        self._grid_doldur()

    def _grid_doldur(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        arama = self.arama_input.text().strip().lower()
        kategori = self.kategori_combo.currentText()
        max_sure = self.sure_spin.value()

        filtreli = []
        for t in self.vy.tarifler:
            if arama and arama not in t.tarif_adi.lower():
                continue
            if kategori != "Tüm Kategoriler" and t.kategori != kategori:
                continue
            if max_sure > 0 and t.hazirlama_suresi > max_sure:
                continue
            filtreli.append(t)

        self.sonuc_lbl.setText(f"{len(filtreli)} tarif bulundu")

        for i, tarif in enumerate(filtreli):
            kart = TarifKart(tarif, self.vy)
            kart.tiklandi.connect(self.tarif_secildi.emit)
            self.grid_layout.addWidget(kart, i // 3, i % 3)

    def yenile(self):
        self._grid_doldur()

    def _tarif_ekle(self):
        from frontend.widgets.diyaloglar import TarifDiyalog
        dlg = TarifDiyalog(self.vy, parent=self)
        if dlg.exec_():
            self.yenile()
            self.veri_degisti.emit()
