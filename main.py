import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from playfair_core import enkripsi, dekripsi, buat_matriks, cari_posisi

# ============================================
# KONFIGURASI TEMA
# ============================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

WARNA_ATURAN = {
    "Same Row": "#3b82f6",
    "Same Column": "#10b981",
    "Rectangle": "#f59e0b",
}
WARNA_DEFAULT = "#1f538d"
WARNA_MUTED = "#94a3b8"
WARNA_HIJAU = "#4ade80"
WARNA_MERAH = "#ef4444"

LABEL_ATURAN = {
    "Same Row": "Same Row",
    "Same Column": "Same Col",
    "Rectangle": "Rectangle",
}

# ============================================
# VARIABEL GLOBAL
# ============================================
teks_dari_file = ""
path_file = ""
label_matriks_cells = []
log_data = []
animasi_matriks_ids = []
animasi_output_id = None
proses_ids = []
sedang_memproses = False

# ============================================
# VALIDASI
# ============================================

def validasi_input(mode):
    """Validasi input sebelum diproses."""
    key = entry_key.get().strip()
    teks = textbox_input.get("1.0", "end").strip()
    
    if not key:
        messagebox.showwarning("Key Kosong", 
            "⚠️ Key tidak boleh kosong!\n\nContoh key: MONARCHY")
        entry_key.focus()
        return None
    
    key_alfabet = ''.join([c for c in key if c.isalpha()])
    if len(key_alfabet) == 0:
        messagebox.showwarning("Key Tidak Valid", 
            "⚠️ Key harus mengandung minimal 1 huruf alfabet!\n\n"
            "Karakter non-alfabet akan diabaikan.")
        entry_key.focus()
        return None
    
    if not teks:
        messagebox.showwarning("Teks Kosong", 
            "⚠️ Teks input kosong!\n\n"
            "Silakan upload file .txt atau ketik langsung.")
        return None
    
    teks_alfabet = ''.join([c for c in teks if c.isalpha()])
    if len(teks_alfabet) == 0:
        messagebox.showwarning("Teks Tidak Valid", 
            "⚠️ Teks input tidak mengandung huruf alfabet!\n\n"
            "Playfair Cipher hanya memproses huruf A-Z.")
        return None
    
    if len(teks_alfabet) > 5000:
        konfirmasi = messagebox.askyesno("Teks Panjang", 
            f"⚠️ Teks kamu cukup panjang ({len(teks_alfabet)} huruf).\n\n"
            f"Proses mungkin memakan waktu beberapa detik.\n"
            f"Lanjutkan?")
        if not konfirmasi:
            return None
    
    return (key, teks)


def peringatan_huruf_hilang(teks_asli):
    """Cek apakah ada karakter yang akan hilang saat preprocessing."""
    huruf = ''.join([c for c in teks_asli if c.isalpha()])
    non_huruf = len(teks_asli) - len(huruf)
    
    if non_huruf > 0:
        return True
    if 'J' in teks_asli.upper():
        return True
    return False


# ============================================
# FUNGSI GUI
# ============================================

def batalkan_animasi(daftar_id):
    while daftar_id:
        animation_id = daftar_id.pop()
        try:
            app.after_cancel(animation_id)
        except Exception:
            pass


def atur_tombol_aksi(state):
    btn_enkripsi.configure(state=state)
    btn_dekripsi.configure(state=state)
    btn_simpan.configure(state=state)
    btn_upload.configure(state=state)
    btn_reset.configure(state=state)




def update_matriks(*args):
    batalkan_animasi(animasi_matriks_ids)
    key = entry_key.get().strip()
    matriks = buat_matriks(key) if key else buat_matriks("A")

    for index, label in enumerate(cell for row in label_matriks_cells for cell in row):
        i, j = divmod(index, 5)
        label.configure(text="·", fg_color="#334155", text_color=WARNA_MUTED)

        def tampilkan_huruf(cell=label, huruf=matriks[i][j]):
            cell.configure(text=huruf, fg_color=WARNA_DEFAULT, text_color="white")

        animasi_matriks_ids.append(app.after(index * 16, tampilkan_huruf))


