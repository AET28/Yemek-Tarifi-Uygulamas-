"""Kullanici sınıfı — platform kullanıcısı (auth değil, domain modeli)."""


class Kullanici:
    def __init__(
        self,
        kullanici_id: int,
        ad: str,
        email: str = "",
    ):
        self.kullanici_id = kullanici_id
        self.ad = ad.strip()
        self.email = email.strip()

    def eklediklerim(self, tum_tarifler: list) -> list:
        return [t for t in tum_tarifler if t.yazar_id == self.kullanici_id]

    def to_dict(self) -> dict:
        return {
            "kullanici_id": self.kullanici_id,
            "ad": self.ad,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kullanici":
        return cls(
            kullanici_id=d["kullanici_id"],
            ad=d["ad"],
            email=d.get("email", ""),
        )
