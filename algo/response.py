import os
import time
import openai
from abc import ABC, abstractmethod
import google.generativeai as genai

class Responser(ABC):

    @abstractmethod
    def respond(self, system_info: str, user_prompt: str) -> str:
        pass


class GPT4Responser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-4'):
        """ environment information """
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
        # openai.api_base = os.environ.get("OPENAI_API_BASE")
        openai.api_key = 'sk-MfsGu5ILuHxYMuoSGYAbX0lwMMO2rnfjIqMZGxI0RgLaf89Y'
        openai.api_base = 'https://www.blueshirtmap.com/v1'
        openai.api_type = 'azure'
        openai.api_version = '2023-07-01-preview'
        self.model = model

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        try:
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=2000,
                stop=None,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"{e}\nRate Limit Reached! Sleeping for 20 secs...")
            time.sleep(20)
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=2000,
                stop=None,
            )
            return response['choices'][0]['message']['content']


class TurboResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-3-turbo'):
        """ environment information """
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
        # openai.api_base = os.environ.get("OPENAI_API_BASE")
        openai.api_key = 'sk-MfsGu5ILuHxYMuoSGYAbX0lwMMO2rnfjIqMZGxI0RgLaf89Y'
        openai.api_base = 'https://www.blueshirtmap.com/v1'

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        messages = [
            {"role": "system", "content": system_info},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.ChatCompletion.create(
            # model='gpt-4',
            # model='gpt-3.5-turbo',
            model = "gpt-4o-mini-2024-07-18",
            # model='gpt-4-code-interpreter',
            # model='gpt-3.5-turbo-16k',
            temperature=0,
            messages=messages
        )
        return response['choices'][0]['message']['content']


class GeminiResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, api_key, model='gemini-pro'):
        """ environment information """
        genai.configure(api_key=api_key)
        config = genai.types.GenerationConfig(
            stop_sequences=['<|endoftext|>'],
            max_output_tokens=2048,
            temperature=0.1,
            top_k=1,
            top_p=1
        )
        self.model = genai.GenerativeModel(model, generation_config=config)

    def respond(self, system_info: str, user_prompt: str) -> str:
        response = self.model.generate_content(system_info + "Code for the bug to be implanted：\n" + user_prompt, stream=True)
        response.resolve()
        return response.text

#
# from openai import OpenAI
# class DeepseekResponser(Responser):
#     """ Openai LLM responser """
#
#     def __init__(self):
#         """ environment information """
#         self.client = OpenAI(api_key="sk-09a35a9c937e44bfb5c0166c0a158a6e", base_url="https://api.deepseek.com")
#
#     def respond(self, system_info: str, user_prompt: str) -> str:
#         response = self.client.chat.completions.create(
#             model="deepseek-chat",
#             messages=[
#                 {"role": "system", "content": system_info},
#                 {"role": "user", "content": user_prompt},
#             ],
#             stream=False
#         )
#         return response.choices[0].message.content


if __name__ == '__main__':
    # gpt4_responser = GPT4Responser()
    # turbo_responser = TurboResponser()
    # print(turbo_responser.respond(system_info="Translate the text into English",
    #                               user_prompt=f"El presidente de la República, Andrés Manuel López Obrador"))
    gen = TurboResponser()
    print(gen.respond(system_info="you are a helpful assistant", user_prompt="fuck you"))
