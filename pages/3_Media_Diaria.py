import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

    fig.update_layout(
        xaxis_title='Dia',
        yaxis_title='Duração (ms)',
        xaxis_tickangle=-45,
        showlegend=False
    )

    st.plotly_chart(fig)

def main():
    st.title("Dispersão Diária dos Tempos")

    uploaded_files = st.file_uploader(
        "",
        type=["csv"],
        accept_multiple_files=True
    )

    caminho_imagem = os.path.join("duvida.png")

    with st.expander("Dúvidas? Clique aqui para ajuda"):
        st.markdown("""
        **Como usar :**
        1. Acesse o Diagnóstico > Gráficos
        2. Faça o filtro desejado
        3. Selecione o tipo de gráfico 'Taxa de Duração de Propostas'
        4. Gere o gráfico
        5. Faça o download:
        """)
        st.image(caminho_imagem)

    if uploaded_files:
        dfs = []

        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file, sep=';')
                dfs.append(df)
            except Exception as e:
                st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")

        if dfs:
            df_concatenado = pd.concat(dfs, ignore_index=True)

            df_concatenado['data'] = pd.to_datetime(df_concatenado['data'], format='%d/%m/%Y %H:%M:%S.%f')
            df_concatenado['dia'] = df_concatenado['data'].dt.strftime('%d-%m-%Y')
            df_concatenado = df_concatenado.sort_values(by='data')

            st.session_state['df'] = df_concatenado
            st.session_state['dias_disponiveis'] = df_concatenado['dia'].unique()

            if 'df' in st.session_state and 'dias_disponiveis' in st.session_state:
                dias_selecionados = st.multiselect(
                    "Selecione os dias para filtrar o gráfico",
                    options=st.session_state['dias_disponiveis'],
                    default=st.session_state['dias_disponiveis']
                )

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