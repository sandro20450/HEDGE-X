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
        # --- INÍCIO DA FASE 2 ---

# 6. Módulo de EV e Kelly (Só renderiza se o Score aprovar)
if hedge_x_score >= 80:
    st.divider()
    st.header("Calculadora de Valor Esperado (EV+) e Kelly")
    st.info("Insira as cotações oferecidas pelo mercado e a probabilidade real que você estimou na Etapa 5 e 6.")

    # Entradas de Dados
    col_odd, col_prob = st.columns(2)

    with col_odd:
        odd_mercado = st.number_input("Odd do Mercado (Decimal)", min_value=1.01, value=2.15, step=0.01)
    
    with col_prob:
        prob_estimada_pct = st.number_input("Sua Probabilidade Estimada (%)", min_value=1.0, max_value=100.0, value=57.0, step=1.0)
        
    # Variáveis Matemáticas
    prob_estimada = prob_estimada_pct / 100
    prob_implicita = 1 / odd_mercado
    
    # Cálculo do EV
    ev_percentual = (prob_estimada * odd_mercado - 1) * 100
    
    # Cálculo do Critério de Kelly
    b = odd_mercado - 1
    p = prob_estimada
    q = 1 - p
    
    if b > 0:
        full_kelly = ((p * b) - q) / b
        # Adotamos o Quarter Kelly (1/4) por padrão de segurança
        quarter_kelly = full_kelly / 4 
    else:
        full_kelly = 0
        quarter_kelly = 0

    st.subheader("Análise Quantitativa do Mercado")
    
    # Painel de Resultados usando Nativos
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.metric(label="Prob. Implícita da Casa", value=f"{prob_implicita * 100:.1f}%")
        
    with res2:
        # Usamos o delta nativo do st.metric para mostrar se o EV é positivo (verde) ou negativo (vermelho)
        st.metric(
            label="Expected Value (EV)", 
            value=f"{ev_percentual:.2f}%", 
            delta=f"{ev_percentual:.2f}%", 
            delta_color="normal" if ev_percentual > 0 else "inverse"
        )
        
    with res3:
        if full_kelly > 0:
            st.metric(label="Quarter Kelly (Stake Sugerida)", value=f"{quarter_kelly * 100:.2f}%")
        else:
            st.metric(label="Quarter Kelly (Stake Sugerida)", value="0.00%")
    
    # Filtro de Qualidade Final (Etapa 9 e 10)
    if ev_percentual > 0:
        st.success("🎯 ENTRADA APROVADA: O mercado apresenta EV positivo. Siga a gestão do Quarter Kelly indicada.")
    else:
        st.warning("⚠️ ENTRADA RECUSADA: O mercado possui EV negativo (vantagem da casa). Aborte a operação e busque outras linhas.")
