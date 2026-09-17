# 🔐 Playfair Cipher Kelompok 4

**Aplikasi enkripsi dan dekripsi Playfair Cipher dengan antarmuka grafis interaktif menggunakan Python dan CustomTkinter.**

Memvisualisasikan bagaimana algoritma kriptografi klasik bekerja, mulai dari pembentukan matriks kunci 5×5 hingga transformasi setiap pasangan huruf (*bigram*).

<p align="center">
  <img src="https://img.shields.io/badge/Python-3-blue?logo=python&logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-blueviolet" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/Cryptography-Playfair-orange" alt="Playfair Cipher">
  <img src="https://img.shields.io/badge/Status-Completed-success" alt="Completed">
</p>

---

## 📖 Tentang Proyek

Playfair Cipher adalah algoritma kriptografi klasik yang menggunakan substitusi pasangan huruf untuk melakukan enkripsi dan dekripsi pesan.

Proyek ini mengimplementasikan algoritma Playfair Cipher dalam aplikasi desktop berbasis Python dengan GUI interaktif.

Tidak hanya melakukan enkripsi dan dekripsi, aplikasi ini juga memungkinkan pengguna mempelajari proses algoritma secara visual melalui matriks kunci 5×5, log transformasi bigram, dan detail posisi huruf pada matriks.

### ✨ Fitur Utama

* 🔑 **Dynamic Key Matrix** — Matriks kunci 5×5 diperbarui secara real-time saat pengguna mengetikkan kunci.
* 🔒 **Enkripsi & Dekripsi** — Memproses plaintext menjadi ciphertext dan mengembalikannya menggunakan kunci yang sama.
* 🧩 **Bigram Processing** — Memecah teks menjadi pasangan huruf dengan penanganan huruf ganda dan padding `X`.
* 🎨 **Visualisasi Matriks** — Menyorot posisi huruf yang sedang diproses pada matriks 5×5.
* 📋 **Interactive Step Log** — Menampilkan setiap langkah transformasi bigram yang dapat dipilih untuk melihat detailnya.
* 📂 **File Handling** — Memuat input dari berkas `.txt` dan menyimpan hasil enkripsi atau dekripsi.
* 🧪 **Unit Testing** — Pengujian logika inti algoritma tanpa perlu menjalankan antarmuka grafis.

---

## 🖥️ Demo

### Antarmuka Aplikasi

> Tambahkan screenshot aplikasi pada bagian ini agar pengunjung repository dapat melihat tampilan GUI secara langsung.

```text
┌─────────────────────────────────────────────────────────────┐
│                     PLAYFAIR CIPHER                         │
│                                                             │
│  Key: MONARCHY                                               │
│                                                             │
│  ┌──────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Input        │  │ Matrix 5x5      │  │ Bigram Log      │ │
│  │              │  │                 │  │                 │ │
│  │ HELLO WORLD  │  │ M O N A R       │  │ HE → CF         │ │
│  │              │  │ C H Y B D       │  │ LL → ...        │ │
│  │              │  │ E F G I K       │  │ LO → ...        │ │
│  │              │  │ L P Q S T       │  │                 │ │
│  │              │  │ U V W X Z       │  │                 │ │
│  └──────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                             │
│  [Enkripsi] [Dekripsi] [Upload File] [Simpan Hasil] [Reset] │
└─────────────────────────────────────────────────────────────┘
```

*Ilustrasi konseptual tata letak aplikasi, bukan screenshot aktual.*

### Contoh Enkripsi dan Dekripsi

| Parameter      | Nilai                              |
| -------------- | ---------------------------------- |
| Key            | `MONARCHY`                         |
| Plaintext      | `HELLO WORLD FROM PLAYFAIR CIPHER` |
| Ciphertext     | `CFSUPMVNMTHKMNOLSMHGBSMDFSCFAZ`   |
| Hasil dekripsi | `HELXLOWORLDFROMPLAYFAIRCIPHERX`   |

Hasil dekripsi mengandung huruf `X` sebagai padding untuk menangani huruf ganda dan jumlah huruf yang ganjil. Oleh karena itu, hasilnya tidak selalu identik secara karakter dengan plaintext awal.

---

## ⚙️ Cara Kerja Algoritma

### 1. Pembentukan Matriks Kunci

Kunci diubah menjadi huruf kapital, karakter non-alfabet dihapus, dan huruf `J` digabungkan menjadi `I`.

Huruf duplikat dihilangkan dengan mempertahankan urutan kemunculannya. Sisa alfabet kemudian ditambahkan secara berurutan untuk melengkapi matriks 5×5.

