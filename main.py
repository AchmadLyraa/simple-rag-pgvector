import psycopg2
from huggingface_hub import InferenceClient

HF_TOKEN = "your-huggingface-token"

conn = psycopg2.connect(
    dbname="chat_rag_pln",
    user="postgres",
    password="your-password",
    host="localhost",
    port=5432,
)
cur = conn.cursor()

client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

texts = [
    "PLN Nusantara Power Unit Pembangkitan Kaltim Teluk mendapatkan apresiasi dari Dirjen Gatrik atas kesiapsiagaan pasokan listrik andal menjelang Natal 2024 dan Tahun Baru 2025, menunjukkan kesiapan pasokan listrik di wilayah Kalimantan menjelang Nataru. PLN NP turut menetapkan Masa Siaga Nataru mulai 18 Desember 2024 sampai 8 Januari 2025 dengan lebih dari 81 ribu personel siaga guna memastikan listrik aman untuk masyarakat. Pada sistem kelistrikan Kalimantan, kebutuhan listrik mencapai 2.359 MW dengan pasokan tersedia 2.960 MW sehingga pasokan listrik berada dalam kondisi aman. Unit Pembangkitan Kaltim Teluk memiliki kapasitas 2 x 110 MW dengan total 220 MW dan produksi energi rata-rata 1,15 juta MWh per tahun. Teknologi seperti Electrostatic Precipitator dan Distributed Control System membantu efisiensi dan pengendalian operasional pembangkit.&#10;(Source: plnnusantarapower.co.id press release) :contentReference[oaicite:0]{index=0}",
    "Direktur Utama PLN Nusantara Power menyatakan bahwa persiapan menjelang Nataru dilaksanakan jauh hari sebelumnya melalui posko siaga dan monitoring 24 jam nonstop oleh karyawan untuk memastikan keandalan pasokan listrik di UP Kaltim Teluk, serta kesiapan operasional pembangkit dalam mendukung kebutuhan energi masyarakat dan industri di Kalimantan.&#10;(Source: plnnusantarapower.co.id press release) :contentReference[oaicite:1]{index=1}",
    "PLN Suku Cadang telah menyelesaikan pengiriman suku cadang dan material critical part untuk pemeliharaan unit pembangkit di Kaltim Teluk agar pembangkit dapat beroperasi kembali setelah masa pemeliharaan, dengan tujuan mempercepat proses overhaul demi keandalan pasokan listrik di wilayah Kalimantan, dimana PLTU Kaltim Teluk berkapasitas 2×110 MW menjadi penopang utama keandalan listrik di regional ini.&#10;(Source: plnsc.co.id siaran pers) :contentReference[oaicite:2]{index=2}",
    "PLN Suku Cadang menyatakan critical part akan segera dipasang untuk mempercepat pemulihan operasional pembangkit dan mendukung keandalan listrik di Kalimantan, menggambarkan peran penting manajemen suku cadang dalam menjaga sistem ketenagalistrikan di wilayah pembangkit.&#10;(Source: plnsc.co.id siaran pers) :contentReference[oaicite:3]{index=3}",
]

# Tambahin 'passage: ' ke setiap teks buat model E5 sesuai dokumentasi
formatted_texts = [f"passage: {t}" for t in texts]

# Ambil embedding
# Output berupa list of lists (setiap list adalah vektor)
embeddings = client.feature_extraction(
    formatted_texts,
    model="intfloat/multilingual-e5-large",
)

cur.execute("TRUNCATE TABLE rag_test RESTART IDENTITY;")

# Masukkan ke Database
for original_text, emb in zip(texts, embeddings):
    # Tambahkan .tolist() biar jadi List Python biasa, bukan NumPy array
    vector_list = emb.tolist() if hasattr(emb, "tolist") else emb

    cur.execute(
        "INSERT INTO rag_test (konten, vektor_ai) VALUES (%s, %s)",
        (original_text, vector_list),
    )

conn.commit()
print("Data berhasil masuk!")
cur.close()
conn.close()
