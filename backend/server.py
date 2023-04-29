# importing dependencies
import os
import openai
import git
import random
import string
from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from langchain.embeddings import CohereEmbeddings
from langchain.document_loaders import TextLoader
from langchain.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


# setting environment variables
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
os.environ['ACTIVELOOP_TOKEN'] = os.environ.get('ACTIVELOOP_TOKEN')
username = 'mdarshad1000'
embeddings = CohereEmbeddings()


app = Flask(__name__)
CORS(app,)
app.secret_key = 'your_secret_key_here'


@cross_origin(supports_credentials=True)
@app.route('/', methods=['POST', 'GET'])
def home():
    return 'Flask is up and running!'

@cross_origin(supports_credentials=True)
@app.route('/clone', methods=['POST', 'GET'])
def clone_and_index():
    # URL of the repository to clone
    repo_url = request.json['url'] if request.json['url'] else ''
    question = request.json['prompt'] if request.json['prompt'] else ''

    print("THIS IS URL", repo_url)
    # Local directory where the repository will be cloned
    local_dir =  ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    print(local_dir)
    print("THIS IS LOCAL DIR", local_dir)
    # Clone the repository
    git.Repo.clone_from(repo_url, local_dir)

    # traversing the directory tree
    root_dir = (f'./{local_dir}')
    print(root_dir)
    docs = []
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
    db = DeepLake(dataset_path=f'hub://{username}/{local_dir}', embedding_function=embeddings)
    db.add_documents(texts)

    # load dataset, establish retreiver, create conversational chain
    db = DeepLake(dataset_path=f'hub://{username}/{local_dir}', read_only=True, embedding_function=embeddings)


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
    
    chat_history = []
    result = qa({"question":question, "chat_history":chat_history})
    chat_history.append((question, result['answer']))

    return {"answer":result['answer']}



if __name__ == '__main__':
    app.run(debug=True, port=1212)