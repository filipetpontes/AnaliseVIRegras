import streamlit as st
import pandas as pd
from io import BytesIO

# Configura o título da página
st.set_page_config(page_title="Análise VI_REGRAS", page_icon="📊")

def vi_regras_to_df(vi_regras):
    vi_regras = vi_regras.replace('\r', '').replace('\n', '').replace('£', ';').replace('<##>', '\\n')
    data = [line.split(';') for line in vi_regras.split('\\n')]
    df = pd.DataFrame(data)
    return df

def duracoes_vi_regras(vi_regras):
    df = vi_regras_to_df(vi_regras)
    df_ok = df.loc[:, [0, 2, 3]]
    df_ok.columns = ['Fluxo/Regra', 'Início', 'Fim']
    df_ok['Início'] = pd.to_datetime(df_ok['Início'], format='%d/%m/%Y %H:%M:%S.%f')
    df_ok['Fim'] = pd.to_datetime(df_ok['Fim'], format='%d/%m/%Y %H:%M:%S.%f')
    df_ok['Duração (ms)'] = (df_ok['Fim'] - df_ok['Início']).dt.total_seconds() * 1000
    return df_ok[['Fluxo/Regra', 'Duração (ms)']]

def to_excel(df):
    """Converte o DataFrame para um arquivo Excel em memória."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tempos de Execução')
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title("Análise VI_REGRAS")

    # Barra lateral personalizada
    st.sidebar.title("Sobre o App")
    st.sidebar.write("Este aplicativo foi desenvolvido para analisar os tempos de execução de fluxos/regras a partir de dados da VI_REGRAS.")
    st.sidebar.write("**Como usar:**")
    st.sidebar.write("1. Cole os dados da VI_REGRAS no campo de texto abaixo.")
    st.sidebar.write("2. Clique em 'Processar' para calcular os tempos de execução.")
    st.sidebar.write("3. Baixe o resultado em Excel clicando em 'Baixar Excel'.")
    st.sidebar.markdown("---")  # Adiciona uma linha horizontal
    st.sidebar.write("Desenvolvido por [Seu Nome]")

    # Campos de entrada de texto
    vi_regras = st.text_area("Cole aqui a VI_REGRAS", placeholder="Cole aqui a VI_REGRAS...", height=100)

    # Botão para processar os dados
    if st.button("Processar"):
        if vi_regras:
            # Processa os dados e gera o DataFrame
            df = duracoes_vi_regras(vi_regras)

            # Exibe a tabela na interface
            st.write("### Resultado dos Tempos de Execução")
            st.dataframe(df)

            # Converte o DataFrame para Excel
            try:
                excel_file = to_excel(df)

                # Botão para baixar o Excel
                st.download_button(
                    label="Baixar Excel",
                    data=excel_file,
                    file_name="tempos_execucao.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except ImportError:
                st.error("A biblioteca 'openpyxl' não está instalada. Por favor, instale-a com o comando: `pip install openpyxl`.")
        else:
            st.warning("Por favor, insira os dados da VI_REGRAS.")

if __name__ == "__main__":
    main()