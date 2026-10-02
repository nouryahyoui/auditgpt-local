import re

# Kol règle: (esm l'tag, pattern regex)
REGLES = [
    ("EMAIL", r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    ("RIB", r"\b\d{2}[ ]?\d{3}[ ]?\d{13}[ ]?\d{2}\b"),
    ("MATRICULE_FISCAL", r"\b\d{7}[A-Z]\b"),
    ("TELEPHONE", r"\b(?:\+216[ ]?)?\d{2}[ ]?\d{3}[ ]?\d{3}\b"),
]


def anonymiser(texte):
    for tag, pattern in REGLES:
        texte = re.sub(pattern, f"[{tag}]", texte)
    return texte


if __name__ == "__main__":
    exemple = (
        "Contactez M. Ali a ali.ben@client.tn ou au 98 123 456. "
        "RIB: 08 006 0123456789012 34. Matricule fiscal: 1234567A."
    )
    print("Avant :", exemple)
    print("Apres :", anonymiser(exemple))