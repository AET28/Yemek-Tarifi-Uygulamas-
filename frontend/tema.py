"""
Mutfak Defteri Tema — Sıcak mutfak paleti.
Koyu zeytin sidebar, terrakotta aksan, krem kağıt.
"""

RENKLER = {
    # Krem katmanlar
    "paper": "#faf6f1",           # ana arkaplan (sıcak krem)
    "paper_off": "#f3ece3",       # alternatif yüzey, hover
    "paper_panel": "#fffdf9",     # kart beyazı
    "paper_inset": "#efe8df",     # input arkaplanı

    # Koyu metin (kahve siyahı)
    "ink": "#2c2420",
    "ink_dim": "#4a3f38",
    "ink_muted": "#7d7369",
    "ink_subtle": "#a89e94",
    "ink_faint": "#d1c9c0",

    # Çizgiler (sıcak)
    "rule": "#2c2420",
    "rule_thin": "#d1c9c0",
    "rule_hairline": "#e6ded5",

    # Accent — terrakotta
    "terra": "#c4623a",           # ana aksan (terrakotta turuncu)
    "terra_dark": "#9e4a28",
    "terra_pale": "#fce9de",

    # Zeytin yeşili (sidebar + ikincil aksan)
    "olive": "#2b3a2e",           # koyu sidebar
    "olive_mid": "#3d5240",       # hover
    "olive_light": "#5a7247",     # vurgular
    "olive_text": "#b8c7ad",      # sidebar soluk metin
    "olive_line": "#3d5240",      # sidebar ayraçlar

    # Durum
    "success": "#3d7a4a",
    "success_pale": "#e5f0e7",
    "warning": "#b8860b",
    "warning_pale": "#fdf3d7",
    "danger": "#b84233",
    "danger_pale": "#fce4e0",

    # Tablo
    "table_header_bg": "#2b3a2e",
    "table_header_text": "#faf6f1",
    "table_zebra": "#f7f1ea",
    "table_row_hover": "#f0e8de",
}


