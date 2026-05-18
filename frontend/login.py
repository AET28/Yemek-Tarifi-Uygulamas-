"""Login Penceresi - Mutfak Defteri — sıcak mutfak teması."""
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics

from backend.auth import AuthYoneticisi, Kullanici

# Tema renkleri
INK = QColor("#2c2420")
INK_DIM = QColor("#4a3f38")
INK_MUTED = QColor("#7d7369")
PAPER = QColor("#faf6f1")
PAPER_OFF = QColor("#f3ece3")
RULE_THIN = QColor("#d1c9c0")
RULE_HAIR = QColor("#e6ded5")
TERRA = QColor("#c4623a")
OLIVE = QColor("#2b3a2e")
OLIVE_LIGHT = QColor("#5a7247")
OLIVE_TEXT = QColor("#b8c7ad")


class _MutfakSolPanel(QWidget):
    """Login sol panel — koyu zeytin arka plan, sıcak tipografi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(560)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        w = rect.width()
        h = rect.height()

        # Koyu zeytin arka plan
        p.fillRect(rect, OLIVE)

        margin = 48

        # Üst ince çizgi
        p.setPen(QPen(QColor("#4a6348"), 1))
        p.drawLine(margin, 56, w - margin, 56)

        # Alt etiket
        p.setPen(OLIVE_TEXT)
        font = QFont("Nunito Sans", 9, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        p.drawText(QRectF(margin, 64, w - margin * 2, 18),
                   Qt.AlignLeft | Qt.AlignVCenter, "TARİF KOLEKSİYONU")

        # Büyük başlık (krem)
        p.setPen(PAPER)
        font = QFont("Merriweather", 44, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 44, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.5)
        p.setFont(font)
        p.drawText(QRectF(margin, 86, w - margin * 2, 70),
                   Qt.AlignLeft | Qt.AlignVCenter, "Mutfak Defteri")

        # Terrakotta çizgi
        p.setPen(QPen(TERRA, 2))
        p.drawLine(margin, 168, margin + 80, 168)
        p.setPen(QPen(QColor("#4a6348"), 1))
        p.drawLine(margin + 80, 168, w - margin, 168)

        # Slogan (italic)
        p.setPen(OLIVE_TEXT)
        font = QFont("Merriweather", 17)
        if not font.exactMatch():
            font = QFont("Georgia", 17)
        font.setItalic(True)
        p.setFont(font)
        slogan_y = 220
        p.drawText(QRectF(margin, slogan_y, w - margin * 2, 30),
                   Qt.AlignLeft, "Tarifini paylaş,")
        p.drawText(QRectF(margin, slogan_y + 32, w - margin * 2, 30),
                   Qt.AlignLeft, "lezzeti çoğalt.")

        # Özellik listesi
        ozellik_y = 320
        ozellikler = [
            "Yemek tarifi koleksiyonu",
            "Malzeme listesi yönetimi",
            "Tarif değerlendirme ve puanlama",
            "Detaylı raporlar ve analiz",
        ]

        for i, oz in enumerate(ozellikler):
            y = ozellik_y + i * 38

            # Terrakotta yuvarlak bullet
            p.setBrush(TERRA)
            p.setPen(Qt.NoPen)
            p.drawEllipse(QRectF(margin, y - 7, 7, 7))

            # Metin (krem)
            p.setPen(PAPER)
            font = QFont("Nunito Sans", 12)
            if not font.exactMatch():
                font = QFont("Segoe UI", 12)
            font.setWeight(QFont.Medium)
            p.setFont(font)
            p.drawText(margin + 20, y, oz)

        # Footer
        p.setPen(QPen(QColor("#4a6348"), 1))
        p.drawLine(margin, h - 48, w - margin, h - 48)

        p.setPen(OLIVE_TEXT)
        font = QFont("Nunito Sans", 9)
        if not font.exactMatch():
            font = QFont("Segoe UI", 9)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "© 2026 Mutfak Defteri")
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignRight | Qt.AlignVCenter, "v1.0")


class LoginPenceresi(QDialog):
    def __init__(self, auth: AuthYoneticisi, parent=None):
        super().__init__(parent)
        self.auth = auth
        self.dogrulanan_kullanici: Kullanici | None = None

        self.setWindowTitle("Mutfak Defteri — Giriş")
        self.setFixedSize(1080, 680)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        ana.addWidget(_MutfakSolPanel())

        sag = QFrame()
        sag.setStyleSheet("background-color: #faf6f1;")
        sag_layout = QVBoxLayout(sag)
        sag_layout.setContentsMargins(56, 64, 56, 48)
        sag_layout.setSpacing(0)

        kat = QLabel("GİRİŞ")
        kat.setStyleSheet(
            "color: #c4623a; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            " "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(kat)
        sag_layout.addSpacing(14)

        baslik = QLabel("Hoş Geldin")
        baslik.setStyleSheet(
            "color: #2c2420; font-family: 'Merriweather', 'Georgia', serif; "
            "font-size: 42px; font-weight: 900; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(baslik)

        alt = QLabel("Devam etmek için hesabına giriş yap.")
        alt.setStyleSheet(
            "color: #7d7369; font-family: 'Merriweather', 'Georgia', serif; "
            "font-size: 14px; font-style: italic; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(alt)
        sag_layout.addSpacing(12)

        ayrac = QFrame()
        ayrac.setFixedHeight(2)
        ayrac.setStyleSheet("background-color: #5a7247;")
        sag_layout.addWidget(ayrac)
        sag_layout.addSpacing(28)

        sag_layout.addWidget(self._etiket("KULLANICI ADI"))
        sag_layout.addSpacing(8)

        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("kullanıcı adınızı girin")
        self.kul_input.setFixedHeight(46)
        self.kul_input.setStyleSheet(self._input_stil())
        self.kul_input.returnPressed.connect(lambda: self.sifre_input.setFocus())
        sag_layout.addWidget(self.kul_input)
        sag_layout.addSpacing(20)

        sag_layout.addWidget(self._etiket("ŞİFRE"))
        sag_layout.addSpacing(8)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("••••••••")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setFixedHeight(46)
        self.sifre_input.setStyleSheet(self._input_stil())
        self.sifre_input.returnPressed.connect(self._giris_yap)
        sag_layout.addWidget(self.sifre_input)
        sag_layout.addSpacing(14)

        self.goster_chk = QCheckBox("Şifreyi göster")
        self.goster_chk.setStyleSheet(
            "QCheckBox { color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; font-weight: 600; "
            "background: transparent; border: none; spacing: 8px; }"
            "QCheckBox::indicator { width: 14px; height: 14px; "
            "border: 1px solid #2c2420; border-radius: 3px; "
            "background-color: #faf6f1; }"
            "QCheckBox::indicator:checked { background-color: #5a7247; "
            "border: 1px solid #5a7247; }"
        )
        self.goster_chk.toggled.connect(self._sifre_goster)
        sag_layout.addWidget(self.goster_chk)
        sag_layout.addSpacing(24)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fce4e0; color: #b84233; "
            "border: 1px solid #b84233; border-radius: 4px; "
            "padding: 12px 16px; "
            "font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 12px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        sag_layout.addWidget(self.hata_lbl)

        self.giris_btn = QPushButton("OTURUM AÇ")
        self.giris_btn.setFixedHeight(50)
        self.giris_btn.setCursor(Qt.PointingHandCursor)
        self.giris_btn.setStyleSheet(
            "QPushButton { background-color: #c4623a; color: #faf6f1; "
            "border: 1px solid #c4623a; border-radius: 4px; "
            "font-family: 'Nunito Sans', 'Segoe UI', sans-serif; font-size: 12px; "
            "font-weight: 800; } "
            "QPushButton:hover { background-color: #9e4a28; "
            "border: 1px solid #9e4a28; }"
        )
        self.giris_btn.clicked.connect(self._giris_yap)
        sag_layout.addWidget(self.giris_btn)
        sag_layout.addSpacing(20)

        hr = QFrame()
        hr.setFixedHeight(1)
        hr.setStyleSheet("background-color: #d1c9c0;")
        sag_layout.addWidget(hr)
        sag_layout.addSpacing(16)

        ipucu = QLabel(
            "<span style=\"color:#7d7369; font-family:'Nunito Sans','Segoe UI',sans-serif; font-size:11px; font-weight:700;\">VARSAYILAN ERİŞİM</span><br><br>"
            "<span style=\"color:#2c2420; font-family:'Nunito Sans','Segoe UI',sans-serif; font-size:13px; font-weight:600;\">"
            "admin <span style='color:#c4623a;'>·</span> admin123</span>"
        )
        ipucu.setStyleSheet(
            "background-color: #f3ece3; "
            "border-left: 3px solid #c4623a; "
            "padding: 14px 18px; border-radius: 4px;"
        )
        sag_layout.addWidget(ipucu)
        sag_layout.addStretch()

        footer = QLabel("© 2026 Mutfak Defteri")
        footer.setStyleSheet(
            "color: #a89e94; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; "
            "background: transparent; border: none;"
        )
        footer.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(footer)

        ana.addWidget(sag, 1)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #4a3f38; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        return lbl

    def _input_stil(self) -> str:
        return (
            "QLineEdit { background-color: #fffdf9; "
            "border: 1px solid #d1c9c0; border-bottom: 2px solid #d1c9c0; "
            "border-radius: 4px; padding: 0 14px; "
            "color: #2c2420; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; font-size: 14px; "
            "selection-background-color: #c4623a; selection-color: #faf6f1; } "
            "QLineEdit:focus { border: 1px solid #c4623a; "
            "border-bottom: 2px solid #c4623a; background-color: #faf6f1; } "
            "QLineEdit:hover { border-bottom: 2px solid #c4623a; }"
        )

    def _sifre_goster(self, checked: bool):
        self.sifre_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )

    def _hata_goster(self, mesaj: str):
        self.hata_lbl.setText(f"  {mesaj.upper()}")
        self.hata_lbl.setVisible(True)

    def _hata_gizle(self):
        self.hata_lbl.setVisible(False)

    def _giris_yap(self):
        kul = self.kul_input.text().strip()
        sifre = self.sifre_input.text()

        if not kul:
            self._hata_goster("Kullanıcı adı boş olamaz.")
            self.kul_input.setFocus()
            return
        if not sifre:
            self._hata_goster("Şifre boş olamaz.")
            self.sifre_input.setFocus()
            return

        kullanici = self.auth.dogrula(kul, sifre)
        if kullanici is None:
            self._hata_goster("Kullanıcı adı veya şifre hatalı.")
            self.sifre_input.clear()
            self.sifre_input.setFocus()
            return

        self.dogrulanan_kullanici = kullanici
        self.accept()
