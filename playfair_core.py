
def bersihkan_key(key):
    key = key.upper()
    key = ''.join([c for c in key if c.isalpha()])
    key = key.replace('J', 'I')
    
    hasil = ""
    for c in key:
        if c not in hasil:
            hasil += c
    return hasil


def buat_matriks(key):
    alfabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_bersih = bersihkan_key(key)
    
    gabungan = key_bersih
    for c in alfabet:
        if c not in gabungan:
            gabungan += c
    
    matriks = []
    for i in range(5):
        baris = []
        for j in range(5):
            baris.append(gabungan[i * 5 + j])
        matriks.append(baris)
    
    return matriks


def cari_posisi(matriks, huruf):
    for i in range(5):
        for j in range(5):
            if matriks[i][j] == huruf:
                return (i, j)
    return None


def siapkan_plaintext(teks):
    teks = teks.upper()
    teks = ''.join([c for c in teks if c.isalpha()])
    teks = teks.replace('J', 'I')
    
    bigram = []
    i = 0
    while i < len(teks):
        a = teks[i]
        if i + 1 < len(teks):
            b = teks[i + 1]
            if a == b:
                bigram.append(a + 'X')
                i += 1
            else:
                bigram.append(a + b)
                i += 2
        else:
            bigram.append(a + 'X')
            i += 1
    
    return bigram


def enkripsi_bigram(matriks, bigram):
    a, b = bigram[0], bigram[1]
    pos_a = cari_posisi(matriks, a)
    pos_b = cari_posisi(matriks, b)
    
    baris_a, kolom_a = pos_a
    baris_b, kolom_b = pos_b
    
    if baris_a == baris_b:
        hasil_a = matriks[baris_a][(kolom_a + 1) % 5]
        hasil_b = matriks[baris_b][(kolom_b + 1) % 5]
        aturan = "Same Row (Geser Kanan)"
    elif kolom_a == kolom_b:
        hasil_a = matriks[(baris_a + 1) % 5][kolom_a]
        hasil_b = matriks[(baris_b + 1) % 5][kolom_b]
        aturan = "Same Column (Geser Bawah)"
    else:
        hasil_a = matriks[baris_a][kolom_b]
        hasil_b = matriks[baris_b][kolom_a]
        aturan = "Rectangle (Tukar Kolom)"
    
    return (hasil_a + hasil_b, aturan)


def dekripsi_bigram(matriks, bigram):
    a, b = bigram[0], bigram[1]
    pos_a = cari_posisi(matriks, a)
    pos_b = cari_posisi(matriks, b)
    
    baris_a, kolom_a = pos_a
    baris_b, kolom_b = pos_b
    
    if baris_a == baris_b:
        hasil_a = matriks[baris_a][(kolom_a - 1) % 5]
        hasil_b = matriks[baris_b][(kolom_b - 1) % 5]
        aturan = "Same Row (Geser Kiri)"
    elif kolom_a == kolom_b:
        hasil_a = matriks[(baris_a - 1) % 5][kolom_a]
        hasil_b = matriks[(baris_b - 1) % 5][kolom_b]
        aturan = "Same Column (Geser Atas)"
    else:
        hasil_a = matriks[baris_a][kolom_b]
        hasil_b = matriks[baris_b][kolom_a]
        aturan = "Rectangle (Tukar Kolom)"
    
    return (hasil_a + hasil_b, aturan)


def enkripsi(teks, key):
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