import numpy as np
from numpy import inf
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import messagebox
from dataJarak import d
from lokasi import lokasi_values
import time


def findroute():
    if not any(var.get() for var in tujuan_vars):
        messagebox.showerror("Error", "Pilih setidaknya satu lokasi tujuan.")
        return

    # Inisialisasi nilai langsung di sini
    iteration = 200
    n_ants = 20 
    alpha = 1
    beta = 5

    lokasi_awal_index = lokasi_values.index(lokasi_awal_combobox.get())
    if lokasi_awal_index is None or not any(var.get() for var in tujuan_vars):
        messagebox.showerror("Error", "Pilih lokasi awal dan tujuan yang valid.")
        return

    selected_indices = [lokasi_awal_index] + [i for i, var in enumerate(tujuan_vars) if var.get()]
    n_citys = len(selected_indices)

    # Mulai pengukuran waktu
    start_time = time.time()

    m = n_ants
    n = n_citys
    e = 0.9

    # Perhitungan rute untuk semua lokasi
    d[d == 0] = 1e-10
    visibility = 1 / d  # Menghindari pembagian dengan nol

    pheromone = .1 * np.ones((len(d), len(d)))

    best_cost = np.inf
    best_route = None
    best_iteration = None

    for ite in range(iteration):
        routes = np.ones((m, len(d) + 1))

        for i in range(m):
            temp_visibility = np.array(visibility)

            for j in range(len(d) - 1):
                combine_feature = np.zeros(len(d))
                cum_prob = np.zeros(len(d))

                cur_loc = int(routes[i, j] - 1)
                temp_visibility[:, cur_loc] = 0

                p_feature = np.power(pheromone[cur_loc, :], alpha)
                v_feature = np.power(temp_visibility[cur_loc, :], beta)

                combine_feature = p_feature * v_feature
                total = np.sum(combine_feature)

                probs = combine_feature / total
                cum_prob = np.cumsum(probs)

                r = np.random.random_sample()
                city = np.nonzero(cum_prob > r)[0][0] + 1

                routes[i, j + 1] = city

            left = list(set(range(1, len(d) + 1)) - set(routes[i, :-2]))[0]
            routes[i, -2] = left
            routes[i, -1] = 1

        route_opt = np.array(routes)
        dist_cost = np.zeros((m, 1))

        for i in range(m):
            s = 0
            for j in range(len(d)):
                s += d[int(route_opt[i, j]) - 1, int(route_opt[i, j + 1]) - 1]

            dist_cost[i] = s

        dist_min_loc = np.argmin(dist_cost)
        dist_min_cost = dist_cost[dist_min_loc][0]

        if dist_min_cost < best_cost:
            best_cost = dist_min_cost
            best_route = routes[dist_min_loc, :]
            best_iteration = ite + 1

        pheromone = (1 - e) * pheromone

        for i in range(m):
            for j in range(len(d)):
                dt = 1 / dist_cost[i][0]
                pheromone[int(route_opt[i, j]) - 1, int(route_opt[i, j + 1]) - 1] += dt

    # Mengambil indeks dan nama rute yang dipilih dengan lokasi awal sebagai yang pertama dan terakhir
    selected_route_indices = [int(i) - 1 for i in best_route if int(i) - 1 in selected_indices]
    if selected_route_indices[0] != lokasi_awal_index:
        selected_route_indices = [lokasi_awal_index] + selected_route_indices
    if selected_route_indices[-1] != lokasi_awal_index:
        selected_route_indices = selected_route_indices + [lokasi_awal_index]

    selected_route_names = [lokasi_values[i] for i in selected_route_indices]

    # Menghitung jarak hanya untuk lokasi yang dipilih dengan urutan rute
    selected_route_distances = [d[selected_route_indices[i], selected_route_indices[i + 1]] for i in range(len(selected_route_indices) - 1)]

    # Debug print statement
    #for i in range(len(selected_route_indices) - 1):
       # print(f"Jarak dari {lokasi_values[selected_route_indices[i]]} ke {lokasi_values[selected_route_indices[i + 1]]} = {d[selected_route_indices[i], selected_route_indices[i + 1]]}")

    selected_cost = sum(selected_route_distances)
    print(f'Total jarak yang dihitung: {selected_cost}')

    #Selesai pengukuran waktu
    end_time = time.time()
    computation_time = end_time - start_time

    #Tampilkan waktu komputasi di terminal
    print(f"Waktu komputasi: {computation_time:.4f} detik")
    print(' > '.join(selected_route_names))

    hasilRute.set(' -> '.join(selected_route_names))
    totalJarak.set(f'{selected_cost}')
    nomorIterasi.set(f'{best_iteration}')
    hasilRuteIndeks.set(f'{selected_route_indices}')

