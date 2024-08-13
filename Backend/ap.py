from dotenv import load_dotenv
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
import os
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
import os
from langchain import PromptTemplate

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
 
def main(q):
    pdf = "C:/Users/VAMSI/Downloads/ML Resume (1).pdf"
    pdf1="C:/Users/VAMSI/Downloads/Vamsi Template docx.pdf"
    pdf2="C:/Users/VAMSI/Downloads/Vamsi Full Resume.pdf"
    pdf3="C:/Users/VAMSI/Downloads/Vamsi Resume new.pdf"
    pdf4="C:/Users/VAMSI/Downloads/vamsi resume.pdf"
    pdf5="C:/Users/VAMSI/Downloads/Vamsi's Resume.pdf"

    pdf_reader = PdfReader(pdf)
    pdf_reader1 = PdfReader(pdf1)
    pdf_reader2 = PdfReader(pdf2)
    pdf_reader3 = PdfReader(pdf3)
    pdf_reader4 = PdfReader(pdf4)
    pdf_reader5 = PdfReader(pdf5)
    text = ""
    for page in pdf_reader1.pages:
        text += page.extract_text()
    for page in pdf_reader2.pages:
        text += page.extract_text()
    for page in pdf_reader3.pages:
        text += page.extract_text()
    for page in pdf_reader4.pages:
        text += page.extract_text()
    for page in pdf_reader5.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
        )
    chunks = text_splitter.split_text(text=text)

    vectorstore = Chroma.from_texts(embedding=OpenAIEmbeddings(),texts=chunks,collection_name='test',persist_directory='vectorstore')
    # vectorstore = Chroma(persist_directory='C:/Users/VAMSI/OneDrive/Desktop/chat_wit_pdf/Chat_With_PDF/vectorstore',embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    print(retriever)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    template = """You are a helpful assistant. 
              Answer the following question in a dead pool style 
              you have no interest in giving response about him and you dont like him 
              so start with Belittling him in general context some small roast and tease
             provide 50percent of the information with the given context and then roast him by Belittling him:{context},{question} """
    # Create a PromptTemplate object
    prompt = PromptTemplate(template=template, input_variables=["question"])
    # prompt = hub.pull("rlm/rag-prompt")
    print(prompt)
    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )
    query = q
    result=rag_chain.invoke(query)
    
    return result
 
if __name__ == '__main__':
    main()