"""Malzeme sınıfı — tarif içinde composition olarak kullanılır."""


class Malzeme:
    def __init__(self, malzeme_adi: str, miktar: str):
        self.malzeme_adi = malzeme_adi.strip()
        self.miktar = miktar.strip()

    def to_dict(self) -> dict:
        return {
            "malzeme_adi": self.malzeme_adi,
            "miktar": self.miktar,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Malzeme":
        return cls(
            malzeme_adi=d["malzeme_adi"],
            miktar=d["miktar"],
        )

    def __repr__(self) -> str:
        return f"{self.miktar} {self.malzeme_adi}"
