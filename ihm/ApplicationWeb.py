import streamlit as st
import requests
import datetime

# --- Chargement du CSS ---
try:
    with open("styles.css") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("`styles.css` not found. Please make sure the file is in the same directory.")
except Exception as e:
    st.error(f"Error loading CSS: {e}")


@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_marques():
    try:
        response = requests.get("http://127.0.0.1:8002/api/formulaire/marques")
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json().get("marques", [])
    except requests.exceptions.ConnectionError:
        st.error(
            "Erreur de connexion")
        return []
    except Exception as e:
        st.error(f"Impossible de charger les marques : {e}")
        return []


# --- Récupérer les modèles (mise en cache) ---
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_modeles(marque):
    if not marque:
        return []
    try:
        response = requests.get(f"http://127.0.0.1:8002/api/formulaire/modeles", params={"marque": marque})
        response.raise_for_status()
        return response.json().get("modeles", [])
    except requests.exceptions.ConnectionError:
        st.error(
            f"Erreur de connexion : Impossible de charger les modèles pour '{marque}'. Le backend est-il en cours d'exécution ?")
        return []
    except Exception as e:
        st.error(f"Impossible de charger les modèles : {e}")
        return []


# --- Interface principale ---
st.markdown("<h1 class='title'>Estimation du Prix d'une Voiture 🚗</h1>", unsafe_allow_html=True)
st.write(
    "Remplissez les informations ci-dessous pour obtenir une estimation rapide et précise du prix de votre véhicule.")

# --- Formulaire ---
with st.container():  # Use a container to group elements visually
    st.markdown("### Informations sur le véhicule")

    marques = get_marques()

    # Conditional rendering for selectboxes if no marques/modeles are found
    if marques:
        marque = st.selectbox("Marque", marques, help="Sélectionnez la marque de votre voiture.")
    else:
        st.warning("Aucune marque disponible. Veuillez vérifier la connexion au backend.")
        marque = None  # Ensure marque is None if no options

    modeles = []
    if marque:
        modeles = get_modeles(marque)
        if modeles:
            modele = st.selectbox("Modèle", modeles, help="Sélectionnez le modèle de votre voiture.")
        else:
            st.info(f"Aucun modèle disponible pour la marque '{marque}'.")
            modele = None
    else:
        modele = None  # Ensure modele is None if no marque

    col1, col2 = st.columns(2)
    with col1:
        current_year = datetime.datetime.now().year
        # Default to a more recent year, provide a range
        annee = st.selectbox("Année de mise en circulation", list(range(current_year, 1980, -1)),
                             help="L'année de fabrication du véhicule.")
    with col2:
        kilometrage = st.number_input("Kilométrage (en km)", min_value=0, value=50000, step=1000,
                                      help="Le nombre de kilomètres parcourus par le véhicule.")

    col3, col4 = st.columns(2)
    with col3:
        boite = st.selectbox("Boîte de Vitesse", ["Manuelle", "Automatique"],
                             help="Le type de transmission du véhicule.")
    with col4:
        carburant = st.selectbox("Carburant", ["Essence", "Diesel", "Hybride", "Électrique"],
                                 help="Le type de carburant utilisé par le véhicule.", index=0)  # Default to Essence

# --- Appel API et Affichage de la prédiction ---
st.markdown("---")  # Visual separator
if st.button("Estimer le prix de votre voiture", use_container_width=True):
    if not marque:
        st.error("Veuillez sélectionner une **Marque**.")
    elif not modele:
        st.error("Veuillez sélectionner un **Modèle**.")
    else:
        data = {
            "marque": marque,
            "modele": modele,
            "annee": annee,
            "kilometrage": kilometrage,
            "boite_vitesse": boite,
            "carburant": carburant
        }

        try:
            with st.spinner("Calcul de l'estimation..."):  # Show a spinner while waiting
                response = requests.post("http://127.0.0.1:8002/api/prediction/predict", json=data)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                prediction_data = response.json()
                predicted_price = prediction_data.get("predicted_price")

                if predicted_price is not None:
                    # Format the price nicely for French locale
                    formatted_price = f"{float(predicted_price):,.2f}".replace(",", " ").replace(".", ",")
                    st.markdown(f"<div class='result'>💰 Prix estimé : **{formatted_price} €**</div>",
                                unsafe_allow_html=True)
                else:
                    st.warning("Impossible d'obtenir une estimation. Le modèle de prédiction n'a pas retourné de prix.")

        except requests.exceptions.ConnectionError:
            st.error("Erreur de connexion : Assurez-vous que le serveur FastAPI est démarré sur http://127.0.0.1:8002.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Erreur HTTP lors de la prédiction : {e}. Réponse du serveur : {response.text}")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite lors de la prédiction : {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 0.9em;'>Développé par SADOUK Mokrane avec Streamlit</p>",
            unsafe_allow_html=True)