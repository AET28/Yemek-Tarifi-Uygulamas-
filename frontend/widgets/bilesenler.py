"""
Mutfak Defteri widget'ları — sıcak mutfak teması.
Koyu zeytin sidebar, terrakotta aksan, krem kağıt.
+ YildizGoster, MalzemeListesi, PuanRozet
"""
import math
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF, QPointF, QSize
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QFont,
    QPainterPath,
    QFontMetrics,
)


# ── Renk paleti (sıcak mutfak) ──
INK = QColor("#2c2420")
INK_DIM = QColor("#4a3f38")
INK_MUTED = QColor("#7d7369")
INK_SUBTLE = QColor("#a89e94")
INK_FAINT = QColor("#d1c9c0")
PAPER = QColor("#faf6f1")
PAPER_OFF = QColor("#f3ece3")
PAPER_PANEL = QColor("#fffdf9")
RULE_THIN = QColor("#d1c9c0")
RULE_HAIR = QColor("#e6ded5")
TERRA = QColor("#c4623a")        # terrakotta aksan
TERRA_DARK = QColor("#9e4a28")
OLIVE = QColor("#2b3a2e")        # sidebar koyu
OLIVE_MID = QColor("#3d5240")
OLIVE_LIGHT = QColor("#5a7247")
OLIVE_TEXT = QColor("#b8c7ad")   # sidebar soluk metin
OLIVE_LINE = QColor("#4a6348")


