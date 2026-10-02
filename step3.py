from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import ollama

# 1. Nقraw w nقassmou l'PDF (kima Step 2)
reader = PdfReader("test.pdf")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = []
for i, page in enumerate(reader.pages):
    texte = page.extract_text()
    if texte:
        for morceau in splitter.split_text(texte):
            chunks.append({"page": i + 1, "texte": morceau})

# 2. Nخلqou base ChromaDB (tتخzen fi dossier "db")
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("documents")

# 3. Kol chunk: nخرjou vecteur w nخzznouh
for n, c in enumerate(chunks):
    reponse = ollama.embed(model="nomic-embed-text", input=c["texte"])
    vecteur = reponse["embeddings"][0]
    collection.upsert(
        ids=[f"chunk_{n}"],
        embeddings=[vecteur],
        documents=[c["texte"]],
        metadatas=[{"page": c["page"]}],
    )

print("Chunks stockes:", collection.count())

# 4. Test: nقلbou 3la chunk yجawb sou2el
question = "Chnowa l'penalite ken ta2khrou fil paiement ?"
q_vecteur = ollama.embed(model="nomic-embed-text", input=question)["embeddings"][0]
resultats = collection.query(query_embeddings=[q_vecteur], n_results=2)

print("\nQuestion:", question)
for doc, meta in zip(resultats["documents"][0], resultats["metadatas"][0]):
    print(f"\n--- Page {meta['page']} ---")
    print(doc)