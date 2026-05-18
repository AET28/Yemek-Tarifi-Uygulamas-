"""Degerlendirme sınıfı — tarif puanlama ve yorum."""
from datetime import datetime


class Degerlendirme:
    def __init__(
        self,
        degerlendirme_id: int,
        tarif_id: int,
        kullanici_id: int,
        puan: int,
        yorum: str = "",
        tarih: str = None,
    ):
        self.degerlendirme_id = degerlendirme_id
        self.tarif_id = tarif_id
        self.kullanici_id = kullanici_id
        self.puan = max(1, min(5, puan))
        self.yorum = yorum
        self.tarih = tarih or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "degerlendirme_id": self.degerlendirme_id,
            "tarif_id": self.tarif_id,
            "kullanici_id": self.kullanici_id,
            "puan": self.puan,
            "yorum": self.yorum,
            "tarih": self.tarih,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Degerlendirme":
        return cls(
            degerlendirme_id=d["degerlendirme_id"],
            tarif_id=d["tarif_id"],
            kullanici_id=d["kullanici_id"],
            puan=d["puan"],
            yorum=d.get("yorum", ""),
            tarih=d.get("tarih"),
        )
