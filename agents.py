# This is the heart of the project. We will build 4 things here. First the Search Agent using create_react_agent + AgentExecutor which will use the web_search tool. Second the Reader Agent using the same pattern but with the scrape_url tool. Third the Write Chain using the modern LCEL pipe syntax -prompt | 11m | StrOutputParser() which takes the research and writes a full report. Fourth the Critic CHain again using LCEL pipeline which reads the report and gives a score and feedback
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv  

load_dotenv()  # Load environment variables from .env file

#Model Setup
llm= ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


#1st Agent
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search],
        system_prompt="You are a search agent. You must search the web to find recent and reliable information. Always use the web_search tool to find URLs and actual sources. Return the search results."
    )


#2nd Agent
def build_reader_agent():
    return create_agent(
        model= llm,
        tools= [scrape_url],
        system_prompt="You are a reader agent. You must select the most relevant URL from the search results and use the scrape_url tool to extract its content. Always perform scraping using the tool."
    )

#Writer chain

writer_prompt= ChatPromptTemplate.from_messages([
    ('system', "You are an expert research writer. Write clear, structured and insightful reports. "),
    ('human', """Write a detailed research report on the topic below.
     Topic: {topic} 
     
     Research Gathered:
     {research}
     
     Structure the report as:
     -Introduction
     -Key Findings (minimum 3 well-explained points)
     -Conclusion
     -Sources (list all URLs found in the research)

     Be detsailed, factual and professional."""),
])

writer_chain= writer_prompt | llm | StrOutputParser()

#Critic Chain

critic_prompt= ChatPromptTemplate.from_messages([
 ('system', "You are an expert research writer. Write clear, structured and insightful reports. "),
 ('human', """Write a detailed research report on the topic below.
  
  Report:
  {report}
  
  Respond in this exact format:
  
  Score : X/10
  
  Strengths:
   - ...
   - ...
  
  Areas to Improve:
  - ...
  - ...
  
  One liner verdict:
  ..."""),
        
])

critic_chain= critic_prompt | llm | StrOutputParser()