def reset_ui():
    for var in tujuan_vars:
        var.set(0)
    hasilRute.set('')
    totalJarak.set('')
    nomorIterasi.set('')
    hasilRuteIndeks.set('')
    lokasi_awal_combobox.set('')


# Membuat UI menggunakan tkinter
root = tk.Tk()
root.title("Aplikasi Pencarian Rute terpendek Lokasi Wisata di Kota Palembang Menggunakan Algoritma Ant Colony Optimization")
root.geometry("1065x800")
root.resizable(False, False)
root.configure(bg="darkcyan")

#Widget untuk frame
label_frame = tk.Frame(root, bg="lavender", highlightbackground="black", highlightcolor="black", highlightthickness=2)
label_frame.place(x=20, y=20, anchor="nw")

lokasi_tujuan_frame = tk.Frame(root, bg="Lavender", highlightbackground="black", highlightcolor="black", highlightthickness=2)
lokasi_tujuan_frame.place(x=20, y=75, anchor="nw")

cari_rute_frame = tk.Frame(root, bg="lavender", highlightbackground="black", highlightcolor="black", highlightthickness=2)
cari_rute_frame.place(x=20, y=460)

jarak_frame = tk.Frame(root, bg="lavender", highlightbackground="black", highlightcolor="black", highlightthickness=2)
jarak_frame.place(x=20, y=558, anchor="nw")

hasilRute_frame = tk.Frame(root, bg="skyblue", highlightbackground="black", highlightcolor="black", highlightthickness=2)
hasilRute_frame.place(x=385, y=20, anchor="nw")

nomor_indeks_frame = tk.Frame(root, bg="skyblue", highlightbackground="black", highlightcolor="black", highlightthickness=2)
nomor_indeks_frame.place(x=385, y=348, anchor="nw")


#label untuk inisialisasi nama variabel
label_awal = tk.Label(label_frame, text="LOKASI AWAL", font="arial 10 bold", bg="Lavender", fg="black")
label_awal.grid(row=0, column=0, padx=10, pady=10)

label_tujuan = tk.Label(label_frame, text="LOKASI TUJUAN", font="arial 10 bold", bg="Lavender", fg="black")
label_tujuan.grid(row=1, column=0, padx=10, pady=10)

label_iterasi = tk.Label(label_frame, text="JUMLAH ITERASI", font="arial 10 bold", bg="Lavender", fg="black")
label_iterasi.grid(row=2, column=0, padx=10, pady=10)

label_semut = tk.Label(label_frame, text="JUMLAH SEMUT", font="arial 10 bold", bg="Lavender", fg="black")
label_semut.grid(row=3, column=0, padx=10, pady=10)

label_alpha = tk.Label(label_frame, text="Alpha", font="arial 10 bold", bg="Lavender", fg="black")
label_alpha.grid(row=4, column=0, padx=10, pady=10)

label_beta = tk.Label(label_frame, text="Beta", font="arial 10 bold", bg="Lavender", fg ="black")
label_beta.grid(row=5, column=0, padx=10, pady=10)

label_jarak = tk.Label(jarak_frame, text="TOTAL JARAK", font="arial 10 bold", bg="Lavender", fg ="black")
label_jarak.grid(row=1, column=0, padx=(25,10), pady=10)

label_iterasi = tk.Label(jarak_frame, text="ITERASI", font="arial 10 bold", bg="Lavender", fg ="black")
label_iterasi.grid(row=0, column=0, padx=(25,10), pady=10)

#widget untuk menampilkan lokasi awal dan lokasi tujuan
lokasi_awal = tk.StringVar()
lokasi_awal.set(lokasi_values[0])  # Inisialisasi dengan nilai awal

