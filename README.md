# Simple RAG with PostgreSQL + pgvector

Ini contoh **RAG paling dasar** buat belajar konsep retrieval pakai vector database.

Simpel:

- Dokumen/teks → embedding → simpan ke PostgreSQL
- Pertanyaan → embedding → cari vector terdekat di database → ambil teksnya

## Intinya

* 1 chunk = 1 embedding = 1 row di tabel
* Similarity tinggi = distance rendah
* Cosine dipakai buat ngukur kemiripan arah vektor
* Database cuma nyimpen dan ngitung jarak

## Catatan Penting

* Model E5:

  * Dokumen pakai format awalan `passage:`
  * Pertanyaan pakai format awalan `query:`
* `::vector` cuma perlu saat SELECT
* INSERT langsung kirim array, PostgreSQL yang ngurus

## Contoh Output
```
PERTANYAAN: Kegiatan PLN pas Natal 2024 dan 2025 ngapain?

HASIL PALING RELEVAN:
--- (Similarity ~): 0.8619 ---
PLN Nusantara Power Unit Pembangkitan Kaltim Teluk mendapatkan apresiasi dari Dirjen Gatrik atas kesiapsiagaan pasokan listrik andal menjelang Natal 2024 dan Tahun Baru 2025, menunjukkan kesiapan pasokan listrik di wilayah Kalimantan menjelang Nataru. PLN NP turut menetapkan Masa Siaga Nataru mulai 18 Desember 2024 sampai 8 Januari 2025 dengan lebih dari 81 ribu personel siaga guna memastikan listrik aman untuk masyarakat. Pada sistem kelistrikan Kalimantan, kebutuhan listrik mencapai 2.359 MW dengan pasokan tersedia 2.960 MW sehingga pasokan listrik berada dalam kondisi aman. Unit Pembangkitan Kaltim Teluk memiliki kapasitas 2 x 110 MW dengan total 220 MW dan produksi energi rata-rata 1,15 juta MWh per tahun. Teknologi seperti Electrostatic Precipitator dan Distributed Control System membantu efisiensi dan pengendalian operasional pembangkit.&#10;(Source: plnnusantarapower.co.id press release) :contentReference[oaicite:0]{index=0}

--- (Similarity ~): 0.825 ---
Direktur Utama PLN Nusantara Power menyatakan bahwa persiapan menjelang Nataru dilaksanakan jauh hari sebelumnya melalui posko siaga dan monitoring 24 jam nonstop oleh karyawan untuk memastikan keandalan pasokan listrik di UP Kaltim Teluk, serta kesiapan operasional pembangkit dalam mendukung kebutuhan energi masyarakat dan industri di Kalimantan.&#10;(Source: plnnusantarapower.co.id press release) :contentReference[oaicite:1]{index=1}
```

DDL:
```
CREATE DATABASE chat_rag_pln;
\c chat_rag_pln;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE rag_test (id serial primary key, content text, embedding vector(1024));
```
