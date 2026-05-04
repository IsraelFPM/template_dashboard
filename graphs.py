import matplotlib.pyplot as plt
import seaborn as sns

# Configuração global opcional para deixar o Seaborn mais bonito
sns.set_theme(style="whitegrid")

def plot_barras(df, x, y, hue=None, tipo='vertical', agrupamento='agrupado', 
                figsize=(8, 4), paleta_cores="viridis"):
    """
    Gera gráficos de barras.
    :param tipo: 'vertical' ou 'horizontal'
    :param agrupamento: 'agrupado' (lado a lado) ou 'empilhado' (stacked)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Barras Empilhadas (Pandas Plot é mais fácil para empilhado estático)
    if agrupamento == 'empilhado':
        # Precisamos pivotar os dados para empilhar corretamente
        df_pivot = df.pivot_table(index=x if tipo == 'vertical' else y, 
                                  columns=hue, values=y if tipo == 'vertical' else x, aggfunc='sum')
        df_pivot.plot(kind='barh' if tipo == 'horizontal' else 'bar', 
                      stacked=True, ax=ax, colormap=paleta_cores)
    
    # Barras Agrupadas (Seaborn é ideal)
    else:
        if tipo == 'horizontal':
            sns.barplot(data=df, x=y, y=x, hue=hue, ax=ax, palette=paleta_cores)
        else:
            sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax, palette=paleta_cores)

    ax.set_title(f"Barras {tipo.capitalize()} - {agrupamento.capitalize()}", pad=15)
    
    # Ajuste de legenda
    if hue:
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
        
    fig.tight_layout() # Evita que a legenda seja cortada
    return fig

def plot_linhas(df, x, y, hue=None, tipo='linha', figsize=(8, 4), paleta_cores="tab10"):
    """
    Gera gráficos de linhas ou áreas.
    :param tipo: 'linha' (multi-linhas) ou 'area'
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if tipo == 'area':
        # Gráfico de área empilhada usando Pandas
        df_pivot = df.pivot_table(index=x, columns=hue, values=y, aggfunc='sum')
        df_pivot.plot(kind='area', ax=ax, colormap=paleta_cores, alpha=0.6)
    else:
        # Multi-linhas usando Seaborn
        sns.lineplot(data=df, x=x, y=y, hue=hue, marker='o', ax=ax, palette=paleta_cores)
        
    ax.set_title(f"Gráfico de {tipo.capitalize()}", pad=15)
    
    if hue:
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
        
    fig.tight_layout()
    return fig

def plot_proporcao(df, categoria, valor, tipo='pizza', figsize=(6, 6), paleta_cores="Set2"):
    """
    Gera gráficos circulares (Pie, Donut).
    Nota: Gauge nativo em Matplotlib é muito complexo de manter, recomenda-se 
    substituir Gauge estático por um gráfico de barra horizontal de meta vs realizado.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Agrupa os dados para a pizza
    df_agrupado = df.groupby(categoria)[valor].sum()
    
    cores = sns.color_palette(paleta_cores, len(df_agrupado))
    
    wedges, texts, autotexts = ax.pie(df_agrupado, labels=df_agrupado.index, 
                                      autopct='%1.1f%%', startangle=90, colors=cores)
    
    # Transforma Pizza em Donut desenhando um círculo branco no meio
    if tipo == 'donut':
        centro_branco = plt.Circle((0,0), 0.70, fc='white')
        fig.gca().add_artist(centro_branco)
        ax.set_title("Gráfico de Donut", pad=15)
    else:
        ax.set_title("Gráfico de Pizza", pad=15)
        
    ax.axis('equal') # Garante que o círculo seja perfeito
    fig.tight_layout()
    return fig