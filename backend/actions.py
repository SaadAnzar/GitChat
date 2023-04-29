#  importing dependencies
import os
import git
import openai
from dotenv import load_dotenv

from langchain.embeddings.cohere import CohereEmbeddings 
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

def clone(url: str) -> None:
    # URL of the repository to clone
    repo_url = url
    # Local directory where the repository will be cloned
    local_dir = "repo"
    # Clone the repository
    git.Repo.clone_from(repo_url, local_dir)

# setting environment variables
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
os.environ['ACTIVELOOP_TOKEN'] = os.environ.get('ACTIVELOOP_TOKEN')
cohere_api_key = os.environ.get('COHERE_API_KEY')
embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)


docs = []
# traversing the directory tree
def traverse_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            try:
                laoder = TextLoader(os.path.join(dirpath, file), encoding='utf-8') # concatenate directory_path and file_name
                docs.extend(laoder.load_and_split())
            except Exception as e:
                print(e)


# dividing the loaded files into chunks
def divide_into_chunks(docs):
    username = 'mdarshad1000'
    embeddings = CohereEmbeddings()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    # performing indexing (caluculating embeddings and upserting to ActiveLoop)
    db = DeepLake(dataset_path=f'hub://{username}/Pulp_Fiction', embedding_function=embeddings)
    db.add_documents(texts)
    # load dataset, establish retreiver, create conversational chain
    db = DeepLake(dataset_path=f'hub://{username}/Pulp_Fiction', read_only=True, embedding_function=embeddings)
    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['fetch_k'] = 100
    retriever.search_kwargs['maximal_marginal_relevance'] = True
    retriever.search_kwargs['k'] = 10
    return retriever

def filter(x):
    if 'com.google' in x['text'].data()['value']:
        return False
    metadata = x['metadata'].data()['value']
    return 'scala' in metadata['source'] or 'py' in metadata['source']

def qna(retriever, question):
    model = ChatOpenAI(model='gpt-3.5-turbo')
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
    questions = question
    chat_history = []
    result = qa({"question":question, "chat_history":chat_history})
    
    chat_history.append((question, result['answer']))
    return (f"Q: {question}\nA: {result['answer']}\n")
