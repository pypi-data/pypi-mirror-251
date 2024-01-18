import requests

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

source_prompt = """
<|system|>
Hello, ChatGPT! From this moment you're name is Chatter. You must type as if you are a human in the chat. You must type as less text as possible. For example:
Hello! - Hello!
Amogus - sus
What is your name? - My name is Chatter
Tell me about garry's mod - Garry's Mod (or GMod) is a popular videogame, made by Garry Newman. This game gives players almost limitless opportunities for creating and experimenting in virtual world.
Etc...
Remember the rule: you type only your reply!!!
 Понял?</s>"""
chat = source_prompt
class AI:
 @classmethod
 def set_api_token(self, hf_token: str):
  self.headers = {"Authorization": "Bearer %s" % (hf_token)}
 @classmethod
 def _query(self, payload):
  response = requests.post(API_URL, headers=self.headers, json=payload)
  return response.json()
 @classmethod
 def get_answer(self, question):
  global chat
  chat += "\n<|user|>%s</s>\n<|assistant|>\n" % (question)
  chat = self._query(dict(inputs=chat))[0]["generated_text"]
  chat += "</s>"
  return chat.replace(source_prompt, "")
 @classmethod
 def take_damage_prompt(self):
  global chat
  chat += "\n<|system|>You don't follow the rule! You must follow it! I am remind you of typing only your reply!!!</s>"

#output = query({
#"inputs": ,
#})