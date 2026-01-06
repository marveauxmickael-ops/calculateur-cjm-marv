import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Calculateur de CJM Freelance",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONNALISÉ ---
# On injecte un peu de CSS pour embellir les métriques et le titre
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #4CAF50;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR : PARAMÈTRES AVANCÉS ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    st.write("Ajustez les variables selon votre statut et vos vacances.")
    
    jours_ouvrables = st.slider(
        "Jours facturés / an",
        min_value=100,
        max_value=250,
        value=215,
        help="Moyenne standard : 210 à 218 jours (compte tenu des congés, jours fériés et maladies)."
    )
    
    coefficient = st.number_input(
        "Coefficient de charges",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1,
        help="1.5 à 1.7 est recommandé pour couvrir les charges sociales, les intercontrats et la précarité."
    )
    
    st.markdown("---")
    st.caption("ℹ️ *Le coefficient 1.6 est une marge de sécurité standard pour convertir un salaire brut cadre en facturation freelance.*")

# --- CONTENU PRINCIPAL ---
st.title("🚀 Calculateur de CJM")
st.markdown("Détermine ton **Tarif Journalier Moyen** idéal pour atteindre tes objectifs de revenus.")

st.divider()

# Zone de saisie principale
col_input, col_empty = st.columns([2, 1])
with col_input:
    salaire_brut = st.number_input(
        "💰 Quel est ton salaire brut annuel cible (€) ?", 
        min_value=0, 
        value=55000, 
        step=1000,
        format="%d"
    )

# --- CALCULS EN TEMPS RÉEL ---
if jours_ouvrables > 0:
    # Calcul du CA nécessaire (Salaire + Charges/Marge)
    ca_objectif = salaire_brut * coefficient
    
    # Calcul du CJM
    cjm = ca_objectif / jours_ouvrables
    
    # Arrondi pour l'affichage (souvent on facture par tranche de 10 ou 50)
    cjm_arrondi = int(round(cjm / 10) * 10) 
else:
    cjm = 0
    cjm_arrondi = 0

# --- AFFICHAGE DES RÉSULTATS ---
st.markdown("### 🎯 Résultats")

# Utilisation de colonnes pour un affichage "Dashboard"
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(
        label="Votre CJM conseillé", 
        value=f"{cjm_arrondi} € / jour", 
        delta="Objectif Minimum"
    )

with res_col2:
    st.metric(
        label="Chiffre d'Affaires annuel visé", 
        value=f"{int(ca_objectif):,} €".replace(",", " "), 
        delta=f"Basé sur {jours_ouvrables} jours"
    )

# --- ANALYSE VISUELLE ---
st.divider()

with st.expander("📊 Comprendre ce calcul (Détails)"):
    st.write(f"""
    Pour te verser **{salaire_brut:,} € brut** par an, tu dois générer un chiffre d'affaires d'environ **{int(ca_objectif):,} €**.
    
    **Pourquoi ?**
    * **Salaire visé :** {salaire_brut} € (Ce que tu veux gagner)
    * **Charges & Sécurité (~{(coefficient-1)*100:.0f}%) :** {int(ca_objectif - salaire_brut)} € 
        *(Couvre : charges patronales/salariales, mutuelle, comptable, matériel, congés payés, intercontrats)*.
    
    Cela revient à diviser ce total par tes **{jours_ouvrables} jours** travaillés.
    """)
    
    # Barre de progression visuelle (juste pour le style)
    st.progress(min(1.0, salaire_brut / 120000), text="Niveau de revenu positionné sur le marché (Indicatif)")

# --- APPEL À L'ACTION ---
if cjm_arrondi > 0:
    st.success(f"💡 **Conseil :** Sur ton devis ou TJM, affiche **{cjm_arrondi} € HT**. N'oublie pas d'ajouter la TVA si applicable.")