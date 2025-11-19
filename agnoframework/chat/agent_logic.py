
import sys
import os
from pathlib import Path

# Add the project root to the Python path
# The current file is in h:/AGENTE_AI/agnoframework/chat/
# The project root is h:/AGENTE_AI/
# So we need to go up two levels.
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from ocr_1 import extract_text_from_image
from agno.agent import Agent
from dotenv import load_dotenv

from config import get_llm_model, get_database
from prompts import PHARM_AGENT_INSTRUCTIONS

load_dotenv()

def get_agent_response(user_message, conversation_id, image_path=None):
    """
    Configura e executa o agente de IA.
    """
    db = get_database()
    llm_model = get_llm_model()

    if image_path:
        print(f"Processando imagem: {image_path}")
        extracted_text = extract_text_from_image(image_path)
        user_message = f"O texto extraído da imagem é:\n---\n{extracted_text}\n---\n\nCom base no texto acima, {user_message}"
        print(f"Nova mensagem do usuário com OCR: {user_message}")


    agent = Agent(
        model=llm_model,
        db=db,
        add_history_to_context=True,
        instructions=PHARM_AGENT_INSTRUCTIONS,
        markdown=True
    )
   
    resposta = agent.run(input=user_message)
    return resposta.content
