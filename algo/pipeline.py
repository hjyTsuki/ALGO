from response import TurboResponser
from abc import ABC, abstractmethod
import openai
from prompts import CF_PROMPT
from loader import get_datasets
class InputGenerator():
    def __init__(self, responser):
        self.SYSTEM_PROMPT = "You are an expert software tester tasked with thoroughly testing a given piece of code. "
        self.responser = responser

    def respond(self, prompt: str) -> str:
        return self.responser.respond(self.SYSTEM_PROMPT, prompt)


class Verifier():
    def __init__(self, responser):
        self.SYSTEM_PROMPT = "You are an AI programming assistant."
        self.responser = responser

    def respond(self, prompt: str) -> str:
        return self.responser.respond(self.SYSTEM_PROMPT, prompt)

def eval(gen_result):
    return None

def main():
    input_gen = InputGenerator(TurboResponser())
    oracle_gen = Verifier(TurboResponser())

    dataset = get_datasets("leetcode")[0: 1]

    gen_result = []

    for item in dataset:
        gen_prompt = CF_PROMPT["data_generator"]
        gen_prompt = gen_prompt.format(problem=item["full"])

        test_case_gen_code = input_gen.respond(gen_prompt)
        print("test_case")
        print(test_case_gen_code)

        oracle_prompt = CF_PROMPT["oracle_generator"]
        oracle_prompt = oracle_prompt.format(problem=item["question"], examples=item["example"])

        oracle = oracle_gen.respond(oracle_prompt)
        print("oracle")
        print(oracle)

        gen_result.append(
            {
                "test_case_gen_code": test_case_gen_code,
                "oracle": oracle
            }
        )

    eval(gen_result)


if __name__ == "__main__":
    main()