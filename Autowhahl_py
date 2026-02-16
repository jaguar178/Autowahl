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
    df = pd.read_csv("vehicles.csv")
    return df

df = load_data()

# -----------------------------
# Titel
# -----------------------------
st.title("🚗 Intelligenter Auto-Finder")
st.write("Finde das perfekt zu dir passende Fahrzeug.")

# -----------------------------
# User-Eingaben
# -----------------------------
st.sidebar.header("Deine Anforderungen")

budget = st.sidebar.slider("Budget (€)", 10000, 80000, 30000, step=1000)
personen = st.sidebar.slider("Anzahl Personen", 1, 7, 4)
fahrprofil = st.sidebar.selectbox("Fahrprofil", ["Stadt", "Langstrecke", "Gemischt"])
umwelt = st.sidebar.selectbox("Umweltbewusstsein", ["Gering", "Mittel", "Hoch"])
fahrzeugtyp = st.sidebar.selectbox(
    "Fahrzeugtyp",
    df["Fahrzeugtyp"].unique()
)
zustand = st.sidebar.selectbox("Neu oder Gebraucht?", ["Neu", "Gebraucht"])

# -----------------------------
# Gewichtungssystem
# -----------------------------
def calculate_score(row):
    score = 0

    # 1. Budget (stark gewichtet)
    if row["Preis"] <= budget:
        score += 40
    else:
        score -= 20

    # 2. Fahrzeugtyp (stark gewichtet)
    if row["Fahrzeugtyp"] == fahrzeugtyp:
        score += 30

    # 3. Sitzplätze
    if row["Sitzplaetze"] >= personen:
        score += 10

    # 4. Zustand
    if row["Zustand"] == zustand:
        score += 10

    # 5. Fahrprofil
    if fahrprofil == "Stadt":
        if row["Antriebsart"] == "Elektro":
            score += 10
        if row["Fahrzeugtyp"] == "Kleinwagen":
            score += 5

    elif fahrprofil == "Langstrecke":
        if row["Reichweite"] > 700:
            score += 10
        if row["Antriebsart"] in ["Diesel"]:
            score += 5

    elif fahrprofil == "Gemischt":
        score += 5

    # 6. Umweltbewusstsein
    if umwelt == "Hoch":
        if row["Antriebsart"] == "Elektro":
            score += 15
        elif row["Verbrauch_CO2"] < 100:
            score += 10

    elif umwelt == "Mittel":
        if row["Verbrauch_CO2"] < 130:
            score += 5

    return score

# Score berechnen
df["Score"] = df.apply(calculate_score, axis=1)

# Bestes Fahrzeug ermitteln
best_car = df.sort_values(by="Score", ascending=False).iloc[0]

# -----------------------------
# Ergebnisanzeige
# -----------------------------
st.subheader("🏆 Unsere Empfehlung für dich:")

col1, col2 = st.columns([1, 2])

with col1:
    st.image(best_car["Bild_URL"], use_container_width=True)

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
# Begründung generieren
# -----------------------------
def generate_reason(car):
    reasons = []

    if car["Preis"] <= budget:
        reasons.append("liegt innerhalb deines Budgets")

    if car["Fahrzeugtyp"] == fahrzeugtyp:
        reasons.append("entspricht deinem gewünschten Fahrzeugtyp")

    if car["Sitzplaetze"] >= personen:
        reasons.append("bietet ausreichend Sitzplätze")

    if umwelt == "Hoch" and car["Antriebsart"] == "Elektro":
        reasons.append("ist besonders umweltfreundlich (Elektroantrieb)")

    if fahrprofil == "Langstrecke" and car["Reichweite"] > 700:
        reasons.append("eignet sich hervorragend für Langstrecken")

    return ", ".join(reasons)

st.markdown("### 💡 Warum dieses Fahrzeug?")
st.write(f"Dieses Fahrzeug wurde ausgewählt, weil es {generate_reason(best_car)}.")

# -----------------------------
# Transparenz
# -----------------------------
with st.expander("🔎 Transparenz: Bewertungssystem anzeigen"):
    st.dataframe(df[["Marke", "Modell", "Score"]].sort_values(by="Score", ascending=False))
