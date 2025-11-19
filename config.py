import os
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb

def get_llm_model():
    """
    Configura e retorna o modelo de linguagem do Groq.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente GROQ_API_KEY não foi definida.")
    return Groq(id="llama-3.1-8b-instant", api_key=api_key)

def get_database():
    """
    Configura e retorna a conexão com o banco de dados SQLite.
    """
    db_path = os.getenv("AGNO_DB_PATH", "./agno.db")
    return SqliteDb(db_file=db_path)