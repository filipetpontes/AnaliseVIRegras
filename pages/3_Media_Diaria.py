import streamlit as st
import pandas as pd
import plotly.express as px
import os

def gera_grafico(df, agrupamento, dias_selecionados=None, horas_selecionadas=None):
    if agrupamento == 'Dia':
        df_filtrado = df[df['dia'].isin(dias_selecionados)]
        x_axis = 'dia'
        title = 'Dispersão da Duração por Dia'
    else:
        df_filtrado = df[df['data_hora'].isin(horas_selecionadas)]
        x_axis = 'data_hora'
        title = 'Dispersão da Duração por Hora'

    fig = px.box(
        df_filtrado,
        x=x_axis,
        y='duracao (ms)',
        title=title,
        labels={'duracao (ms)': 'Duração (ms)', x_axis: 'Data e Hora'},
        hover_data={'duracao (ms)': True, x_axis: True},
    )

    fig.update_layout(
        xaxis_title='Data e Hora',
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

    if os.path.exists(caminho_imagem):
        with st.expander("Dúvidas?"):
            st.markdown("""
            **Como usar :**
            1. Acesse o Diagnóstico > Gráficos
            2. Faça o filtro desejado
            3. Selecione o tipo de gráfico 'Taxa de Duração de Propostas'
            4. Gere o gráfico
            5. Faça o download:
            """)
            st.image(caminho_imagem)
    else:
        st.warning("Arquivo de imagem 'duvida.png' não encontrado.")

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
            df_concatenado['hora'] = df_concatenado['data'].dt.strftime('%H:00')
            df_concatenado['data_hora'] = df_concatenado['data'].dt.strftime('%d/%m %H:00')  # Combina data e hora

            df_concatenado = df_concatenado.sort_values(by='data')

            st.session_state['df'] = df_concatenado
            st.session_state['dias_disponiveis'] = df_concatenado['dia'].unique()
            st.session_state['horas_disponiveis'] = df_concatenado['data_hora'].unique()

            if 'df' in st.session_state and 'dias_disponiveis' in st.session_state and 'horas_disponiveis' in st.session_state:
                agrupamento = st.radio(
                    "Escolha o agrupamento",
                    options=['Dia', 'Hora'],
                    index=0
                )

                if agrupamento == 'Dia':
                    dias_selecionados = st.multiselect(
                        "Selecione os dias para filtrar o gráfico",
                        options=st.session_state['dias_disponiveis'],
                        default=st.session_state['dias_disponiveis']
                    )
                    if dias_selecionados:
                        gera_grafico(st.session_state['df'], agrupamento, dias_selecionados=dias_selecionados)
                    else:
                        st.warning("Selecione pelo menos um dia para gerar o gráfico.")
                else:
                    horas_selecionadas = st.multiselect(
                        "Selecione as horas para filtrar o gráfico",
                        options=st.session_state['horas_disponiveis'],
                        default=st.session_state['horas_disponiveis']
                    )
                    if horas_selecionadas:
                        gera_grafico(st.session_state['df'], agrupamento, horas_selecionadas=horas_selecionadas)
                    else:
                        st.warning("Selecione pelo menos uma hora para gerar o gráfico.")
        else:
            st.warning("Nenhum arquivo válido foi carregado.")
    else:
        st.warning("Nenhum arquivo foi carregado ainda.")

if __name__ == "__main__":
    main()