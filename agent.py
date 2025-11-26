from agno.agent import Agent
from dotenv import load_dotenv

from config import get_llm_model, get_database
from prompts import PHARM_AGENT_INSTRUCTIONS

load_dotenv()

def main():
    """
    Configura e executa o agente de IA de vendas.
    """
    db = get_database()
    llm_model = get_llm_model()

    agent = Agent(
        model=llm_model,
        db=db,
        add_history_to_context=True,
        instructions=PHARM_AGENT_INSTRUCTIONS,
        markdown=True
    )
   
if __name__ == "__main__":
    main()