lokasi_tujuan = tk.StringVar()
lokasi_tujuan.set(lokasi_values[0])

tujuan_vars = {}
lokasi_awal_combobox = Combobox(label_frame, values=lokasi_values, font="arial 10", state="r", width=27)
lokasi_awal_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

lokasi_tujuan_checkbox = tk.Canvas(label_frame, height=200, width=190, highlightbackground="black", highlightcolor="black", highlightthickness=1)
scrollbar = tk.Scrollbar(label_frame, orient="vertical", command=lokasi_tujuan_checkbox.yview, highlightbackground="black", highlightcolor="black", highlightthickness=1)
scrollable_frame = ttk.Frame(lokasi_tujuan_checkbox)

scrollable_frame.bind(
    "<Configure>",
    lambda e: lokasi_tujuan_checkbox.configure(
        scrollregion=lokasi_tujuan_checkbox.bbox("all")
    )
)

lokasi_tujuan_checkbox.create_window((0, 0), window=scrollable_frame, anchor="nw")
lokasi_tujuan_checkbox.configure(yscrollcommand=scrollbar.set)

tujuan_vars = [tk.IntVar() for _ in lokasi_values]
tujuan_checkbuttons = [tk.Checkbutton(scrollable_frame, text=lokasi, variable=var) for lokasi, var in zip(lokasi_values, tujuan_vars)]
for cb in tujuan_checkbuttons:
    cb.pack(anchor='w')

lokasi_tujuan_checkbox.grid(row=1, column=1,pady=10, sticky="nsew")
scrollbar.grid(row=1, column=2,padx=10, pady=10, sticky="ns")

# Konfigurasi grid untuk lokasi_tujuan_frame agar scrollbar mengisi ruang yang tersedia
lokasi_tujuan_frame.grid_columnconfigure(0, weight=1)
lokasi_tujuan_frame.grid_rowconfigure(0, weight=1)


hasilRute = tk.StringVar()
hasilRute.set('')

totalJarak = tk.StringVar()
totalJarak.set('')

nomorIterasi = tk.StringVar()
nomorIterasi.set('')

hasilRuteIndeks = tk.StringVar()
hasilRuteIndeks.set('')

#widget untuk menampilkan nilai iterasi dan total jarak
iterasi_ke = tk.Label(jarak_frame, textvariable=nomorIterasi,width=25, height=1,bd=2, bg="white")
iterasi_ke.grid(row=0, column=1, padx=(12,25), pady=12, sticky="w")

total_jarak = tk.Label(jarak_frame, textvariable= totalJarak, width=25, height=1,bd=2, bg="white", wraplength=630,anchor="nw", justify="left")
total_jarak.grid(row=1, column=1, padx=(12,25), pady=12, sticky="w")

#widget untuk menampilkan hasil rute dan indeks hasil rute
rute_terpendek = tk.Label(hasilRute_frame, textvariable= hasilRute, width=90, height=19,bd=2, bg="white", wraplength=630,anchor="nw", justify="left")
rute_terpendek.grid(row=0, column=0, padx=10, pady=10, sticky="w")

rute_terpendek_indeks_label = tk.Label(nomor_indeks_frame, textvariable=hasilRuteIndeks, width=90, height=7, bd=2, bg="white", wraplength=630, anchor="nw", justify="left")
rute_terpendek_indeks_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

#widget tombol
tombol_cari_rute = tk.Button(cari_rute_frame, text="Cari Rute", bg="black", fg="white", width=22, command=findroute)
tombol_cari_rute.grid(row=0, column=0, padx=5, pady=8, sticky="n")

tombol_inform_wisata = tk.Button(cari_rute_frame, text="Informasi Wisata", bg="black", fg="white", width=22)
tombol_inform_wisata.grid(row=0, column=1, padx=5, pady=8, sticky="n")

tombol_panduan = tk.Button(cari_rute_frame, text="Panduan", bg="black", fg="white", width=22)
tombol_panduan.grid(row=1, column=0, padx=5, pady=8, sticky="n")

tombol_reset = tk.Button(cari_rute_frame, text="Reset", bg="black", fg="white", width=22, command=reset_ui)
tombol_reset.grid(row=1, column=1, padx=5, pady=8, sticky="n")

root.mainloop()
