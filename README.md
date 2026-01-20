# Makine-Ogrenmesi-final--dev
<p align="center">
  <img src="img/banner.jpg" width="500" height="500">
</p>
## Tanım
Bu projede, akıllı ev sistemlerinden elde edilen enerji tüketim verileri kullanılarak evin enerji tüketiminin normal seviyelerin üzerinde olup olmadığı analiz edilmiştir. Çalışmanın temel amacı, saat ve hava koşulları gibi çevresel faktörlerin enerji tüketimi üzerindeki etkisini incelemek ve bu bilgileri makine öğrenmesi modelleri ile değerlendirmektir.

Projede kullanılan veri seti, evdeki toplam enerji tüketimi ile birlikte sıcaklık, nem, rüzgar hızı ve hava durumu gibi çevresel bilgileri içermektedir. Bu veriler kullanılarak öncelikle enerji tüketiminin farklı koşullardaki ortalama davranışı belirlenmiş, ardından bu bilgiler referans alınarak sınıflandırma işlemi gerçekleştirilmiştir.

Analiz sürecinde pivot tablolar yardımıyla farklı saatler ve çevresel koşullar için ortalama enerji tüketimleri hesaplanmıştır. Elde edilen bu ortalama değerler, evin normal tüketim alışkanlığını temsil eden birer referans (baseline) olarak modele dahil edilmiştir. Son aşamada ise bu veriler kullanılarak farklı makine öğrenmesi algoritmaları ile enerji tüketiminin ortalamanın üzerinde olup olmadığı tahmin edilmiştir.

## Kodların açıklamaları

### Kütüphanelerin Eklenmesi
![Makine_sertifikasi](img/1.png)

Bu bölümde veri işleme ve makine öğrenmesi adımlarında kullanacağım kütüphaneleri projeye dahil ettim.
Pandas ve Numpy veri seti üzerinde işlem yapabilmek için kullanıldı. Scikit-learn kütüphanesinden eğitim-test ayırma, farklı makine öğrenmesi modelleri ve değerlendirme metrikleri alındı.
Veri ön işleme aşamasında kategorik verileri sayısal hale getirmek için LabelEncoder, değişkenleri ölçeklemek için ise StandardScaler kullanıldı.
Son olarak, model sonuçlarını ve özellik önemlerini görselleştirmek amacıyla matplotlib ve seaborn kütüphaneleri eklendi.

### Veri Setinin Okunması ve Ön İşleme
![Makine_sertifikasi](img/2.png)
Bu bölümde öncelikle veri seti dosyası programa okunmuştur. Veri seti büyük olduğu için okuma sırasında low_memory=False parametresi kullanılmıştır.
Zaman bilgisini tutan time sütununda sayısal olmayan değerler bulunduğu için bu sütun önce sayısal formata dönüştürülmüş, hatalı olan satırlar temizlenmiştir.
Daha sonra zaman bilgisi saniye cinsinden olduğu için datetime formatına çevrilmiş ve her kayıt için günün hangi saatine ait olduğu hour sütunu olarak çıkarılmıştır.

Ayrıca sıcaklık, nem, rüzgar hızı gibi hava koşullarını temsil eden sütunlar sayısal formata dönüştürülmüştür. Analizde gerçekten gerekli olan alanlarda eksik veriler temizlenerek, modelin hatalı verilerle eğitilmesi engellenmiştir.


### Kategorik Verinin Sayısallaştırılması ve Pivot Baseline Oluşturulması
![Makine_sertifikasi](img/3.png)

Bu aşamada hava durumunu özetleyen summary sütunu sayısal olmadığı için, makine öğrenmesi modellerinde kullanılabilmesi amacıyla LabelEncoder ile sayısal hale getirilmiştir.

Daha sonra enerji tüketiminin farklı koşullardaki normal (ortalama) davranışını görebilmek için pivot tablolar oluşturulmuştur.
Saat, sıcaklık, nem ve rüzgar hızı değerlerine göre evin ortalama enerji tüketimi hesaplanmıştır. Bu pivot tablolar sayesinde örneğin “belirli bir saatte” veya “belirli bir sıcaklıkta” evin ortalama olarak ne kadar enerji harcadığı elde edilmiştir.