def reset_warna_matriks():
    for row in label_matriks_cells:
        for cell in row:
            cell.configure(fg_color=WARNA_DEFAULT, text_color="white")


def highlight_bigram(bigram):
    reset_warna_matriks()
    key = entry_key.get().strip()
    matriks = buat_matriks(key) if key else buat_matriks("A")

    for huruf in bigram:
        pos = cari_posisi(matriks, huruf)
        if not pos:
            continue
        i, j = pos
        cell = label_matriks_cells[i][j]
        cell.configure(fg_color=WARNA_MERAH, text_color="white")
        app.after(110, lambda target=cell: target.configure(fg_color="#ffffff", text_color="#111827"))
        app.after(220, lambda target=cell: target.configure(fg_color=WARNA_MERAH, text_color="white"))


def pilih_step(index):
    step = log_data[index]
    highlight_bigram(step["bigram"])

    warna = "#64748b"
    for nama_aturan, warna_aturan in WARNA_ATURAN.items():
        if nama_aturan in step["aturan"]:
            warna = warna_aturan
            break

    detail_text = (
        f"Langkah #{index + 1}\n"
        f"─────────────────\n"
        f"Bigram   : {step['bigram']}\n"
        f"Aturan   : {step['aturan']}\n"
        f"Hasil    : {step['hasil']}"
    )
    label_detail.configure(text=detail_text, text_color="white")
    frame_detail.configure(border_color=warna)
    label_status.configure(text=f"Langkah #{index + 1} dipilih.", text_color=warna)


def tampilkan_log_gui(log, mode="ENKRIPSI"):
    global log_data
    log_data = log

    for widget in frame_log_list.winfo_children():
        widget.destroy()

    header = ctk.CTkLabel(
        frame_log_list,
        text=f"📋 Langkah {mode.title()} ({len(log)} bigram)",
        font=("Roboto", 12, "bold"),
        text_color="#e2e8f0",
    )
    header.pack(pady=(5, 8), anchor="w", padx=5)

    for idx, step in enumerate(log):
        warna = "#334155"
        nama_singkat = step["aturan"]
        for nama_aturan, warna_aturan in WARNA_ATURAN.items():
            if nama_aturan in step["aturan"]:
                warna = warna_aturan
                nama_singkat = LABEL_ATURAN.get(nama_aturan, nama_aturan)
                break

        btn = ctk.CTkButton(
            frame_log_list,
            text=f" [{idx + 1}]  {step['bigram']}  →  {step['hasil']}   ({nama_singkat})",
            font=("Roboto", 11),
            anchor="w",
            fg_color=warna,
            hover_color="#475569",
            height=32,
            command=lambda i=idx: pilih_step(i),
        )
        btn.pack(fill="x", pady=2, padx=5)


