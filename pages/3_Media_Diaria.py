import streamlit as st
import pandas as pd
import plotly.express as px

def gera_grafico(df, dias_selecionados):
    # Filtra os dados com base nos dias selecionados
    df_filtrado = df[df['dia'].isin(dias_selecionados)]

    # Criar o boxplot com Plotly
    fig = px.box(
        df_filtrado,
        x='dia',
        y='duracao (ms)',
        title='Dispersão da Duração por Dia',
        labels={'duracao (ms)': 'Duração (ms)', 'dia': 'Dia'},
        hover_data={'duracao (ms)': True, 'dia': True},  # Personaliza as informações exibidas ao passar o mouse
    )

    # Personaliza o texto ao passar o mouse
    fig.update_traces(
        hovertemplate="<b>Dia:</b> %{x}<br><b>Duração (ms):</b> %{y}<br><extra></extra>"
    )

    fig.update_layout(
        xaxis_title='Dia',
        yaxis_title='Duração (ms)',
        xaxis_tickangle=-45,
        showlegend=False
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

def main():
    st.title("Dispersão Diária dos Tempos")

    # Seção de Dúvidas ou Ajuda
    with st.expander("Dúvidas? Clique aqui para ajuda"):
        st.markdown("""
        **Como usar esta aplicação:**
        1. **Carregue os arquivos CSV**: Selecione um ou mais arquivos CSV que contenham os dados de duração de propostas.
        2. **Processar os dados**: Após carregar os arquivos, clique no botão "Processar" para gerar o gráfico.
        3. **Filtrar por dias**: Use o filtro de dias para selecionar quais dias deseja visualizar no gráfico.
        4. **Interpretar o gráfico**: O gráfico exibe a dispersão da duração das propostas por dia.

        **Dúvidas comuns:**
        - **Formato do arquivo CSV**: Certifique-se de que o arquivo CSV tenha as colunas `data` e `duracao (ms)`.
        - **Problemas ao carregar arquivos**: Verifique se os arquivos estão no formato correto e se não estão corrompidos.
        - **Como interpretar o gráfico**: O gráfico é um boxplot, que mostra a distribuição da duração das propostas. A linha central representa a mediana, e as caixas representam os quartis.
        """)
        st.image('duvida.png')
    uploaded_files = st.file_uploader(
        "",
        type=["csv"],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos CSV para upload. Esses arquivos podem ser gerados no Diagnóstico > Gráficos > Taxa de Duração de Propostas"
    )

    if uploaded_files:
        dfs = []

        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file, sep=';')
                dfs.append(df)  # Adiciona o DataFrame à lista
            except Exception as e:
                st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")

        # Concatena todos os DataFrames em um único DataFrame
        if dfs:
            df_concatenado = pd.concat(dfs, ignore_index=True)

            # Processamento dos dados
            df_concatenado['data'] = pd.to_datetime(df_concatenado['data'], format='%d/%m/%Y %H:%M:%S.%f')
            df_concatenado['dia'] = df_concatenado['data'].dt.strftime('%d-%m-%Y')
            df_concatenado = df_concatenado.sort_values(by='data')

            # Exibe o DataFrame concatenado (opcional, para debug)
            st.dataframe(df_concatenado)

            # Armazena o DataFrame e as datas disponíveis na sessão
            st.session_state['df'] = df_concatenado
            st.session_state['dias_disponiveis'] = df_concatenado['dia'].unique()

            # Verifica se o DataFrame e os dias estão na sessão
            if 'df' in st.session_state and 'dias_disponiveis' in st.session_state:
                # Filtro de dias
                dias_selecionados = st.multiselect(
                    "Selecione os dias para filtrar o gráfico",
                    options=st.session_state['dias_disponiveis'],
                    default=st.session_state['dias_disponiveis']  # Todos os dias selecionados por padrão
                )

                # Gera o gráfico com os dias selecionados
                if dias_selecionados:
                    gera_grafico(st.session_state['df'], dias_selecionados)
                else:
                    st.warning("Selecione pelo menos um dia para gerar o gráfico.")
        else:
            st.warning("Nenhum arquivo válido foi carregado.")
    else:
        st.warning("Nenhum arquivo foi carregado ainda.")

if __name__ == "__main__":
    main()