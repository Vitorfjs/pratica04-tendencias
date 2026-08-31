import streamlit as st
import math
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(page_title="Laboratório BM25 com PDFs", layout="wide")
st.title("⚙️ Laboratório de Rank BM25 com Upload de PDFs")

# Função auxiliar para limpar e tokenizar texto
def tokenizar(texto):
    return re.findall(r'\b\w+\b', texto.lower())

# Upload dos arquivos PDF
st.subheader("1. Envie os 3 arquivos PDF")
uploaded_files = st.file_uploader(
    "Selecione até 3 PDFs para indexação", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 3:
        st.warning("⚠️ Você enviou mais de 3 arquivos. Serão processados apenas os 3 primeiros.")
        uploaded_files = uploaded_files[:3]

    # Extração de texto dos PDFs enviados
    docs = {}
    for file in uploaded_files:
        try:
            reader = PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_pagina = page.extract_text()
                if texto_pagina:
                    texto_completo += " " + texto_pagina
            
            # Se o PDF estiver vazio ou for imagem escaneada
            if not texto_completo.strip():
                docs[file.name] = "documento vazio ou não textual"
            else:
                docs[file.name] = texto_completo
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {file.name}: {e}")

    # Interface de busca e parâmetros
    st.subheader("2. Configuração de Busca e Parâmetros")
    
    col_q, col_k1, col_b = st.columns([2, 1, 1])
    
    with col_q:
        query = st.text_input("Termo de busca (Query):", value="inteligência")
    with col_k1:
        k1 = st.slider("Parâmetro k1 (Saturação)", min_value=0.0, max_value=3.0, value=1.2, step=0.1)
    with col_b:
        b = st.slider("Parâmetro b (Tamanho do doc)", min_value=0.0, max_value=1.0, value=0.75, step=0.05)

    if query.strip() and docs:
        query_tokens = tokenizar(query)
        doc_tokens = {nome: tokenizar(texto) for nome, texto in docs.items()}

        # Cálculos de comprimento de documentos
        dl = {nome: len(tokens) for nome, tokens in doc_tokens.items()}
        avgdl = sum(dl.values()) / len(dl) if len(dl) > 0 and sum(dl.values()) > 0 else 1
        N = len(docs)

        # Cálculo do BM25 (suporta 1 ou mais palavras na query)
        resultados = []
        
        for nome, tokens in doc_tokens.items():
            score_total = 0.0
            detalhes_termos = {}

            for q_term in query_tokens:
                # Frequência do termo no documento atual
                f = tokens.count(q_term)
                
                # Document Frequency (quantos documentos contêm o termo)
                df_t = sum(1 for d_toks in doc_tokens.values() if q_term in d_toks)
                
                # IDF com suavização padrão BM25
                if df_t > 0:
                    idf = math.log((N - df_t + 0.5) / (df_t + 0.5) + 1.0)
                else:
                    idf = 0.0

                # Fórmula do BM25 por termo
                numerador = f * (k1 + 1)
                denominador = f + k1 * (1 - b + b * (dl[nome] / avgdl if avgdl > 0 else 1))
                score_termo = idf * (numerador / denominador) if denominador > 0 else 0
                
                score_total += score_termo
                detalhes_termos[q_term] = f

            resultados.append({
                "Documento": nome,
                "Total de Palavras (|D|)": dl[nome],
                "Frequência dos Termos": str(detalhes_termos),
                "Score BM25": round(score_total, 4)
            })

        # Exibição do ranking
        df_bm25 = pd.DataFrame(resultados).sort_values(by="Score BM25", ascending=False)
        
        st.subheader("3. Ranking Resultante")
        st.dataframe(df_bm25, use_container_width=True)

        # Visualização de prévias dos documentos
        with st.expander("📄 Ver prévia do texto extraído dos PDFs"):
            for nome, texto in docs.items():
                st.markdown(f"**{nome}:**")
                st.text(texto[:300] + ("..." if len(texto) > 300 else ""))
    else:
        st.info("Digite uma palavra ou frase na busca para calcular o ranking.")

else:
    st.info("👆 Faça o upload de 3 PDFs para começar a análise.")