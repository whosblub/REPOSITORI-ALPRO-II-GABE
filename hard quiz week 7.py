import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import base64
import time  # Import modul time untuk pengukuran waktu

class ItemLiburan:
    def __init__(self, kategori, nama, harga, nilai_kepuasan):
        self.kategori = kategori  # 'destinasi', 'penginapan', 'transportasi', 'kuliner', 'hidden gem'
        self.nama = nama
        self.harga = harga
        self.nilai_kepuasan = nilai_kepuasan  # Mengganti "skor kenikmatan" dengan "nilai kepuasan"
    
    def __str__(self):
        return f"{self.nama} ({self.kategori} - Rp {self.harga:,}, Nilai: {self.nilai_kepuasan})"

class PerencanaLiburan:
    def __init__(self, anggaran, negara_asal="Indonesia", negara_tujuan="Socotra Island, Yemen"):
        self.anggaran = anggaran
        self.negara_asal = negara_asal
        self.negara_tujuan = negara_tujuan
        self.daftar_item = []
        self.itinerary_terbaik = []
        self.nilai_terbaik = 0
        self.biaya_terbaik = 0
        self.sisa_anggaran_terbaik = anggaran
        self.kategori_wajib = ['destinasi', 'penginapan', 'transportasi', 'kuliner']
        self.kategori_ditemukan = set()
        self.cuaca = None  # Menyimpan informasi cuaca
        self.delay = 0  # Menyimpan informasi delay
    
    def set_cuaca(self, cuaca):
        self.cuaca = cuaca

    def set_delay(self, delay):
        self.delay = delay

    def tambah_item(self, kategori, nama, harga, nilai_kepuasan):
        self.daftar_item.append(ItemLiburan(kategori, nama, harga, nilai_kepuasan))
    
    def backtrack_rencana(self, itinerary_saat_ini=None, indeks_saat_ini=0, biaya_saat_ini=0, 
                         nilai_saat_ini=0, kategori_saat_ini=None, destinasi_dipilih=False):
        if itinerary_saat_ini is None:
            itinerary_saat_ini = []
        
        if kategori_saat_ini is None:
            kategori_saat_ini = set()
        
        # Pertimbangan delay
        biaya_saat_ini += self.delay * 500000  # Misalnya, biaya tambahan per jam delay
        sisa_anggaran = self.anggaran - biaya_saat_ini
        
        # Pertimbangan cuaca
        if self.cuaca == "Hujan":
            for item in self.daftar_item:
                if item.kategori == 'destinasi':
                    item.nilai_kepuasan -= 2  # Mengurangi nilai kepuasan jika hujan
        
        # Jika anggaran habis dan semua kategori wajib terpenuhi
        if sisa_anggaran == 0 and all(kat in kategori_saat_ini for kat in self.kategori_wajib) and destinasi_dipilih:
            if nilai_saat_ini > self.nilai_terbaik:
                self.itinerary_terbaik = itinerary_saat_ini.copy()
                self.nilai_terbaik = nilai_saat_ini
                self.biaya_terbaik = biaya_saat_ini
                self.sisa_anggaran_terbaik = sisa_anggaran
                self.kategori_ditemukan = kategori_saat_ini.copy()
                return True
        
        # Jika anggaran hampir habis dan lebih baik dari solusi sebelumnya
        elif 0 <= sisa_anggaran <= 10000 and all(kat in kategori_saat_ini for kat in self.kategori_wajib) and destinasi_dipilih:
            if sisa_anggaran < self.sisa_anggaran_terbaik:
                self.itinerary_terbaik = itinerary_saat_ini.copy()
                self.nilai_terbaik = nilai_saat_ini
                self.biaya_terbaik = biaya_saat_ini
                self.sisa_anggaran_terbaik = sisa_anggaran
                self.kategori_ditemukan = kategori_saat_ini.copy()
        
        # Jika sudah habis semua item atau melebihi anggaran, kembali
        if indeks_saat_ini >= len(self.daftar_item) or biaya_saat_ini > self.anggaran:
            return False
        
        item = self.daftar_item[indeks_saat_ini]
        
        if biaya_saat_ini + item.harga <= self.anggaran:
            itinerary_saat_ini.append(item)
            new_kategori = kategori_saat_ini.copy()
            new_kategori.add(item.kategori)
            new_destinasi_dipilih = destinasi_dipilih
            if item.kategori == 'destinasi' and 'Socotra' in item.nama:
                new_destinasi_dipilih = True
            
            if self.backtrack_rencana(
                itinerary_saat_ini, 
                indeks_saat_ini + 1, 
                biaya_saat_ini + item.harga, 
                nilai_saat_ini + item.nilai_kepuasan,
                new_kategori, 
                new_destinasi_dipilih
            ):
                return True
            
            itinerary_saat_ini.pop()
        
        return self.backtrack_rencana(
            itinerary_saat_ini, 
            indeks_saat_ini + 1, 
            biaya_saat_ini, 
            nilai_saat_ini, 
            kategori_saat_ini, 
            destinasi_dipilih
        )
    
    def dapatkan_rencana_optimal(self):
        self.backtrack_rencana()
        return self.itinerary_terbaik, self.biaya_terbaik, self.nilai_terbaik, self.anggaran - self.biaya_terbaik
    
    def cetak_itinerary(self):
        if not self.itinerary_terbaik:
            print("Tidak ditemukan itinerary yang memungkinkan.")
            return
        
        print(f"\nRencana Perjalanan Optimal ke Socotra Island (Anggaran: Rp {self.anggaran:,}):")
        print(f"Total Biaya: Rp {self.biaya_terbaik:,}")
        print(f"Sisa Anggaran: Rp {self.anggaran - self.biaya_terbaik:,}")
        print(f"Total Nilai Kepuasan: {self.nilai_terbaik}")
        print(f"Cuaca: {self.cuaca}")  # Menampilkan informasi cuaca
        print(f"Delay: {self.delay} jam")  # Menampilkan informasi delay
        
        kategori_groups = {}
        for item in self.itinerary_terbaik:
            if item.kategori not in kategori_groups:
                kategori_groups[item.kategori] = []
            kategori_groups[item.kategori].append(item)
        
        for kategori in ['destinasi', 'penginapan', 'transportasi', 'kuliner', 'hidden gem']:
            if kategori in kategori_groups:
                print(f"\n{kategori.upper()}:")
                for i, item in enumerate(kategori_groups[kategori], 1):
                    print(f"{i}. {item.nama} - Rp {item.harga:,} (Nilai: {item.nilai_kepuasan})")
    
    def tampilkan_gui(self):
        root = tk.Tk()
        root.title("Rencana Perjalanan ke Socotra Island")
        root.geometry("1200x800")
        root.configure(bg="#e6f2ff")
        
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        header_font = font.Font(family="Helvetica", size=14, weight="bold")
        normal_font = font.Font(family="Helvetica", size=11)
        info_font = font.Font(family="Helvetica", size=12)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#e6f2ff")
        style.configure("Header.TLabel", font=header_font, background="#e6f2ff", foreground="#003366")
        style.configure("Title.TLabel", font=title_font, background="#e6f2ff", foreground="#003366")
        style.configure("Info.TLabel", font=info_font, background="#e6f2ff", foreground="#003366")
        
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=10)
        
        ttk.Label(header_frame, text="𓆅 SOCOTRA ADVENTURE PLANNER", style="Title.TLabel").pack(side="left", padx=10)
        
        summary_frame = ttk.Frame(main_frame)
        summary_frame.pack(fill="x", pady=10)
        
        budget_frame = tk.Frame(summary_frame, bg="#cce6ff", relief="ridge", bd=2)
        budget_frame.pack(side="left", padx=10, pady=10, ipadx=20, ipady=10)
        
        tk.Label(budget_frame, text="ANGGARAN", font=header_font, bg="#cce6ff", fg="#003366").pack(anchor="w")
        tk.Label(budget_frame, text=f"Rp {self.anggaran:,}", font=info_font, bg="#cce6ff", fg="#003366").pack(anchor="w")
        
        cost_frame = tk.Frame(summary_frame, bg="#d9f2e6", relief="ridge", bd=2)
        cost_frame.pack(side="left", padx=10, pady=10, ipadx=20, ipady=10)
        
        tk.Label(cost_frame, text="TOTAL BIAYA", font=header_font, bg="#d9f2e6", fg="#006633").pack(anchor="w")
        tk.Label(cost_frame, text=f"Rp {self.biaya_terbaik:,}", font=info_font, bg="#d9f2e6", fg="#006633").pack(anchor="w")
        
        remaining_frame = tk.Frame(summary_frame, bg="#fff2cc", relief="ridge", bd=2)
        remaining_frame.pack(side="left", padx=10, pady=10, ipadx=20, ipady=10)
        
        tk.Label(remaining_frame, text="SISA ANGGARAN", font=header_font, bg="#fff2cc", fg="#806600").pack(anchor="w")
        tk.Label(remaining_frame, text=f"Rp {self.anggaran - self.biaya_terbaik:,}", font=info_font, bg="#fff2cc", fg="#806600").pack(anchor="w")
        
        score_frame = tk.Frame(summary_frame, bg="#ffe6e6", relief="ridge", bd=2)
        score_frame.pack(side="left", padx=10, pady=10, ipadx=20, ipady=10)
        
        tk.Label(score_frame, text="NILAI KEPUASAN", font=header_font, bg="#ffe6e6", fg="#990000").pack(anchor="w")
        tk.Label(score_frame, text=f"{self.nilai_terbaik}", font=info_font, bg="#ffe6e6", fg="#990000").pack(anchor="w")
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        itinerary_frame = ttk.Frame(notebook)
        chart_frame = ttk.Frame(notebook)
        
        notebook.add(itinerary_frame, text="Itinerary")
        notebook.add(chart_frame, text="Analisis Biaya")
        
        kategori_groups = {}
        for item in self.itinerary_terbaik:
            if item.kategori not in kategori_groups:
                kategori_groups[item.kategori] = []
            kategori_groups[item.kategori].append(item)
        
        kategori_icons = {
            'destinasi': '🏝️',
            'penginapan': '🏠',
            'transportasi': '✈️',
            'kuliner': '🍽️',
            'hidden gem': '🔍'
        }
        
        kategori_colors = {
            'destinasi': "#cce6ff",
            'penginapan': "#d9f2e6",
            'transportasi': "#e6ccff",
            'kuliner': "#fff2cc",
            'hidden gem': "#ffe6e6"
        }
        
        canvas = tk.Canvas(itinerary_frame, bg="#e6f2ff")
        scrollbar = ttk.Scrollbar(itinerary_frame, orient="vertical", command=canvas.yview)
        itinerary_content = ttk.Frame(canvas)
        
        canvas.create_window((0, 0), window=itinerary_content, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=1150, height=500)
        
        itinerary_content.bind("<Configure>", configure_scroll)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        row = 0
        for kategori in ['destinasi', 'penginapan', 'transportasi', 'kuliner', 'hidden gem']:
            if kategori in kategori_groups:
                kategori_frame = tk.Frame(itinerary_content, bg=kategori_colors[kategori], relief="ridge", bd=1)
                kategori_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=10, pady=5, ipadx=5, ipady=5)
                
                header_text = f"{kategori_icons[kategori]} {kategori.upper()}"
                tk.Label(kategori_frame, text=header_text, font=header_font, bg=kategori_colors[kategori]).pack(anchor="w", padx=10)
                
                row += 1
                
                for i, item in enumerate(kategori_groups[kategori], 1):
                    item_frame = tk.Frame(itinerary_content, bg="#ffffff", relief="groove", bd=1)
                    item_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=20, pady=2, ipadx=5, ipady=5)
                    
                    tk.Label(item_frame, text=f"{i}. {item.nama}", font=normal_font, bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", padx=10)
                    tk.Label(item_frame, text=f"Rp {item.harga:,}", font=normal_font, bg="#ffffff").grid(row=0, column=1, padx=10)
                    
                    stars = "★" * item.nilai_kepuasan + "☆" * (10 - item.nilai_kepuasan)
                    tk.Label(item_frame, text=stars, font=normal_font, bg="#ffffff", fg="#ffcc00").grid(row=0, column=2, padx=10)
                    
                    row += 1
        
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        kategori_biaya = {}
        kategori_nilai = {}
        
        for kategori in ['destinasi', 'penginapan', 'transportasi', 'kuliner', 'hidden gem']:
            if kategori in kategori_groups:
                kategori_biaya[kategori] = sum(item.harga for item in kategori_groups[kategori])
                kategori_nilai[kategori] = sum(item.nilai_kepuasan for item in kategori_groups[kategori])
        
        labels = list(kategori_biaya.keys())
        sizes = list(kategori_biaya.values())
        colors = [kategori_colors[k] for k in labels]
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribusi Biaya per Kategori')
        
        categories = list(kategori_nilai.keys())
        scores = list(kategori_nilai.values())
        bar_colors = [kategori_colors[k] for k in categories]
        
        bars = ax2.bar(categories, scores, color=bar_colors)
        ax2.set_title('Nilai Kepuasan per Kategori')
        ax2.set_ylabel('Total Nilai')
        ax2.set_ylim(0, max(scores) * 1.2)
        
        chart_canvas = FigureCanvasTkAgg(fig, chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=10)
        
        footer_text = ttk.Label(footer_frame, text="© 2025 Socotra Adventure Planner | Dibuat dengan ❤ untuk para petualang",
                               font=("Helvetica", 9), background="#e6f2ff", foreground="#666666")
        footer_text.pack(side="right", padx=10)
        
        root.mainloop()

def buat_item_pelengkap(jumlah_minimum=100000, jumlah_maksimum=1000000, interval=50000):
    item_pelengkap = []
    jumlah_saat_ini = jumlah_minimum
    while jumlah_saat_ini <= jumlah_maksimum:
        item_pelengkap.append(ItemLiburan('kuliner', f'Snack dan minuman selama perjalanan (Rp {jumlah_saat_ini:,})', jumlah_saat_ini, 3))
        item_pelengkap.append(ItemLiburan('transportasi', f'Biaya transportasi lokal tambahan (Rp {jumlah_saat_ini:,})', jumlah_saat_ini, 2))
        item_pelengkap.append(ItemLiburan('hidden gem', f'Kunjungan ke lokasi rahasia dengan biaya masuk (Rp {jumlah_saat_ini:,})', jumlah_saat_ini, 4))
        jumlah_saat_ini += interval
    return item_pelengkap

if __name__ == "__main__":
    anggaran = 50000000
    
    perencana = PerencanaLiburan(anggaran=anggaran)
    
    # Set cuaca dan delay
    perencana.set_cuaca("Hujan")  # Misalnya cuaca buruk
    perencana.set_delay(2)  # Misalnya, ada delay 2 jam
    
    # Data harga real-time (2023)
    
    # Transportasi (Pesawat)
    perencana.tambah_item('transportasi', 'Tiket pesawat PP Jakarta-Dubai (Emirates)', 12500000, 7)
    perencana.tambah_item('transportasi', 'Tiket pesawat PP Jakarta-Dubai (Garuda)', 13000000, 8)
    perencana.tambah_item('transportasi', 'Tiket pesawat Dubai-Socotra via Seiyun (Yemenia Airways)', 8700000, 6)
    perencana.tambah_item('transportasi', 'Tiket pesawat Dubai-Socotra (Flynas)', 8000000, 5)
    
    # Sewa mobil
    perencana.tambah_item('transportasi', 'Sewa mobil 4x4 dengan sopir di Socotra (7 hari)', 7000000, 8)
    perencana.tambah_item('transportasi', 'Transportasi lokal di Dubai', 1200000, 5)
    perencana.tambah_item('transportasi', 'Biaya visa dan izin masuk Socotra', 3000000, 4)
    perencana.tambah_item('transportasi', 'Transportasi dari/ke Bandara Soekarno-Hatta', 450000, 3)
    perencana.tambah_item('transportasi', 'Transportasi lokal di Hadiboh', 500000, 4)
    
    # Destinasi di Socotra
    perencana.tambah_item('destinasi', 'Pohon Darah Naga di Dixsam Plateau, Socotra', 500000, 9)
    perencana.tambah_item('destinasi', 'Pantai Qalansiyah, Socotra', 300000, 8)
    perencana.tambah_item('destinasi', 'Bukit pasir Zahek, Socotra', 450000, 7)
    perencana.tambah_item('destinasi', 'Gua Hoq, Socotra', 600000, 8)
    perencana.tambah_item('destinasi', 'Burj Khalifa observation deck, Dubai', 400000, 6)
    perencana.tambah_item('destinasi', 'Pegunungan Haggier, Socotra', 550000, 8)
    perencana.tambah_item('destinasi', 'Dataran Tinggi Diksam, Socotra', 350000, 7)
    
    # Penginapan (Motel)
    perencana.tambah_item('penginapan', 'Socotra Eco Lodge (5 malam)', 5000000, 7)
    perencana.tambah_item('penginapan', 'Camping di pantai Arher (2 malam)', 1000000, 9)
    perencana.tambah_item('penginapan', 'Hotel transit di Dubai (1 malam)', 2500000, 6)
    perencana.tambah_item('penginapan', 'Penginapan lokal di Hadiboh (2 malam)', 1200000, 5)
    perencana.tambah_item('penginapan', 'Camping di Diksam (1 malam)', 600000, 8)
    perencana.tambah_item('penginapan', 'Motel di Dubai (1 malam)', 1500000, 6)
    perencana.tambah_item('penginapan', 'Motel di Hadiboh (1 malam)', 800000, 5)
    
    # Kuliner
    perencana.tambah_item('kuliner', 'Seafood segar di restoran Qalansiyah', 800000, 8)
    perencana.tambah_item('kuliner', 'Makanan khas Yaman di Hadiboh', 600000, 7)
    perencana.tambah_item('kuliner', 'Makanan di camp selama perjalanan', 1500000, 6)
    perencana.tambah_item('kuliner', 'Kuliner Arab di Dubai', 1000000, 7)
    perencana.tambah_item('kuliner', 'Kopi dan camilan selama perjalanan', 900000, 5)
    perencana.tambah_item('kuliner', 'Makanan khas tradisional Socotri', 750000, 7)
    perencana.tambah_item('kuliner', 'Breakfast di hotel Dubai', 500000, 6)
    
    # Hidden Gems
    perencana.tambah_item('hidden gem', 'Laguna tersembunyi di Detwah, Socotra', 400000, 9)
    perencana.tambah_item('hidden gem', 'Desa tradisional di pegunungan Haggier', 700000, 8)
    perencana.tambah_item('hidden gem', 'Mata air alami Diksam', 350000, 7)
    perencana.tambah_item('hidden gem', 'Hutan pohon bottleneck yang langka', 300000, 8)
    perencana.tambah_item('hidden gem', 'Snorkeling di terumbu karang Shoab', 850000, 8)
    perencana.tambah_item('hidden gem', 'Desa nelayan tersembunyi di teluk Shoab', 600000, 7)
    
    # Tambahan
    perencana.tambah_item('kuliner', 'Suplai makanan darurat', 350000, 3)
    perencana.tambah_item('transportasi', 'Perahu ke Pantai Shoab', 650000, 6)
    perencana.tambah_item('hidden gem', 'Pemandian air panas alami', 450000, 7)
    perencana.tambah_item('kuliner', 'Perlengkapan makan camping', 250000, 3)
    
    item_pelengkap = buat_item_pelengkap(100000, 1000000, 50000)
    for item in item_pelengkap:
        perencana.tambah_item(item.kategori, item.nama, item.harga, item.nilai_kepuasan)
    
    # Mengukur waktu eksekusi
    start_time = time.time()  # Catat waktu mulai
    perencana.backtrack_rencana()
    end_time = time.time()  # Catat waktu selesai
    
    # Tampilkan waktu eksekusi
    print(f"Waktu eksekusi: {end_time - start_time:.2f} detik")
    
    perencana.cetak_itinerary()
    
    perencana.tampilkan_gui()

    # Logika Backtracking
# 1. Inisialisasi: Algoritma dimulai dengan inisialisasi variabel yang diperlukan, termasuk itinerary_saat_ini, indeks_saat_ini, biaya_saat_ini, nilai_saat_ini, dan kategori_saat_ini.
# 2. Pertimbangan Cuaca dan Delay: Sebelum melakukan backtracking, algoritma memeriksa kondisi cuaca dan delay. Jika cuaca buruk, nilai kepuasan untuk destinasi akan dikurangi. Jika ada delay, biaya tambahan akan ditambahkan ke biaya saat ini.
# 3. Basis Kasus: Jika anggaran habis dan semua kategori wajib terpenuhi, algoritma memeriksa apakah itinerary saat ini memiliki nilai kepuasan yang lebih tinggi daripada yang terbaik yang ditemukan sebelumnya. Jika ya, itinerary saat ini disimpan sebagai yang terbaik.
# 4. Rekursi: Algoritma mencoba untuk memasukkan item saat ini ke dalam itinerary. Jika berhasil, algoritma melanjutkan untuk memeriksa item berikutnya. Jika tidak, algoritma akan mencoba untuk melanjutkan tanpa item saat ini.
# 5. Backtrack: Jika tidak ada solusi yang ditemukan dengan memasukkan item saat ini, algoritma akan menghapus item tersebut dari itinerary dan melanjutkan untuk memeriksa item berikutnya.

# Kelebihan dan Kekurangan Pendekatan Backtracking
# Kelebihan:
# - Komprehensif: Backtracking menjelajahi semua kemungkinan kombinasi, sehingga dapat menemukan solusi optimal.
# - Fleksibilitas: Dapat digunakan untuk berbagai jenis masalah kombinatorial, termasuk perencanaan perjalanan, penjadwalan, dan pemecahan teka-teki.

# Kekurangan:
# - Waktu Eksekusi: Backtracking dapat menjadi sangat lambat untuk masalah besar karena kompleksitas waktu yang tinggi. Dalam kasus terburuk, waktu eksekusi dapat meningkat secara eksponensial.
# - Memori: Memerlukan lebih banyak memori untuk menyimpan semua kemungkinan kombinasi yang sedang dieksplorasi, yang dapat menjadi masalah untuk masalah besar.