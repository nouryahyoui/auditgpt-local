from fpdf import FPDF

pdf = FPDF()
pdf.set_font("Helvetica", size=12)

texte = (
    "Contrat de prestation de services. "
    "Article 1: Le client doit payer la facture dans un delai de 30 jours. "
    "Article 2: En cas de retard de paiement, une penalite de 5 pourcent "
    "du montant sera appliquee par mois de retard. "
    "Article 3: Les donnees du client sont confidentielles et ne peuvent "
    "pas etre transmises a des tiers. "
    "Article 4: Le contrat peut etre resilie avec un preavis de 60 jours. "
)

for page in range(1, 4):
    pdf.add_page()
    pdf.multi_cell(0, 8, f"Page {page}. " + texte * 3)

pdf.output("test.pdf")
print("test.pdf cree")