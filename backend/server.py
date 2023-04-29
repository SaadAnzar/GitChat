# importing dependencies
import os
import openai
import git
from flask import Flask, request, session
from flask_cors import CORS
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


@app.route('/', methods=['POST', 'GET'])
def home():
    return 'Flask is up and running!'


@app.route('/clone', methods=['POST', 'GET'])
def clone_and_index():

    # URL of the repository to clone
    repo_url = request.json['url'] if request.json['url'] else ''
    # Local directory where the repository will be cloned
    local_dir = "repo"
    # Clone the repository
    git.Repo.clone_from(repo_url, local_dir)

    # traversing the directory tree
    root_dir = './repo'
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
    db = DeepLake(dataset_path=f'hub://{username}/pf', embedding_function=embeddings)
    db.add_documents(texts)

    # load dataset, establish retreiver, create conversational chain
    db = DeepLake(dataset_path=f'hub://{username}/pf', read_only=True, embedding_function=embeddings)
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

    return qa

@app.route('/message', methods=['POST', 'GET'])
def message():
    if request.method == 'POST':
        def filter(x):
            if 'com.google' in x['text'].data()['value']:
                return False
            metadata = x['metadata'].data()['value']
            return 'scala' in metadata['source'] or 'py' in metadata['source']


        model = ChatOpenAI(model='gpt-3.5-turbo')
        qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)




if __name__ == '__main__':
    app.run(debug=True, port=1212)