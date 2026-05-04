# Dashboard Modular com Streamlit

Este projeto implementa um dashboard analítico web utilizando Streamlit, focado em uma arquitetura modular ("plug and play") [cite: 3]. A versão atual utiliza dados simulados (mock data) e foca na renderização rápida de gráficos estáticos utilizando as bibliotecas Matplotlib e Seaborn [cite: 27]. Toda a aplicação está pronta para ser executada via contêineres Docker.

## Estrutura do Projeto

A arquitetura separa as responsabilidades em módulos independentes [cite: 57]:

* `main.py`: O arquivo principal da aplicação. Atua exclusivamente como a "vitrine" [cite: 59]. Ele importa os dados (com cache), coleta as seleções dos filtros, processa as regras de negócio de filtragem e organiza o layout.
* `filters.py`: Módulo responsável por renderizar os widgets de interatividade (como botões e caixas de seleção) na barra lateral (`st.sidebar`) e retornar as escolhas do usuário [cite: 12, 14].
* `graphs.py`: Fábrica de gráficos. Contém funções isoladas que recebem o DataFrame filtrado e os parâmetros estéticos, retornando apenas a figura gerada, sem a presença de comandos do Streamlit internos às funções [cite: 28, 29].
* `Dockerfile` e `docker-compose.yml`: Receitas de infraestrutura para hospedar a aplicação [cite: 63, 65].
* `requirements.txt`: Lista de dependências Python [cite: 62].

## Como Executar

A aplicação está empacotada com Docker para garantir a consistência do ambiente.

1.  Certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.
2.  Abra o terminal na raiz do projeto e execute [cite: 66]:
    ```bash
    docker-compose up --build
    ```
3.  Acesse `http://localhost:8501` no seu navegador. As alterações feitas no código refletirão quase instantaneamente graças ao volume mapeado [cite: 65, 80].

## Guia de Customização e Expansão

A arquitetura foi projetada para que novas funcionalidades sejam adicionadas de forma orgânica.

### 1. Como adicionar e customizar novos Filtros

Os filtros são elementos de entrada que geram variáveis [cite: 11].

* **No arquivo `filters.py`:** Adicione o novo widget (ex: um seletor de datas) usando a API do Streamlit (`st.sidebar.date_input`, `st.sidebar.slider`, etc.). Retorne as novas variáveis junto com as existentes (podendo ser uma tupla ou dicionário).
* **No arquivo `main.py`:** Capture a nova variável retornada pela função `renderizar_filtros()`. Aplique a lógica de cruzamento e corte no DataFrame base (ex: `df_filtrado = df_bruto[df_bruto['Ano'] == filtro_ano]`).

### 2. Como adicionar novos Gráficos

A premissa continua a mesma: as funções de gráfico recebem dados e parâmetros, retornando apenas a figura `fig` [cite: 28].

* **No arquivo `graphs.py`:** Crie uma nova função `def plot_novo(df, x, y, hue=None, paleta_cores="Set2", ...):`. Crie a lógica do gráfico estático utilizando `matplotlib.pyplot` ou `seaborn`. Lembre-se de retornar o objeto `fig` no final.
* **No arquivo `main.py`:** Importe a nova função no topo do arquivo. Organize sua tela criando colunas (ex: `col1, col2 = st.columns(2)` [cite: 105]). Chame a nova função, passando o `df_filtrado` e os parâmetros customizados desejados. Exiba o gráfico na coluna utilizando o comando estático `st.pyplot(fig_gerada)`.

### 3. Como adicionar novas Páginas ao Dashboard

Para transformar este projeto de página única em uma aplicação multipáginas (Multipage App) com navegação nativa, siga o padrão estrutural recomendado pelo Streamlit:

1.  **Crie uma nova pasta:** Na mesma raiz onde se encontra o arquivo `main.py`, crie uma pasta chamada `pages` [cite: 212].
2.  **Adicione os novos arquivos:** Coloque seus outros scripts Python para as novas páginas dentro desta pasta `pages` [cite: 213] (Exemplo: `pages/1_Visao_RH.py`, `pages/2_Relatorio_Financeiro.py`).
3.  **Navegação Automática:** O Streamlit fará a leitura dessa pasta de forma automática e gerará um menu interativo na barra lateral para que o usuário navegue [cite: 214].
4.  **Reutilização:** Você pode continuar importando normalmente as funções `renderizar_filtros` e as de criação de gráficos de dentro das suas novas páginas, garantindo que todo o seu aplicativo mantenha o design padronizado. Lembre-se apenas que a memória em cache é compartilhada globalmente entre todas as páginas [cite: 202].

## Notas de Desempenho

Por padrão, a exibição de gráficos estáticos envia imagens PNG leves do servidor para o navegador do cliente, protegendo usuários com computadores mais simples de possíveis travamentos associados à renderização web pesada [cite: 268, 269].