import psycopg2
from huggingface_hub import InferenceClient

HF_TOKEN = "your-huggingface-token"

# 1. Koneksi ke PostgreSQL
# Database ini menyimpan teks (konten) dan embedding vektornya (pgvector)
conn = psycopg2.connect(
    dbname="chat_rag_pln",
    user="postgres",
    password="your-password",
    host="localhost",
    port=5432,
)
cur = conn.cursor()

# Client HuggingFace untuk generate embedding
client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

# 2. Pertanyaan dari user (natural language)
query = "Kegiatan PLN pas Natal 2024 dan 2025 ngapain?"

# Model E5 membedakan QUERY dan PASSAGE saat training,
# maka teks pencarian WAJIB diawali prefix "query: "
query_text = f"query: {query}"

# 3. Ubah pertanyaan menjadi embedding vektor (1024 dimensi)
query_vector_raw = client.feature_extraction(
    query_text, model="intfloat/multilingual-e5-large"
)

# Pastikan embedding berbentuk list Python,
# karena psycopg2 tidak bisa langsung terima object numpy / tensor
query_vector = (
    query_vector_raw.tolist()
    if hasattr(query_vector_raw, "tolist")
    else query_vector_raw
)

# 4. Pencarian ke database menggunakan similarity vektor
# Operator <=> adalah cosine distance dari pgvector
# - nilai/jarak mendekati 0  -> makin mirip
# - nilai/jarak mendekati 1  -> makin tidak mirip
cur.execute(
    """
    SELECT
        konten,
        vektor_ai <=> %s::vector AS distance
    FROM rag_test
    ORDER BY distance ASC
    LIMIT 2;
    """,
    (query_vector,),
)

results = cur.fetchall()

# 5. Tampilkan hasil retrieval
print(f"\nPERTANYAAN: {query}\n")
print("HASIL PALING RELEVAN:")
for row in results:
    display_score = 1 - row[1]
    print(f"--- (Similarity ~): {round(display_score, 4)} ---")
    print(f"{row[0]}\n")

# 6. Tutup koneksi database
cur.close()
conn.close()
