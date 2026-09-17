from playfair_core import buat_matriks, enkripsi, dekripsi

# Key & plaintext contoh
key = "MONARCHY"
teks = "HELLO WORLD"

# Tampilkan matriks
print("=== MATRIKS 5x5 ===")
matriks = buat_matriks(key)
for baris in matriks:
    print(" ".join(baris))

# Test enkripsi
print("\n=== ENKRIPSI ===")
matriks, hasil_enkripsi, log = enkripsi(teks, key)
print(f"Plaintext : {teks}")
print(f"Hasil     : {hasil_enkripsi}")
for step in log:
    print(f"  {step['bigram']} -> {step['hasil']} ({step['aturan']})")

# Test dekripsi
print("\n=== DEKRIPSI ===")
matriks, hasil_dekripsi, log = dekripsi(hasil_enkripsi, key)
print(f"Ciphertext : {hasil_enkripsi}")
print(f"Hasil      : {hasil_dekripsi}")