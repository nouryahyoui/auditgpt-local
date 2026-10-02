import datetime
import streamlit as st
import chromadb
import ollama
from anonymiser import anonymiser
from auth import verifier

st.set_page_config(page_title="AuditGPT Local", page_icon="🔒")


def ecrire_log(utilisateur, question):
    ligne = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} | {utilisateur} | {anonymiser(question)}\n"
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(ligne)


# ---------- LOGIN ----------
if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None

if st.session_state.utilisateur is None:
    st.title("🔒 AuditGPT Local")
    st.subheader("Connexion")
    with st.form("login"):
        nom = st.text_input("Nom d'utilisateur")
        mdp = st.text_input("Mot de passe", type="password")
        ok = st.form_submit_button("Se connecter")
    if ok:
        if verifier(nom, mdp):
            st.session_state.utilisateur = nom
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
    st.stop()

# ---------- APP (visible bark ba3d login) ----------
st.title("🔒 AuditGPT Local")
st.caption("Assistant IA prive: 100% local, aucune donnee envoyee au cloud")

with st.sidebar:
    st.write(f"Connecte: **{st.session_state.utilisateur}**")
    if st.button("Se deconnecter"):
        st.session_state.utilisateur = None
        st.rerun()

client = chromadb.PersistentClient(path="db")
collection = client.get_collection("documents")


def repondre(question):
    q_vecteur = ollama.embed(model="nomic-embed-text", input=question)["embeddings"][0]
    res = collection.query(query_embeddings=[q_vecteur], n_results=3)

    contexte = ""
    sources = []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        contexte += f"[Page {meta['page']}] {doc}\n\n"
        sources.append((meta["page"], doc))

    # Anonymisation avant envoi au LLM
    question = anonymiser(question)
    contexte = anonymiser(contexte)

    prompt = f"""Tu es un assistant pour un cabinet d'audit.
Reponds a la question en utilisant UNIQUEMENT le contexte ci-dessous.
Si la reponse n'est pas dans le contexte, dis: "Je ne trouve pas la reponse dans les documents."
Reponds en francais, de facon courte, et cite la page entre parentheses.

CONTEXTE:
{contexte}

QUESTION: {question}

REPONSE:"""

    rep = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return rep["message"]["content"], sources


question = st.text_input("Posez votre question sur le document :")

if question:
    ecrire_log(st.session_state.utilisateur, question)

    with st.spinner("Recherche en cours..."):
        reponse, sources = repondre(question)

    with st.expander("Donnees envoyees au modele (apres anonymisation)"):
        st.code(anonymiser(question))

    st.subheader("Reponse")
    st.write(reponse)

    if "Je ne trouve pas" not in reponse:
        with st.expander("Sources utilisees"):
            for page, texte in sources:
                st.markdown(f"**Page {page}**")
                st.write(texte)