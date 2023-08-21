import os

# flask imports
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from decouple import config
from flask_wtf import FlaskForm
from wtforms import SubmitField

# llm imports
import os
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings

# python script imports
from python.handle_user_input import get_query

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY', default='you-will-never-guess')
app.config['UPLOAD_FOLDER'] = './static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}


class UploadForm(FlaskForm):
    submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def setup_retriever():
    #OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') # set in .env file
    
    # load context urls from file
    with open('context_urls.txt', 'r') as file: ## make this filename an environment variable
        context_urls = [line.strip() for line in file]

    # prep documents
    loader            = WebBaseLoader(context_urls)
    documents         = loader.load()
    text_splitter     = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts             = text_splitter.split_documents(documents)
    persist_directory = 'db'
    embeddings        = OpenAIEmbeddings() #embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-xl", device="cpu")
    vectordb          = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory)
    retriever         = vectordb.as_retriever()

    # chain to answer questions 
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0.2), chain_type="stuff", retriever=retriever, return_source_documents=True)
    
    return qa_chain

llm = setup_retriever() # set up llm once

## ROUTES ## 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            sound = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sound = sound + 10  # Increase volume
            output_filename = "loud_" + filename
            sound.export(os.path.join(app.config['UPLOAD_FOLDER'], output_filename), format='wav')
            return render_template('index.html', form=form, filename=filename)#output_filename)
    return render_template('index.html', form=form)

@app.route('/ask_llm', methods=['POST'])
def ask_llm():
    user_input = get_query(request.json['userInput'], request.json['error'], request.json['errorValue'])

    print('LLM thinking...')
    llm_response = llm(user_input)
    print('LLM finished thinking.')
    
    return jsonify(result=llm_response['result'])

@app.route('/ask_llm_only', methods=['POST'])
def ask_llm_only():
    user_input = request.json['userInput']

    print('LLM thinking...')
    llm_response = llm(user_input)
    print('LLM finished thinking.')
    
    return jsonify(result=llm_response['result'])

@app.route('/get-js-code', methods=['POST'])
def get_js_code():
  user_input = request.json['result']
  js_code = user_input # ex. "wavesurfer.setVolume(0.5)"  
  return jsonify(result=js_code)

if __name__ == '__main__':
    app.run(debug=True)
