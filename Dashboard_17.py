import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

credentials = service_account.Credentials.from_service_account_file(r'c:\Users\yuri-\AppData\Local\Programs\Python\Python311\hopeful-hold-371415-c85ac257b965.json')
query_pandas = """SELECT * FROM RS_Parametros_Basicos.df_rs_SAC_pb"""
df = pd.read_gbq(query_pandas,project_id='hopeful-hold-371415', credentials=credentials)

# Configurações da página
st.set_page_config(
    page_title="Painel Monitoramnto Ambiental",
    page_icon="🧊",
    layout="wide",
)

st.columns([1.5,7,1])[1].subheader("Painel de Monitoramento Ambiental: Qualidade da Água - Vigiagua 17ª CRS")
with st.sidebar:
    st.write('Selecione os filtros!')
    data_inicial = st.date_input(
        "Data inicial",
        datetime.date(2014, 1, 1))

    data_final = st.date_input(
        "Data inicial",
        datetime.date.today())
    
    municipios = st.selectbox(
    'Qual município você quer ver?',
    df['Municipio'], index=497)
col2, col3 = st.columns([2,3])



#INICIO PRIMEIRO GRÁFICO (ECOLI 17ª CRS - HEATMAP)
#-------------------------------------------------
df_17 = df[df['CRS']=='17ª CRS']
df_17_ecoli = df_17[df_17['Parametro'] == 'Escherichia coli']
crosstab_ecoli_17_a = pd.crosstab(index=df_17_ecoli['Municipio'],columns=df_17_ecoli['Ano'], 
                    values=df_17_ecoli[df_17_ecoli['Resultado']=='PRESENTE']['UF'],aggfunc='count')
crosstab_ecoli_17_b = pd.crosstab(index=df_17_ecoli['Municipio'],columns=df_17_ecoli['Ano'], 
                    values=df_17_ecoli['Resultado'],aggfunc='count')

crosstab_ecoli_17 = round(crosstab_ecoli_17_a/crosstab_ecoli_17_b,4)

annot_kws={'fontsize':20,
           'color':'black',
           'alpha':0.7,
           'verticalalignment':'center',
           'weight':'bold'}
plt.figure(figsize=(35, 18), dpi=144)

cmap = sns.color_palette("YlOrBr", as_cmap=True)

crosstab_ecoli_17 = crosstab_ecoli_17.fillna(-1)
nan_mask = crosstab_ecoli_17 == -1
mask = crosstab_ecoli_17.isnull()
sns.set_style("darkgrid")
fig = sns.heatmap(crosstab_ecoli_17,annot=True, cmap=cmap,  annot_kws=annot_kws, fmt='.2%', linewidth=2, mask=nan_mask, vmin=0, vmax=0.5)
for i in range(crosstab_ecoli_17.shape[0]):
    for j in range(crosstab_ecoli_17.shape[1]):
        if nan_mask.iloc[i, j]:
            fig.text(j + 0.5, i + 0.5, "S/D", ha='center', va='center', fontsize=20, color='black', alpha=0.7, weight='bold')
cbar = fig.collections[0].colorbar
cbar.set_ticks([0,0.5])
cbar.set_ticklabels(["0.00%","50.00%"], fontsize=24)
#fig.set_facecolor("white")
fig.xaxis.tick_top()
plt.xticks(fontsize=26)
plt.yticks(fontsize=26)
plt.title('MAPA DE CALOR: PORCENTAGEM DE AMOSTRAS COM PRESENÇA DE ESCHERICHIA COLI POR ANO E MUNICÍPIO DA 17ª CRS', weight='bold', pad=30).set_fontsize('30')
fig.set(xlabel=None)
fig.set(ylabel=None)
#plt.show()
with col2:
    st.pyplot(fig)
#-------------------------------------------------
#FINAL PRIMEIRO GRÁFICO (ECOLI 17ª CRS - HEATMAP)

#df_rs_ecoli = df[df['Parametro'] == 'Escherichia coli']