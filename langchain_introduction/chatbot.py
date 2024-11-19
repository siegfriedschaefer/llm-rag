
import dotenv
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
import os

dotenv.load_dotenv()

# chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
# chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
# chat_model = ChatOpenAI(model="gpt-4-turbo", temperature=0.5)
# chat_model = ChatOpenAI(model="o1-preview-2024-09-12", temperature=0.5)

chat_model = ChatMistralAI(model="Mixtral-8x22B-Instruct-v0.1", 
                        api_key=os.getenv('OVHAI_ENDPOINTS_API_KEY'),
                        endpoint='https://mixtral-8x22b-instruct-v01.endpoints.kepler.ai.cloud.ovh.net/api/openai_compat/v1', 
                        max_tokens=1500, 
                        streaming=True)

