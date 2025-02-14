import streamlit as st
import pandas as pd
import plotly.express as px

def gera_grafico(df):
    # Processamento dos dados
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S.%f')
    df['dia'] = df['data'].dt.strftime('%d-%m-%Y')
    df = df.sort_values(by='data')

    # Cálculo da média e contagem por dia
    media_por_dia = df.groupby('dia')['duracao (ms)'].mean().reset_index()
    contagem_por_dia = df.groupby('dia')['duracao (ms)'].count().reset_index()

    # Criar o boxplot com Plotly
    fig = px.box(
        df,
        x='dia',
        y='duracao (ms)',
        title='Boxplot da Duração por Dia',
        labels={'duracao (ms)': 'Duração (ms)', 'dia': 'Dia'},
        points="all"  # Mostra todos os pontos de dados
    )

    # Adicionar informações de volume e média ao gráfico
    for i, row in contagem_por_dia.iterrows():
        fig.add_annotation(
            x=row['dia'],
            y=df['duracao (ms)'].min() * 0.9,  # Posiciona a anotação abaixo do gráfico
            text=f"Volume: {row['duracao (ms)']}",
            showarrow=False,
            font=dict(color='red')
        )
    for i, row in media_por_dia.iterrows():
        fig.add_annotation(
            x=row['dia'],
            y=df['duracao (ms)'].min() * 0.8,  # Posiciona a anotação abaixo do gráfico
            text=f"Média: {row['duracao (ms)']:.2f}",
            showarrow=False,
            font=dict(color='blue')
        )

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
    st.title("Média Diária")

    uploaded_files = st.file_uploader(
        "Escolha os arquivos CSV",
        type=["csv"],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos CSV para upload"
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file, sep=';')
                st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")
                st.subheader(f"Pré-visualização: {uploaded_file.name}")
                st.dataframe(df.head())

                if st.button(f"Gerar Boxplot para {uploaded_file.name}"):
                    gera_grafico(df)

            except Exception as e:
                st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")
    else:
        st.warning("Nenhum arquivo foi carregado ainda.")

if __name__ == "__main__":
    main()