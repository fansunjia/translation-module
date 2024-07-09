import requests
import json
import pandas as pd
import requests
import json
import os
import re
from tqdm import tqdm
import qianfan
import requests
import json
os.environ["QIANFAN_ACCESS_KEY"] = "ALTAKCTIeA2uEd4DfIWxXypzuC"
os.environ["QIANFAN_SECRET_KEY"] = "6fb99576e08343bf9554ab2b4322d741"

class translation:
    def __init__(self, LLM_name = None, translation_prompt = None):
        self.LLM_name = LLM_name
        self.access_token = None
        self.get_access_token()
        if LLM_name is not None:
            self.chat_comp = qianfan.ChatCompletion()
        if translation_prompt is not None:
            self.translation_prompt = translation_prompt
        else:
            self.translation_prompt = "你是一个翻译员，可以准确的将输入的语言翻译到目标语言上。你的回答中，只能包括已经翻译为目标语言的文本。"

    def translate(self, text, method = "ML", from_language = "auto", to_language = "zh"):
        if method == "LLM":
            return self.translate_LLM(text, from_language = from_language, to_language = to_language)
        elif method == "ML":
            return self.translate_ML(text, from_language = from_language, to_language = to_language)


    def translate_LLM(self, text, from_language = "auto", to_language = "en"):
        text_prompt = "翻译的目标语言是" + to_language + "，翻译的源语言是" + from_language + "，请翻译以下内容："+ text
        resp = self.chat_comp.do(model=self.LLM_name, messages=[{
            "syetem": self.translation_prompt,
            "role": "user",
            "content": text_prompt,
            "temperature": 0.3,
            "top_p": 0.3
        }])
        print(resp["body"]['result'])
        return resp["body"]['result']

    def translate_ML(self, text, from_language = "auto", to_language = "en"):
        url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + self.access_token

        payload = json.dumps({
            "q": text,
            "from": from_language,
            "to": to_language
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": "nbUZdYB5oOKJjmZvpmzimt6F",
                  "client_secret": "gaIRpzoDx2IBKtMVxwmWH8bLFko8zbmf"}
        self.access_token = str(requests.post(url, params=params).json().get("access_token"))
