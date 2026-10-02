from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Nfتho l'PDF
reader = PdfReader("test.pdf")

# 2. Nطلّعو l'texte men kol page (w nحfdhou raqm l'page)
pages = []
for i, page in enumerate(reader.pages):
    texte = page.extract_text()
    if texte:
        pages.append({"page": i + 1, "texte": texte})

print("Nombre de pages:", len(pages))

# 3. Nقassmou l'texte l'9to3
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = []
for p in pages:
    for morceau in splitter.split_text(p["texte"]):
        chunks.append({"page": p["page"], "texte": morceau})

print("Nombre de chunks:", len(chunks))
print("Exemple de chunk:")
print(chunks[0])