import streamlit as st
import handler
import raizac

st.set_page_config(page_title = "Raizac - Produtos naturais",
                 layout = "wide",
                 page_icon = "https://png.pngtree.com/png-clipart/20200709/original/pngtree-organic-logo-leafs-in-hand-logo-natural-products-logo-png-image_3984007.jpg")

st.title("Raizac - Loja de produtos naturais")

abas = st.tabs(["Saída de Estoque", "Gráficos", "Contato"])

with abas[0]:
    raizac.mostrar()
with abas[1]:
    handler.mostrar()
with abas[2]:
    st.header("Contato")
    st.write("Desenvolvido por Jeronimo Silva")
    st.write("Email: shaolin.jr@gmail.com")
    st.write("Telefone (21) 9 6962 4869")
