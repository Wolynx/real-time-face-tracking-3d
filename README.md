# 🎥 Gerçek Zamanlı 3B Yüz Takibi ve Isı Haritası

Bu proje, webcam kullanarak yüzü gerçek zamanlı olarak takip eder
ve kafa pozisyonunu 3 boyutlu bir sahnede görselleştirir.

Program kapatıldığında, kullanıcının en çok bulunduğu bölgeleri
gösteren bir **ısı haritası (heat map)** oluşturulur.

---

## 🚀 Özellikler

- MediaPipe Face Mesh ile gerçek zamanlı yüz takibi
- EMA (Exponential Moving Average) ile yumuşak hareket
- PyVista ile 3B sahne çizimi
- Hareket izi (trail) gösterimi
- Oturum sonrası ısı haritası raporu
- FPS (kare/saniye) gösterimi

---

## 🧠 Nasıl Çalışır?

- Burun noktası referans alınır
- Yüz genişliği kullanılarak derinlik (Z ekseni) tahmin edilir
- Pozisyonlar yumuşatma filtresinden geçirilir
- Tüm veriler saklanarak yoğunluk tabanlı ısı haritası üretilir

---

## 📦 Gereksinimler

- Python 3.9 veya üstü
- Webcam

Kurulum:

```bash
pip install -r requirements.txt
