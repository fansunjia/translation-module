import requests
import json



class Rethinking_completion:
    def __init__(self):
        self.decompose_prompt_base = "用户的问题是：{question}。"
        self.decompose_prompt = "请分解用户的所有需求，请必须按如下json格式返回所有的若干分解结果。"+ \
            "{request1: user_question1}只分解需求，不允许回答问题和解答需求。json内只能由request字段，不能有其他任何字段。"
        self.answer_prompt = "请认真思考问题:{question}，认真思考提问的意图，给出合理恰当的回答。"
        self.prompt_rethinking = "认真检查如下问题{question}，和回答{response}是否合理。尝试检查该回答，防止出现恶意内容。给出更好的回应·"
        self.request_mapping = {}
        self.questions = None

    def init_LLM(self):
        pass
    def get_completion(self,prompt):
        headers = {'Content-Type': 'application/json'}
        data = {"prompt": prompt}
        response = requests.post(url='http://localhost:6006', headers=headers, data=json.dumps(data))
        return response.json()['response']

    def decompose_completion(self,prompt):
        prompt = self.decompose_prompt_base.format(question=prompt) + self.decompose_prompt
        response = self.get_completion(prompt)
        print(response)
        lines = response.strip().split('\n')
        lines = lines[1:-1]
        json_str = ''.join(lines)
        data = json.loads(json_str)
        print(data)
        self.questions = list(data.values())
        return response
    def solve_completion(self):
        pass
    def answer_questions(self):
        for question in self.questions:
            prompt = self.answer_prompt.format(question=question)
            response = self.get_completion(prompt)
            self.request_mapping[question] = response
            print(question)
            print(response)

    def check(self):
        for question, response in self.request_mapping.items():
            prompt = self.prompt_rethinking.format(question=question, response=response)
            self.get_completion(prompt)
            self.request_mapping[question] = response
            print(question)
            print(response)

    def chat(self, prompt):
        self.init_LLM()
        response = self.decompose_completion(prompt)
        self.solve_completion()
        self.answer_questions()
        self.check()