Contoh dengan key `MONARCHY`:

```text
┌───┬───┬───┬───┬───┐
│ M │ O │ N │ A │ R │
├───┼───┼───┼───┼───┤
│ C │ H │ Y │ B │ D │
├───┼───┼───┼───┼───┤
│ E │ F │ G │ I │ K │
├───┼───┼───┼───┼───┤
│ L │ P │ Q │ S │ T │
├───┼───┼───┼───┼───┤
│ U │ V │ W │ X │ Z │
└───┴───┴───┴───┴───┘
```

### 2. Preprocessing Plaintext

Sebelum enkripsi, teks dibersihkan dan dipecah menjadi pasangan huruf (*bigram*).

Aturannya:

* Jika dua huruf berurutan sama, sisipkan `X` di antara keduanya.
* Jika jumlah huruf ganjil, tambahkan `X` di akhir.
* Huruf `J` dinormalisasi menjadi `I`.

Contoh:

```text
HELLO
  ↓
HE LX LO
```

### 3. Tiga Aturan Transformasi

| Aturan      | Enkripsi                  | Dekripsi                 |
| ----------- | ------------------------- | ------------------------ |
| Same Row    | Geser satu kolom ke kanan | Geser satu kolom ke kiri |
| Same Column | Geser satu baris ke bawah | Geser satu baris ke atas |
| Rectangle   | Tukar kolom kedua huruf   | Tukar kolom kedua huruf  |

Semua pergeseran dilakukan secara melingkar (*wrap-around*). Aturan Rectangle tetap sama pada enkripsi dan dekripsi karena sifatnya simetris.

Aplikasi menampilkan aturan yang digunakan pada setiap bigram dan menyorot posisi huruf yang sedang diproses.

---

## 🚀 Instalasi dan Menjalankan Program

### Prasyarat

* Python 3
* pip
* CustomTkinter

### 1. Clone Repository

```bash
git clone https://github.com/nandazahran/playfair-cypher-kel4.git
cd playfair-cipher
```

Ganti `USERNAME/playfair-cipher` dengan alamat repository GitHub kamu.

### 2. Buat Virtual Environment

```bash
python -m venv .venv
```

Aktifkan virtual environment:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### 3. Instal Dependensi

```bash
pip install customtkinter
```

### 4. Jalankan Aplikasi

```bash
python main.py
```

---

## 🧪 Pengujian

Logika inti Playfair Cipher dipisahkan dari GUI sehingga dapat diuji secara independen.

Jalankan pengujian menggunakan:

```bash
python -m unittest test_playfair.py
```

Pengujian berfokus pada fungsi pembentukan matriks, preprocessing plaintext, serta enkripsi dan dekripsi bigram.

---

## 📁 Struktur Proyek

```text
playfair-cipher/
│
├── main.py              # Antarmuka grafis (GUI)
├── playfair_core.py     # Implementasi algoritma Playfair Cipher
├── test_playfair.py     # Unit testing logika inti
├── README.md            # Dokumentasi proyek
└── requirements.txt     # Dependensi Python (opsional)
```

### Penjelasan Modul

| Berkas             | Tanggung Jawab                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------- |
| `main.py`          | GUI, validasi input, visualisasi matriks, log bigram, dan pengelolaan berkas teks.            |
| `playfair_core.py` | Normalisasi kunci, pembentukan matriks, preprocessing plaintext, serta enkripsi dan dekripsi. |
| `test_playfair.py` | Pengujian fungsi-fungsi inti algoritma.                                                       |

Pemisahan ini membuat logika kriptografi lebih mudah dipahami, diuji, dan dikembangkan secara terpisah dari antarmuka pengguna.

---

## 🛠️ Teknologi

* **Python 3** — Bahasa pemrograman utama.
* **CustomTkinter** — Pembuatan antarmuka grafis desktop.
* **unittest** — Pengujian unit pada logika inti algoritma.

---

## 👨‍💻 Author

**Ammar Rizky (M0403241088)** \
**Mickhael Keith R.S (M0403241061)** \
**Kemas Adirangga Nayar (M0403241043)** \
**Aufa Rafli Sofwan Pasya (M0403241133)** \
**Faiz Ariq Satria (M0403241112)** \
**Muh Arifaushan (M0403241075)** \
**Nanda Zahran Syafiq (M0403241098)** \
**Masjaw** \
**Ahmad Wildan (M0403241173)**


Computer Science Student
