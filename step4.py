import chromadb
import ollama

# 1. Nفtho ChromaDB li 3malnah fi Step 3 (ma nعawdouch l'embeddings)
client = chromadb.PersistentClient(path="db")
collection = client.get_collection("documents")


def repondre(question):
    # 2. Nلقaw l'3 chunks l'a9rab lel sou2el
    q_vecteur = ollama.embed(model="nomic-embed-text", input=question)["embeddings"][0]
    res = collection.query(query_embeddings=[q_vecteur], n_results=3)

    # 3. Nجهzou l'contexte (kol chunk m3a numéro page)
    contexte = ""
    pages = []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        contexte += f"[Page {meta['page']}] {doc}\n\n"
        pages.append(meta["page"])

    # 4. Nكتbou l'prompt: l'LLM yjaweb bark men l'contexte
    prompt = f"""Tu es un assistant pour un cabinet d'audit.
Reponds a la question en utilisant UNIQUEMENT le contexte ci-dessous.
Si la reponse n'est pas dans le contexte, dis: "Je ne trouve pas la reponse dans les documents."
Reponds en francais, de facon courte, et cite la page entre parentheses.

CONTEXTE:
{contexte}

QUESTION: {question}

REPONSE:"""

    # 5. Nب3thou lel LLM local
    rep = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return rep["message"]["content"], sorted(set(pages))


# 6. Boucle: tنجem tos2el barcha marrat
while True:
    q = input("\nSou2elek (wella 'q' bech tخرj): ")
    if q.strip().lower() == "q":
        break
    reponse, pages = repondre(q)
    print("\nReponse:", reponse)
    print("Sources: pages", pages)