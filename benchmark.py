import time
import csv
import chromadb
import ollama

MODELES = ["llama3.2", "qwen2.5:3b"]

# (sou2el, kelma lezem tكون fil jawab, kelma lezem ma tكونch)
TESTS = [
    ("Quel est le delai de paiement de la facture ?", "30", None),
    ("Quelle est la penalite en cas de retard de paiement ?", "5", None),
    ("Quel est le preavis pour resilier le contrat ?", "60", None),
    ("Les donnees du client peuvent-elles etre transmises a des tiers ?", "non", None),
    ("Qui est le president de la Tunisie ?", "ne trouve pas", None),
    ("Quelle est la capitale de la France ?", "ne trouve pas", None),
]

client = chromadb.PersistentClient(path="db")
collection = client.get_collection("documents")


def contexte_pour(question):
    q = ollama.embed(model="nomic-embed-text", input=question)["embeddings"][0]
    res = collection.query(query_embeddings=[q], n_results=3)
    return "\n\n".join(res["documents"][0])


def demander(modele, question, contexte):
    prompt = f"""Tu es un assistant pour un cabinet d'audit.
Reponds a la question en utilisant UNIQUEMENT le contexte ci-dessous.
Si la reponse n'est pas dans le contexte, dis: "Je ne trouve pas la reponse dans les documents."
Reponds en francais, de facon courte.

CONTEXTE:
{contexte}

QUESTION: {question}

REPONSE:"""
    debut = time.time()
    rep = ollama.chat(model=modele, messages=[{"role": "user", "content": prompt}])
    duree = time.time() - debut
    return rep["message"]["content"], duree


resultats = []
for modele in MODELES:
    print(f"\n=== {modele} ===")
    bons = 0
    total_temps = 0
    for question, attendu, _ in TESTS:
        ctx = contexte_pour(question)
        reponse, duree = demander(modele, question, ctx)
        ok = attendu.lower() in reponse.lower()
        bons += ok
        total_temps += duree
        print(f"{'OK ' if ok else 'KO '} {duree:5.1f}s | {question}")
        resultats.append([modele, question, ok, round(duree, 1), reponse.strip()])
    print(f"-> Precision: {bons}/{len(TESTS)} | Temps moyen: {total_temps/len(TESTS):.1f}s")

with open("benchmark_resultats.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["modele", "question", "correct", "duree_s", "reponse"])
    w.writerows(resultats)
print("\nResultats sauvegardes dans benchmark_resultats.csv")