import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Calculateur d'Objectifs Financiers")

# --- Inputs utilisateur ---
objectif = st.number_input("Objectif financier total (€)", min_value=1.0, value=150000.0)
epargne_actuelle = st.number_input("Épargne actuelle (€)", min_value=0.0, value=900.0)
duree_annees = st.number_input("Durée pour atteindre l'objectif (années)", min_value=0.1, value=3.0)
taux_annuel = st.slider("Taux de rendement annuel (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.01)

# --- Calculs ---
duree_mois = int(duree_annees * 12)
taux_mensuel = taux_annuel / 100 / 12
montant_restant = objectif - epargne_actuelle

# Calcul de la mensualité nécessaire
if taux_mensuel == 0:
    mensualite = montant_restant / duree_mois
else:
    # Formule pour mensualité avec intérêts composés
    mensualite = montant_restant * (taux_mensuel / ((1 + taux_mensuel)**duree_mois - 1))

# --- Projection mois par mois ---
projections = []
solde = epargne_actuelle
for i in range(1, duree_mois + 1):
    solde = solde * (1 + taux_mensuel) + mensualite
    projections.append(solde)

# --- Affichage résumé ---
st.subheader("Résumé")
st.write(f"Pour atteindre **{objectif:.2f} €** en {duree_annees:.1f} ans, vous devez épargner **{mensualite:.2f} € / mois**.")

# --- Graphique ---
st.subheader("Projection de l'épargne")
df = pd.DataFrame({'Mois': range(1, duree_mois + 1), 'Épargne cumulée (€)': projections})
st.line_chart(df.set_index('Mois'))

# --- Tableau détaillé optionnel ---
if st.checkbox("Afficher le tableau détaillé"):
    st.dataframe(df)