ANA_STIL = f"""
/* GENEL ============================================================ */
QWidget {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    font-family: "Nunito Sans", "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {RENKLER['paper']};
}}

QToolTip {{
    background-color: {RENKLER['olive']};
    color: {RENKLER['paper']};
    border: none;
    padding: 7px 12px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
}}

/* SIDEBAR — koyu zeytin yeşili ====================================== */
#Sidebar {{
    background-color: {RENKLER['olive']};
    border-right: none;
}}

#MastheadBaslik {{
    color: {RENKLER['paper']};
    background: transparent;
    border: none;
    font-family: "Merriweather", "Georgia", serif;
    font-weight: 900;
    font-size: 22px;
}}

#MastheadAlt {{
    color: {RENKLER['olive_text']};
    background: transparent;
    border: none;
    font-family: "Nunito Sans", sans-serif;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
}}

#MenuBaslik {{
    color: {RENKLER['olive_text']};
    font-family: "Nunito Sans", sans-serif;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    background: transparent;
    border: none;
}}

QPushButton#MenuButon {{
    background-color: transparent;
    color: {RENKLER['olive_text']};
    text-align: left;
    padding-left: 24px;
    padding-right: 24px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0;
    font-family: "Nunito Sans", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#MenuButon:hover {{
    background-color: {RENKLER['olive_mid']};
    color: {RENKLER['paper']};
}}

QPushButton#MenuButon:checked {{
    background-color: rgba(255,255,255,0.06);
    color: {RENKLER['paper']};
    font-weight: 700;
    border-left: 3px solid {RENKLER['terra']};
}}

#KullaniciKart {{
    background-color: {RENKLER['olive_mid']};
    border: 1px solid {RENKLER['olive_line']};
    border-radius: 4px;
}}

#KullaniciKart QLabel {{
    background: transparent;
    border: none;
}}

#KullaniciAd {{
    color: {RENKLER['paper']};
    font-weight: 700;
    font-size: 12px;
    font-family: "Nunito Sans", sans-serif;
}}

#KullaniciDurum {{
    color: {RENKLER['olive_text']};
    font-size: 10px;
    font-family: "Nunito Sans", sans-serif;
    text-transform: uppercase;
    font-weight: 600;
}}

#PlanRozet {{
    background-color: {RENKLER['terra']};
    color: {RENKLER['paper']};
    border: none;
    border-radius: 3px;
    padding: 3px 9px;
    font-size: 9px;
    font-weight: 800;
    font-family: "Nunito Sans", sans-serif;
    min-width: 50px;
}}

/* SAYFA BAŞLIKLARI ================================================ */
#SayfaBaslik {{
    color: {RENKLER['ink']};
    background: transparent;
    border: none;
    font-family: "Merriweather", "Georgia", serif;
    font-size: 38px;
    font-weight: 900;
}}

#SayfaAltBaslik {{
    color: {RENKLER['ink_muted']};
    background: transparent;
    border: none;
    font-family: "Nunito Sans", sans-serif;
    font-size: 13px;
    font-weight: 400;
    font-style: italic;
}}

#KicekerBaslik {{
    color: {RENKLER['terra']};
    background: transparent;
    border: none;
    font-family: "Nunito Sans", sans-serif;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
}}

#PullQuote {{
    color: {RENKLER['ink']};
    background: transparent;
    border: none;
    border-left: 3px solid {RENKLER['terra']};
    padding-left: 16px;
    font-family: "Merriweather", "Georgia", serif;
    font-size: 16px;
    font-weight: 500;
    font-style: italic;
}}

/* KARTLAR ========================================================= */
#Kart {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_hairline']};
    border-radius: 6px;
}}

#Kart QLabel {{
    background: transparent;
    border: none;
}}

#KartBaslik {{
    color: {RENKLER['ink']};
    font-family: "Merriweather", "Georgia", serif;
    font-size: 18px;
    font-weight: 800;
    background: transparent;
    border: none;
}}

#KartAltBaslik {{
    color: {RENKLER['ink_muted']};
    font-family: "Nunito Sans", sans-serif;
    font-size: 12px;
    background: transparent;
    border: none;
    font-style: italic;
}}

/* BUTONLAR ======================================================== */
QPushButton {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['rule_thin']};
    padding: 6px 16px;
    border-radius: 4px;
    font-family: "Nunito Sans", sans-serif;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    min-width: 80px;
    min-height: 28px;
}}

QPushButton:hover {{
    background-color: {RENKLER['paper']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton:disabled {{
    background-color: {RENKLER['paper_inset']};
    color: {RENKLER['ink_faint']};
    border: 1px solid {RENKLER['rule_hairline']};
}}

QPushButton#PrimaryButon {{
    background-color: {RENKLER['terra']};
    background: {RENKLER['terra']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['terra']};
}}

QPushButton#PrimaryButon:hover {{
    background-color: {RENKLER['terra_dark']};
    background: {RENKLER['terra_dark']};
    border: 1px solid {RENKLER['terra_dark']};
}}

QPushButton#BasariButon {{
    background-color: {RENKLER['olive_light']};
    background: {RENKLER['olive_light']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['olive_light']};
}}

QPushButton#BasariButon:hover {{
    background-color: {RENKLER['olive']};
    background: {RENKLER['olive']};
    border: 1px solid {RENKLER['olive']};
}}

QPushButton#IkincilButon {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton#IkincilButon:hover {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
}}

QPushButton#HayaletButon {{
    background-color: transparent;
    color: {RENKLER['ink_dim']};
    border: 1px solid {RENKLER['rule_thin']};
}}

QPushButton#HayaletButon:hover {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton#TehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['rule_thin']};
}}

QPushButton#TehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['danger']};
}}

QPushButton#KucukIkincilButon {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['ink']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 700;
}}

QPushButton#KucukIkincilButon:hover {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
}}

QPushButton#KucukTehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['rule_thin']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 700;
}}

QPushButton#KucukTehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['danger']};
}}

/* FORM ALANLARI =================================================== */
QLineEdit, QSpinBox, QDateTimeEdit, QComboBox, QTextEdit {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-bottom: 2px solid {RENKLER['rule_thin']};
    border-radius: 4px;
    padding-left: 12px;
    padding-right: 12px;
    color: {RENKLER['ink']};
    selection-background-color: {RENKLER['terra']};
    selection-color: {RENKLER['paper']};
    font-family: "Nunito Sans", sans-serif;
    font-size: 13px;
}}

QLineEdit:focus, QSpinBox:focus, QDateTimeEdit:focus,
QComboBox:focus, QTextEdit:focus {{
    border: 1px solid {RENKLER['terra']};
    border-bottom: 2px solid {RENKLER['terra']};
    background-color: {RENKLER['paper']};
}}

QLineEdit:hover, QSpinBox:hover, QDateTimeEdit:hover,
QComboBox:hover, QTextEdit:hover {{
    border-bottom: 2px solid {RENKLER['terra']};
}}

#AramaInput {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-bottom: 2px solid {RENKLER['ink']};
    padding-left: 16px;
    padding-right: 16px;
    border-radius: 4px;
    font-family: "Nunito Sans", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

#AramaInput:focus {{
    border: 1px solid {RENKLER['terra']};
    border-bottom: 2px solid {RENKLER['terra']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDateTimeEdit::up-button, QDateTimeEdit::down-button {{
    background-color: transparent;
    border: none;
    width: 16px;
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['ink']};
    margin-right: 12px;
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-radius: 4px;
    selection-background-color: {RENKLER['terra']};
    selection-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    padding: 4px;
    outline: 0;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 10px;
    border-radius: 3px;
    min-height: 22px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {RENKLER['paper_off']};
}}

QLabel#FormEtiket {{
    color: {RENKLER['ink_dim']};
    font-family: "Nunito Sans", sans-serif;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    background: transparent;
    border: none;
}}

/* TABLOLAR ======================================================== */
QTableWidget {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_hairline']};
    border-top: 3px solid {RENKLER['olive']};
    border-radius: 0;
    gridline-color: transparent;
    color: {RENKLER['ink']};
    selection-background-color: transparent;
    outline: 0;
    alternate-background-color: {RENKLER['table_zebra']};
}}

QTableWidget::item {{
    padding-left: 8px;
    padding-right: 8px;
    border: none;
    border-bottom: 1px solid {RENKLER['rule_hairline']};
    background-color: transparent;
    color: {RENKLER['ink']};
}}

QTableWidget::item:selected {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
}}

QTableWidget::item:hover {{
    background-color: {RENKLER['table_row_hover']};
}}

QHeaderView::section {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink_muted']};
    padding-top: 14px;
    padding-bottom: 14px;
    padding-left: 14px;
    padding-right: 14px;
    border: none;
    border-bottom: 1px solid {RENKLER['olive_light']};
    font-family: "Nunito Sans", sans-serif;
    font-weight: 800;
    font-size: 9px;
    text-transform: uppercase;
}}

QHeaderView::section:first {{
    border-top-left-radius: 0;
}}

QHeaderView::section:last {{
    border-top-right-radius: 0;
}}

QTableCornerButton::section {{
    background-color: {RENKLER['paper']};
    border: none;
}}

/* SCROLLBAR ======================================================= */
QScrollBar:vertical {{
    background: transparent;
    width: 7px;
    border: none;
    margin: 4px 2px 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {RENKLER['ink_faint']};
    border-radius: 3px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {RENKLER['terra']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 7px;
    border: none;
    margin: 2px 4px 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {RENKLER['ink_faint']};
    border-radius: 3px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {RENKLER['terra']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* DİYALOG ========================================================= */
QDialog {{
    background-color: {RENKLER['paper']};
}}

QMessageBox {{
    background-color: {RENKLER['paper_panel']};
}}

QMessageBox QLabel {{
    color: {RENKLER['ink']};
    font-family: "Nunito Sans", sans-serif;
    font-size: 13px;
    background: transparent;
    border: none;
}}

QMessageBox QPushButton {{
    min-width: 90px;
}}

/* ROZETLER ======================================================== */
QLabel#RozetBasari {{
    background-color: {RENKLER['success_pale']};
    color: {RENKLER['success']};
    border: 1px solid {RENKLER['success']};
    border-radius: 3px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Nunito Sans", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
}}

QLabel#RozetUyari {{
    background-color: {RENKLER['warning_pale']};
    color: {RENKLER['warning']};
    border: 1px solid {RENKLER['warning']};
    border-radius: 3px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Nunito Sans", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
}}

QLabel#RozetTehlike {{
    background-color: {RENKLER['danger']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['danger']};
    border-radius: 3px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Nunito Sans", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
}}

QLabel#RozetNotr {{
    background-color: transparent;
    color: {RENKLER['ink_muted']};
    border: 1px solid {RENKLER['rule_thin']};
    border-radius: 3px;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Nunito Sans", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
}}

/* DİĞER =========================================================== */
QFrame#Ayirici {{
    background-color: {RENKLER['olive_light']};
    max-height: 2px;
    min-height: 2px;
    border: none;
}}

QFrame#AyiriciInce {{
    background-color: {RENKLER['rule_hairline']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}
"""
