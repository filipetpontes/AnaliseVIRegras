import streamlit as st
import pandas as pd

def vi_regras_to_df(vi_regras):
    vi_regras = vi_regras.replace('\r', '').replace('\n', '').replace('£', ';').replace('<##>', '\\n')
    data = [line.split(';') for line in vi_regras.split('\\n')]
    df = pd.DataFrame(data)
    return df

def compara_tempo_vi_regras(vi_regras_1, vi_regras_2):
    df1 = vi_regras_to_df(vi_regras_1)
    df2 = vi_regras_to_df(vi_regras_2)

    df1_ok = df1.loc[:, [0, 2, 3]]
    df1_ok.columns = ['FLUXO', 'INICIO', 'FIM']
    df1_ok['INICIO'] = pd.to_datetime(df1_ok['INICIO'], format='%d/%m/%Y %H:%M:%S.%f')
    df1_ok['FIM'] = pd.to_datetime(df1_ok['FIM'], format='%d/%m/%Y %H:%M:%S.%f')
    df1_ok['DURACAO'] = (df1_ok['FIM'] - df1_ok['INICIO']).dt.total_seconds() * 1000

    df2_ok = df2.loc[:, [0, 2, 3]]
    df2_ok.columns = ['FLUXO', 'INICIO', 'FIM']
    df2_ok['INICIO'] = pd.to_datetime(df2_ok['INICIO'], format='%d/%m/%Y %H:%M:%S.%f')
    df2_ok['FIM'] = pd.to_datetime(df2_ok['FIM'], format='%d/%m/%Y %H:%M:%S.%f')
    df2_ok['DURACAO'] = (df2_ok['FIM'] - df2_ok['INICIO']).dt.total_seconds() * 1000

    df_merged = pd.merge(df1_ok[['FLUXO', 'DURACAO']], df2_ok[['FLUXO', 'DURACAO']], on='FLUXO', how='inner')

    df_merged.columns = ['FLUXO', 'DURACAO_1', 'DURACAO_2']

    df_merged['DIFERENCA (%)'] = (df_merged['DURACAO_2'] - df_merged['DURACAO_1']) / df_merged['DURACAO_1'] * 100
    df_merged['DIFERENCA (%)'] = df_merged['DIFERENCA (%)'].fillna(0)
    df_merged['DIFERENCA (%)'] = df_merged['DIFERENCA (%)'].round(2)
    df_merged['FLUXO'] = df_merged['FLUXO'].str.split('#').str[0]
    
    # Renomeando as colunas
    df_merged = df_merged.rename(columns={
        'FLUXO': 'Fluxo/Regra',
        'DURACAO_1': 'Proposta 1 (ms)',
        'DURACAO_2': 'Proposta 2 (ms)',
        'DIFERENCA (%)': 'Diferença (%)'
    })

    # Adicionando o símbolo de porcentagem (%) aos valores da coluna "Diferença (%)"
    df_merged['Diferença (%)'] = df_merged['Diferença (%)'].astype(str) + ' %'

    return df_merged

def main():
    st.title("NeuroAnáliseVIRegras")

    # Campos de entrada de texto
    vi_regras_1 = st.text_area("Proposta 1", placeholder="Cole aqui a VI_REGRAS...", height=100)
    vi_regras_2 = st.text_area("Proposta 2", placeholder="Cole aqui a VI_REGRAS...", height=100)

    # Botão para processar os dados
    if st.button("Gerar Tabela"):
        if vi_regras_1 and vi_regras_2:
            # Processa os dados e gera o DataFrame
            df = compara_tempo_vi_regras(vi_regras_1, vi_regras_2)

            # Exibe a tabela na interface
            st.write("### Resultado da Comparação")
            st.dataframe(df)

            # Botão para baixar o Excel
            st.download_button(
                label="Baixar Excel",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="comparativo.csv",
                mime="text/csv"
            )
        else:
            st.warning("Por favor, insira os dados das duas propostas.")

if __name__ == "__main__":
    main()