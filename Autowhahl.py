import streamlit as st
import pandas as pd

# -----------------------------
# Konfiguration
# -----------------------------
st.set_page_config(page_title="Auto-Finder", layout="wide")

# -----------------------------
# Daten laden
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("vehicles.csv")
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("❌ Keine Fahrzeugdaten vorhanden.")
    st.stop()

# -----------------------------
# Titel
# -----------------------------
st.title("🚗 Intelligenter Auto-Finder")
st.write("Finde das perfekt zu dir passende Fahrzeug.")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Deine Anforderungen")

budget = st.sidebar.slider("Budget (€)", 10000, 80000, 30000, step=1000)
personen = st.sidebar.slider("Anzahl Personen", 1, 7, 4)
fahrprofil = st.sidebar.selectbox("Fahrprofil", ["Stadt", "Langstrecke", "Gemischt"])
umwelt = st.sidebar.selectbox("Umweltbewusstsein", ["Gering", "Mittel", "Hoch"])

if "Fahrzeugtyp" not in df.columns:
    st.error("Spalte 'Fahrzeugtyp' fehlt in der CSV.")
    st.stop()

fahrzeugtyp = st.sidebar.selectbox(
    "Fahrzeugtyp",
    sorted(df["Fahrzeugtyp"].dropna().unique())
)

zustand = st.sidebar.selectbox("Neu oder Gebraucht?", ["Neu", "Gebraucht"])

# -----------------------------
# Score-Funktion
# -----------------------------
def calculate_score(row):
    score = 0

    # Budget
    if row["Preis"] <= budget:
        score += 40
    else:
        score -= 20

    # Fahrzeugtyp
    if row["Fahrzeugtyp"] == fahrzeugtyp:
        score += 30

    # Sitzplätze
    if row["Sitzplaetze"] >= personen:
        score += 10

    # Zustand
    if row["Zustand"] == zustand:
        score += 10

    # Fahrprofil
    if fahrprofil == "Stadt":
        if row["Antriebsart"] == "Elektro":
            score += 10
        if row["Fahrzeugtyp"] == "Kleinwagen":
            score += 5

    elif fahrprofil == "Langstrecke":
        if row["Reichweite"] > 700:
            score += 10
        if row["Antriebsart"] == "Diesel":
            score += 5

    elif fahrprofil == "Gemischt":
        score += 5

    # Umwelt
    if umwelt == "Hoch":
        if row["Antriebsart"] == "Elektro":
            score += 15
        elif row["Verbrauch_CO2"] < 100:
            score += 10

    elif umwelt == "Mittel":
        if row["Verbrauch_CO2"] < 130:
            score += 5

    return score

# -----------------------------
# Score berechnen
# -----------------------------
df["Score"] = df.apply(calculate_score, axis=1)

df_sorted = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

if df_sorted.empty:
    st.warning("⚠️ Kein passendes Fahrzeug gefunden.")
    st.stop()

best_car = df_sorted.loc[0]

# -----------------------------
# Ergebnisanzeige
# -----------------------------
st.subheader("🏆 Unsere Empfehlung für dich:")

col1, col2 = st.columns([1, 2])

with col1:
    if "Bild_URL" in best_car and pd.notna(best_car["Bild_URL"]):
        st.image(best_car["Bild_URL"], use_container_width=True)
    else:
        st.info("Kein Bild verfügbar")

with col2:
    st.markdown(f"## {best_car['Marke']} {best_car['Modell']}")
    st.write(f"**Preis:** {best_car['Preis']} €")
    st.write(f"**Antriebsart:** {best_car['Antriebsart']}")
    st.write(f"**PS:** {best_car['PS']}")
    st.write(f"**Reichweite:** {best_car['Reichweite']} km")
    st.write(f"**CO₂:** {best_car['Verbrauch_CO2']} g/km")
    st.write(f"**Sitzplätze:** {best_car['Sitzplaetze']}")
    st.write(f"**Fahrzeugtyp:** {best_car['Fahrzeugtyp']}")
    st.write(f"**Zustand:** {best_car['Zustand']}")

# -----------------------------
# Begründung
# -----------------------------
def generate_reason(car):
    reasons = []

    if car["Preis"] <= budget:
        reasons.append("innerhalb deines Budgets liegt")

    if car["Fahrzeugtyp"] == fahrzeugtyp:
        reasons.append("deinem gewünschten Fahrzeugtyp entspricht")

    if car["Sitzplaetze"] >= personen:
        reasons.append("ausreichend Sitzplätze bietet")

    if umwelt == "Hoch" and car["Antriebsart"] == "Elektro":
        reasons.append("besonders umweltfreundlich ist")

    if fahrprofil == "Langstrecke" and car["Reichweite"] > 700:
        reasons.append("sich hervorragend für Langstrecken eignet")

    return ", ".join(reasons) if reasons else "gut zu deinen Kriterien passt"

st.markdown("### 💡 Warum dieses Fahrzeug?")
st.write(f"Dieses Fahrzeug wurde ausgewählt, weil es {generate_reason(best_car)}.")

# -----------------------------
# Transparenz
# -----------------------------
with st.expander("🔎 Transparenz: Bewertungssystem anzeigen"):
    st.dataframe(df_sorted[["Marke", "Modell", "Score"]])

