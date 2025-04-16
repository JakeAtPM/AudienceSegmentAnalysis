import openai
from dotenv import load_dotenv

#api key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
