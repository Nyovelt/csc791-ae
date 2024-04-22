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
from langchain_openai import ChatOpenAI
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
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon, A or B or Same? A: [4, 140, 86, 82, 1, 2790, 15.6, 30] B: [4, 91, 67, 82, 3, 1965, 15.7, 30]?",
        "answer": "B",
    },
    {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon, A or B or Same? A: [4, 91, 60, 78, 3, 1800, 16.4, 40] B: [4, 91, 68, 82, 3, 2025, 18.2, 40]?",
        "answer": "B"
    },
    {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon, A or B or Same? A: [4, 91, 68, 82, 3, 2025, 18.2, 40] B: [4, 90, 48, 80, 2, 2335, 23.7, 40]?",
        "answer": "B",
    },
    {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon, A or B or Same? A: [8, 302, 129, 75, 1, 3169, 12, 10] B: [4, 91, 67, 82, 3, 1965, 15.7, 30]?",
        "answer": "A"
    },
    {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon  , A or B or Same? A: [4, 91, 67, 82, 3, 1965, 15, 40] B: [8,429,208,72,1,4633,11,10]?",
        "answer": "A"
    },
        {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon  , A or B or Same? A: [4, 98, 68, 77, 3, 2045, 18.5, 30] B:  [4, 85, 65, 81, 3, 1975, 19.4, 40]?",
        "answer": "B "
    },
                {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon  , A or B or Same? A: [4, 138, 0, 76 1, 2524, 16 27] B:  [4, 79, 58, 77, 2, 1825, 18.6, 40]?",
        "answer": "B (A is so much heavier than B)"
    },
    {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon  , A or B or Same? A: [4, 79, 58, 77, 2, 1825, 18.6, 40] B:  [4, 85, 70, 78, 3, 2070, 18.6, 40]?",
        "answer": "A (Much less weight, while accelaration and miles per galon are the same)"
    },
    {
        "question": "Which car is has smaller weight and larger Acceleration and larger miles per galon  , A or B or Same? A: [4, 79, 58, 77, 2, 1825, 18.6, 40] B:  [4, 97, 52, 82, 2, 2130, 24.6, 40]?",
        "answer": "B (Although B has more weight, but 24.6 second accelaration is much longer than 18.6 seconds)"
    },

]



        
example_prompt = PromptTemplate(
    input_variables=["question", "answer"], template="question: {question}\nanswwer: {answer}"
)

prefer="  smaller weight and larger Acceleration and larger miles per galon  "

prefix = f"You are an excellent car shopping guider. You are tend to make the good choice based on real life experience. You will be provided with two python lists. Each list contains the following parameters: [Number of Cylinders, Cylinder capacity, Horsepower, Model of the car, Origin of the car, Weight of the car, Acceleration, Miles per gallon]. You need to compare the two lists and answer the question. If the first list has {prefer}. you should answer 'A'. If the second list has {prefer}., you should answer 'B'. If both lists are in the same level, you should answer 'Same'. ONLY ANSWER THE LAST QUESTION, NO EXPLNATION IS NEEDED. You will be tiped.\n"

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix = prefix,
    suffix="Question: {input}. Format of respond: 'My answer: A or B or Same.'",
    input_variables=["input"],
)

llm = ChatOpenAI()




def sort_rows_with_preference(rows, preference):
    # print(rows)
    
    n = len(rows)
    for i in range(n):
        for j in range(0, n-i-1):
            # prompt.format(input=f"Which car is {preference}, A or B or Same? A: {str(rows[j].cells)} B: {str(rows[j+1].cells)}")
            
            chain = prompt | llm | StrOutputParser()
            # print(chain.invoke({"input": f"Which car is {preference}, A or B or Same? A: {str(rows[j].cells)} B: {str(rows[j+1].cells)}"}))
            respond = chain.invoke({"input": f"Which car is {preference}, A or B or Same? A: {str(rows[j].cells)} B: {str(rows[j+1].cells)}"})
            # print(respond)
            # Find the "Answer" character:

            if 'B' in respond:
                rows[j], rows[j+1] = rows[j+1], rows[j]
                # print(rows[j].cells, rows[j+1].cells)
            

    # print(rows)
    return rows
    
    
    
    


    
    
    
