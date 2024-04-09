from langchain.prompts import (PromptTemplate, ChatPromptTemplate, FewShotChatMessagePromptTemplate)
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_community.llms import Ollama
import pandas as pd
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.agents.types import AgentType
from langchain.chains import LLMChain
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import re
from io import StringIO
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

# Define the document content description
document_content_description = "Tables of automotive parameters"

# Define the headers
columns = ["Clndrs", "Volumn", "HpX", "Model", "Origin", "Lbs-", "Acc-", "Mpg+"]

# Add prompt information for columns headers
columns_prompt_info = {
    "Clndrs": "Number of Cylinders",
    "Volumn": "Cylinder capacity",
    "HpX": "Horsepower",
    "Model": "Model of the car",
    "Origin": "Origin of the car, e.g. 1 for USA, 2 for Europe, 3 for Japan",
    "Lbs-": "Weight of the car",
    "Acc-": "Acceleration",
    "Mpg+": "Miles per gallon",
}

examples = [
    {
        "question": "Which car is has more horse power, A or B or Same? A: [4, 140, 86, 82, 1, 2790, 15.6, 30] B: [4, 91, 67, 82, 3, 1965, 15.7, 30]?",
        "answer": "A",
    },
    {
        "question": "Which car is has more horse Cylinders, A or B or Same? A: [4, 140, 86, 82, 1, 2790, 15.6, 30] B: [4, 91, 67, 82, 3, 1965, 15.7, 30]?",
        "answer": "Same"
    },
    {
        "question": "Which car is has more horse power, A or B or Same? A: [4, 140, 86, 82, 1, 2790, 15.6, 30] B: [4, 91, 67, 82, 3, 1965, 15.7, 30]?",
        "answer": "A",
    },
    {
        "question": "Which car is has more horse Cylinders, A or B or Same? A: [4, 140, 86, 82, 1, 2790, 15.6, 30] B: [4, 91, 67, 82, 3, 1965, 15.7, 30]?",
        "answer": "Same"
    },
]


        
example_prompt = PromptTemplate(
    input_variables=["question", "answer"], template="question: {question}\nanswwer: {answer}"
)


prefix = "You are an excellent car shopping guider. You will be provided with two python lists. Each list contains the following parameters: Number of Cylinders, Cylinder capacity, Horsepower, Model of the car, Origin of the car, Weight of the car, Acceleration, Miles per gallon. You need to compare the two lists and answer the question. If the first list has more horsepower, you should answer 'A'. If the second list has more horsepower, you should answer 'B'. If both lists have the same horsepower, you should answer 'Same'. ONLY ANSWER THE LAST QUESTION! .\n"

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix = prefix,
    suffix="Question: {input}. Format of respond: 'My answer: A or B or Same.'",
    input_variables=["input"],
)

llm = Ollama(model="llama2:13b")

def sort_rows_with_preference(rows, preference):
    # print(rows)
    
    n = len(rows)
    for i in range(n):
        for j in range(0, n-i-1):
            # prompt.format(input=f"Which car is {preference}, A or B or Same? A: {str(rows[j].cells)} B: {str(rows[j+1].cells)}")
            
            chain = prompt | llm | StrOutputParser()
            # print(chain.invoke({"input": f"Which car is {preference}, A or B or Same? A: {str(rows[j].cells)} B: {str(rows[j+1].cells)}"}))
            respond = chain.invoke({"input": f"Which car is {preference}, A or B or Same? A: {str(rows[j].cells)} B: {str(rows[j+1].cells)}"})
            if 'B' in respond:
                rows[j], rows[j+1] = rows[j+1], rows[j]

    # print(rows)
    return rows
    
    
    
    


    
    
    
