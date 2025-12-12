# Logistic Management ERP (Use Case)

Proyek ini adalah studi kasus (use case) yang mencontohkan bagaimana sistem manajemen logistik dapat dibuat menggunakan Odoo 19. Modul ini tidak ditujukan untuk penggunaan produksi, melainkan sebagai contoh arsitektur, alur kerja, dan fitur dasar yang umum digunakan pada sistem logistik.

## Modul Utama

1. logistic_shipment
Digunakan untuk membuat dan mengelola data pengiriman.

Fitur:
- Pengaturan channel / marketplace (Shopee, Tokopedia, dll)
- Pemilihan service type (regular, express, cargo)
- Data pengirim & penerima
- Berat & deskripsi barang
- Perhitungan otomatis due date berdasarkan service type
- Status pengiriman yang berubah otomatis berdasarkan tracking terbaru

2. shipment_tracking
Digunakan untuk mencatat setiap update perjalanan paket.

Data yang ditracking:
- Timestamp
- Drop point
- Lokasi
- Status (drop_off, in_transit, delivered, dll)
- Catatan tambahan
- Petugas yang menangani
- Tracking terhubung langsung dengan shipment untuk menampilkan status real-time.

## Fitur Tambahan: Laporan (Report PDF)

Use case ini juga menyertakan contoh implementasi dua jenis laporan yang dapat diunduh dari Odoo.

1. Shipment Detail Report

Detail laporan mengenai shipment.

Berisi:
- Informasi shipment
- Tanggal & status
- Nama pengirim & penerima
- Deskripsi Barang
- Tracking History

2. Shipment Label

Label kecil untuk ditempelkan ke paket.

Berisi:
- Shipment ID
- Nama pengirim & penerima
- Service type
- Berat barang
- Channel
- Deskripsi barang

## Setup Odoo 19 dengan Docker

Proyek ini menjalankan Odoo 19 dengan PostgreSQL 16 menggunakan Docker Compose. Addons kustom, log, dan konfigurasi Odoo di-mount dari host.

### Struktur Folder

```
odoo19/
├── odoo/                   # Kode sumber Odoo
├── custom_addons/          # Modul Odoo kustom
├── config/                 # docker-compose.yml
│   └── docker-compose.yml
├── logs/                   # Log Odoo
└── data/                   # Data PostgreSQL
```

## Prasyarat

- Docker Desktop
- WSL 2 backend aktif (untuk Windows)
- Port 8069 (Odoo) dan 5432 (PostgreSQL)

## Langkah Instalasi

1. Install wkhtmltopdf (Konversi HTML menjadi pdf)
```
sudo apt update
sudo apt install -y wkhtmltopdf
```

2. Install Python3
```
sudo apt install python3-pip
```

3. Install passlib (dengan venv)
```
source odoo19/odoo/venv/bin/activate 
pip install passlib
deactivate
```

4. Buka terminal di folder config:
```cd ~/odoo19/config```

5. Initialize database dan jalankan container:
```
docker compose up -d
docker exec -it config-odoo-1 odoo -c /etc/odoo/odoo.conf -d ODOO_DB -i base --stop-after-init
docker compose up -d
```


6. Cek container yang sedang berjalan:
```docker compose ps```

## Akses Layanan

1. Odoo: 
    ```
    url: http://localhost:8069
    email: admin
    password: admin
    database: ODOO_DB
    ```
    
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