import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

os.environ['OPENAI_API_KEY'] = os.environ['OPENAI_KEY']

# App Framework
st.title('YouTube GPT Creator')
prompt = st.text_input('Plug in your prompt here:')

# Prompt template
title_template = PromptTemplate(
  input_variables = ['topic'],
  template = 'write me a youtube video title {topic}'
)

script_template = PromptTemplate(
  input_variables = ['title', 'wikipedia_research'],
  template = 'write me a youtube video script based on the title {title} while leveraging this wikipedia research {wikipedia_research}'
)

# Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# Create LLM
llm = OpenAI(temperature = 0.9)
title_chain = LLMChain(llm=llm, prompt = title_template, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt = script_template, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# LLM respond to prompt
if prompt:
  title = title_chain.run(prompt)
  wiki_research = wiki.run(prompt)
  script = script_chain.run(title=title, wikipedia_research=wiki_research)
  
  st.write(title)
  st.write(script)
  
  with st.expander('Title History'):
    st.info(title_memory.buffer)

  with st.expander('Title History'):
    st.info(script_memory.buffer)