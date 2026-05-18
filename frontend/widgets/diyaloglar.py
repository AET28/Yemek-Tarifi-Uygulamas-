"""Diyaloglar — TarifDiyalog, KullaniciDiyalog, DegerlendirmeDiyalog."""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QComboBox, QSpinBox, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
)
from PyQt5.QtCore import Qt

from backend.veri_yoneticisi import VeriYoneticisi, KATEGORILER
from backend.malzeme import Malzeme


class TarifDiyalog(QDialog):
    """Yeni tarif ekle veya mevcut tarifi düzenle."""

    def __init__(self, vy: VeriYoneticisi, tarif_id: int = None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.tarif_id = tarif_id
        self.malzeme_listesi: list[Malzeme] = []

        if tarif_id:
            tarif = vy.tarif_bul(tarif_id)
            self.setWindowTitle("Tarif Düzenle")
            self.malzeme_listesi = list(tarif.malzemeler)
        else:
            self.setWindowTitle("Yeni Tarif")

        self.setFixedSize(640, 700)
        self.setModal(True)
        self._arayuz_olustur()

        if tarif_id:
            tarif = vy.tarif_bul(tarif_id)
            self.ad_input.setText(tarif.tarif_adi)
            idx = self.kategori_combo.findText(tarif.kategori)
            if idx >= 0:
                self.kategori_combo.setCurrentIndex(idx)
            self.sure_spin.setValue(tarif.hazirlama_suresi)
            self.aciklama_input.setPlainText(tarif.aciklama)
            yazar_idx = self.yazar_combo.findData(tarif.yazar_id)
            if yazar_idx >= 0:
                self.yazar_combo.setCurrentIndex(yazar_idx)
            self._malzeme_tablo_yenile()

    def _arayuz_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        # Başlık
        baslik = QLabel("YENİ TARİF" if not self.tarif_id else "TARİF DÜZENLE")
        baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(baslik)

        # Tarif adı
        layout.addWidget(self._etiket("TARİF ADI"))
        self.ad_input = QLineEdit()
        self.ad_input.setFixedHeight(38)
        self.ad_input.setPlaceholderText("Tarif adını girin")
        layout.addWidget(self.ad_input)

        # Kategori + Süre + Yazar
        satir = QHBoxLayout()
        satir.setSpacing(12)

        sol = QVBoxLayout()
        sol.addWidget(self._etiket("KATEGORİ"))
        self.kategori_combo = QComboBox()
        self.kategori_combo.setFixedHeight(38)
        for k in KATEGORILER:
            self.kategori_combo.addItem(k)
        sol.addWidget(self.kategori_combo)
        satir.addLayout(sol)

        orta = QVBoxLayout()
        orta.addWidget(self._etiket("HAZIRLAMA SÜRESİ"))
        self.sure_spin = QSpinBox()
        self.sure_spin.setFixedHeight(38)
        self.sure_spin.setRange(1, 999)
        self.sure_spin.setValue(30)
        self.sure_spin.setSuffix(" dk")
        orta.addWidget(self.sure_spin)
        satir.addLayout(orta)

        sag = QVBoxLayout()
        sag.addWidget(self._etiket("YAZAR"))
        self.yazar_combo = QComboBox()
        self.yazar_combo.setFixedHeight(38)
        for k in self.vy.kullanicilar:
            self.yazar_combo.addItem(k.ad, k.kullanici_id)
        sag.addWidget(self.yazar_combo)
        satir.addLayout(sag)

        layout.addLayout(satir)

        # Malzeme ekleme
        layout.addWidget(self._etiket("MALZEMELER"))

        malz_satir = QHBoxLayout()
        malz_satir.setSpacing(8)

        self.malz_adi_input = QLineEdit()
        self.malz_adi_input.setFixedHeight(34)
        self.malz_adi_input.setPlaceholderText("Malzeme adı")
        malz_satir.addWidget(self.malz_adi_input, 2)

        self.malz_miktar_input = QLineEdit()
        self.malz_miktar_input.setFixedHeight(34)
        self.malz_miktar_input.setPlaceholderText("Miktar (ör: 2 su bardağı)")
        malz_satir.addWidget(self.malz_miktar_input, 2)

        ekle_btn = QPushButton("EKLE")
        ekle_btn.setObjectName("KucukIkincilButon")
        ekle_btn.setFixedHeight(34)
        ekle_btn.setMinimumWidth(80)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._malzeme_ekle)
        malz_satir.addWidget(ekle_btn)

        layout.addLayout(malz_satir)

        # Malzeme tablosu
        self.malz_tablo = QTableWidget()
        self.malz_tablo.setColumnCount(3)
        self.malz_tablo.setHorizontalHeaderLabels(["MALZEME", "MİKTAR", ""])
        self.malz_tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.malz_tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.malz_tablo.setColumnWidth(2, 60)
        self.malz_tablo.verticalHeader().setVisible(False)
        self.malz_tablo.setSelectionMode(QTableWidget.NoSelection)
        self.malz_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.malz_tablo.setMaximumHeight(160)
        layout.addWidget(self.malz_tablo)

        # Açıklama
        layout.addWidget(self._etiket("YAPILIŞI"))
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setFixedHeight(100)
        self.aciklama_input.setPlaceholderText("Tarif açıklaması...")
        layout.addWidget(self.aciklama_input)

        # Hata
        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fce4e0; color: #c4623a; "
            "border: 1px solid #c4623a; border-radius: 0; "
            "padding: 8px 12px; "
            "font-family: 'Nunito Sans', 'Segoe UI', sans-serif; font-size: 11px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        layout.addWidget(self.hata_lbl)

        # Butonlar
        btn_satir = QHBoxLayout()
        btn_satir.addStretch()

        iptal_btn = QPushButton("İPTAL")
        iptal_btn.setObjectName("HayaletButon")
        iptal_btn.setFixedHeight(38)
        iptal_btn.setMinimumWidth(100)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)
        btn_satir.addWidget(iptal_btn)

        kaydet_btn = QPushButton("KAYDET")
        kaydet_btn.setObjectName("PrimaryButon")
        kaydet_btn.setFixedHeight(38)
        kaydet_btn.setMinimumWidth(110)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
        kaydet_btn.clicked.connect(self._kaydet)
        btn_satir.addWidget(kaydet_btn)

        layout.addLayout(btn_satir)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setObjectName("FormEtiket")
        return lbl

    def _malzeme_ekle(self):
        adi = self.malz_adi_input.text().strip()
        miktar = self.malz_miktar_input.text().strip()
        if not adi or not miktar:
            return
        self.malzeme_listesi.append(Malzeme(adi, miktar))
        self.malz_adi_input.clear()
        self.malz_miktar_input.clear()
        self.malz_adi_input.setFocus()
        self._malzeme_tablo_yenile()

    def _malzeme_tablo_yenile(self):
        self.malz_tablo.setRowCount(len(self.malzeme_listesi))
        for i, m in enumerate(self.malzeme_listesi):
            self.malz_tablo.setRowHeight(i, 32)
            self.malz_tablo.setItem(i, 0, QTableWidgetItem(m.malzeme_adi))
            self.malz_tablo.setItem(i, 1, QTableWidgetItem(m.miktar))

            sil_btn = QPushButton("✕")
            sil_btn.setFixedSize(28, 28)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.setStyleSheet(
                "QPushButton { background: transparent; color: #c4623a; "
                "border: none; font-size: 14px; font-weight: 700; } "
                "QPushButton:hover { color: #9a1f1c; }"
            )
            sil_btn.clicked.connect(lambda _, idx=i: self._malzeme_sil(idx))
            self.malz_tablo.setCellWidget(i, 2, sil_btn)

    def _malzeme_sil(self, idx: int):
        if 0 <= idx < len(self.malzeme_listesi):
            self.malzeme_listesi.pop(idx)
            self._malzeme_tablo_yenile()

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        kategori = self.kategori_combo.currentText()
        sure = self.sure_spin.value()
        aciklama = self.aciklama_input.toPlainText().strip()
        yazar_id = self.yazar_combo.currentData()

        if not ad:
            self.hata_lbl.setText("Tarif adı boş olamaz.")
            self.hata_lbl.setVisible(True)
            return
        if not self.malzeme_listesi:
            self.hata_lbl.setText("En az 1 malzeme ekleyin.")
            self.hata_lbl.setVisible(True)
            return

        try:
            if self.tarif_id:
                self.vy.tarif_guncelle(
                    self.tarif_id,
                    tarif_adi=ad,
                    kategori=kategori,
                    hazirlama_suresi=sure,
                    malzemeler=list(self.malzeme_listesi),
                    aciklama=aciklama,
                    yazar_id=yazar_id,
                )
            else:
                self.vy.tarif_ekle(
                    tarif_adi=ad,
                    kategori=kategori,
                    hazirlama_suresi=sure,
                    malzemeler=list(self.malzeme_listesi),
                    aciklama=aciklama,
                    yazar_id=yazar_id or 0,
                )
            self.accept()
        except ValueError as e:
            self.hata_lbl.setText(str(e))
            self.hata_lbl.setVisible(True)


class KullaniciDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.setWindowTitle("Yeni Kullanıcı")
        self.setFixedSize(420, 280)
        self.setModal(True)
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        baslik = QLabel("YENİ KULLANICI")
        baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(baslik)

        lbl_ad = QLabel("AD SOYAD")
        lbl_ad.setObjectName("FormEtiket")
        layout.addWidget(lbl_ad)
        self.ad_input = QLineEdit()
        self.ad_input.setFixedHeight(38)
        self.ad_input.setPlaceholderText("Ad Soyad")
        layout.addWidget(self.ad_input)

        lbl_email = QLabel("E-POSTA")
        lbl_email.setObjectName("FormEtiket")
        layout.addWidget(lbl_email)
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(38)
        self.email_input.setPlaceholderText("ornek@mail.com")
        layout.addWidget(self.email_input)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fce4e0; color: #c4623a; "
            "border: 1px solid #c4623a; border-radius: 0; "
            "padding: 8px 12px; "
            "font-family: 'Nunito Sans', 'Segoe UI', sans-serif; font-size: 11px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        layout.addWidget(self.hata_lbl)

        btn_satir = QHBoxLayout()
        btn_satir.addStretch()

        iptal_btn = QPushButton("İPTAL")
        iptal_btn.setObjectName("HayaletButon")
        iptal_btn.setFixedHeight(38)
        iptal_btn.setMinimumWidth(100)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)
        btn_satir.addWidget(iptal_btn)

        kaydet_btn = QPushButton("KAYDET")
        kaydet_btn.setObjectName("PrimaryButon")
        kaydet_btn.setFixedHeight(38)
        kaydet_btn.setMinimumWidth(110)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
        kaydet_btn.clicked.connect(self._kaydet)
        btn_satir.addWidget(kaydet_btn)

        layout.addLayout(btn_satir)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        email = self.email_input.text().strip()

        if not ad:
            self.hata_lbl.setText("Ad boş olamaz.")
            self.hata_lbl.setVisible(True)
            return

        try:
            self.vy.kullanici_ekle(ad, email)
            self.accept()
        except ValueError as e:
            self.hata_lbl.setText(str(e))
            self.hata_lbl.setVisible(True)


class DegerlendirmeDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, tarif_id: int, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.tarif_id = tarif_id
        self.setWindowTitle("Değerlendir")
        self.setFixedSize(460, 380)
        self.setModal(True)
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        baslik = QLabel("DEĞERLENDİR")
        baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(baslik)

        tarif = self.vy.tarif_bul(self.tarif_id)
        if tarif:
            tarif_lbl = QLabel(tarif.tarif_adi)
            tarif_lbl.setStyleSheet(
                "color: #2c2420; font-family: 'Merriweather', 'Georgia', serif; "
                "font-size: 20px; font-weight: 900; "
                "background: transparent; border: none;"
            )
            layout.addWidget(tarif_lbl)

        # Kullanıcı seçimi
        lbl_kul = QLabel("KULLANICI")
        lbl_kul.setObjectName("FormEtiket")
        layout.addWidget(lbl_kul)
        self.kullanici_combo = QComboBox()
        self.kullanici_combo.setFixedHeight(38)
        for k in self.vy.kullanicilar:
            self.kullanici_combo.addItem(k.ad, k.kullanici_id)
        layout.addWidget(self.kullanici_combo)

        # Puan
        lbl_puan = QLabel("PUAN (1-5)")
        lbl_puan.setObjectName("FormEtiket")
        layout.addWidget(lbl_puan)
        self.puan_spin = QSpinBox()
        self.puan_spin.setFixedHeight(38)
        self.puan_spin.setRange(1, 5)
        self.puan_spin.setValue(5)
        layout.addWidget(self.puan_spin)

        # Yorum
        lbl_yorum = QLabel("YORUM")
        lbl_yorum.setObjectName("FormEtiket")
        layout.addWidget(lbl_yorum)
        self.yorum_input = QTextEdit()
        self.yorum_input.setFixedHeight(80)
        self.yorum_input.setPlaceholderText("Yorumunuz (isteğe bağlı)...")
        layout.addWidget(self.yorum_input)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fce4e0; color: #c4623a; "
            "border: 1px solid #c4623a; border-radius: 0; "
            "padding: 8px 12px; "
            "font-family: 'Nunito Sans', 'Segoe UI', sans-serif; font-size: 11px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        layout.addWidget(self.hata_lbl)

        btn_satir = QHBoxLayout()
        btn_satir.addStretch()

        iptal_btn = QPushButton("İPTAL")
        iptal_btn.setObjectName("HayaletButon")
        iptal_btn.setFixedHeight(38)
        iptal_btn.setMinimumWidth(100)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)
        btn_satir.addWidget(iptal_btn)

        gonder_btn = QPushButton("GÖNDER")
        gonder_btn.setObjectName("PrimaryButon")
        gonder_btn.setFixedHeight(38)
        gonder_btn.setMinimumWidth(110)
        gonder_btn.setCursor(Qt.PointingHandCursor)
        gonder_btn.clicked.connect(self._gonder)
        btn_satir.addWidget(gonder_btn)

        layout.addLayout(btn_satir)

    def _gonder(self):
        kullanici_id = self.kullanici_combo.currentData()
        puan = self.puan_spin.value()
        yorum = self.yorum_input.toPlainText().strip()

        try:
            self.vy.degerlendirme_ekle(self.tarif_id, kullanici_id, puan, yorum)
            self.accept()
        except ValueError as e:
            self.hata_lbl.setText(str(e))
            self.hata_lbl.setVisible(True)
