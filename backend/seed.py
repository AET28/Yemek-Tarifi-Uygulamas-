"""Seed verisi — 15 tarif, 8 kullanıcı, ~25 değerlendirme."""
from backend.veri_yoneticisi import VeriYoneticisi
from backend.malzeme import Malzeme


def seed_yukle(vy: VeriYoneticisi):
    """Boş veritabanına örnek veri yükler."""
    if vy.tarifler:
        return  # Zaten veri var

    # ===== KULLANICILAR (8 kişi) =====
    kullanicilar = [
        ("Beko Yılmaz", "beko@mail.com"),
        ("Ali Demir", "ali@mail.com"),
        ("Ayşe Kaya", "ayse@mail.com"),
        ("Mehmet Şahin", "mehmet@mail.com"),
        ("Zeynep Arslan", "zeynep@mail.com"),
        ("Can Öztürk", "can@mail.com"),
        ("Selin Yıldız", "selin@mail.com"),
        ("Murat Koç", "murat@mail.com"),
    ]
    for ad, email in kullanicilar:
        vy.kullanici_ekle(ad, email)

    # ===== TARİFLER (15 tane) =====
    tarifler = [
        {
            "tarif_adi": "Mercimek Çorbası",
            "kategori": "Çorba",
            "hazirlama_suresi": 45,
            "yazar_id": 1,
            "aciklama": "Kırmızı mercimeği yıkayıp süzün. Soğanı yağda kavurun. Havuç ve patatesi küçük küçük doğrayıp ekleyin. Mercimeği ekleyip sıcak su ile kaynatın. Yumuşayınca blenderdan geçirin. Tuz, karabiber ve pul biber ile tatlandırın. Üzerine tereyağlı sos gezdirin.",
            "malzemeler": [
                ("Kırmızı mercimek", "1.5 su bardağı"),
                ("Soğan", "1 adet"),
                ("Havuç", "1 adet"),
                ("Patates", "1 adet"),
                ("Tereyağı", "2 yemek kaşığı"),
                ("Tuz", "1 tatlı kaşığı"),
                ("Karabiber", "1 çay kaşığı"),
                ("Pul biber", "1 çay kaşığı"),
            ],
        },
        {
            "tarif_adi": "Adana Kebap",
            "kategori": "Ana Yemek",
            "hazirlama_suresi": 90,
            "yazar_id": 2,
            "aciklama": "Kıymayı kuyruk yağı ile iyice yoğurun. Pul biber, tuz ve karabiberi ekleyin. En az 2 saat buzdolabında dinlendirin. Şişlere sararak mangal közünde veya ızgarada pişirin. Lavaş, soğan ve közlenmiş domates ile servis edin.",
            "malzemeler": [
                ("Dana kıyma", "500 gr"),
                ("Kuyruk yağı", "100 gr"),
                ("Pul biber", "2 yemek kaşığı"),
                ("Tuz", "1 tatlı kaşığı"),
                ("Karabiber", "1 çay kaşığı"),
                ("Soğan", "2 adet"),
                ("Domates", "3 adet"),
                ("Lavaş", "4 adet"),
            ],
        },
        {
            "tarif_adi": "Mantı",
            "kategori": "Ana Yemek",
            "hazirlama_suresi": 180,
            "yazar_id": 3,
            "aciklama": "Un, yumurta, su ve tuz ile hamur yoğurun. İnce açıp küçük kareler kesin. Kıyma, soğan, tuz ve baharatla iç harç hazırlayın. Karelerin ortasına iç koyup kapatın. Kaynar tuzlu suda haşlayın. Sarımsaklı yoğurt ve tereyağlı pul biberli sos ile servis edin.",
            "malzemeler": [
                ("Un", "3 su bardağı"),
                ("Yumurta", "1 adet"),
                ("Dana kıyma", "250 gr"),
                ("Soğan", "1 adet"),
                ("Yoğurt", "2 su bardağı"),
                ("Sarımsak", "3 diş"),
                ("Tereyağı", "2 yemek kaşığı"),
                ("Pul biber", "1 yemek kaşığı"),
                ("Nane", "1 tatlı kaşığı"),
                ("Tuz", "1 tatlı kaşığı"),
            ],
        },
        {
            "tarif_adi": "Sütlaç",
            "kategori": "Tatlı",
            "hazirlama_suresi": 60,
            "yazar_id": 1,
            "aciklama": "Pirinci yıkayıp 1 saat suda bekletin. Süzüp bir miktar su ile haşlayın. Sütü ekleyip kaynatın. Şeker ve pirinç ununun karışımını ekleyin. Kıvam alınca güveç kaplarına bölün. Fırında üstü kızarana dek pişirin.",
            "malzemeler": [
                ("Pirinç", "0.5 su bardağı"),
                ("Süt", "1 litre"),
                ("Şeker", "1 su bardağı"),
                ("Pirinç unu", "2 yemek kaşığı"),
                ("Vanilya", "1 paket"),
                ("Tarçın", "süsleme için"),
            ],
        },
        {
            "tarif_adi": "Künefe",
            "kategori": "Tatlı",
            "hazirlama_suresi": 45,
            "yazar_id": 4,
            "aciklama": "Kadayıfı ince ince didikleyin. Erimiş tereyağı ile karıştırın. Yarısını kalıba yayın, peyniri ortaya koyun, kalan kadayıfı üstüne kapatın. Kısık ateşte iki tarafını da kızartın. Ilık şerbeti üzerine gezdirip antep fıstığı ile servis edin.",
            "malzemeler": [
                ("Kadayıf", "250 gr"),
                ("Künefe peyniri", "200 gr"),
                ("Tereyağı", "100 gr"),
                ("Şeker", "2 su bardağı"),
                ("Su", "1.5 su bardağı"),
                ("Limon suyu", "1 çay kaşığı"),
                ("Antep fıstığı", "2 yemek kaşığı"),
            ],
        },
        {
            "tarif_adi": "Çoban Salata",
            "kategori": "Salata",
            "hazirlama_suresi": 15,
            "yazar_id": 5,
            "aciklama": "Domates, salatalık, biber ve soğanı küçük küçük doğrayın. Maydanoz yapraklarını ince kıyın. Zeytinyağı, limon suyu ve tuz ile harmanlayın.",
            "malzemeler": [
                ("Domates", "3 adet"),
                ("Salatalık", "2 adet"),
                ("Sivri biber", "2 adet"),
                ("Soğan", "1 adet"),
                ("Maydanoz", "1 demet"),
                ("Zeytinyağı", "3 yemek kaşığı"),
                ("Limon", "1 adet"),
                ("Tuz", "1 çay kaşığı"),
            ],
        },
        {
            "tarif_adi": "Menemen",
            "kategori": "Kahvaltı",
            "hazirlama_suresi": 20,
            "yazar_id": 6,
            "aciklama": "Biberleri ve domatesleri küçük küçük doğrayın. Zeytinyağında önce biberleri kavurun. Domatesleri ekleyip suyunu salana dek pişirin. Yumurtaları kırıp karıştırın. Tuz ve pul biber ekleyin. Yumurtalar pişene dek karıştırarak pişirin.",
            "malzemeler": [
                ("Yumurta", "4 adet"),
                ("Domates", "3 adet"),
                ("Sivri biber", "2 adet"),
                ("Zeytinyağı", "2 yemek kaşığı"),
                ("Tuz", "1 çay kaşığı"),
                ("Pul biber", "1 çay kaşığı"),
            ],
        },
        {
            "tarif_adi": "İmam Bayıldı",
            "kategori": "Ana Yemek",
            "hazirlama_suresi": 75,
            "yazar_id": 7,
            "aciklama": "Patlıcanları alacalı soyup ortadan yarın. Tuzlu suda bekletin. Soğan, domates ve biberi doğrayıp zeytinyağında kavurun. Patlıcanları tepsiye dizin, iç harcı üzerlerine paylaştırın. Fırında 180°C'de 40 dakika pişirin.",
            "malzemeler": [
                ("Patlıcan", "4 adet"),
                ("Soğan", "2 adet"),
                ("Domates", "3 adet"),
                ("Sivri biber", "3 adet"),
                ("Sarımsak", "4 diş"),
                ("Zeytinyağı", "0.5 su bardağı"),
                ("Tuz", "1 tatlı kaşığı"),
            ],
        },
        {
            "tarif_adi": "Karnıyarık",
            "kategori": "Ana Yemek",
            "hazirlama_suresi": 80,
            "yazar_id": 8,
            "aciklama": "Patlıcanları soyup kızartın. Kıymayı soğan ile kavurun, domates rendesi ve biberi ekleyin. Patlıcanları ortadan yarıp iç harcı doldurun. Tepsiye dizin, üzerlerine domates dilimleri koyun. 180°C fırında 30 dakika pişirin.",
            "malzemeler": [
                ("Patlıcan", "4 adet"),
                ("Dana kıyma", "300 gr"),
                ("Soğan", "1 adet"),
                ("Domates", "2 adet"),
                ("Sivri biber", "2 adet"),
                ("Sarımsak", "2 diş"),
                ("Sıvı yağ", "kızartma için"),
                ("Tuz", "1 tatlı kaşığı"),
                ("Karabiber", "1 çay kaşığı"),
            ],
        },
        {
            "tarif_adi": "Lahmacun",
            "kategori": "Hamur İşi",
            "hazirlama_suresi": 60,
            "yazar_id": 1,
            "aciklama": "Un, maya, su ve tuzla hamur yoğurun. Dinlendirin. Kıyma, soğan, domates, biber ve maydanozu karıştırıp iç harç yapın. Hamuru bezeler ayırıp ince açın. İç harcı yayın. 250°C fırında 8-10 dakika pişirin.",
            "malzemeler": [
                ("Un", "3 su bardağı"),
                ("Maya", "1 paket"),
                ("Dana kıyma", "300 gr"),
                ("Soğan", "2 adet"),
                ("Domates", "2 adet"),
                ("Sivri biber", "3 adet"),
                ("Maydanoz", "1 demet"),
                ("Pul biber", "1 yemek kaşığı"),
                ("Tuz", "1 tatlı kaşığı"),
            ],
        },
        {
            "tarif_adi": "Pide",
            "kategori": "Hamur İşi",
            "hazirlama_suresi": 50,
            "yazar_id": 3,
            "aciklama": "Hamuru un, maya, su, yoğurt ve tuzla yoğurun. 1 saat mayalandırın. Kıyma, kaşar ve sebze karışımı ile iç hazırlayın. Hamuru kayık şeklinde açıp iç malzemeyi yayın. 220°C fırında 15 dakika pişirin. Üzerine yumurta kırıp 3 dakika daha pişirin.",
            "malzemeler": [
                ("Un", "4 su bardağı"),
                ("Maya", "1 paket"),
                ("Yoğurt", "2 yemek kaşığı"),
                ("Dana kıyma", "250 gr"),
                ("Kaşar peyniri", "150 gr"),
                ("Soğan", "1 adet"),
                ("Domates", "1 adet"),
                ("Yumurta", "2 adet"),
                ("Tuz", "1 tatlı kaşığı"),
            ],
        },
        {
            "tarif_adi": "Baklava",
            "kategori": "Tatlı",
            "hazirlama_suresi": 120,
            "yazar_id": 2,
            "aciklama": "Yufkaları tepsiye sererek aralarına erimiş tereyağı sürün. Her 4-5 yufkada bir ceviz içi serpin. Üstünü de yufka ile kapatıp baklava şeklinde kesin. Kalan tereyağını üzerine gezdirin. 170°C fırında kızarana dek pişirin. Ilımış şerbeti üzerine dökün.",
            "malzemeler": [
                ("Yufka", "1 kg"),
                ("Ceviz içi", "300 gr"),
                ("Tereyağı", "250 gr"),
                ("Şeker", "3 su bardağı"),
                ("Su", "2.5 su bardağı"),
                ("Limon suyu", "1 yemek kaşığı"),
            ],
        },
        {
            "tarif_adi": "Kuru Fasulye",
            "kategori": "Ana Yemek",
            "hazirlama_suresi": 120,
            "yazar_id": 5,
            "aciklama": "Fasulyeleri bir gece suda bekletin. Soğanı yağda kavurun, salçayı ekleyin. Haşlanmış fasulyeleri ve sıcak suyu ekleyin. Kısık ateşte yumuşayana dek pişirin. Tuz ve baharatları en sona ekleyin.",
            "malzemeler": [
                ("Kuru fasulye", "2 su bardağı"),
                ("Soğan", "1 adet"),
                ("Domates salçası", "2 yemek kaşığı"),
                ("Biber salçası", "1 yemek kaşığı"),
                ("Sıvı yağ", "3 yemek kaşığı"),
                ("Tuz", "1 tatlı kaşığı"),
                ("Karabiber", "1 çay kaşığı"),
                ("Pul biber", "1 çay kaşığı"),
            ],
        },
        {
            "tarif_adi": "Pilav",
            "kategori": "Ana Yemek",
            "hazirlama_suresi": 30,
            "yazar_id": 4,
            "aciklama": "Pirinci yıkayıp ılık tuzlu suda 20 dakika bekletin. Tereyağında şehriyeyi kavurun. Süzülmüş pirinci ekleyip kavurun. Sıcak suyu ekleyin. Kaynayınca kısık ateşe alıp suyunu çekene dek pişirin. Ocaktan alıp 15 dakika demlendirin.",
            "malzemeler": [
                ("Pirinç", "2 su bardağı"),
                ("Tereyağı", "2 yemek kaşığı"),
                ("Şehriye", "1 yemek kaşığı"),
                ("Su", "3 su bardağı"),
                ("Tuz", "1 tatlı kaşığı"),
            ],
        },
        {
            "tarif_adi": "Cacık",
            "kategori": "Salata",
            "hazirlama_suresi": 15,
            "yazar_id": 6,
            "aciklama": "Salatalığı rendeleyin veya küçük küçük doğrayın. Yoğurdu çırpın. Sarımsağı ezin. Hepsini karıştırıp zeytinyağı ve nane ekleyin. Buzdolabında soğutarak servis edin.",
            "malzemeler": [
                ("Yoğurt", "2 su bardağı"),
                ("Salatalık", "1 adet"),
                ("Sarımsak", "2 diş"),
                ("Zeytinyağı", "1 yemek kaşığı"),
                ("Nane", "1 tatlı kaşığı"),
                ("Tuz", "1 çay kaşığı"),
            ],
        },
    ]

    for td in tarifler:
        malzemeler = [Malzeme(adi, miktar) for adi, miktar in td["malzemeler"]]
        vy.tarif_ekle(
            tarif_adi=td["tarif_adi"],
            kategori=td["kategori"],
            hazirlama_suresi=td["hazirlama_suresi"],
            malzemeler=malzemeler,
            aciklama=td["aciklama"],
            yazar_id=td["yazar_id"],
        )

    # ===== DEĞERLENDİRMELER (~25 tane) =====
    degerlendirmeler = [
        (1, 2, 5, "Çok lezzetli oldu, herkes bayıldı."),
        (1, 3, 4, "Güzel ama biraz daha tuz koyardım."),
        (1, 5, 5, "Anneannemin tarifi gibi, mükemmel."),
        (2, 1, 4, "Acılı sevenlere tavsiye ederim."),
        (2, 3, 5, "Et kalitesi çok önemli, harika oldu."),
        (3, 4, 5, "Yapması zahmetli ama her lokmaya değer."),
        (3, 5, 4, "Yoğurt sosu çok güzel olmuş."),
        (3, 6, 3, "Bence biraz daha ince açılmalı."),
        (4, 2, 4, "Fırında üstü güzel kızardı."),
        (4, 3, 5, "En sevdiğim tatlı, tarif çok başarılı."),
        (5, 1, 5, "Peyniri güzel eritilirse müthiş oluyor."),
        (5, 6, 4, "Şerbeti biraz daha az olabilirdi."),
        (6, 1, 4, "Yazın en güzel salata."),
        (6, 7, 5, "Basit ama lezzetli."),
        (7, 1, 5, "Kahvaltının vazgeçilmezi."),
        (7, 8, 4, "Ben kaşarlı yapıyorum, o da güzel."),
        (8, 1, 4, "Zeytinyağlı klasik, çok başarılı."),
        (8, 3, 3, "Patlıcanları daha çok kızartmak lazım."),
        (9, 2, 5, "Anneannemin tarifinden bile güzel."),
        (10, 5, 4, "Hamuru ince açmak önemli."),
        (10, 7, 5, "Ev yapımı lahmacun bambaşka."),
        (11, 2, 4, "Kıymalı pide favorim."),
        (12, 6, 5, "Baklava yapılabilecek en güzel tarif."),
        (13, 1, 4, "Pilav yanında harika gidiyor."),
        (14, 3, 4, "Tereyağlı pilavın sırrı demlendirmede."),
        (15, 1, 5, "Yaz aylarının kurtarıcısı."),
    ]

    for tarif_id, kullanici_id, puan, yorum in degerlendirmeler:
        try:
            vy.degerlendirme_ekle(tarif_id, kullanici_id, puan, yorum)
        except ValueError:
            pass  # Kendi tarifini değerlendirmeye çalışırsa atla
