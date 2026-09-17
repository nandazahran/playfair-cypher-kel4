# ============================================
# PLAYFAIR CIPHER - CORE LOGIC
# ============================================

def bersihkan_key(key):
    """Membersihkan key: uppercase, hilangkan non-alfabet, ganti J->I, hapus duplikat."""
    key = key.upper()
    key = ''.join([c for c in key if c.isalpha()])
    key = key.replace('J', 'I')
    
    # Hapus duplikat, pertahankan urutan
    hasil = ""
    for c in key:
        if c not in hasil:
            hasil += c
    return hasil


def buat_matriks(key):
    """Membuat matriks 5x5 dari key + sisa alfabet (tanpa J)."""
    alfabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Tanpa J
    key_bersih = bersihkan_key(key)
    
    # Gabungkan key + alfabet, lalu hapus duplikat
    gabungan = key_bersih
    for c in alfabet:
        if c not in gabungan:
            gabungan += c
    
    # Ubah jadi matriks 5x5 (list of list)
    matriks = []
    for i in range(5):
        baris = []
        for j in range(5):
            baris.append(gabungan[i * 5 + j])
        matriks.append(baris)
    
    return matriks


def cari_posisi(matriks, huruf):
    """Mencari posisi (baris, kolom) sebuah huruf dalam matriks."""
    for i in range(5):
        for j in range(5):
            if matriks[i][j] == huruf:
                return (i, j)
    return None


def siapkan_plaintext(teks):
    """Bersihkan plaintext & pecah menjadi bigram sesuai aturan Playfair."""
    teks = teks.upper()
    teks = ''.join([c for c in teks if c.isalpha()])
    teks = teks.replace('J', 'I')
    
    # Pecah jadi bigram
    bigram = []
    i = 0
    while i < len(teks):
        a = teks[i]
        if i + 1 < len(teks):
            b = teks[i + 1]
            if a == b:
                # Jika sama, sisipkan X
                bigram.append(a + 'X')
                i += 1
            else:
                bigram.append(a + b)
                i += 2
        else:
            # Huruf terakhir ganjil, tambahkan X
            bigram.append(a + 'X')
            i += 1
    
    return bigram


def enkripsi_bigram(matriks, bigram):
    """Mengenkripsi satu bigram, mengembalikan (hasil, aturan_yang_dipakai)."""
    a, b = bigram[0], bigram[1]
    pos_a = cari_posisi(matriks, a)
    pos_b = cari_posisi(matriks, b)
    
    baris_a, kolom_a = pos_a
    baris_b, kolom_b = pos_b
    
    if baris_a == baris_b:
        # Aturan 1: Same Row -> geser kanan
        hasil_a = matriks[baris_a][(kolom_a + 1) % 5]
        hasil_b = matriks[baris_b][(kolom_b + 1) % 5]
        aturan = "Same Row (Geser Kanan)"
    elif kolom_a == kolom_b:
        # Aturan 2: Same Column -> geser bawah
        hasil_a = matriks[(baris_a + 1) % 5][kolom_a]
        hasil_b = matriks[(baris_b + 1) % 5][kolom_b]
        aturan = "Same Column (Geser Bawah)"
    else:
        # Aturan 3: Rectangle -> tukar kolom
        hasil_a = matriks[baris_a][kolom_b]
        hasil_b = matriks[baris_b][kolom_a]
        aturan = "Rectangle (Tukar Kolom)"
    
    return (hasil_a + hasil_b, aturan)


def dekripsi_bigram(matriks, bigram):
    """Mendekripsi satu bigram, mengembalikan (hasil, aturan_yang_dipakai)."""
    a, b = bigram[0], bigram[1]
    pos_a = cari_posisi(matriks, a)
    pos_b = cari_posisi(matriks, b)
    
    baris_a, kolom_a = pos_a
    baris_b, kolom_b = pos_b
    
    if baris_a == baris_b:
        # Same Row -> geser kiri
        hasil_a = matriks[baris_a][(kolom_a - 1) % 5]
        hasil_b = matriks[baris_b][(kolom_b - 1) % 5]
        aturan = "Same Row (Geser Kiri)"
    elif kolom_a == kolom_b:
        # Same Column -> geser atas
        hasil_a = matriks[(baris_a - 1) % 5][kolom_a]
        hasil_b = matriks[(baris_b - 1) % 5][kolom_b]
        aturan = "Same Column (Geser Atas)"
    else:
        # Rectangle -> tukar kolom (sama seperti enkripsi)
        hasil_a = matriks[baris_a][kolom_b]
        hasil_b = matriks[baris_b][kolom_a]
        aturan = "Rectangle (Tukar Kolom)"
    
    return (hasil_a + hasil_b, aturan)


def enkripsi(teks, key):
    """Fungsi utama enkripsi: mengembalikan hasil + log langkah-langkah."""
    matriks = buat_matriks(key)
    bigram_list = siapkan_plaintext(teks)
    
    hasil = ""
    log = []
    for bg in bigram_list:
        hasil_bg, aturan = enkripsi_bigram(matriks, bg)
        hasil += hasil_bg
        log.append({
            "bigram": bg,
            "hasil": hasil_bg,
            "aturan": aturan
        })
    
    return matriks, hasil, log


def dekripsi(teks, key):
    """Fungsi utama dekripsi: mengembalikan hasil + log langkah-langkah."""
    matriks = buat_matriks(key)
    bigram_list = siapkan_plaintext(teks)
    
    hasil = ""
    log = []
    for bg in bigram_list:
        hasil_bg, aturan = dekripsi_bigram(matriks, bg)
        hasil += hasil_bg
        log.append({
            "bigram": bg,
            "hasil": hasil_bg,
            "aturan": aturan
        })
    
    return matriks, hasil, log