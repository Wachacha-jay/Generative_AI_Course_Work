import os;
import dotenv;
import from byllm.llm { Model }


glob llm = Model(model_name="gemini/gemini-2.0-flash");


""" Write a poem about topic """
def write_poetry(topic: str) -> str by llm();


with entry {
    poem = write_poetry("A serene landscape with mountains.");
    print(poem);
}
