"""Kullanıcılar — tablo görünümü."""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend.veri_yoneticisi import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader, MuhurAvatar, Rozet, HucreSarmalayici, ButonGrubu,
)


class KullanicilarSayfasi(QWidget):
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
        icerik_layout = QVBoxLayout(icerik)
        icerik_layout.setContentsMargins(48, 36, 48, 48)
        icerik_layout.setSpacing(24)

        header = EditorialHeader(
            kategori="KULLANICILAR",
            baslik="Kullanıcılar",
            altyazi="Platform kullanıcıları ve istatistikleri.",
            sag_etiket="MUTFAK DEFTERİ",
        )
        icerik_layout.addWidget(header)

        # Butonlar
        btn_satir = QHBoxLayout()
        btn_satir.setSpacing(12)
        btn_satir.addStretch()

        ekle_btn = QPushButton("YENİ KULLANICI")
        ekle_btn.setObjectName("PrimaryButon")
        ekle_btn.setStyleSheet("background-color: #c4623a; color: #ffffff; border: none; font-weight: bold; border-radius: 4px;")
        ekle_btn.setFixedHeight(40)
        ekle_btn.setMinimumWidth(170)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._kullanici_ekle)
        btn_satir.addWidget(ekle_btn)

        icerik_layout.addLayout(btn_satir)

        # Tablo
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels([
            "KULLANICI", "E-POSTA", "EKLEDİĞİ TARİF", "DEĞERLENDİRME", "İŞLEMLER",
        ])
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tablo.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.tablo.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.tablo.setColumnWidth(2, 140)
        self.tablo.setColumnWidth(3, 140)
        self.tablo.setColumnWidth(4, 160)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionMode(QTableWidget.NoSelection)
        self.tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablo.setAlternatingRowColors(True)

        icerik_layout.addWidget(self.tablo)
        icerik_layout.addStretch()

        scroll.setWidget(icerik)
        ana.addWidget(scroll)

    def yenile(self):
        self.tablo.setRowCount(len(self.vy.kullanicilar))

        for i, k in enumerate(self.vy.kullanicilar):
            self.tablo.setRowHeight(i, 56)

            # Avatar + Ad
            avatar_w = QWidget()
            avatar_l = QHBoxLayout(avatar_w)
            avatar_l.setContentsMargins(10, 6, 10, 6)
            avatar_l.setSpacing(10)
            avatar = MuhurAvatar(k.ad, boyut=34)
            avatar_l.addWidget(avatar)
            ad_lbl = QLabel(k.ad)
            ad_lbl.setStyleSheet(
                "color: #2c2420; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                "font-size: 13px; font-weight: 600; "
                "background: transparent; border: none;"
            )
            avatar_l.addWidget(ad_lbl)
            avatar_l.addStretch()
            self.tablo.setCellWidget(i, 0, avatar_w)

            # Email
            email_item = QTableWidgetItem(k.email)
            email_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.tablo.setItem(i, 1, email_item)

            # Tarif sayısı
            tarif_sayi = self.vy.kullanici_tarif_sayisi(k.kullanici_id)
            rozet = Rozet(f"{tarif_sayi} TARİF", "basari" if tarif_sayi > 0 else "notr")
            self.tablo.setCellWidget(i, 2, HucreSarmalayici(rozet))

            # Değerlendirme sayısı
            deg_sayi = self.vy.kullanici_degerlendirme_sayisi(k.kullanici_id)
            rozet2 = Rozet(f"{deg_sayi} YORUM", "uyari" if deg_sayi > 0 else "notr")
            self.tablo.setCellWidget(i, 3, HucreSarmalayici(rozet2))

            # İşlemler
            sil_btn = QPushButton("SİL")
            sil_btn.setObjectName("KucukTehlikeButon")
            sil_btn.setFixedHeight(28)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.clicked.connect(lambda _, kid=k.kullanici_id: self._kullanici_sil(kid))
            self.tablo.setCellWidget(i, 4, ButonGrubu([sil_btn]))

    def _kullanici_ekle(self):
        from frontend.widgets.diyaloglar import KullaniciDiyalog
        dlg = KullaniciDiyalog(self.vy, parent=self)
        if dlg.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _kullanici_sil(self, kullanici_id: int):
        from PyQt5.QtWidgets import QMessageBox
        cevap = QMessageBox.question(
            self, "Kullanıcı Sil",
            "Bu kullanıcıyı silmek istediğinize emin misiniz?\nDeğerlendirmeleri silinecek, tarifleri kalacak.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            self.vy.kullanici_sil(kullanici_id)
            self.yenile()
            self.veri_degisti.emit()
