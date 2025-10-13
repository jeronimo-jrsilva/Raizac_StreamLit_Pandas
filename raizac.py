# run -> streamlit run main.py

import streamlit as st
import requests


def mostrar():
    # Título

    st.title("Raizac Produtos Naturais!")

    #Campos
    codigo_produto = st.text_input("Código do produto")
    nome_produto = st.text_input("Nome do produto")
    #valor_produto = st.text_input("Valor do produto", min_value=0.0, format="R$")
    valor_produto2 = st.number_input("Valor do produto", min_value=0.0, format="%.2f")
    quantidade_produto = st.number_input("Quantidade do produto", min_value=0, step=1)

    categorias = ["Alimentos", "Bebidas", "Suplementos", "Outros"]
    categoria_produto = st.selectbox("Categoria do produto",categorias)

    descricao_produto = st.text_area("Descrição do produto")
    data_da_compra = st.date_input("Data da compra")
    data_string = data_da_compra.strftime("%d/%m/%Y")
    total = valor_produto2*quantidade_produto

    cep = st.text_input("Digite seu CEP (apenas números)")
    numero_loja = st.text_input("Numero da loja")

    endereco = ""
    cidade = ""
    estado = ""

    if cep and len(cep)==8 and cep.isdigit():
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            data = response.json()
            if "erro" not in data:
                logradouro = data.get("logradouro","")
                bairro = data.get("bairro","")
                endereco = f"{logradouro} - {bairro}" if bairro else logradouro
                cidade = data.get("localidade","")
                estado = data.get("uf","")
                st.success("Endereço encontrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao consultar o CEP: {e}")
    elif cep and (len(cep)!=8 or not cep.isdigit()):
        st.warning("Digite um CEP válido com 8 números")

    endereco = st.text_input("Endereço (rua/avenica;bairro)",value=endereco)
    cidade = st.text_input("Cidade",value=cidade)
    estado = st.text_input("Estado",value=estado)

    #salvar as informações
    if st.button("Adicionar produto"):
        if not codigo_produto or not nome_produto:
            st.warning("Preencha todos os campos obrigatórios")
        else:
            with open("produtos.txt",'a') as arquivo:
                arquivo.write(f"Código: {codigo_produto}\n")
                arquivo.write(f"Produto: {nome_produto}\n")
                arquivo.write(f"Valor unitário: R$ {valor_produto2:.2f}\n")
                arquivo.write(f"Quantidade: {quantidade_produto}\n")
                arquivo.write(f"Categoria: {categoria_produto}\n")
                arquivo.write(f"Descrição: {descricao_produto}\n")
                arquivo.write(f"Total: R$ {total:.2f}\n")
                arquivo.write(f"Data: {data_string}\n")
                arquivo.write(f"CEP: {cep}\n")
                arquivo.write(f"Número: {numero_loja}\n")
                arquivo.write(f"Endereço: {endereco}\n")
                arquivo.write(f"Cidade: {cidade}\n")
                arquivo.write(f"Estado: {estado}\n")
                arquivo.write(f"{'':=^40}\n")
