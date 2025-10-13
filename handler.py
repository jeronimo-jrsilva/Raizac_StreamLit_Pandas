# run -> streamlit run main.py
import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sea
import plotly.express as px
from geopy.geocoders import Nominatim
#import time

#from main import endereco
def mostrar():

    st.set_page_config(
        #page_title = "Raizac",
        #page_icon = "📊",
        #layout = "wide"
        #layout = "normal"
    )

    st.title("📊 Dashboars  - Raizac")

    def carregar_dados(arquivo):
        try:
            with open(arquivo, "r") as file:
                linhas = file.readlines()
            produtos=[]
            produto={}
            for linha in linhas:
                linha = linha.strip()
                if linha.startswith("Código"):
                    produto["Código"] = linha.split("Código:")[1].strip()
                elif linha.startswith("Produto"):
                    produto["Produto"] = linha.split("Produto:")[1].strip()
                elif linha.startswith("Valor"):
                    #produto["Valor"] = float(linha.split("R$")[1].replace(",", ".").strip())
                    produto["Valor"] = linha.split("R$")[1].strip().replace(".", ",")
                elif linha.startswith("Quantidade"):
                    produto["Quantidade"] = int(linha.split("Quantidade:")[1].strip())
                elif linha.startswith("Categoria"):
                    produto["Categoria"] = linha.split("Categoria:")[1].strip()
                elif linha.startswith("Descrição"):
                    produto["Descrição"] = linha.split("Descrição:")[1].strip()
                elif linha.startswith("Total"):
                    produto["Total"] = float(linha.split("R$")[1].replace(",", ".").strip())
                elif linha.startswith("Data"):
                    produto["Data"] = linha.split("Data:")[1].strip()
                elif linha.startswith("CEP"):
                    produto["CEP"] = linha.split("CEP:")[1].strip()
                elif linha.startswith("Número"):
                    produto["Número"] = linha.split("Número:")[1].strip()
                elif linha.startswith("Endereço"):
                    produto["Endereço"] = linha.split("Endereço:")[1].strip()
                elif linha.startswith("Cidade"):
                    produto["Cidade"] = linha.split("Cidade:")[1].strip()
                elif linha.startswith("Estado"):
                    produto["Estado"] = linha.split("Estado:")[1].strip()
                elif linha.startswith("="):
                    produtos.append(produto)
                    produto={}
            df = pd.DataFrame(produtos)
            df["Data"] = pd.to_datetime(df["Data"],errors = "coerce",format="%d/%m/%Y")
            return df
        except FileNotFoundError:
            st.error("Arquivo não encontrado")
            return pd.DataFrame()

    df = carregar_dados("produtos.txt")
    df_resumido = df[["Produto","Valor","Categoria","Quantidade", "Data"]]
    if not df.empty:
        st.header("Tabela de dados:")
        #st.dataframe(df)
        st.dataframe(df_resumido)

        # grafico de pizza
        df_categoria = df.groupby("Categoria")["Total"].sum().reset_index()
        graf_pizza = px.pie(df_categoria, values="Total", names="Categoria", title = "Participação no valor total por categoria")
        st.plotly_chart(graf_pizza)

        # graf de dispersão
        graf_disp = px.scatter(df,x="Valor", y="Quantidade",color="Categoria", hover_data=["Produto"], title = "Correlação entre preço e qtd")
        st.plotly_chart(graf_disp)

        # graf barras top 5
        top5 = df.sort_values(by="Valor", ascending = False).head(5)
        graf_bar = px.bar(top5, x="Produto", y="Valor", color="Categoria", title="Top 5 produtos mais caros")

        # linhas por data
        st.plotly_chart(graf_bar)
        df_data = df.groupby("Data")["Total"].sum().reset_index()
        graf_linha = px.line(df_data,x="Data", y="Total", markers = True, title = "Total vendido por data")
        st.plotly_chart(graf_linha)

        geolocalizacao = Nominatim(user_agent="raizac_dashboard")

        def obter_coordenadas(row):
            endereco2 = f'{row["Endereço"]},{row["Número"]},{row["Cidade"]},{row["Estado"]},Brasil'
            try:
                localizacao = geolocalizacao.geocode(endereco2, timeout=10)
                if localizacao:
                    return pd.Series({"lat" : localizacao.latitude, "lon" : localizacao.longitude})
            except:
                return pd.Series({"lat" : None, "lon" : None})
            return pd.Series({"lat" : None, "lon" : None})

        if "lat" not in df.columns or "lon" not in df.columns:
            coords = df.apply(obter_coordenadas,axis=1)
            df["lat"] = coords["lat"]
            df["lon"] = coords["lon"]
        mapa_df = df.dropna(subset = ["lat","lon"])
        if not mapa_df.empty:
            st.map(mapa_df[["lat","lon"]])
        else:
            st.warning("Nenhum endereço válido para mostrar no mapa")

    else:
        st.warning("Arquivo não encontrado")
