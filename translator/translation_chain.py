from langchain.chains import LLMChain
from langchain_community.chat_models.zhipuai import ChatZhipuAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from utils import LOG

class TranslationChain:
    def __init__(self, model_name: str = "glm-4", verbose: bool = True):

        # Translation task is always performed by the System role
        template = (
            """You are a translation expert, proficient in various languages. \n
            Translates {source_language} to {target_language}."""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        LOG.debug(f"[system_message_prompt]\n {system_message_prompt}")
        # The text to be translated is input by the Human role
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        LOG.debug(f"[human_template]\n {human_template}")
        # Construct ChatPromptTemplate using the templates of System and Human roles
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        LOG.debug(f"[chat_prompt_template]\n {chat_prompt_template}")
        # Set temperature to 0.01 for translation result stability
        # in that setting a temperature to zero is not supported for zhipuAi
        chat = ChatZhipuAI(model_name=model_name, temperature=0.01, verbose=verbose)
        LOG.debug(f"[chat]\n {chat}")
        self.chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)

    def run(self, text: str, source_language: str, target_language: str) -> (str, bool):
        result = ""
        try:
            result = self.chain.run({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
            })
            LOG.debug(f"[translation_result]\n {result}")
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return result, False
        return result, True