# ============================================================
# METRİK KART
# ============================================================
class MetrikKart(QFrame):
    def __init__(self, etiket: str, deger: str = "0", altyazi: str = "",
                 accent: bool = False, parent=None):
        super().__init__(parent)
        renk = "#c4623a" if accent else "#5a7247"
        self.setStyleSheet(
            "QFrame { background-color: #fffdf9; "
            "border: 1px solid #e6ded5; "
            f"border-top: 3px solid {renk}; "
            "border-radius: 6px; }"
        )
        self.setFixedHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        et = QLabel(etiket.upper())
        et.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        layout.addWidget(et)
        layout.addStretch()

        self.deger_lbl = QLabel(str(deger))
        font = QFont("Merriweather", 36, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 36, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1)
        self.deger_lbl.setFont(font)
        self.deger_lbl.setStyleSheet(
            "color: #2c2420; "
            "font-family: 'Merriweather', 'Georgia', serif; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.deger_lbl)

        self.alt_lbl = QLabel(altyazi)
        self.alt_lbl.setStyleSheet(
            "color: #7d7369; font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            "font-size: 11px; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.alt_lbl)

    def deger_ayarla(self, deger):
        deger_str = str(deger)
        n = len(deger_str)
        if n <= 3:
            size = 36
        elif n == 4:
            size = 30
        else:
            size = 26
        font = QFont("Merriweather", size, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", size, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        self.deger_lbl.setFont(font)
        self.deger_lbl.setText(deger_str)

    def altyazi_ayarla(self, altyazi):
        self.alt_lbl.setText(altyazi)


# ============================================================
# MASTHEAD — Koyu sidebar logosu
# ============================================================
class Masthead(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(92)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Üst ince zeytin çizgisi
        p.setPen(QPen(OLIVE_LINE, 1))
        p.drawLine(22, 18, w - 22, 18)

        # Terrakotta küçük kare ikon (sol tarafta)
        p.setBrush(TERRA)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(22, 30, 8, 8), 2, 2)

        # Ana isim — krem renk serif
        p.setPen(QColor("#faf6f1"))
        font = QFont("Merriweather", 19, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Georgia", 19, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.5)
        p.setFont(font)
        p.drawText(QRectF(36, 24, w - 58, 28),
                   Qt.AlignLeft | Qt.AlignVCenter, "Mutfak Defteri")

        # Alt etiket — soluk zeytin
        p.setPen(OLIVE_TEXT)
        font = QFont("Nunito Sans", 8, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 8, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        p.drawText(QRectF(22, 58, w - 44, 14),
                   Qt.AlignLeft | Qt.AlignVCenter, "TARİF KOLEKSİYONU")

        # Alt ince çizgi
        p.setPen(QPen(OLIVE_LINE, 1))
        p.drawLine(22, h - 8, w - 22, h - 8)


# ============================================================
# SAYFA HEADER
# ============================================================
class EditorialHeader(QWidget):
    def __init__(self, kategori: str, baslik: str, altyazi: str,
                 sag_etiket: str = "", sag_meta: str = "",
                 parent=None):
        super().__init__(parent)
        self.kategori = kategori
        self.baslik = baslik
        self.altyazi = altyazi
        self.sag_etiket = sag_etiket
        self.sag_meta = sag_meta
        self.setMinimumHeight(170)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Üst zeytin çizgi
        p.setPen(QPen(OLIVE_LIGHT, 2))
        p.drawLine(0, 0, w, 0)

        # Kategori tag (terrakotta)
        p.setPen(TERRA)
        font = QFont("Nunito Sans", 9, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Segoe UI", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        kat_y = 30
        p.drawText(0, kat_y, self.kategori)

        # Sağ etiket
        if self.sag_etiket:
            p.setPen(INK_MUTED)
            fm = QFontMetrics(font)
            sag_x = w - fm.horizontalAdvance(self.sag_etiket)
            p.drawText(sag_x, kat_y, self.sag_etiket)

        # Büyük başlık
        p.setPen(INK)
        font = QFont("Merriweather", 38, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 38, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1)
        p.setFont(font)
        p.drawText(QRectF(0, 44, w, 56),
                   Qt.AlignLeft | Qt.AlignTop, self.baslik)

        # Altyazı
        p.setPen(INK_DIM)
        font = QFont("Merriweather", 13)
        if not font.exactMatch():
            font = QFont("Georgia", 13)
        font.setItalic(True)
        p.setFont(font)
        p.drawText(QRectF(0, 106, w, 24),
                   Qt.AlignLeft | Qt.AlignTop, self.altyazi)

        # Sağ meta
        if self.sag_meta:
            p.setPen(INK_MUTED)
            font = QFont("Nunito Sans", 10)
            if not font.exactMatch():
                font = QFont("Segoe UI", 10)
            p.setFont(font)
            fm = QFontMetrics(font)
            meta_x = w - fm.horizontalAdvance(self.sag_meta)
            p.drawText(meta_x, h - 16, self.sag_meta)

        # Alt çift çizgi (zeytin + terrakotta)
        p.setPen(QPen(OLIVE_LIGHT, 1))
        p.drawLine(0, h - 5, w, h - 5)
        p.setPen(QPen(TERRA, 2))
        p.drawLine(0, h - 1, 60, h - 1)


# ============================================================
# AVATAR — Yuvarlak dolgulu baş harf
# ============================================================
class MuhurAvatar(QWidget):
    """Dolgulu daire + baş harf avatarı."""

    PALETLER = [
        (QColor("#c4623a"), QColor("#fffdf9")),   # terra
        (QColor("#5a7247"), QColor("#fffdf9")),   # olive
        (QColor("#2b3a2e"), QColor("#fffdf9")),   # dark olive
        (QColor("#b8860b"), QColor("#fffdf9")),   # gold
        (QColor("#7d5a50"), QColor("#fffdf9")),   # warm brown
    ]

    def __init__(self, ad: str, boyut: int = 40, parent=None):
        super().__init__(parent)
        self.ad = ad.strip()
        self.bas_harf = self.ad[0].upper() if self.ad else "?"
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        idx = hash(self.ad) % len(self.PALETLER)
        bg, fg = self.PALETLER[idx]

        # Dolgulu daire
        p.setBrush(bg)
        p.setPen(Qt.NoPen)
        p.drawEllipse(1, 1, w - 2, h - 2)

        # Harf
        p.setPen(fg)
        font = QFont("Merriweather", int(w * 0.38), QFont.Bold)
        if not font.exactMatch():
            font = QFont("Georgia", int(w * 0.38), QFont.Bold)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.bas_harf)


# ============================================================
# KART
# ============================================================
class Kart(QFrame):
    def __init__(self, baslik: str = None, alt_baslik: str = None,
                 accent: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("Kart")
        self.accent = accent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(28, 24, 28, 24)
        self.layout.setSpacing(14)

        if baslik:
            ust = QHBoxLayout()
            ust.setContentsMargins(0, 0, 0, 0)
            ust.setSpacing(0)

            if accent:
                marker = QFrame()
                marker.setFixedSize(3, 28)
                marker.setStyleSheet("background-color: #c4623a; border: none;")
                ust.addWidget(marker, 0, Qt.AlignVCenter)
                ust.addSpacing(10)

            baslik_l = QVBoxLayout()
            baslik_l.setSpacing(2)
            baslik_l.setContentsMargins(0, 0, 0, 0)

            self.baslik_lbl = QLabel(baslik)
            self.baslik_lbl.setObjectName("KartBaslik")
            baslik_l.addWidget(self.baslik_lbl)

            if alt_baslik:
                self.alt_baslik_lbl = QLabel(alt_baslik)
                self.alt_baslik_lbl.setObjectName("KartAltBaslik")
                baslik_l.addWidget(self.alt_baslik_lbl)

            ust.addLayout(baslik_l)
            ust.addStretch()
            self.layout.addLayout(ust)

            ayrac = QFrame()
            ayrac.setObjectName("AyiriciInce")
            ayrac.setFixedHeight(1)
            ayrac.setStyleSheet("background-color: #e6ded5;")
            self.layout.addWidget(ayrac)


# ============================================================
# KATEGORİ BAR
# ============================================================
class KategoriBarYatay(QWidget):
    def __init__(self, dagilim: dict, parent=None):
        super().__init__(parent)
        self.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.setMinimumHeight(n * 42 + 10)

    def paintEvent(self, e):
        if not self.dagilim:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        sirali = sorted(self.dagilim.items(), key=lambda x: -x[1])
        max_v = max(v for _, v in sirali) if sirali else 1

        no_w = 36
        kat_w = 130
        sag_w = 50
        bar_x = no_w + kat_w + 6
        bar_w = w - bar_x - sag_w - 6

        satir_y = 4

        for i, (kategori, sayi) in enumerate(sirali):
            # Numara
            p.setPen(INK_FAINT)
            font = QFont("Merriweather", 16, QFont.Bold)
            if not font.exactMatch():
                font = QFont("Georgia", 16, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(0, satir_y, no_w, 34),
                       Qt.AlignLeft | Qt.AlignVCenter, f"{i + 1:02d}")

            # Kategori adı
            p.setPen(INK)
            font = QFont("Nunito Sans", 12, QFont.DemiBold)
            if not font.exactMatch():
                font = QFont("Segoe UI", 12, QFont.DemiBold)
            p.setFont(font)
            p.drawText(QRectF(no_w, satir_y, kat_w, 34),
                       Qt.AlignLeft | Qt.AlignVCenter, kategori)

            # Bar arka çizgi
            p.setPen(QPen(INK_FAINT, 1))
            p.drawLine(bar_x, satir_y + 24, bar_x + bar_w, satir_y + 24)

            # Bar dolu — ilk terra, diğerleri zeytin
            dolu_w = (sayi / max_v) * bar_w
            renk = TERRA if i == 0 else OLIVE_LIGHT
            p.setBrush(renk)
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(QRectF(bar_x, satir_y + 19, dolu_w, 10), 3, 3)

            # Sağ sayı
            p.setPen(INK)
            font = QFont("Merriweather", 14, QFont.Bold)
            if not font.exactMatch():
                font = QFont("Georgia", 14, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(bar_x + bar_w + 6, satir_y, sag_w, 34),
                       Qt.AlignRight | Qt.AlignVCenter, str(sayi))

            satir_y += 42


# ============================================================
# Yardımcı Sarmalayıcılar
# ============================================================
class Rozet(QLabel):
    STILLER = {
        "basari": (
            "background-color: #e5f0e7; color: #3d7a4a; "
            "border: 1px solid #3d7a4a;"
        ),
        "uyari": (
            "background-color: #fdf3d7; color: #b8860b; "
            "border: 1px solid #b8860b;"
        ),
        "tehlike": (
            "background-color: #b84233; color: #faf6f1; "
            "border: 1px solid #b84233;"
        ),
        "notr": (
            "background-color: transparent; color: #7d7369; "
            "border: 1px solid #d1c9c0;"
        ),
    }

    def __init__(self, metin: str, tip: str = "basari", parent=None):
        super().__init__(metin, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(28)
        self.setMinimumWidth(96)

        renk_stil = self.STILLER.get(tip, self.STILLER["notr"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 3px; "
            f"padding: 4px 12px; "
            f"font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            f"font-size: 9px; font-weight: 800; "
            f" }}"
        )


class HucreSarmalayici(QWidget):
    def __init__(self, icerik: QWidget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(0)
        layout.addWidget(icerik, 0, Qt.AlignVCenter)


class ButonGrubu(QWidget):
    def __init__(self, butonlar: list, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)
        for b in butonlar:
            layout.addWidget(b)
        layout.addStretch()


class Ayirici(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Ayirici")
        self.setFixedHeight(2)


class AyiriciInce(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AyiriciInce")
        self.setFixedHeight(1)


# ============================================================
# YILDIZ GÖSTER — terrakotta yıldızlar
# ============================================================
class YildizGoster(QWidget):
    def __init__(self, puan: float = 0.0, boyut: int = 16, parent=None):
        super().__init__(parent)
        self.puan = puan
        self.yildiz_boyut = boyut
        self.setFixedSize(boyut * 5 + 8, boyut + 4)

    def puan_ayarla(self, puan: float):
        self.puan = puan
        self.update()

    def _yildiz_yolu(self, cx: float, cy: float, r: float) -> QPainterPath:
        path = QPainterPath()
        for i in range(5):
            aci_dis = math.radians(-90 + i * 72)
            aci_ic = math.radians(-90 + i * 72 + 36)
            px_dis = cx + r * math.cos(aci_dis)
            py_dis = cy + r * math.sin(aci_dis)
            px_ic = cx + r * 0.4 * math.cos(aci_ic)
            py_ic = cy + r * 0.4 * math.sin(aci_ic)
            if i == 0:
                path.moveTo(px_dis, py_dis)
            else:
                path.lineTo(px_dis, py_dis)
            path.lineTo(px_ic, py_ic)
        path.closeSubpath()
        return path

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        b = self.yildiz_boyut
        r = b / 2 - 1

        for i in range(5):
            cx = b / 2 + i * (b + 2)
            cy = b / 2 + 2
            yol = self._yildiz_yolu(cx, cy, r)

            doluluk = max(0.0, min(1.0, self.puan - i))

            if doluluk >= 1.0:
                p.setBrush(TERRA)
                p.setPen(Qt.NoPen)
                p.drawPath(yol)
            elif doluluk > 0:
                p.setBrush(Qt.NoBrush)
                p.setPen(QPen(TERRA, 1))
                p.drawPath(yol)
                p.save()
                p.setClipRect(QRectF(cx - r, cy - r, 2 * r * doluluk, 2 * r))
                p.setBrush(TERRA)
                p.setPen(Qt.NoPen)
                p.drawPath(yol)
                p.restore()
            else:
                p.setBrush(Qt.NoBrush)
                p.setPen(QPen(INK_FAINT, 1))
                p.drawPath(yol)


# ============================================================
# MALZEME LİSTESİ
# ============================================================
class MalzemeListesi(QWidget):
    def __init__(self, malzemeler: list = None, parent=None):
        super().__init__(parent)
        self.malzemeler = malzemeler or []
        self._hesapla_yukseklik()

    def malzemeleri_ayarla(self, malzemeler: list):
        self.malzemeler = malzemeler
        self._hesapla_yukseklik()
        self.update()

    def _hesapla_yukseklik(self):
        n = len(self.malzemeler) if self.malzemeler else 1
        self.setMinimumHeight(n * 34 + 10)

    def paintEvent(self, e):
        if not self.malzemeler:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        y = 4
        for i, m in enumerate(self.malzemeler):
            # Numara
            p.setPen(TERRA)
            font = QFont("Merriweather", 12, QFont.Bold)
            if not font.exactMatch():
                font = QFont("Georgia", 12, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(0, y, 32, 28),
                       Qt.AlignRight | Qt.AlignVCenter, f"{i + 1:02d}")

            # Miktar (kalın)
            p.setPen(INK)
            font = QFont("Nunito Sans", 12, QFont.Bold)
            if not font.exactMatch():
                font = QFont("Segoe UI", 12, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(44, y, 140, 28),
                       Qt.AlignLeft | Qt.AlignVCenter, m.miktar)

            # Malzeme adı
            p.setPen(INK_DIM)
            font = QFont("Nunito Sans", 12)
            if not font.exactMatch():
                font = QFont("Segoe UI", 12)
            p.setFont(font)
            p.drawText(QRectF(190, y, w - 200, 28),
                       Qt.AlignLeft | Qt.AlignVCenter, m.malzeme_adi)

            # Alt noktalı çizgi
            p.setPen(QPen(RULE_HAIR, 1, Qt.DotLine))
            p.drawLine(44, y + 32, w, y + 32)

            y += 34


# ============================================================
# PUAN ROZET
# ============================================================
class PuanRozet(QLabel):
    def __init__(self, puan: float, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(28)
        self.setMinimumWidth(96)
        self.puan_ayarla(puan)

    def puan_ayarla(self, puan: float):
        if puan >= 4.5:
            metin = "MÜKEMMEL"
            renk_stil = "background-color: #e5f0e7; color: #3d7a4a; border: 1px solid #3d7a4a;"
        elif puan >= 3.5:
            metin = "İYİ"
            renk_stil = "background-color: #fdf3d7; color: #b8860b; border: 1px solid #b8860b;"
        elif puan > 0:
            metin = "ORTA"
            renk_stil = "background-color: transparent; color: #7d7369; border: 1px solid #d1c9c0;"
        else:
            metin = "DEĞERLENDİRİLMEDİ"
            renk_stil = "background-color: transparent; color: #a89e94; border: 1px solid #e6ded5;"

        self.setText(metin)
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 3px; padding: 4px 12px; "
            f"font-family: 'Nunito Sans', 'Segoe UI', sans-serif; "
            f"font-size: 9px; font-weight: 800; "
            f" }}"
        )
