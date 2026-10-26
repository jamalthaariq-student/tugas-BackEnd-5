# Tugas Backend 5: REST API Flask

REST API sederhana untuk mengelola kategori, item/produk, dan user. Aplikasi menggunakan Flask Blueprint dan memisahkan routing, validasi/logika bisnis, serta penyimpanan data mock.

## Struktur Proyek

```text
app/
├── __init__.py
├── config.py
├── repositories/
│   ├── product_repo.py
│   └── user_repo.py
├── routes/v1/
│   ├── product_routes.py
│   └── users_routes.py
├── services/
│   ├── product_service.py
│   └── user_service.py
└── utils/response_helper.py
run.py
requirements.txt
README.md
LAPORAN_TUGAS.md
```

Route menerima HTTP request dan mengembalikan respons melalui `response_helper.py`. Service menjalankan validasi dan logika bisnis. Repository mengelola data mock untuk produk/kategori dan user secara terpisah.

## Persiapan dan Menjalankan

Pastikan Python tersedia, lalu jalankan dari direktori proyek:

```bash
pip install -r requirements.txt
python run.py
```

Server berjalan pada `http://127.0.0.1:5000`.

## API v1

Semua endpoint memakai prefix `/api/v1`. Relasi produk dan kategori ditunjukkan oleh field `category` pada setiap item, yang nilainya harus cocok dengan nama kategori tersedia. Request dengan body harus menggunakan `Content-Type: application/json`.

| Method | URI                       | Input                                              | Respons sukses                                   | Respons gagal                                               |
| ------ | ------------------------- | -------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------- |
| GET    | `/api/v1/categories`      | Tidak ada                                          | `200`; daftar kategori dan jumlahnya pada `data` | Tidak ada kegagalan bisnis yang didefinisikan               |
| GET    | `/api/v1/items`           | Query opsional `category` dan `min_price`          | `200`; daftar item dan jumlah hasil pada `data`  | `min_price` yang bukan integer tidak dipakai sebagai filter |
| GET    | `/api/v1/items/<item_id>` | ID integer di URI                                  | `200`; item pada `data`                          | `404`; error berisi field `item_id` dan alasan              |
| POST   | `/api/v1/items`           | `name`, `category`, `price`; `stock` opsional      | `201`; item baru pada `data`                     | `400`; error validasi berisi field dan alasan               |
| PUT    | `/api/v1/items/<item_id>` | JSON parsial: `name`, `category`, `price`, `stock` | `200`; item yang diperbarui pada `data`          | `400`; input tidak valid. `404`; item tidak ditemukan       |
| DELETE | `/api/v1/items/<item_id>` | ID integer di URI                                  | `200`; pesan berhasil dihapus                    | `404`; error berisi field `item_id` dan alasan              |
| GET    | `/api/v1/users`           | Tidak ada                                          | `200`; daftar user dan jumlahnya pada `data`     | Tidak ada kegagalan bisnis yang didefinisikan               |
| POST   | `/api/v1/users`           | `username`, `email`, dan `role: "user"`            | `201`; user baru pada `data`                     | `400`; error validasi berisi field dan alasan               |

### Contoh Request

Menambahkan item. Harga wajib lebih besar dari 0; stok harus berupa bilangan bulat nonnegatif dan default-nya `0` jika tidak dikirim.

```json
{
  "name": "Kaos Sablon",
  "category": "Pakaian",
  "price": 100000,
  "stock": 8
}
```

Mendaftarkan user:

```json
{
  "username": "pengguna_baru",
  "email": "pengguna@example.com",
  "role": "user"
}
```

## Format Respons

Respons sukses menggunakan format berikut:

```json
{
  "status": "success",
  "message": "Success",
  "data": {}
}
```

Respons gagal validasi menyebut field dan alasannya:

```json
{
  "status": "fail",
  "message": "Input tidak valid",
  "errors": [{ "field": "price", "reason": "Harga harus lebih besar dari 0" }]
}
```

## Aturan Data

- Nama item wajib berupa teks yang tidak kosong.
- Kategori item harus tersedia pada resource kategori.
- Harga item harus berupa angka lebih besar dari 0.
- Stok item harus berupa bilangan bulat `0` atau lebih.
- Data disimpan pada list mock dalam memori; perubahan akan kembali ke data awal ketika aplikasi dimulai ulang.

