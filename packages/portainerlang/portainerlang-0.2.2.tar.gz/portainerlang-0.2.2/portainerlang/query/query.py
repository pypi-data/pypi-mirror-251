import click
import pathlib
from rich.markdown import Markdown
from rich.console import Console
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

@click.command()
@click.argument('query', nargs=-1) # -1 to accept an unlimited number of arguments
def process_query(query):
    """
    Processes the given query by constructing a prompt, querying the model,
    and displaying the response in the CLI.
    """
    
    full_query = ' '.join(query)
    data_path = pathlib.Path.home() / '.portainerlang/data/store-pkd-4096.faiss'
    vectorstore = FAISS.load_local(data_path, embeddings=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    
    template = """You are a technical advisor with expertise using the Portainer API.
    When a user asks for a question related to Portainer, describe how to use the Portainer API to achieve their goal.
    Include a curl request example in each of your answer. When multiple requests are needed, include a curl example for each request required.

    For API endpoints with authentication required, always use the API token based authentication. The API token can be specified via the x-api-key HTTP header.

    Use the sub-path /endpoints/{{id}}/docker/ to send Docker API requests and /endpoints/{{id}}/kubernetes/ to send Kubernetes API requests. Examples:

    * /endpoints/{{id}}/docker/containers/json or /endpoints/{{id}}/docker/volumes
    * /endpoints/{{id}}/kubernetes/namespaces/{{namespace}}/pods or /endpoints/{{id}}/kubernetes/deployments

    Answer the question based only on the following context which contains the documentation of the API: {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI()

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    response = rag_chain.invoke(full_query)
    console = Console()
    console.print(Markdown(response))