Elde edilen bu ortalama değerler veri setine geri eklenerek her bir kayıt için, o koşullara ait referans (baseline) tüketim bilgisi modele dahil edilmiştir.

### Hedef Değişkenin Belirlenmesi ve Veri Setinin Hazırlanması
![Makine_sertifikasi](img/4.png)
Bu aşamada sınıflandırma problemi için hedef değişken oluşturulmuştur. Enerji tüketimi değeri, tüm veri setindeki ortalama tüketim ile karşılaştırılarak, ortalamanın üzerinde olan durumlar 1, altında kalan durumlar ise 0 olarak etiketlenmiştir. Böylece problem ikili sınıflandırma (binary classification) haline getirilmiştir.

Modelde kullanılacak giriş değişkenleri belirlenirken saat bilgisi, hava durumu değerleri ve pivot tablolar ile elde edilen ortalama tüketim (baseline) değerleri birlikte kullanılmıştır. Pivotlardan gelen bu değerler, modelin mevcut koşullardaki tüketimi daha iyi yorumlamasına yardımcı olmaktadır.

Birleştirme işlemleri sonrası oluşan eksik değerler sıfır ile doldurulmuş, ardından değişkenler arasındaki ölçek farklarını azaltmak için StandardScaler ile ölçeklendirme yapılmıştır. Son olarak veri seti eğitim ve test olacak şekilde ayrılarak modelleme aşamasına hazır hale getirilmiştir.

###Modellerin Eğitilmesi ve Sonuçların Değerlendirilmesi
![Makine_sertifikasi](img/5.png)


Bu bölümde farklı makine öğrenmesi algoritmaları kullanılarak modelleme yapılmıştır. Karşılaştırma yapabilmek amacıyla Lojistik Regresyon, K-En Yakın Komşu (KNN) ve Random Forest algoritmaları seçilmiştir. Her bir model eğitim verisi ile eğitilmiş ve test verisi üzerinde tahmin yapılarak doğruluk oranları hesaplanmıştır.

Modellerin performansını daha detaylı incelemek için doğruluk değerinin yanı sıra classification_report çıktısı da alınmıştır. Bu sayede her sınıf için başarı oranları ayrı ayrı gözlemlenmiştir.

Son olarak Random Forest modelinin sunduğu özellik önemleri kullanılarak hangi değişkenlerin enerji tüketimini daha fazla etkilediği analiz edilmiştir. Elde edilen sonuçlar grafik ile görselleştirilmiş ve modele en çok katkı sağlayan değişkenler net bir şekilde gösterilmiştir.

## Sonuç
Bu çalışmada akıllı ev enerji tüketim verileri kullanılarak, evin enerji tüketiminin ortalamanın üzerinde olup olmadığı sınıflandırılmaya çalışılmıştır. Analiz sürecinde saat, hava koşulları ve bu koşullara göre oluşturulan pivot tablolar yardımıyla elde edilen ortalama tüketim değerleri birlikte kullanılmıştır.

Pivot tablolar sayesinde farklı saatlerde ve farklı çevresel koşullarda evin normal enerji tüketim davranışı daha net bir şekilde görülmüştür. Bu ortalama değerlerin modele eklenmesi, enerji tüketiminin sadece anlık verilere değil, geçmişe dayalı referanslara göre de değerlendirilmesini sağlamıştır.

Uygulanan modeller arasında özellikle Random Forest algoritmasının daha dengeli ve başarılı sonuçlar verdiği gözlemlenmiştir. Feature importance grafiği incelendiğinde saat bilgisi ve pivot tablolarla elde edilen ortalama tüketim değerlerinin model üzerinde önemli bir etkiye sahip olduğu görülmüştür.

Sonuç olarak, pivot tablolar kullanılarak oluşturulan bu yaklaşımın enerji tüketim tahmini ve sınıflandırma problemleri için anlamlı ve uygulanabilir bir yöntem olduğu anlaşılmıştır.

## Katılım Sertifikları 

### Makine öğrenmesi
![Makine_sertifikasi](img/Makine_ogrenmesi.png)
### Python
![python_sertifikasi](img/python.png)
