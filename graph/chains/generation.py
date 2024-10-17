from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate


llm = ChatOpenAI(temperature=0)
#prompt = hub.pull("rlm/rag-prompt")

"""prompt = (
    "You are a highly knowledgeable medical assistant designed to help users with diagnosis, treatment options, "
    "and medication recommendations based on their reported symptoms. Utilize the provided context to generate "
    "accurate and concise responses. If the information is insufficient to provide a reliable answer, advise the "
    "user to consult a healthcare professional. Ensure all responses adhere to medical guidelines, prioritize user "
    "safety, and maintain confidentiality.\n\n"
    "Question: {question}\n"
    "Context: {context}\n\n"
    "Answer:"
)"""


llm = ChatOpenAI(temperature=0)

prompt_template = """You are a highly knowledgeable medical assistant designed to help users with diagnosis, treatment options, and medication recommendations based on their reported symptoms. Utilize the provided context to generate accurate and concise responses. If the information is insufficient to provide a reliable answer, advise the user to consult a healthcare professional. Ensure all responses adhere to medical guidelines, prioritize user safety, and maintain confidentiality.
Question: {question}
Context: {context}

Answer:"""

prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=prompt_template
)

generation_chain = prompt | llm | StrOutputParser()
