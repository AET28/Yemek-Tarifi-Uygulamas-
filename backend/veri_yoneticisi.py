"""VeriYoneticisi — JSON kalıcılık + CRUD + iş mantığı."""
import json
import os
from backend.tarif import Tarif
from backend.malzeme import Malzeme
from backend.kullanici import Kullanici
from backend.degerlendirme import Degerlendirme

KATEGORILER = (
    "Çorba", "Ana Yemek", "Tatlı", "Salata",
    "Kahvaltı", "İçecek", "Aperatif", "Hamur İşi",
)


class VeriYoneticisi:
    def __init__(self, veri_klasoru: str = "data"):
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self._tarif_dosya = os.path.join(veri_klasoru, "tarifler.json")
        self._kullanici_dosya = os.path.join(veri_klasoru, "kullanicilar.json")
        self._degerlendirme_dosya = os.path.join(veri_klasoru, "degerlendirmeler.json")

        self.tarifler: list[Tarif] = []
        self.kullanicilar: list[Kullanici] = []
        self.degerlendirmeler: list[Degerlendirme] = []

        self._yukle()

    # ========== Kalıcılık ==========

    def _yukle(self):
        self.tarifler = self._json_oku(self._tarif_dosya, Tarif.from_dict)
        self.kullanicilar = self._json_oku(self._kullanici_dosya, Kullanici.from_dict)
        self.degerlendirmeler = self._json_oku(self._degerlendirme_dosya, Degerlendirme.from_dict)

    @staticmethod
    def _json_oku(dosya: str, from_dict_fn) -> list:
        if not os.path.exists(dosya):
            return []
        try:
            with open(dosya, "r", encoding="utf-8") as f:
                return [from_dict_fn(d) for d in json.load(f)]
        except (json.JSONDecodeError, KeyError, TypeError):
            return []

    def _json_yaz(self, dosya: str, liste: list):
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in liste], f, ensure_ascii=False, indent=2)

    def kaydet(self):
        self._json_yaz(self._tarif_dosya, self.tarifler)
        self._json_yaz(self._kullanici_dosya, self.kullanicilar)
        self._json_yaz(self._degerlendirme_dosya, self.degerlendirmeler)

    # ========== Tarif CRUD ==========

    def _yeni_tarif_id(self) -> int:
        if not self.tarifler:
            return 1
        return max(t.tarif_id for t in self.tarifler) + 1

    def tarif_ekle(self, tarif_adi: str, kategori: str, hazirlama_suresi: int,
                   malzemeler: list[Malzeme], aciklama: str = "",
                   yazar_id: int = 0) -> Tarif:
        if not tarif_adi.strip():
            raise ValueError("Tarif adı boş olamaz.")
        if kategori not in KATEGORILER:
            raise ValueError(f"Geçersiz kategori: {kategori}")
        if hazirlama_suresi <= 0:
            raise ValueError("Hazırlama süresi 0'dan büyük olmalı.")
        if not malzemeler:
            raise ValueError("En az 1 malzeme gerekli.")

        tarif = Tarif(
            tarif_id=self._yeni_tarif_id(),
            tarif_adi=tarif_adi,
            kategori=kategori,
            hazirlama_suresi=hazirlama_suresi,
            malzemeler=malzemeler,
            aciklama=aciklama,
            yazar_id=yazar_id,
        )
        self.tarifler.append(tarif)
        self.kaydet()
        return tarif

    def tarif_guncelle(self, tarif_id: int, **kwargs) -> Tarif:
        tarif = self.tarif_bul(tarif_id)
        if not tarif:
            raise ValueError("Tarif bulunamadı.")
        for anahtar, deger in kwargs.items():
            if hasattr(tarif, anahtar):
                setattr(tarif, anahtar, deger)
        self.kaydet()
        return tarif

    def tarif_sil(self, tarif_id: int):
        tarif = self.tarif_bul(tarif_id)
        if not tarif:
            raise ValueError("Tarif bulunamadı.")
        self.tarifler.remove(tarif)
        # Cascade: ilgili değerlendirmeleri sil
        self.degerlendirmeler = [
            d for d in self.degerlendirmeler if d.tarif_id != tarif_id
        ]
        self.kaydet()

    def tarif_bul(self, tarif_id: int) -> Tarif | None:
        for t in self.tarifler:
            if t.tarif_id == tarif_id:
                return t
        return None

    # ========== Kullanıcı CRUD ==========

    def _yeni_kullanici_id(self) -> int:
        if not self.kullanicilar:
            return 1
        return max(k.kullanici_id for k in self.kullanicilar) + 1

    def kullanici_ekle(self, ad: str, email: str = "") -> Kullanici:
        if not ad.strip():
            raise ValueError("Kullanıcı adı boş olamaz.")
        kullanici = Kullanici(
            kullanici_id=self._yeni_kullanici_id(),
            ad=ad,
            email=email,
        )
        self.kullanicilar.append(kullanici)
        self.kaydet()
        return kullanici

    def kullanici_sil(self, kullanici_id: int):
        kullanici = self.kullanici_bul(kullanici_id)
        if not kullanici:
            raise ValueError("Kullanıcı bulunamadı.")
        self.kullanicilar.remove(kullanici)
        # Tarifler kalsın ama yazar "Silinmiş Kullanıcı" olur
        # Değerlendirmeler silinir
        self.degerlendirmeler = [
            d for d in self.degerlendirmeler if d.kullanici_id != kullanici_id
        ]
        self.kaydet()

    def kullanici_bul(self, kullanici_id: int) -> Kullanici | None:
        for k in self.kullanicilar:
            if k.kullanici_id == kullanici_id:
                return k
        return None

    def kullanici_adi(self, kullanici_id: int) -> str:
        k = self.kullanici_bul(kullanici_id)
        return k.ad if k else "Silinmiş Kullanıcı"

    # ========== Değerlendirme CRUD ==========

    def _yeni_degerlendirme_id(self) -> int:
        if not self.degerlendirmeler:
            return 1
        return max(d.degerlendirme_id for d in self.degerlendirmeler) + 1

    def degerlendirme_ekle(self, tarif_id: int, kullanici_id: int,
                           puan: int, yorum: str = "") -> Degerlendirme:
        if puan < 1 or puan > 5:
            raise ValueError("Puan 1-5 arasında olmalı.")

        tarif = self.tarif_bul(tarif_id)
        if not tarif:
            raise ValueError("Tarif bulunamadı.")

        # Tarif sahibi kendi tarifini değerlendiremez
        if tarif.yazar_id == kullanici_id:
            raise ValueError("Kendi tarifinizi değerlendiremezsiniz.")

        # Upsert: aynı kullanıcı aynı tarife tekrar değerlendirme bırakırsa güncelle
        mevcut = None
        for d in self.degerlendirmeler:
            if d.tarif_id == tarif_id and d.kullanici_id == kullanici_id:
                mevcut = d
                break

        if mevcut:
            mevcut.puan = max(1, min(5, puan))
            mevcut.yorum = yorum
            from datetime import datetime
            mevcut.tarih = datetime.now().isoformat()
            self.kaydet()
            return mevcut

        deg = Degerlendirme(
            degerlendirme_id=self._yeni_degerlendirme_id(),
            tarif_id=tarif_id,
            kullanici_id=kullanici_id,
            puan=puan,
            yorum=yorum,
        )
        self.degerlendirmeler.append(deg)
        self.kaydet()
        return deg

    # ========== Sorgular ==========

    def tarif_ortalama_puan(self, tarif_id: int) -> float:
        ilgili = [d for d in self.degerlendirmeler if d.tarif_id == tarif_id]
        if not ilgili:
            return 0.0
        return sum(d.puan for d in ilgili) / len(ilgili)

    def tarif_degerlendirme_sayisi(self, tarif_id: int) -> int:
        return sum(1 for d in self.degerlendirmeler if d.tarif_id == tarif_id)

    def kullanici_tarif_sayisi(self, kullanici_id: int) -> int:
        return sum(1 for t in self.tarifler if t.yazar_id == kullanici_id)

    def kullanici_degerlendirme_sayisi(self, kullanici_id: int) -> int:
        return sum(1 for d in self.degerlendirmeler if d.kullanici_id == kullanici_id)

    def kategori_dagilimi(self) -> dict:
        dagilim = {}
        for t in self.tarifler:
            dagilim[t.kategori] = dagilim.get(t.kategori, 0) + 1
        return dagilim

    def genel_ortalama_puan(self) -> float:
        if not self.degerlendirmeler:
            return 0.0
        return sum(d.puan for d in self.degerlendirmeler) / len(self.degerlendirmeler)

    def en_yuksek_puanli_tarifler(self, n: int = 5) -> list[tuple]:
        """(Tarif, ortalama_puan) listesi döner."""
        sonuc = []
        for t in self.tarifler:
            ort = self.tarif_ortalama_puan(t.tarif_id)
            if ort > 0:
                sonuc.append((t, ort))
        sonuc.sort(key=lambda x: -x[1])
        return sonuc[:n]

    def en_aktif_kullanicilar(self, n: int = 5) -> list[tuple]:
        """(Kullanici, degerlendirme_sayisi) listesi döner."""
        sonuc = []
        for k in self.kullanicilar:
            sayi = self.kullanici_degerlendirme_sayisi(k.kullanici_id)
            sonuc.append((k, sayi))
        sonuc.sort(key=lambda x: -x[1])
        return sonuc[:n]
