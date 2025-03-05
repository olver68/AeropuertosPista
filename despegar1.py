import streamlit as st
import pandas as pd

# Cargar datos
csv_file = "aeronaves.csv"

try:
    df = pd.read_csv(csv_file, encoding='latin1')
except FileNotFoundError:
    st.error(f"El archivo {csv_file} no fue encontrado.")
    st.stop()
except pd.errors.ParserError:
    st.error("Error al leer el archivo CSV. Verifica el formato.")
    st.stop()

# Asegurar que LCRi es numérico
df["LCRi"] = pd.to_numeric(df["LCRi"], errors="coerce")

# Sidebar
st.sidebar.title("Configuración del Aeropuerto")

# Nombre del aeropuerto
nombre_aeropuerto = st.sidebar.text_input("Nombre del Aeropuerto:", value="Tuxtla Gutiérrez")

# Datos del aeropuerto
st.sidebar.header("Datos de Pista")
LRP = st.sidebar.number_input("Longitud de pista (m)", min_value=0.0, value=3102.0, step=100.0)
H = st.sidebar.number_input("Altitud sobre el nivel del mar (m)", min_value=0.0, value=73.0, step=10.0)
TA = st.sidebar.number_input("Temperatura ambiente (°C)", min_value=-50.0, value=30.0, step=1.0)
P = st.sidebar.number_input("Pendiente longitudinal (%)", min_value=-10.0, value=0.65, step=0.01)

# Botón para procesar los datos
if st.sidebar.button("Revisar aeronaves"):
    # Calcular factores
    FH = 1 + (0.07 * H / 300)
    FT = 1 + 0.01 * (TA - (14.991 - 0.0065 * H))
    FC = FH * FT

    if FC > 1.35:
        st.sidebar.warning("⚠️ El factor combinado (FC) es mayor a 1.35. " +
                   "Se recomienda evaluar un procedimiento alternativo o verificar los datos ingresados.")
        LCR = None
    else:
        FP = 1 + 0.1 * P
        LCR = LRP / (FC * FP)

        # Mostrar LCRmin en el sidebar
        st.sidebar.metric(label="LCR(m) máx.que puede Despegar", value=f"{LCR:.2f}")

        # Evaluar si las aeronaves pueden despegar
        df["Puede Despegar"] = df["LCRi"].apply(lambda x: "Sí" if LCR > x else "No")

        # Mostrar resultados
        st.subheader(f"Aeronaves en {nombre_aeropuerto}")
        st.dataframe(df)
