from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO, emit
from bot import ChatBot, VectorDB
from scripts.ipfs import Decentralized_db
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)
vectordb = VectorDB()
decentdb = Decentralized_db()
# Global variable for single-user state
choose_topic = True
choose_book = True
chatbot = None
user_sessions = {}
@app.route('/')
def index():
    global choose_topic
    global choose_book
    choose_topic = True
    choose_book = True
    return render_template('chat.html')

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Check if the file is part of the request
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        
        # Check if no file was selected
        if file.filename == '':
            return "No file selected", 400

        # Validate file type
        if file and file.filename.endswith('.txt'):
            # Save to decentdb
            cid = decentdb.upload_file_to_pinata(file, file.filename)
            # Add title to vectordb
            vectordb.add_book(file.filename.strip(".txt"))
            # Respond with the CID
            return {'cid': cid}, 200
        else:
            return "Invalid file type, only .txt files are allowed", 400

    # Render the HTML form if the request method is GET
    return render_template('add-book.html')



@socketio.on('message')
def handle_message(msg):
    global choose_topic  # Declare the global variable
    global choose_book
    global chatbot
    session_id = request.sid

    # Store user message or initialize if not present
    if session_id not in user_sessions:
        user_sessions[session_id] = {"messages": []}

    user_sessions[session_id]["messages"].append({"role": "user", "content": msg})

    # Check the choose_topic flag
    if choose_topic:
        results = vectordb.find_book(msg)
        print(results)
        books = results['documents'][0]
        books = str([book + ".txt" for book in books])
        response = "Here are the books most closely related to your topic:" + books
        response += ". Enter your cid on the next line"
        choose_topic = False  # Set it to False after the first execution
    elif choose_book:
        cid = msg.strip()
        file_data = decentdb.retrieve_file_from_cid(cid)
        text = file_data.decode('utf-8')
        print(text)
        chatbot = ChatBot(text)
        response = chatbot.chat_with_agent("Summarize the text")
        response = "Here is a summary of the text. Please also ask any follow up questions:\n" + response
        choose_book = False
    else:
        response = chatbot.chat_with_agent(msg)

    # Store bot response
    emit('message', response, room=session_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)
