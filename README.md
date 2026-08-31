# Prática 04: Laboratório de Ranking com BM25

Aplicação interativa desenvolvida em **Streamlit** para demonstrar o funcionamento do algoritmo de recuperação de informação **BM25** (Best Matching 25) aplicado diretamente sobre documentos em formato PDF.

---

## 👥 Integrantes

* **Vitor Ferreira Gonçalves Silva**
* **Miguel Figueiredo Falcão de Oliveira**
* **Rafael Queiroz Almeida**

* Com auxílio de Inteligência Artificial Generativa

---

## 📌 Sobre a Atividade

O objetivo do laboratório é analisar como os parâmetros do algoritmo BM25 influenciam a pontuação e a ordenação de relevância de documentos textuais:

* **Upload de Documentos:** Permite o envio dinâmico de até 3 arquivos PDF para indexação e extração de texto em tempo real via `pypdf`.
* **Parâmetro $k_1$ (Saturação de Termos):** Ajusta o impacto da repetição de uma mesma palavra na pontuação final.
* **Parâmetro $b$ (Normalização de Tamanho):** Controla o grau de penalização aplicado a documentos mais longos em relação ao tamanho médio do corpus ($avgdl$).
* **Busca e Ranking:** Calcula o score BM25 (com suporte a múltiplos termos) e apresenta uma tabela com o ranking comparativo e a prévia do texto processado.

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/Vitorfjs/pratica04-tendencias.git
cd pratica04-tendencias
