import streamlit as st
import pandas as pd
from io import BytesIO

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
    return df_ok

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Comparativo')
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title("Tempos de Execução")

    # Campos de entrada de texto
    vi_regras = st.text_area("Proposta", placeholder="Cole aqui a VI_REGRAS...", height=100)

    # Botão para processar os dados
    if st.button("Processar"):
        if vi_regras:
            # Processa os dados e gera o DataFrame
            df = duracoes_vi_regras(vi_regras)

            # Exibe a tabela na interface
            st.dataframe(df)

            # Converte o DataFrame para Excel
            excel_file = to_excel(df)

            # Botão para baixar o Excel
            st.download_button(
                label="Baixar Excel",
                data=excel_file,
                file_name="tempos_execucao.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Por favor, insira os dados das duas propostas.")

if __name__ == "__main__":
    main()