def upload_file():
    global teks_dari_file, path_file
    path_baru = filedialog.askopenfilename(
        title="Pilih file teks",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not path_baru:
        return
    
    if not path_baru.lower().endswith(".txt"):
        konfirmasi = messagebox.askyesno("File Bukan .txt", 
            "⚠️ File yang kamu pilih bukan .txt.\n\n"
            "Tetap lanjutkan membaca file ini?")
        if not konfirmasi:
            return
    
    try:
        ukuran = os.path.getsize(path_baru)
        if ukuran > 5 * 1024 * 1024:
            konfirmasi = messagebox.askyesno("File Besar",
                f"⚠️ File berukuran {ukuran / 1024:.1f} KB.\n\n"
                f"Proses mungkin lambat. Lanjutkan?")
            if not konfirmasi:
                return
    except Exception:
        pass
    
    try:
        with open(path_baru, "r", encoding="utf-8") as f:
            isi = f.read()
        
        if not isi.strip():
            messagebox.showwarning("File Kosong", 
                "⚠️ File yang kamu pilih kosong!\n\n"
                "Silakan pilih file lain.")
            return
        
        teks_dari_file = isi
        path_file = path_baru
        
        label_file.configure(text=f"📄 {os.path.basename(path_baru)} ({len(isi)} karakter)")
        textbox_input.delete("1.0", "end")
        textbox_input.insert("1.0", isi)
        
        if peringatan_huruf_hilang(isi):
            label_status.configure(
                text="ℹ️ Catatan: karakter non-alfabet & huruf J akan diabaikan/dikonversi.",
                text_color="#fbbf24"
            )
        else:
            label_status.configure(text="✅ File berhasil di-upload.", text_color="#4ade80")
    
    except UnicodeDecodeError:
        messagebox.showerror("Error Encoding", 
            "❌ File tidak bisa dibaca sebagai teks UTF-8.\n\n"
            "Pastikan file berisi teks biasa, bukan biner.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file:\n{e}")


def tampilkan_output_bertahap(hasil, selesai):
    global animasi_output_id
    textbox_output.delete("1.0", "end")
    ukuran_chunk = max(1, len(hasil) // 30)

    def ketik(posisi=0):
        global animasi_output_id
        if posisi >= len(hasil):
            animasi_output_id = None
            selesai()
            return
        textbox_output.insert("end", hasil[posisi:posisi + ukuran_chunk])
        textbox_output.see("end")
        animasi_output_id = app.after(18, lambda: ketik(posisi + ukuran_chunk))

    ketik()


def selesaikan_proses(mode, hasil, log):
    global sedang_memproses
    tampilkan_log_gui(log, mode)
    reset_warna_matriks()
    label_detail.configure(
        text="Klik salah satu langkah\ndi panel kanan untuk detail.",
        text_color="gray",
    )
    frame_detail.configure(border_color="#475569")
    progress_proses.set(1)
    label_status.configure(
        text=f"✅ {mode.title()} selesai ({len(log)} bigram diproses)",
        text_color=WARNA_HIJAU,
    )
    sedang_memproses = False
    atur_tombol_aksi("normal")


def jalankan_proses(mode):
    global sedang_memproses
    if sedang_memproses:
        return

    validasi = validasi_input(mode.lower())
    if validasi is None:
        return

    key, teks = validasi
    try:
        _, hasil, log = (enkripsi(teks, key) if mode == "ENKRIPSI" else dekripsi(teks, key))
    except Exception as e:
        messagebox.showerror(f"Error {mode.title()}", f"Terjadi kesalahan:\n{e}")
        return

    sedang_memproses = True
    atur_tombol_aksi("disabled")
    label_status.configure(text=f"Memulai {mode.lower()}...", text_color="#60a5fa")
    progress_proses.set(0)

    tahap = [
        (0.12, "Membaca input"),
        (0.38, "Menyusun matriks"),
        (0.68, "Memproses bigram"),
        (0.90, "Menyiapkan hasil"),
    ]

    for index, (nilai, pesan) in enumerate(tahap):
        proses_ids.append(app.after(
            index * 145,
            lambda value=nilai, text=pesan: (
                progress_proses.set(value),
                label_status.configure(text=f"{text}...", text_color="#60a5fa"),
            ),
        ))

    proses_ids.append(app.after(
        len(tahap) * 145,
        lambda: tampilkan_output_bertahap(hasil, lambda: selesaikan_proses(mode, hasil, log)),
    ))


def proses_enkripsi():
    jalankan_proses("ENKRIPSI")


def proses_dekripsi():
    jalankan_proses("DEKRIPSI")


def simpan_hasil():
    hasil = textbox_output.get("1.0", "end").strip()
    if not hasil:
        messagebox.showwarning("Belum Ada Hasil", 
            "⚠️ Belum ada hasil untuk disimpan!\n\n"
            "Proses enkripsi/dekripsi terlebih dahulu.")
        return
    
    path_simpan = filedialog.asksaveasfilename(
        title="Simpan hasil",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        initialfile="hasil_playfair.txt"
    )
    if not path_simpan:
        return
    
    if os.path.exists(path_simpan):
        konfirmasi = messagebox.askyesno("File Sudah Ada",
            f"⚠️ File '{os.path.basename(path_simpan)}' sudah ada.\n\n"
            f"Timpa file tersebut?")
        if not konfirmasi:
            return
    
    try:
        with open(path_simpan, "w", encoding="utf-8") as f:
            f.write(hasil)
        messagebox.showinfo("Sukses", 
            f"✅ Hasil berhasil disimpan di:\n{path_simpan}")
        label_status.configure(text=f"💾 Tersimpan: {os.path.basename(path_simpan)}", text_color="#a78bfa")
    except Exception as e:
        messagebox.showerror("Error Simpan", f"Gagal menyimpan file:\n{e}")


def reset_semua():
    global animasi_output_id, sedang_memproses
    konfirmasi = messagebox.askyesno("Reset", "Yakin ingin reset semua input dan hasil?")
    if not konfirmasi:
        return

    if animasi_output_id:
        app.after_cancel(animasi_output_id)
        animasi_output_id = None
    batalkan_animasi(proses_ids)
    sedang_memproses = False
    atur_tombol_aksi("normal")
    entry_key.delete(0, "end")
    textbox_input.delete("1.0", "end")
    textbox_output.delete("1.0", "end")
    label_file.configure(text="Belum ada file dipilih")

    for widget in frame_log_list.winfo_children():
        widget.destroy()

    label_detail.configure(
        text="Klik salah satu langkah\ndi panel kanan untuk detail.",
        text_color="gray",
    )
    frame_detail.configure(border_color="#475569")
    progress_proses.set(0)
    update_matriks()
    label_status.configure(text="🔄 Aplikasi direset.", text_color=WARNA_MUTED)


# ============================================
# MEMBANGUN GUI
# ============================================
app = ctk.CTk()
app.title("Playfair Cipher - Enkripsi & Dekripsi")
app.geometry("1250x820")
app.minsize(1100, 720)

judul = ctk.CTkLabel(app, text="🔐 PLAYFAIR CIPHER", font=("Roboto", 24, "bold"))
judul.pack(pady=(12, 8))

# ----- FRAME KEY -----
frame_key = ctk.CTkFrame(app)
frame_key.pack(pady=5, padx=20, fill="x")

label_key = ctk.CTkLabel(frame_key, text="🔑 Key:", font=("Roboto", 13, "bold"))
label_key.pack(side="left", padx=(15, 10), pady=10)

entry_key = ctk.CTkEntry(frame_key, placeholder_text="Contoh: MONARCHY", width=350, font=("Roboto", 12))
entry_key.pack(side="left", padx=10, pady=10)
entry_key.bind("<KeyRelease>", update_matriks)

btn_reset = ctk.CTkButton(
    frame_key, text="🔄 Reset", command=reset_semua,
    width=100, fg_color="#64748b", hover_color="#475569",
)
btn_reset.pack(side="right", padx=15, pady=10)

# ----- FRAME FILE -----
frame_file = ctk.CTkFrame(app)
frame_file.pack(pady=5, padx=20, fill="x")

btn_upload = ctk.CTkButton(frame_file, text="📂 Upload File .txt", command=upload_file, width=180)
btn_upload.pack(side="left", padx=(15, 10), pady=10)

label_file = ctk.CTkLabel(frame_file, text="Belum ada file dipilih", font=("Roboto", 11))
label_file.pack(side="left", padx=10, pady=10)

# ----- AREA UTAMA -----
frame_utama = ctk.CTkFrame(app)
frame_utama.pack(pady=10, padx=20, fill="both", expand=True)

# Kiri
frame_kiri = ctk.CTkFrame(frame_utama, width=350)
frame_kiri.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

label_input = ctk.CTkLabel(frame_kiri, text="📥 Input", font=("Roboto", 12, "bold"))
label_input.pack(pady=(10, 5))

textbox_input = ctk.CTkTextbox(frame_kiri, wrap="word", height=140, font=("Roboto", 12))
textbox_input.pack(fill="both", expand=True, padx=10, pady=(0, 10))

label_output = ctk.CTkLabel(frame_kiri, text="📤 Output", font=("Roboto", 12, "bold"))
label_output.pack(pady=(10, 5))

textbox_output = ctk.CTkTextbox(frame_kiri, wrap="word", height=140, font=("Roboto", 12))
textbox_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# Tengah
frame_tengah = ctk.CTkFrame(frame_utama, width=380)
frame_tengah.pack(side="left", fill="y", padx=5, pady=10)
frame_tengah.pack_propagate(False)

label_matriks_judul = ctk.CTkLabel(frame_tengah, text="🔲 Matriks 5x5", font=("Roboto", 13, "bold"))
label_matriks_judul.pack(pady=(10, 5))

frame_grid = ctk.CTkFrame(frame_tengah, fg_color="transparent")
frame_grid.pack(pady=5)

for i in range(5):
    baris_labels = []
    for j in range(5):
        lbl = ctk.CTkLabel(
            frame_grid, text="?", width=48, height=48,
            font=("Roboto", 18, "bold"),
            fg_color=WARNA_DEFAULT, corner_radius=6, text_color="white",
        )
        lbl.grid(row=i, column=j, padx=2, pady=2)
        baris_labels.append(lbl)
    label_matriks_cells.append(baris_labels)

label_detail_judul = ctk.CTkLabel(frame_tengah, text="🔍 Detail Bigram", font=("Roboto", 12, "bold"))
label_detail_judul.pack(pady=(15, 5))

frame_detail = ctk.CTkFrame(frame_tengah, border_width=2, border_color="#475569", corner_radius=8)
frame_detail.pack(fill="x", padx=15, pady=5)

label_detail = ctk.CTkLabel(
    frame_detail,
    text="Klik salah satu langkah\ndi panel kanan untuk detail.",
    font=("Roboto", 11), justify="left", text_color="gray",
)
label_detail.pack(pady=12, padx=10)

# Kanan
frame_kanan = ctk.CTkFrame(frame_utama, width=380)
frame_kanan.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

frame_log_list = ctk.CTkScrollableFrame(frame_kanan, fg_color="#0f172a")
frame_log_list.pack(fill="both", expand=True, padx=5, pady=5)

# ----- AKSI -----
frame_aksi = ctk.CTkFrame(app)
frame_aksi.pack(pady=(5, 2), padx=20, fill="x")

btn_enkripsi = ctk.CTkButton(
    frame_aksi, text="🔒 Enkripsi", command=proses_enkripsi,
    fg_color="#2563eb", hover_color="#1d4ed8", width=150,
)
btn_enkripsi.pack(side="left", padx=15, pady=12)

btn_dekripsi = ctk.CTkButton(
    frame_aksi, text="🔓 Dekripsi", command=proses_dekripsi,
    fg_color="#059669", hover_color="#047857", width=150,
)
btn_dekripsi.pack(side="left", padx=10, pady=12)

btn_simpan = ctk.CTkButton(
    frame_aksi, text="💾 Simpan Hasil", command=simpan_hasil,
    fg_color="#7c3aed", hover_color="#6d28d9", width=150,
)
btn_simpan.pack(side="right", padx=15, pady=12)

# ----- STATUS DAN PROGRESS ANIMASI -----
progress_proses = ctk.CTkProgressBar(app, height=7, progress_color="#3b82f6")
progress_proses.pack(fill="x", padx=35, pady=(3, 2))
progress_proses.set(0)

label_status = ctk.CTkLabel(app, text="Siap digunakan.", font=("Roboto", 11), text_color="gray")
label_status.pack(pady=(0, 8))

app.bind("<Control-Return>", lambda event: proses_enkripsi())
app.bind("<Control-Shift-Return>", lambda event: proses_dekripsi())

update_matriks()
app.mainloop()