from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv(r"./lna.env")
class TavilySearch():
  def __init__(self):
    # os.environ['TAVILY_API_KEY'] = 'tvly-************'
    os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")
    #这个需要到网站上注册一下，每个账户有一定的免费额度，https://app.tavily.com/home
    self.tool = TavilySearchResults(max_results=2)
    self.llm = ChatOpenAI(
      model_name="qwen-max",
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    self.prompt = ChatPromptTemplate.from_messages(['system',"""
      请根据联网查询的内容回答用户的问题。
      这是联网的查询内容：{context}
      这是用户的问题: {question}
      """])
  def search_internet(self,question):
    context = self.tool.invoke(question)
    response = self.llm.invoke(self.prompt.format_prompt(context=context,question=question))
    return response.content

  
# ts=TavilySearch()
# print(ts.search_internet("杭州今天天气如何？"))

