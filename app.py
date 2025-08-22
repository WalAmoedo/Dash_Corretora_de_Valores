import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard - Corretora de Valores",
    page_icon="💹",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("df_limpo.csv", sep=",")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro por Região
regioes_disponiveis = sorted(df['Região'].dropna().unique())
regioes_selecionadas = st.sidebar.multiselect("Região", regioes_disponiveis, default=regioes_disponiveis)

# Filtro por Estado
estados_disponiveis = sorted(df['Estado'].dropna().unique())
estados_selecionados = st.sidebar.multiselect("Estado (UF)", estados_disponiveis, default=estados_disponiveis)

# Filtro por Perfil de Investidor
perfis_disponiveis = sorted(df['Perfil_Investidor'].dropna().unique())
perfis_selecionados = st.sidebar.multiselect("Perfil de Investidor", perfis_disponiveis, default=perfis_disponiveis)

# --- Filtragem do DataFrame ---
df_filtrado = df[
    (df['Região'].isin(regioes_selecionadas)) &
    (df['Estado'].isin(estados_selecionados)) &
    (df['Perfil_Investidor'].isin(perfis_selecionados))
]

# --- Conteúdo Principal ---
st.title("📊 Dashboard - Corretora de Valores")
st.markdown("Explore os dados dos clientes da corretora. Use os filtros à esquerda para refinar sua análise. 🔎")

# --- Métricas Principais (KPIs) ---
st.subheader("📌 Métricas Gerais")

if not df_filtrado.empty:
    patrimonio_medio = df_filtrado['Patrimonio_Total'].mean()
    patrimonio_max = df_filtrado['Patrimonio_Total'].max()
    total_clientes = df_filtrado.shape[0]
    perfil_mais_comum = df_filtrado["Perfil_Investidor"].mode()[0]
else:
    patrimonio_medio, patrimonio_max, total_clientes, perfil_mais_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Patrimônio Médio", f"R$ {patrimonio_medio:,.2f}")
col2.metric("Maior Patrimônio", f"R$ {patrimonio_max:,.2f}")
col3.metric("Total de Clientes", f"{total_clientes:,}")
col4.metric("Perfil Mais Comum", perfil_mais_comum)

st.markdown("---")

# --- Análises Visuais ---
st.subheader("📈 Gráficos de Análise")

col_graf1, col_graf2 = st.columns(2)

# Gráfico 1 - Distribuição por Região
with col_graf1:
    if not df_filtrado.empty:
        grafico_regiao = px.pie(
            df_filtrado,
            names="Região",
            title="Distribuição de Clientes por Região",
            hole=0.5
        )
        grafico_regiao.update_traces(textinfo="percent+label")
        st.plotly_chart(grafico_regiao, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir por região.")

# Gráfico 2 - Perfil x Patrimônio
with col_graf2:
    if not df_filtrado.empty:
        grafico_perfil = px.box(
            df_filtrado,
            x="Perfil_Investidor",
            y="Patrimonio_Total",
            title="Distribuição de Patrimônio por Perfil de Investidor",
            labels={"Patrimonio_Total": "Patrimônio (R$)", "Perfil_Investidor": "Perfil"}
        )
        st.plotly_chart(grafico_perfil, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de perfil.")

col_graf3, col_graf4 = st.columns(2)

# Gráfico 3 - Valor pago à corretora
with col_graf3:
    if not df_filtrado.empty:
        grafico_taxas = px.histogram(
            df_filtrado,
            x="Valor_Pago_Corretora",
            nbins=30,
            title="Distribuição do Valor Pago em Taxas",
            labels={"Valor_Pago_Corretora": "Taxas Pagas (R$)"}
        )
        st.plotly_chart(grafico_taxas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de taxas.")

# Gráfico 4 - Patrimônio por Estado
with col_graf4:
    if not df_filtrado.empty:
        grafico_estado = px.bar(
            df_filtrado.groupby("Estado")["Patrimonio_Total"].mean().reset_index(),
            x="Estado",
            y="Patrimonio_Total",
            title="Patrimônio Médio por Estado",
            labels={"Patrimonio_Total": "Patrimônio Médio (R$)", "Estado": "UF"}
        )
        st.plotly_chart(grafico_estado, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir por estado.")

st.markdown("---")

# --- Tabela Detalhada ---
st.subheader("📑 Dados Detalhados")
st.dataframe(df_filtrado)

