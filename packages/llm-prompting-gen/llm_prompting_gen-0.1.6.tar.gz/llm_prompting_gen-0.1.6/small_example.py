
from llm_prompting_gen.generators import PromptEngineeringGenerator
from langchain.chat_models import ChatOpenAI

# Simply load a JSON file following the format of llm_prompting_gen.models.prompt_engineering.PromptElement
# Make sure env variable OPENAI_API_KEY is set
llm = ChatOpenAI(temperature=0.0)
keyword_extractor = PromptEngineeringGenerator.from_json("templates/test.json", llm=llm)
llm_output = keyword_extractor.generate(text="Explain Prompt Engineering")


