import streamlit as st
import pandas as pd
import os
import datetime

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(page_title="HEDGE-X V1.0", layout="wide")

st.title("HEDGE-X PROTOCOL V1.0 📈")
st.info("Módulo Quantitativo de Análise Esportiva - Foco em Expectativa Matemática Positiva (EV+)")

st.divider()

# ==========================================
# FASE 1: FILTRO PRIMÁRIO E SCORE
# ==========================================
st.header("Filtro Primário: Avaliação de Cenário")
st.write("Insira as notas (0 a 100) para cada métrica da partida.")

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

categorias = [
    intensidade, pressao, controle, eficiencia, 
    solidez, escanteios, ritmo, gols_ht, 
    gols_ft, contexto, motivacao, desgaste
]
hedge_x_score = sum(categorias) / len(categorias)

st.divider()
st.subheader("Resultado: HEDGE-X SCORE")

col_metric, col_status = st.columns([1, 2])

with col_metric:
    st.metric(label="Score Final", value=f"{hedge_x_score:.1f} / 100")

with col_status:
    if hedge_x_score >= 80:
        st.success("✅ PROTOCOLO APROVADO: A partida apresenta assimetria técnica suficiente para buscar valor no mercado.")
    else:
        st.error("❌ PROTOCOLO RECUSADO: Pontuação inferior a 80.")
        st.warning("Nenhum mercado identificado apresenta vantagem estatística suficiente. A melhor decisão é não apostar.")


# ==========================================
# FASE 2, 3 E 4: APENAS SE SCORE >= 80
# ==========================================
if hedge_x_score >= 80:
    st.divider()
    st.header("Calculadora de Valor Esperado (EV+) e Kelly")
    
    col_odd, col_prob = st.columns(2)
    with col_odd:
        odd_mercado = st.number_input("Odd do Mercado (Decimal)", min_value=1.01, value=2.15, step=0.01)
    with col_prob:
        prob_estimada_pct = st.number_input("Sua Probabilidade Estimada (%)", min_value=1.0, max_value=100.0, value=57.0, step=1.0)
        
    prob_estimada = prob_estimada_pct / 100
    prob_implicita = 1 / odd_mercado
    ev_percentual = (prob_estimada * odd_mercado - 1) * 100
    
    b = odd_mercado - 1
    p = prob_estimada
    q = 1 - p
    
    if b > 0:
        full_kelly = ((p * b) - q) / b
        quarter_kelly = full_kelly / 4 
    else:
        full_kelly = 0
        quarter_kelly = 0

    res1, res2, res3 = st.columns(3)
    with res1:
        st.metric(label="Prob. Implícita da Casa", value=f"{prob_implicita * 100:.1f}%")
    with res2:
        st.metric(
            label="Expected Value (EV)", 
            value=f"{ev_percentual:.2f}%", 
            delta=f"{ev_percentual:.2f}%", 
            delta_color="normal" if ev_percentual > 0 else "inverse"
        )
    with res3:
        st.metric(label="Quarter Kelly (Stake Sugerida)", value=f"{max(0, quarter_kelly * 100):.2f}%")
    
    if ev_percentual > 0:
        st.success("🎯 ENTRADA APROVADA: Mercado com EV positivo.")
        
        # ==========================================
        # FASE 3: REGISTRO NO BANCO DE DADOS
        # ==========================================
        st.divider()
        st.header("Módulo de Registro 🧠")
        
        with st.form("form_salvar_aposta"):
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                nome_partida = st.text_input("Partida (Ex: Brasil x Japão)")
            with col_form2:
                mercado_alvo = st.text_input("Mercado (Ex: Ambas Marcam - Sim)")
                
            salvar = st.form_submit_button("Gravar no Banco de Dados")
            
            if salvar:
                if nome_partida and mercado_alvo:
                    novo_dado = {
                        "Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Partida": nome_partida,
                        "Mercado": mercado_alvo,
                        "Prob_Estimada": prob_estimada,
                        "Odd": odd_mercado,
                        "EV_%": round(ev_percentual, 2),
                        "Stake_%": round(quarter_kelly * 100, 2),
                        "Resultado_Real": "Pendente" # Aguardando o fim do jogo (0 ou 1)
                    }
                    
                    arquivo_csv = "historico_hedgex.csv"
                    df_novo = pd.DataFrame([novo_dado])
                    
                    if os.path.exists(arquivo_csv):
                        df_novo.to_csv(arquivo_csv, mode='a', header=False, index=False)
                    else:
                        df_novo.to_csv(arquivo_csv, index=False)
                    
                    st.success("✅ Operação registrada com sucesso!")
                else:
                    st.error("Preencha a partida e o mercado.")

    else:
        st.warning("⚠️ ENTRADA RECUSADA: EV negativo (vantagem da casa).")

# ==========================================
# FASE 4: CALIBRAÇÃO E BRIER SCORE
# ==========================================
arquivo_csv = "historico_hedgex.csv"
if os.path.exists(arquivo_csv):
    st.divider()
    st.header("Calibração de Modelo (Brier Score)")
    st.info("Atualize o 'Resultado_Real' das partidas encerradas (1 = Green, 0 = Red) para calibrar a IA.")
    
    df_historico = pd.read_csv(arquivo_csv)
    
    # Editor de dados nativo do Streamlit (Dark Mode friendly)
    df_editado = st.data_editor(
        df_historico,
        column_config={
            "Resultado_Real": st.column_config.SelectboxColumn(
                "Resultado Real (FT)",
                help="1 para Ganha, 0 para Perdida, Pendente aguardando",
                options=["Pendente", "1", "0"],
                required=True
            )
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Salvar alterações feitas na tabela interativa
    if st.button("Salvar Resultados"):
        df_editado.to_csv(arquivo_csv, index=False)
        st.success("Resultados atualizados no banco de dados!")
    
    # Cálculo do Brier Score para as apostas resolvidas
    df_resolvidas = df_editado[df_editado["Resultado_Real"].isin(["1", "0"])].copy()
    
    if not df_resolvidas.empty:
        df_resolvidas["Resultado_Real"] = df_resolvidas["Resultado_Real"].astype(float)
        # Brier Score = Média de (Probabilidade Estimada - Resultado Real)^2
        df_resolvidas["Brier_Erro"] = (df_resolvidas["Prob_Estimada"] - df_resolvidas["Resultado_Real"]) ** 2
        brier_score = df_resolvidas["Brier_Erro"].mean()
        
        st.subheader("Desempenho Matemático do Protocolo")
        st.metric(
            label="Brier Score Geral (Mais próximo de 0 = Melhor)", 
            value=f"{brier_score:.4f}",
            help="Penaliza projeções excessivamente confiantes que se mostram incorretas."
        )
