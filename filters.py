import streamlit as st

def renderizar_filtros(df):
    """
    Renderiza os filtros na barra lateral e retorna as seleções.
    """
    st.sidebar.header("Filtros do Dashboard")
    
    # Exemplo: O usuário escolhe a opção na tela e a variável armazena o valor [cite: 15, 16]
    categorias_disponiveis = df['Categoria'].unique()
    filtro_categoria = st.sidebar.selectbox("Escolha a Categoria", categorias_disponiveis)
    
    # Retorna um dicionário ou múltiplas variáveis com as escolhas
    return filtro_categoria