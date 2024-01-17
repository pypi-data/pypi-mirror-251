import argparse
import os
import pathlib
import requests
import zipfile
import click
from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.markdown import Markdown
from rich.console import Console

from .utils.env import initialize_environment

def create_app_directory():
    # Example for a user-specific directory
    app_dir = pathlib.Path.home() / '.portainerlang'
    
    # Create the directory if it doesn't exist
    if not app_dir.exists():
        app_dir.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    create_app_directory()
    # Rest of your CLI application logic

def download_and_extract(url, extract_to):
    extract_to_path = pathlib.Path.home() / extract_to
    extract_to_path.mkdir(parents=True, exist_ok=True)

    # Check if the directory is empty
    if any(extract_to_path.iterdir()):
        print("Assets already exist. Skipping download.")
        return

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kilobyte

            zip_file_path = extract_to_path / 'temp_archive.zip'

            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(zip_file_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_path)

            os.remove(zip_file_path)
        else:
            raise Exception(f"Failed to download the file: Status code {response.status_code}")
    except Exception as e:
        raise Exception(f"Error in download_and_extract: {e}")

@click.command()
@click.argument('query', nargs=-1)  # -1 to accept an unlimited number of arguments
def process_query(query):
    """Process the entire query as a single argument."""
    # Join the query terms into a single string
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

def main():
    create_app_directory()

    try:
        download_and_extract("https://anthony.portainer.io/portainerlang-faiss.zip", ".portainerlang/data")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    required_vars = [
        'OPENAI_API_KEY',
    ]
    initialize_environment(required_vars)

    process_query()

if __name__ == '__main__':
    main()
