# importing dependencies
import os
import openai
import cohere
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# co = cohere.Client('1x0mSd5XIqEOiaauP4sacMJdmAB5hsT48Xy9ZiUl')
# setting environment variables
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
os.environ['ACTIVELOOP_TOKEN'] = os.environ.get('ACTIVELOOP_TOKEN')
cohere_api_key = os.environ.get('COHERE_API_KEY')

# embeddings = OpenAIEmbeddings()
embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)

root_dir = './repo'
docs = []
# traversing the directory tree
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        try:
            laoder = TextLoader(os.path.join(dirpath, file), encoding='utf-8') # concatenate directory_path and file_name
            docs.extend(laoder.load_and_split())
        except Exception as e:
            print(e)


# dividing the loaded files into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

# performing indexing (caluculating embeddings and upserting to ActiveLoop)
username = 'mdarshad1000'
db = DeepLake(dataset_path=f'hub://{username}/twitt', embedding_function=embeddings)
db.add_documents(texts)

# load dataset, establish retreiver, create conversational chain
db = DeepLake(dataset_path=f'hub://{username}/twitt', read_only=True, embedding_function=embeddings)
print(type(db))

retriever = db.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['maximal_marginal_relevance'] = True
retriever.search_kwargs['k'] = 10

def filter(x):
    if 'com.google' in x['text'].data()['value']:
        return False
    metadata = x['metadata'].data()['value']
    return 'scala' in metadata['source'] or 'py' in metadata['source']


model = ChatOpenAI(model='gpt-3.5-turbo')
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

questions = [
    "what are the packages imported?",
    "What does the chat function do?",
]

chat_history = []

for question in questions:
    result = qa({"question":question, "chat_history":chat_history})
    
    chat_history.append((question, result['answer']))
    print(f"Q: {question}\nA: {result['answer']}\n")

print(type(retriever))