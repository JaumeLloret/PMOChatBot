from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, OpenAIError

load_dotenv()

app = Flask(__name__)

client = OpenAI(
  api_key = os.environ.get("SECRET_KEY"),
)

@app.route('/', methods = ['GET'])
def index():
  return render_template('index.html')

@app.route('/prompt', methods = ['POST'])
def prompt():
  try:
    data = request.get_json()
    input_text = data['text']

    if not input_text:
      raise ValueError("El campo 'text' no puede estar vacío.")

    chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": input_text,
          }
      ],
      model="gpt-3.5-turbo",
    )

    generated_text = chat_completion.choices[0].message.content
    
    return jsonify({'generated_text': generated_text}), 200
  except RateLimitError:
    return jsonify({'error': 'Se ha alcanzado el límite de solicitudes. Por favor, inténtelo de nuevo más tarde.'}), 429
  except OpenAIError as e:
    error_message = str(e)
    return jsonify({'error': error_message}), 500
  except KeyError:
    return jsonify({'error': 'El campo "text" no está presente en los datos JSON.'}), 400
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Ocurrió un error inesperado: {}'.format(str(e))}), 500

if __name__ == '__main__':
  app.run()