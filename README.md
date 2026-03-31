# Projeto: Pharma Agent

Assistente inteligente para cadastro automatizado de receitas, com interface inspirada em soluções de IA de ponta. Realiza leitura de imagens via OCR, interpretação com LLM, e exibe dados organizados para consulta e integração em sistemas farmacêuticos.
# <img width="1914" height="936" alt="{3D1060E2-58D3-466E-A52C-83B76325DC1C}" src="https://github.com/user-attachments/assets/28750924-b765-4ffb-a379-9143ef825ac3" />

## Destaques

*   **Chat moderno e funcional:** Interface de chat para interação direta com o agente de IA.
*   **Processamento multimodal (imagem → texto → dado estruturado):** Extrai informações de imagens de receitas usando OCR e as processa com um LLM.
*   **Backend Django, banco SQLite:** Utiliza o framework Django para o backend e SQLite para o banco de dados.
*   **Framework de agentes Agno:** Orquestração do agente de IA e do modelo de linguagem.
*   **UI/UX inspirada no Perplexity:** Design da interface de usuário inspirado em soluções de IA de ponta.

## Tecnologias Utilizadas
*   **Agno:** Orquestrador de LLMs
*   **Backend:** Django (Python)
*   **LLM:** Groq (com modelos como Llama-3.1-8b-instant)
*   **OCR:** pytesseract
*   **Banco de Dados:** SQLite (para desenvolvimento)
*   **Frontend:** HTML, CSS, JavaScript
*   **Gerenciamento de Ambiente:** `python-dotenv`

## Configuração do Projeto

Siga estes passos para configurar e rodar o projeto localmente:

### 1. Clonar o Repositório

```bash
git clone https://github.com/augdev1/pharmagent.git
cd pharmagent
```

### 2. Configurar Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependências

Instale todas as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (na mesma pasta que `manage.py`) com base no `.env.example`. **Substitua `YOUR_ACTUAL_GROQ_API_KEY` pela sua chave de API real do Groq.**

```dotenv
GROQ_API_KEY="SUA_CHAVE_DE_API_GROQ_AQUI"
AGNO_DB_PATH="./agno.db"
DJANGO_SECRET_KEY="sua-chave-secreta-aqui" # Gere uma chave segura para produção
DJANGO_DEBUG="True"
```

### 4.5 Instalar OCR no Windows (Tesseract)

Você deve instalar o OCR **antes de usar upload/leitura de imagem** na aplicação.

1. Baixe e instale o Tesseract OCR para Windows.
2. Caminho padrão esperado: `C:\Program Files\Tesseract-OCR\tesseract.exe`
3. Se instalar em outro local, defina no `.env`:

```dotenv
TESSERACT_CMD="C:\\seu\\caminho\\tesseract.exe"
```

Sem o Tesseract instalado, o fluxo de OCR (`pytesseract`) não consegue extrair texto das imagens.

### 5. Migrações do Banco de Dados

Aplique as migrações do Django para configurar o banco de dados:

```bash
python agnoframework/manage.py migrate
```

### 6. Coletar Arquivos Estáticos (Opcional, para deploy)

```bash
python agnoframework/manage.py collectstatic
```

## Como Rodar a Aplicação

Para iniciar o servidor de desenvolvimento Django:

```bash
python agnoframework/manage.py runserver
```

Acesse a aplicação no seu navegador em `http://127.0.0.1:8000/`.

## Inicialização rápida (estilo "npm run dev")

Agora você pode iniciar o projeto com um único comando:

```bash
python dev.py
```

Esse comando:
- carrega o `.env`
- executa `migrate`
- sobe o `runserver` em `127.0.0.1:8000`

Opções úteis:

```bash
python dev.py --no-migrate
python dev.py --host 0.0.0.0 --port 8001
```
