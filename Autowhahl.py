import streamlit as st
import pandas as pd
from io import StringIO

# -----------------------------
# Konfiguration
# -----------------------------
st.set_page_config(page_title="Auto-Finder", layout="wide")

# -----------------------------
# Eingebaute Fahrzeugdaten (ohne Links)
# -----------------------------
CSV_DATA = """
Marke,Modell,Preis,Antriebsart,PS,Reichweite,Verbrauch_CO2,Sitzplaetze,Fahrzeugtyp,Zustand
Tesla,Model 3,42990,Elektro,283,602,0,5,Limo,Neu
BMW,320d,38900,Diesel,190,800,119,5,Limo,Neu
Audi,A4 Avant,41000,Benzin,204,750,135,5,Kombi,Neu
Volkswagen,Golf 8,28900,Benzin,150,650,120,5,Kompakt,Gebraucht
Mercedes,C220d,45000,Diesel,200,850,122,5,Limo,Neu
Hyundai,Kona Elektro,36900,Elektro,204,484,0,5,SUV,Neu
Toyota,Corolla Hybrid,27900,Hybrid,140,900,89,5,Kompakt,Gebraucht
Skoda,Octavia Combi,31000,Diesel,150,900,115,5,Kombi,Gebraucht
Ford,Focus,24000,Benzin,125,600,125,5,Kompakt,Gebraucht
Kia,Ceed SW,26000,Benzin,160,650,130,5,Kombi,Neu
Tesla,Model Y,49990,Elektro,351,533,0,5,SUV,Neu
BMW,X3,55000,Diesel,265,850,140,5,SUV,Neu
Audi,Q5,53000,Diesel,204,820,138,5,SUV,Gebraucht
Volkswagen,Tiguan,42000,Benzin,190,700,145,5,SUV,Gebraucht
Mercedes,A180,32000,Benzin,136,650,130,5,Kompakt,Neu
Renault,Zoe,23900,Elektro,135,395,0,5,Kleinwagen,Gebraucht
Opel,Corsa-e,25900,Elektro,136,337,0,5,Kleinwagen,Neu
Peugeot,3008,34000,Benzin,180,680,140,5,SUV,Gebraucht
Volvo,XC60,60000,Hybrid,340,900,49,5,SUV,Neu
Dacia,Duster,18900,Benzin,110,600,139,5,SUV,Gebraucht
"""

@st.cache_data
def load_data():
    return pd.read_csv(StringIO(CSV_DATA))

df = load_data()

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
fahrzeugtyp = st.sidebar.selectbox("Fahrzeugtyp", sorted(df["Fahrzeugtyp"].unique()))
zustand = st.sidebar.selectbox("Neu oder Gebraucht?", ["Neu", "Gebraucht"])

# -----------------------------
# Score-Funktion
# -----------------------------
def calculate_score(row):
    score = 0

    if row["Preis"] <= budget:
        score += 40
    else:
        score -= 20

    if row["Fahrzeugtyp"] == fahrzeugtyp:
        score += 30

    if row["Sitzplaetze"] >= personen:
        score += 10

    if row["Zustand"] == zustand:
        score += 10

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
df_sorted = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

best_car = df_sorted.loc[0]

# -----------------------------
# Anzeige
# -----------------------------
st.subheader("🏆 Unsere Empfehlung für dich:")

st.markdown(f"## {best_car['Marke']} {best_car['Modell']}")
st.write(f"**Preis:** {best_car['Preis']} €")
st.write(f"**Antriebsart:** {best_car['Antriebsart']}")
st.write(f"**PS:** {best_car['PS']}")
st.write(f"**Reichweite:** {best_car['Reichweite']} km")
st.write(f"**CO₂:** {best_car['Verbrauch_CO2']} g/km")
st.write(f"**Sitzplätze:** {best_car['Sitzplaetze']}")
st.write(f"**Fahrzeugtyp:** {best_car['Fahrzeugtyp']}")
st.write(f"**Zustand:** {best_car['Zustand']}")

st.markdown("### 🔎 Score-Ranking")
st.dataframe(df_sorted[["Marke", "Modell", "Score"]])

