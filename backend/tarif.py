"""Tarif sınıfı — malzeme listesi composition ile tutulur."""
from datetime import datetime
from backend.malzeme import Malzeme


class Tarif:
    def __init__(
        self,
        tarif_id: int,
        tarif_adi: str,
        kategori: str,
        hazirlama_suresi: int,
        malzemeler: list = None,
        aciklama: str = "",
        yazar_id: int = 0,
        eklenme_tarihi: str = None,
    ):
        self.tarif_id = tarif_id
        self.tarif_adi = tarif_adi.strip()
        self.kategori = kategori
        self.hazirlama_suresi = hazirlama_suresi
        self.malzemeler: list[Malzeme] = malzemeler or []
        self.aciklama = aciklama
        self.yazar_id = yazar_id
        self.eklenme_tarihi = eklenme_tarihi or datetime.now().isoformat()

    # --- Malzeme işlemleri ---

    def malzeme_ekle(self, malzeme: Malzeme):
        self.malzemeler.append(malzeme)

    def malzeme_sil(self, malzeme_adi: str):
        self.malzemeler = [
            m for m in self.malzemeler
            if m.malzeme_adi.lower() != malzeme_adi.lower()
        ]

    # --- Puan ---

    def ortalama_puan(self, degerlendirmeler: list) -> float:
        ilgili = [d for d in degerlendirmeler if d.tarif_id == self.tarif_id]
        if not ilgili:
            return 0.0
        return sum(d.puan for d in ilgili) / len(ilgili)

    # --- Serileştirme ---

    def to_dict(self) -> dict:
        return {
            "tarif_id": self.tarif_id,
            "tarif_adi": self.tarif_adi,
            "kategori": self.kategori,
            "hazirlama_suresi": self.hazirlama_suresi,
            "malzemeler": [m.to_dict() for m in self.malzemeler],
            "aciklama": self.aciklama,
            "yazar_id": self.yazar_id,
            "eklenme_tarihi": self.eklenme_tarihi,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Tarif":
        malzemeler = [Malzeme.from_dict(m) for m in d.get("malzemeler", [])]
        return cls(
            tarif_id=d["tarif_id"],
            tarif_adi=d["tarif_adi"],
            kategori=d["kategori"],
            hazirlama_suresi=d["hazirlama_suresi"],
            malzemeler=malzemeler,
            aciklama=d.get("aciklama", ""),
            yazar_id=d.get("yazar_id", 0),
            eklenme_tarihi=d.get("eklenme_tarihi"),
        )
