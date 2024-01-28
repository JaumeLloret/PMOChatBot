from flask import Flask, request, render_template  #pip install flask
from decouple import config
import openai #pip install openai

app = Flask(__name__)

openai.api_key = config('SECRET_KEY', default='secret_key_openAI')

@app.route('/', methods = ['GET'])
def index():
  return render_template(index.html)

@app.route('/prompt', methods = ['POST'])
def prompt():
  data = request.get_json()
  input_text = data['text']
  
  response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [{"role": "user", "content": input_text}]
  )
  
  generated_text = response.choices[0].message.content
  
  return generated_text

if __name__ == '__main__':
  app.run()