import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def gera_grafico(df):
    df = pd.read_csv('/content/drive/MyDrive/Eletrozema/Vivaldi/duracao.csv', sep=';')
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S.%f')
    df['dia'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S.%f').dt.strftime('%d-%m-%Y')
    df = df.sort_values(by='data')
    dias = df['dia'].unique()
    x=0
    virada = pd.to_datetime(virada, format='%d-%m-%Y')
    for i, dia in enumerate(dias):
        dia = pd.to_datetime(dia, format='%d-%m-%Y')
        if virada >= dia:
            x = i + 0.5
    
    media_por_dia = df.groupby('dia')['duracao (ms)'].mean().reset_index()
    contagem_por_dia = df.groupby('dia')['duracao (ms)'].count().reset_index()

    # Criar o gráfico boxplot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='dia', y='duracao (ms)', data=df, ax=ax)

    # Adicionar as informações de volume e média
    for i, row in contagem_por_dia.iterrows():
        ax.text(i, df['duracao (ms)'].max() * -0.3, f'Volume: {row["duracao (ms)"]}', horizontalalignment='center', color='red', weight='normal')
    for i, row in media_por_dia.iterrows():
        ax.text(i, df['duracao (ms)'].max() * -0.4, f'Média: {row["duracao (ms)"]:.2f}', horizontalalignment='center', color='red', weight='normal')

    # Configurar o gráfico
    ax.set_xlabel('Dia')
    ax.set_ylabel('Duração (ms)')
    ax.set_title('Comparação da Duração entre Dias')
    ax.tick_params(axis='x', rotation=45)

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


def main():
    st.title("Média Diária")

    uploaded_files = st.file_uploader(
        "Escolha os arquivos CSV",
        type=["csv"],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos CSV para upload"
    )

    dataframes = {}
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Armazena o DataFrame no dicionário usando o nome do arquivo como chave
                dataframes[uploaded_file.name] = df
                
                # Mostra mensagem de sucesso
                st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")
                
                # Mostra um preview dos dados
                st.subheader(f"Pré-visualização: {uploaded_file.name}")
                st.dataframe(df.head())
                
            except Exception as e:
                st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")
    else:
        st.warning("Nenhum arquivo foi carregado ainda.")

    if dataframes:
        st.subheader("Arquivos Carregados:")
        for filename in dataframes:
            st.write(f"- {filename} ({len(dataframes[filename])} linhas)")
    # if st.button("Processar"):
        

if __name__ == "__main__":
    main()