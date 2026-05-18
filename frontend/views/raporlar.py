"""Raporlar — kategori dağılımı, top 5 tarifler, top 5 kullanıcılar, CSV export."""
import csv
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog,
)
from PyQt5.QtCore import Qt

from backend.veri_yoneticisi import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader, Kart, KategoriBarYatay, YildizGoster,
    MuhurAvatar, Rozet,
)


class RaporlarSayfasi(QWidget):
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

        header = EditorialHeader(
            kategori="ANALİZ",
            baslik="Raporlar",
            altyazi="Platform istatistikleri ve sıralamalar.",
            sag_etiket="MUTFAK DEFTERİ",
        )
        self.icerik_layout.addWidget(header)

        # CSV Export
        export_satir = QHBoxLayout()
        export_satir.addStretch()
        self.export_btn = QPushButton("CSV EXPORT")
        self.export_btn.setObjectName("IkincilButon")
        self.export_btn.setFixedHeight(38)
        self.export_btn.setMinimumWidth(140)
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self._csv_export)
        export_satir.addWidget(self.export_btn)
        self.icerik_layout.addLayout(export_satir)

        # İki kolon
        kolonlar = QHBoxLayout()
        kolonlar.setSpacing(24)

        # Sol: Kategori dağılımı
        sol = QVBoxLayout()
        sol.setSpacing(16)

        kat_baslik = QLabel("KATEGORİ DAĞILIMI")
        kat_baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        sol.addWidget(kat_baslik)

        self.kategori_bar = KategoriBarYatay({})
        sol.addWidget(self.kategori_bar)
        sol.addStretch()

        kolonlar.addLayout(sol, 1)

        # Sağ: Top 5 listeler
        sag = QVBoxLayout()
        sag.setSpacing(16)

        # En yüksek puanlı
        top_baslik = QLabel("EN YÜKSEK PUANLI TARİFLER")
        top_baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        sag.addWidget(top_baslik)

        self.top_tablo = QTableWidget()
        self.top_tablo.setColumnCount(3)
        self.top_tablo.setHorizontalHeaderLabels(["SIRA", "TARİF", "PUAN"])
        self.top_tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.top_tablo.setColumnWidth(0, 50)
        self.top_tablo.setColumnWidth(2, 80)
        self.top_tablo.verticalHeader().setVisible(False)
        self.top_tablo.setSelectionMode(QTableWidget.NoSelection)
        self.top_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.top_tablo.setMaximumHeight(240)
        sag.addWidget(self.top_tablo)

        # En aktif kullanıcılar
        aktif_baslik = QLabel("EN AKTİF KULLANICILAR")
        aktif_baslik.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        sag.addWidget(aktif_baslik)

        self.aktif_tablo = QTableWidget()
        self.aktif_tablo.setColumnCount(3)
        self.aktif_tablo.setHorizontalHeaderLabels(["SIRA", "KULLANICI", "DEĞERLENDİRME"])
        self.aktif_tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.aktif_tablo.setColumnWidth(0, 50)
        self.aktif_tablo.setColumnWidth(2, 120)
        self.aktif_tablo.verticalHeader().setVisible(False)
        self.aktif_tablo.setSelectionMode(QTableWidget.NoSelection)
        self.aktif_tablo.setEditTriggers(QTableWidget.NoEditTriggers)
        self.aktif_tablo.setMaximumHeight(240)
        sag.addWidget(self.aktif_tablo)

        sag.addStretch()

        kolonlar.addLayout(sag, 1)

        self.icerik_layout.addLayout(kolonlar)
        self.icerik_layout.addStretch()

        scroll.setWidget(icerik)
        ana.addWidget(scroll)

    def yenile(self):
        # Kategori dağılımı
        dagilim = self.vy.kategori_dagilimi()
        self.kategori_bar.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.kategori_bar.setMinimumHeight(n * 40 + 10)
        self.kategori_bar.update()

        # Top 5 tarifler
        top5 = self.vy.en_yuksek_puanli_tarifler(5)
        self.top_tablo.setRowCount(len(top5))
        for i, (tarif, ort) in enumerate(top5):
            self.top_tablo.setRowHeight(i, 40)
            sira = QTableWidgetItem(f"{i + 1}")
            sira.setTextAlignment(Qt.AlignCenter)
            self.top_tablo.setItem(i, 0, sira)
            self.top_tablo.setItem(i, 1, QTableWidgetItem(tarif.tarif_adi))
            puan = QTableWidgetItem(f"{ort:.1f}")
            puan.setTextAlignment(Qt.AlignCenter)
            self.top_tablo.setItem(i, 2, puan)

        # En aktif kullanıcılar
        aktif5 = self.vy.en_aktif_kullanicilar(5)
        self.aktif_tablo.setRowCount(len(aktif5))
        for i, (kul, sayi) in enumerate(aktif5):
            self.aktif_tablo.setRowHeight(i, 40)
            sira = QTableWidgetItem(f"{i + 1}")
            sira.setTextAlignment(Qt.AlignCenter)
            self.aktif_tablo.setItem(i, 0, sira)
            self.aktif_tablo.setItem(i, 1, QTableWidgetItem(kul.ad))
            deg = QTableWidgetItem(str(sayi))
            deg.setTextAlignment(Qt.AlignCenter)
            self.aktif_tablo.setItem(i, 2, deg)

    def _csv_export(self):
        dosya, _ = QFileDialog.getSaveFileName(
            self, "CSV Kaydet", "tarifler_rapor.csv",
            "CSV Dosyası (*.csv)",
        )
        if not dosya:
            return

        with open(dosya, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Tarif ID", "Tarif Adı", "Kategori", "Hazırlama Süresi (dk)",
                "Malzeme Sayısı", "Yazar", "Ortalama Puan", "Değerlendirme Sayısı",
            ])
            for t in self.vy.tarifler:
                ort = self.vy.tarif_ortalama_puan(t.tarif_id)
                deg_sayi = self.vy.tarif_degerlendirme_sayisi(t.tarif_id)
                yazar = self.vy.kullanici_adi(t.yazar_id)
                writer.writerow([
                    t.tarif_id, t.tarif_adi, t.kategori,
                    t.hazirlama_suresi, len(t.malzemeler),
                    yazar, f"{ort:.1f}", deg_sayi,
                ])

        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export", f"CSV dosyası kaydedildi:\n{dosya}")
