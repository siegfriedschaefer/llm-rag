
import dotenv
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
# chat_model = ChatOpenAI(model="gpt-4-turbo", temperature=0.5)
# chat_model = ChatOpenAI(model="o1-preview-2024-09-12", temperature=0.5)
