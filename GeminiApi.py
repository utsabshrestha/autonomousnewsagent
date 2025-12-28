from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

class GeminiApi:
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = None
    model="gemini-2.5-flash"
    # model="gemma-3-27b"
    llm = None

    def __init__(self):
        try:
            Google_api_key = os.environ["GOOGLE_API_KEY"]
            if not Google_api_key:
                print(f"Google Api Key is not accessible")
                exit(1)

            self.llm = ChatGoogleGenerativeAI(model=self.model, temperature=0)
            response = self.llm.invoke("Introduce yourself in few words")
            print(response.content)
        except Exception as error:
            print(f"Error @ {GeminiApi.__init__.__name__} : {error}")

    def GetInstance(self):
        return self.llm