# Logistic Management ERP

Modul ``logistic_shipment`` dan ``shipment_tracking`` dibuat untuk mempermudah manajemen pengiriman barang di Odoo. Modul ``logistic_shipment`` berfokus pada pembuatan dan pengelolaan pengiriman, termasuk menentukan channel, jenis layanan, pengirim, penerima, berat, deskripsi barang, serta perhitungan otomatis tanggal jatuh tempo berdasarkan tipe layanan. Modul ini juga menampilkan status pengiriman terakhir secara otomatis berdasarkan data tracking.

Modul ``shipment_tracking`` berfungsi untuk memantau setiap update pengiriman secara detail, mencatat timestamp, drop point, lokasi, status, catatan, dan penanggung jawab. Modul ini terintegrasi dengan ``logistic_shipment`` sehingga setiap update tracking otomatis memperbarui status shipment. Dengan kombinasi kedua modul ini, pengguna dapat membuat shipment, memantau status pengiriman secara real-time, dan melihat history pergerakan barang, sehingga proses logistik menjadi lebih efisien dan transparan.

## Setup Odoo 19 dengan Docker

Proyek ini menjalankan Odoo 19 dengan PostgreSQL 16 menggunakan Docker Compose. Addons kustom, log, dan konfigurasi Odoo di-mount dari host.

### Struktur Folder
odoo19/
├── odoo/                   # Kode sumber Odoo
├── custom_addons/          # Modul Odoo kustom
├── config/                 # docker-compose.yml
│   └── docker-compose.yml
├── logs/                   # Log Odoo
└── data/                   # Data PostgreSQL

## Prasyarat

- Docker Desktop
- WSL 2 backend aktif (untuk Windows)
- Port 8069 (Odoo) dan 5432 (PostgreSQL)

## Langkah Instalasi

1. Buka terminal di folder config:
```cd ~/odoo19/config```

2. Build dan jalankan container:
```docker compose up -d```

3. Cek container yang sedang berjalan:
```docker compose ps```

## Akses Layanan

1. Odoo: http://localhost:8069
2. PostgreSQL: 
    ```
    host: db, 
    port: 5432, 
    database: ODOO_DB
    user: odoo, 
    password: odoo, 

    ```

## Volumes

```
../custom_addons:/mnt/extra-addons → mount modul kustom

../logs:/var/log/odoo → log Odoo

../data/db:/var/lib/postgresql/data → data PostgreSQL persisten

../odoo/debian/odoo.conf:/etc/odoo/odoo.conf → file konfigurasi Odoo
```

## Stop / Hapus Container
Perintah ini menghentikan dan menghapus container, tetapi volume persisten tetap ada.
```docker compose down```