import streamlit as st

# 1. Configuração base da página
st.set_page_config(page_title="HEDGE-X V1.0", layout="wide")

# 2. Cabeçalho Principal (Usando nativos de forma limpa)
st.title("HEDGE-X PROTOCOL V1.0 📈")
st.info("Módulo Quantitativo de Análise Esportiva - Foco em Expectativa Matemática Positiva (EV+)")

st.divider()

st.header("Filtro Primário: Avaliação de Cenário")
st.write("Insira as notas (0 a 100) para cada métrica da partida.")

# 3. Organização em colunas para não poluir a tela
col1, col2, col3 = st.columns(3)

with col1:
    intensidade = st.number_input("Intensidade Ofensiva", 0, 100, 85)
    pressao = st.number_input("Pressão", 0, 100, 80)
    controle = st.number_input("Controle Territorial", 0, 100, 80)
    eficiencia = st.number_input("Eficiência Ofensiva", 0, 100, 85)

with col2:
    solidez = st.number_input("Solidez Defensiva", 0, 100, 80)
    escanteios = st.number_input("Escanteios", 0, 100, 90)
    ritmo = st.number_input("Ritmo", 0, 100, 85)
    gols_ht = st.number_input("Gols no 1º Tempo", 0, 100, 80)

with col3:
    gols_ft = st.number_input("Gols no 2º Tempo", 0, 100, 85)
    contexto = st.number_input("Contexto da Partida", 0, 100, 95)
    motivacao = st.number_input("Motivação", 0, 100, 100)
    desgaste = st.number_input("Desgaste (Físico/Viagens)", 0, 100, 75)

# 4. Motor de Cálculo
categorias = [
    intensidade, pressao, controle, eficiencia, 
    solidez, escanteios, ritmo, gols_ht, 
    gols_ft, contexto, motivacao, desgaste
]
hedge_x_score = sum(categorias) / len(categorias)

st.divider()

# 5. Painel de Decisão (Visuais Nativos)
st.subheader("Resultado: HEDGE-X SCORE")

col_metric, col_status = st.columns([1, 2])

with col_metric:
    # Componente perfeito para dashboards numéricos
    st.metric(label="Score Final", value=f"{hedge_x_score:.1f} / 100")

with col_status:
    # Lógica de bloqueio do protocolo
    if hedge_x_score >= 80:
        st.success("✅ PROTOCOLO APROVADO: A partida apresenta assimetria técnica suficiente para buscar valor no mercado.")
    else:
        st.error("❌ PROTOCOLO RECUSADO: Pontuação inferior a 80.")
        st.warning("Nenhum mercado identificado apresenta vantagem estatística suficiente. A melhor decisão é não apostar.")
