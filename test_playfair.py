from playfair_core import buat_matriks, enkripsi, dekripsi

key = "MONARCHY"
teks = "HELLO WORLD"

print("=== MATRIKS 5x5 ===")
matriks = buat_matriks(key)
for baris in matriks:
    print(" ".join(baris))

print("\n=== ENKRIPSI ===")
matriks, hasil_enkripsi, log = enkripsi(teks, key)
print(f"Plaintext : {teks}")
print(f"Hasil     : {hasil_enkripsi}")
for step in log:
    print(f"  {step['bigram']} -> {step['hasil']} ({step['aturan']})")

print("\n=== DEKRIPSI ===")
matriks, hasil_dekripsi, log = dekripsi(hasil_enkripsi, key)
print(f"Ciphertext : {hasil_enkripsi}")
print(f"Hasil      : {hasil_dekripsi}")