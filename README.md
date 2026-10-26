# Laporan Tugas: Spesifikasi dan Standardisasi REST API

## Identitas Proyek

- Proyek: Tugas Backend 5
- Framework: Flask
- Versi API: v1 (`/api/v1`)
- Repository GitHub: Belum diunggah. Remote lokal saat ini menunjuk ke [repository Tugas Backend 4](https://github.com/jamalthaariq-student/tugas-backend-modular-app-p4), bukan tujuan yang terkonfirmasi untuk tugas ini.
- Link laporan Google Drive: [Tempelkan link file Google Drive setelah laporan diunggah]
- Learning Class STIKOM: [Kirim link Google Drive laporan pada kelas]

## Tujuan dan Desain

API menyediakan resource `categories` dan `items` yang berelasi. Setiap item mengacu pada kategori melalui field `category` yang berisi nama kategori. Kategori dan produk dapat ditelusuri melalui `GET /api/v1/categories` dan `GET /api/v1/items`; daftar item juga dapat difilter memakai query `category` dan `min_price`.

Endpoint versi pertama memakai prefix `/api/v1` agar perubahan kontrak berikutnya dapat diperkenalkan sebagai versi baru tanpa mengubah klien versi lama. Aplikasi memisahkan routing, service, dan repository. Seluruh endpoint menggunakan `success_response` atau `fail_response` dari `app/utils/response_helper.py`. Error validasi memuat nama field dan alasan kesalahannya.

## Tabel Spesifikasi Endpoint

| Method | URI                       | Input                                                                                                                                                          | Respons sukses                                                                | Respons gagal                                                                                                          |
| ------ | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| GET    | `/api/v1/categories`      | Tidak ada                                                                                                                                                      | `200 OK`; `data.categories` adalah daftar kategori dan `data.total` jumlahnya | Tidak ada kegagalan bisnis yang didefinisikan                                                                          |
| GET    | `/api/v1/items`           | Query opsional: `category` (string), `min_price` (integer)                                                                                                     | `200 OK`; `data.items` berisi hasil dan `data.total` jumlahnya                | `min_price` yang tidak dapat diparse sebagai integer tidak menghasilkan error; parser Flask mengembalikan nilai kosong |
| GET    | `/api/v1/items/<item_id>` | `item_id` integer pada URI                                                                                                                                     | `200 OK`; `data` berisi item                                                  | `404 Not Found`; `errors` berisi `field: item_id` dan alasan barang tidak ditemukan                                    |
| POST   | `/api/v1/items`           | JSON object wajib berisi `name` string nonkosong, `category` dari daftar kategori, `price` angka lebih besar dari 0; `stock` opsional integer >= 0 (default 0) | `201 Created`; `data` berisi item baru                                        | `400 Bad Request`; `errors` mencantumkan setiap field dan alasan validasi                                              |
| PUT    | `/api/v1/items/<item_id>` | JSON object parsial; field yang didukung: `name`, `category`, `price`, `stock`                                                                                 | `200 OK`; `data` berisi item setelah diperbarui                               | `400 Bad Request` untuk nilai tidak valid; `404 Not Found` untuk ID yang tidak ada                                     |
| DELETE | `/api/v1/items/<item_id>` | `item_id` integer pada URI                                                                                                                                     | `200 OK`; pesan penghapusan berhasil                                          | `404 Not Found`; `errors` berisi `field: item_id` dan alasan barang tidak ditemukan                                    |
| GET    | `/api/v1/users`           | Tidak ada                                                                                                                                                      | `200 OK`; `data.users` dan `data.total`                                       | Tidak ada kegagalan bisnis yang didefinisikan                                                                          |
| POST   | `/api/v1/users`           | JSON object dengan `username` nonkosong, `email` dengan format dasar yang memuat `@`, dan `role: "user"`                                                       | `201 Created`; `data` berisi user baru                                        | `400 Bad Request`; `errors` menyebut field dan alasan, termasuk jika Content-Type bukan JSON                           |

Semua request yang mengirim body harus menggunakan `Content-Type: application/json`.

## Format Respons

Contoh sukses:

```json
{
  "status": "success",
  "message": "Success",
  "data": {
    "categories": [{ "id": 1, "name": "Elektronik" }],
    "total": 1
  }
}
```

Contoh gagal validasi:

```json
{
  "status": "fail",
  "message": "Input tidak valid",
  "errors": [{ "field": "price", "reason": "Harga harus lebih besar dari 0" }]
}
```

## Aturan Validasi

- `name` wajib berupa string dan tidak boleh kosong.
- `category` untuk produk wajib cocok dengan kategori yang tersedia.
- `price` wajib berupa angka yang lebih besar dari 0.
- `stock` opsional saat membuat item, default-nya `0`, dan harus berupa bilangan bulat nonnegatif.
- `PUT` mendukung pembaruan parsial; field yang tidak dikirim tidak diubah.
- `username` wajib nonkosong dan `email` wajib memuat `@`.
- `role` pada registrasi wajib bernilai `user`.
- ID yang tidak ditemukan menghasilkan status `404` dengan field serta alasan kesalahan.

## Cara Menjalankan dan Verifikasi

Jalankan `pip install -r requirements.txt`, lalu `python run.py`. Server lokal tersedia pada `http://127.0.0.1:5000`.

Verifikasi menggunakan Flask test client sebelumnya mencakup 11 skenario kategori, item, dan user. Pengujian tersebut dilakukan sebelum field `stock` ditambahkan; perubahan `stock` belum diverifikasi ulang dengan test client.

