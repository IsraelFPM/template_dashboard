import pandas as pd
import streamlit as st

from graphs import plot_barras
from graphs import plot_linhas
from graphs import plot_proporcao


@st.cache_data
def carregar_dados_mock():
    """Simula os dados que virão do banco/parquet."""
    return pd.DataFrame({
        'Data': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'Categoria': ['A', 'B', 'C'] * 4,
        'Subcategoria': ['X', 'Y'] * 6,
        'Valor': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
        'Meta': [12, 18, 18, 28, 28, 38, 38, 48, 48, 58, 58, 68]
    })

def renderizar_filtros(df):
    """Módulo de filtros Plug and Play na barra lateral."""
    st.sidebar.header("Filtros")
    
    # Filtro de Categoria
    categorias = ['Todas'] + list(df['Categoria'].unique())
    cat_selecionada = st.sidebar.selectbox("Categoria", categorias)
    
    # Aplica o filtro localmente para retornar a string de escolha
    return cat_selecionada
# --- Fluxo Principal ---
st.set_page_config(layout="wide")
st.title("Dashboard Estático (Versão 1)")

# 1. Carrega os dados
df_bruto = carregar_dados_mock()

# 2. Chama os filtros e obtém variáveis
filtro_cat = renderizar_filtros(df_bruto)

# 3. Aplica a lógica de filtro nos dados
df_filtrado = df_bruto.copy()
if filtro_cat != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Categoria'] == filtro_cat]

# 4. Layout e Renderização dos Gráficos
st.markdown("### Visão Geral de Barras")
col1, col2 = st.columns(2) # Divide a tela [cite: 247]

with col1:
    # Chama a função passando parâmetros customizados
    fig_barras_v = plot_barras(df_filtrado, x='Subcategoria', y='Valor', hue='Categoria', 
                               tipo='vertical', agrupamento='agrupado')
    # Renderiza imagem estática no Streamlit
    st.pyplot(fig_barras_v)

with col2:
    fig_barras_h = plot_barras(df_filtrado, x='Categoria', y='Valor', hue='Subcategoria', 
                               tipo='horizontal', agrupamento='empilhado', paleta_cores="magma")
    st.pyplot(fig_barras_h)

st.markdown("### Visão Temporal e Proporção")
col3, col4 = st.columns([2, 1]) # Coluna 3 é o dobro do tamanho da 4 [cite: 249]

with col3:
    fig_linhas = plot_linhas(df_filtrado, x='Data', y='Valor', hue='Categoria', tipo='area')
    st.pyplot(fig_linhas)

with col4:
    fig_donut = plot_proporcao(df_filtrado, categoria='Subcategoria', valor='Valor', tipo='donut')
    st.pyplot(fig_donut)