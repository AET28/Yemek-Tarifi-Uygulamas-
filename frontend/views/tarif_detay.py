"""Tarif Detay — tek tarif görünümü."""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QPushButton, QSizePolicy, QTextEdit,
)
from PyQt5.QtCore import Qt, pyqtSignal

from backend.veri_yoneticisi import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader, MalzemeListesi, YildizGoster, PuanRozet,
    MuhurAvatar, Rozet, Kart,
)


class TarifDetaySayfasi(QWidget):
    geri_istendi = pyqtSignal()
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.tarif_id = None
        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.icerik = QWidget()
        self.icerik_layout = QVBoxLayout(self.icerik)
        self.icerik_layout.setContentsMargins(48, 36, 48, 48)
        self.icerik_layout.setSpacing(24)

        self.scroll.setWidget(self.icerik)
        ana.addWidget(self.scroll)

    def tarif_goster(self, tarif_id: int):
        self.tarif_id = tarif_id
        self._icerik_olustur()

    def _icerik_temizle(self):
        while self.icerik_layout.count():
            item = self.icerik_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

    def _icerik_olustur(self):
        self._icerik_temizle()

        tarif = self.vy.tarif_bul(self.tarif_id)
        if not tarif:
            return

        # Geri butonu
        geri_btn = QPushButton("← GERİ")
        geri_btn.setObjectName("HayaletButon")
        geri_btn.setFixedHeight(32)
        geri_btn.setFixedWidth(120)
        geri_btn.setCursor(Qt.PointingHandCursor)
        geri_btn.clicked.connect(self.geri_istendi.emit)
        self.icerik_layout.addWidget(geri_btn)

        # Header
        ort = self.vy.tarif_ortalama_puan(tarif.tarif_id)
        deg_sayi = self.vy.tarif_degerlendirme_sayisi(tarif.tarif_id)
        yazar = self.vy.kullanici_adi(tarif.yazar_id)

        header = EditorialHeader(
            kategori=tarif.kategori.upper(),
            baslik=tarif.tarif_adi,
            altyazi=f"Hazırlama süresi: {tarif.hazirlama_suresi} dakika — {yazar}",
            sag_etiket=f"{deg_sayi} DEĞERLENDİRME",
            sag_meta=tarif.eklenme_tarihi[:10] if tarif.eklenme_tarihi else "",
        )
        self.icerik_layout.addWidget(header)

        # Puan satırı
        puan_satir = QHBoxLayout()
        puan_satir.setSpacing(12)

        if ort > 0:
            yildiz = YildizGoster(ort, boyut=20)
            puan_satir.addWidget(yildiz)
            puan_lbl = QLabel(f"{ort:.1f}")
            puan_lbl.setStyleSheet(
                "color: #2c2420; font-family: 'Merriweather', 'Georgia', serif; "
                "font-size: 24px; font-weight: 900; "
                "background: transparent; border: none;"
            )
            puan_satir.addWidget(puan_lbl)
            rozet = PuanRozet(ort)
            puan_satir.addWidget(rozet)

        puan_satir.addStretch()

        # Düzenle + Sil butonları
        duzenle_btn = QPushButton("DÜZENLE")
        duzenle_btn.setObjectName("KucukIkincilButon")
        duzenle_btn.setFixedHeight(30)
        duzenle_btn.setMinimumWidth(110)
        duzenle_btn.setCursor(Qt.PointingHandCursor)
        duzenle_btn.clicked.connect(self._duzenle)
        puan_satir.addWidget(duzenle_btn)

        sil_btn = QPushButton("SİL")
        sil_btn.setObjectName("KucukTehlikeButon")
        sil_btn.setFixedHeight(30)
        sil_btn.setMinimumWidth(80)
        sil_btn.setCursor(Qt.PointingHandCursor)
        sil_btn.clicked.connect(self._sil)
        puan_satir.addWidget(sil_btn)

        self.icerik_layout.addLayout(puan_satir)

        # Malzeme listesi
        malz_baslik = QLabel("MALZEMELER")
        malz_baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        self.icerik_layout.addWidget(malz_baslik)

        malz_liste = MalzemeListesi(tarif.malzemeler)
        self.icerik_layout.addWidget(malz_liste)

        # Yapılış
        if tarif.aciklama:
            yapilis_baslik = QLabel("YAPILIŞI")
            yapilis_baslik.setStyleSheet(
                "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                "font-size: 10px; font-weight: 800; "
                "background: transparent; border: none;"
            )
            self.icerik_layout.addWidget(yapilis_baslik)

            aciklama = QLabel(tarif.aciklama)
            aciklama.setWordWrap(True)
            aciklama.setStyleSheet(
                "color: #4a3f38; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                "font-size: 13px; line-height: 1.6; "
                "background: transparent; border: none;"
            )
            self.icerik_layout.addWidget(aciklama)

        # Değerlendirmeler
        deg_baslik = QLabel("DEĞERLENDİRMELER")
        deg_baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        self.icerik_layout.addWidget(deg_baslik)

        ilgili_deg = [
            d for d in self.vy.degerlendirmeler
            if d.tarif_id == self.tarif_id
        ]

        if ilgili_deg:
            for d in ilgili_deg:
                kart = Kart()
                kart_icerik = QHBoxLayout()
                kart_icerik.setSpacing(12)

                k_adi = self.vy.kullanici_adi(d.kullanici_id)
                avatar = MuhurAvatar(k_adi, boyut=36)
                kart_icerik.addWidget(avatar)

                bilgi = QVBoxLayout()
                bilgi.setSpacing(4)

                ust = QHBoxLayout()
                ust.setSpacing(8)
                ad_lbl = QLabel(k_adi)
                ad_lbl.setStyleSheet(
                    "color: #2c2420; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                    "font-size: 12px; font-weight: 700; "
                    "background: transparent; border: none;"
                )
                ust.addWidget(ad_lbl)
                yildiz = YildizGoster(d.puan, boyut=12)
                ust.addWidget(yildiz)
                puan_txt = QLabel(f"{d.puan}/5")
                puan_txt.setStyleSheet(
                    "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                    "font-size: 11px; background: transparent; border: none;"
                )
                ust.addWidget(puan_txt)
                ust.addStretch()
                bilgi.addLayout(ust)

                if d.yorum:
                    yorum_lbl = QLabel(d.yorum)
                    yorum_lbl.setWordWrap(True)
                    yorum_lbl.setStyleSheet(
                        "color: #4a3f38; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                        "font-size: 12px; font-style: italic; "
                        "background: transparent; border: none;"
                    )
                    bilgi.addWidget(yorum_lbl)

                kart_icerik.addLayout(bilgi, 1)
                kart.layout.addLayout(kart_icerik)
                self.icerik_layout.addWidget(kart)
        else:
            bos = QLabel("Henüz değerlendirme yok.")
            bos.setStyleSheet(
                "color: #a89e94; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
                "font-size: 12px; font-style: italic; "
                "background: transparent; border: none;"
            )
            self.icerik_layout.addWidget(bos)

        # Değerlendir butonu
        degerlendir_btn = QPushButton("DEĞERLENDİR")
        degerlendir_btn.setObjectName("PrimaryButon")
        degerlendir_btn.setFixedHeight(42)
        degerlendir_btn.setCursor(Qt.PointingHandCursor)
        degerlendir_btn.clicked.connect(self._degerlendir)
        self.icerik_layout.addWidget(degerlendir_btn)

        self.icerik_layout.addStretch()

    def _degerlendir(self):
        from frontend.widgets.diyaloglar import DegerlendirmeDiyalog
        dlg = DegerlendirmeDiyalog(self.vy, self.tarif_id, parent=self)
        if dlg.exec_():
            self._icerik_olustur()
            self.veri_degisti.emit()

    def _duzenle(self):
        from frontend.widgets.diyaloglar import TarifDiyalog
        dlg = TarifDiyalog(self.vy, tarif_id=self.tarif_id, parent=self)
        if dlg.exec_():
            self._icerik_olustur()
            self.veri_degisti.emit()

    def _sil(self):
        from PyQt5.QtWidgets import QMessageBox
        cevap = QMessageBox.question(
            self, "Tarif Sil",
            "Bu tarifi silmek istediğinize emin misiniz?\nİlgili değerlendirmeler de silinecektir.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            self.vy.tarif_sil(self.tarif_id)
            self.veri_degisti.emit()
            self.geri_istendi.emit()

    def yenile(self):
        if self.tarif_id:
            self._icerik_olustur()
