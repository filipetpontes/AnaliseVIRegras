import streamlit as st
import pandas as pd
import plotly.express as px

def gera_grafico(df, dias_selecionados):
    # Filtra os dados com base nos dias selecionados
    df_filtrado = df[df['dia'].isin(dias_selecionados)]

    # Cálculo da média e contagem por dia
    media_por_dia = df_filtrado.groupby('dia')['duracao (ms)'].mean().reset_index()
    contagem_por_dia = df_filtrado.groupby('dia')['duracao (ms)'].count().reset_index()

    # Criar o boxplot com Plotly
    fig = px.box(
        df_filtrado,
        x='dia',
        y='duracao (ms)',
        title='Dispersão da Duração por Dia',
        labels={'duracao (ms)': 'Duração (ms)', 'dia': 'Dia'},
        points="all"  # Mostra todos os pontos de dados
    )

    # Adicionar informações de volume e média ao gráfico
    # for i, row in contagem_por_dia.iterrows():
    #     fig.add_annotation(
    #         x=row['dia'],
    #         y=df_filtrado['duracao (ms)'].min() * 0.9,  # Posiciona a anotação abaixo do gráfico
    #         text=f"Volume: {row['duracao (ms)']}",
    #         showarrow=False,
    #         font=dict(color='red')
    #     )
    # for i, row in media_por_dia.iterrows():
    #     fig.add_annotation(
    #         x=row['dia'],
    #         y=df_filtrado['duracao (ms)'].min() * 0.8,  # Posiciona a anotação abaixo do gráfico
    #         text=f"Média: {row['duracao (ms)']:.2f}",
    #         showarrow=False,
    #         font=dict(color='blue')
    #     )

    # Configurar o layout do gráfico
    fig.update_layout(
        xaxis_title='Dia',
        yaxis_title='Duração (ms)',
        xaxis_tickangle=-45,
        showlegend=False
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

    # Exibir a tabela de contagem de volume por dia
    st.subheader("Volume de Dados por Dia")
    st.dataframe(contagem_por_dia)

def main():
    st.title("Dispersão Diária")

    uploaded_files = st.file_uploader(
        "",
        type=["csv"],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos CSV para upload\nEsses arquivos podem ser gerados no Diagnóstico > Gráficos > Taxa de Duração de Propostas"
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file, sep=';')

                # Processamento dos dados
                df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S.%f')
                df['dia'] = df['data'].dt.strftime('%d-%m-%Y')
                df = df.sort_values(by='data')

                # Gerar gráfico inicial com todos os dias
                if st.button(f"Processar"):
                    st.session_state['df'] = df  # Armazena o DataFrame na sessão
                    st.session_state['dias_disponiveis'] = df['dia'].unique()  # Armazena os dias disponíveis

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

            except Exception as e:
                st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")
    else:
        st.warning("Nenhum arquivo foi carregado ainda.")

if __name__ == "__main__":
    main()