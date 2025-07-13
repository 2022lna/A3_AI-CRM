from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 创建一个名为loader的TextLoader对象，加载文本文件"data/text.txt"
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
class RAG_QA:
   def __init__(self): 
      load_dotenv(r"./lna.env")
      self.llm = ChatOpenAI(
                  model="qwen-max",
                  api_key=os.getenv("DASHSCOPE_API_KEY"),
                  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
              )
      loader = TextLoader("./QA.txt",encoding="utf-8")
      # 调用TextLoader对象的load方法，加载文本文件内容
      docs=loader.load()
      text_splitter = RecursiveCharacterTextSplitter(
          chunk_size=300,           # 每块约 300 字符
          chunk_overlap=50,         # 块之间重叠 50 字符，保证上下文连续
          separators=["\n\n", "\n", "。", "；", "？", "！", "，", " ", ""],  # 按中文语义优先切分
          length_function=len,
          add_start_index=True
      )
      # 切分文档
      split_docs = text_splitter.split_documents(docs)
      # # 输出查看
      # for i, doc in enumerate(split_docs):
      #     print(f"Chunk {i+1}:\n{doc.page_content}\n{'-'*50}")
      from langchain.embeddings import DashScopeEmbeddings
      #这里要换成阿里提供的通用文本向量工具
      # 创建一个DashScopeEmbeddings对象并赋值给embeddings_model变量
      embeddings_model = DashScopeEmbeddings(
          dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
      )
      texts = [doc.page_content for doc in split_docs]
      # # 使用embeddings_model对象的embed_documents方法对文档列表进行嵌入处理
      # embeddings = embeddings_model.embed_documents(texts)
      from langchain_community.vectorstores import Chroma
      self.vectorstore = Chroma.from_texts(texts, embeddings_model)#创建向量库

   def query(self, question):
      results = self.vectorstore.similarity_search(question, k=2)# 查询
      if not results:
          context = "没有查询到相关信息"  # 处理无结果的情况
      context= "\n\n".join([f"文档片段 {i+1}:\n{doc.page_content}" for i, doc in enumerate(results)])
      prompt = ChatPromptTemplate.from_messages([('system',"""
      你是一个智能助手，请基于以下RAG查询文档的返回内容回答用户问题，
      回答时请以：根据文档查询结果来看类似的话术开头，注意回答内容的语句要通顺                                             
      相关文档查询结果和文档内容如下：{context}                                           
      """),
      ('user',"""用户问题: {question}""")
      ])
      return self.llm.invoke(prompt.format(context=context, question=question)).content
# rag_qa = RAG_QA()
# print(rag_qa.query("course 表的作用是什么？它包含哪些字段？"))