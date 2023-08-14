import os

# flask imports
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from decouple import config
from flask_wtf import FlaskForm
from wtforms import SubmitField

# llm imports
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# python script imports
from python.handle_user_input import load_embeddings, get_query

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY', default='you-will-never-guess')
app.config['UPLOAD_FOLDER'] = './static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}

class UploadForm(FlaskForm):
    submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

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
    print('Starting LLM setup...')
    user_input = get_query(request.json['userInput'])
    embeddings_path = "./embeddings"
    db_instructEmbedd = load_embeddings(sotre_name='instructEmbeddings', path=embeddings_path)
    retriever = db_instructEmbedd.as_retriever(search_kwargs={"k": 3})
    
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') # set in .env file

    # create the chain to answer questions 
    qa_chain_instrucEmbed = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY), 
                                    chain_type="stuff", 
                                    retriever=retriever, 
                                    return_source_documents=True)
    llm_response = qa_chain_instrucEmbed(user_input)
    print('Finished LLM setup.')  
    return jsonify(result=llm_response['result'])

@app.route('/get-js-code', methods=['POST'])
def get_js_code():
  user_input = request.json['result']
  js_code = user_input # ex. "wavesurfer.setVolume(0.5)"  
  return jsonify(result=js_code)

if __name__ == '__main__':
    app.run(debug=True)
