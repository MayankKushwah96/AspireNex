import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import scrolledtext
import random
import pyjokes  
import wikipedia

# Set NLTK data directory to within the virtual environment
venv_dir = os.getcwd()
nltk_data_dir = os.path.join(venv_dir, 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

nltk.data.path.append(nltk_data_dir)

# Download NLTK data if not already downloaded
def download_nltk_data_if_needed():
    nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
    nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)
    nltk.download('wordnet', download_dir=nltk_data_dir, quiet=True)

# Check if WordNet is available, and download if needed
if not nltk.data.find('corpora/wordnet.zip'):
    download_nltk_data_if_needed()

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    
    # Stop words removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return tokens

def get_response(user_input):
    user_input = user_input.lower()
    
    exit_phrases = [
        "exit", "quit", "bye", "goodbye", "see you", "take care", "later", "peace", 
        "adios", "farewell", "ciao", "catch you later", "see you later", "see ya", 
        "i'm out", "i'm leaving", "gotta go", "talk to you later", "bye bye", 
        "good night", "so long", "take it easy", "i'm off", "i'm done", 
        "that's all", "that's it", "hasta la vista", "sayonara", "cheerio", 
        "au revoir", "catch you soon", "i'm heading out", "i have to go", 
        "have a good day", "i'm signing off", "toodle-oo", "godspeed", 
        "see you next time", "all the best", "i'm checking out", "stay safe", 
        "i'll catch you later", "i'm bouncing", "i'm off now", "i need to go", 
        "gotta run", "i'm out of here", "until next time", "i'm departing"
    ]
    exit_responses = [
        "Goodbye! Have a great day!","See you later!","Take care!","Farewell! Stay safe!","Catch you later!","It was nice chatting with you. Goodbye!",
        "Adios! Have a good one!","Bye! Come back soon!","Take it easy!","Catch you next time!","Goodbye! Hope to see you again!",
        "Stay safe and take care!","So long! Have a good day!","Good night! Rest well!","Bye bye! Take care!","I'm signing off now. Goodbye!",
        "Hasta la vista!","Sayonara! Until next time!","Cheerio! Have a great day!","Au revoir! See you soon!","Godspeed! Stay well!",
        "Until next time, take care!","I'm checking out. Bye!","Catch you soon! Stay safe!","Goodbye! Best wishes!",
        "I'm off now. Take care!","Gotta run! Bye!","I'm out of here. Take care!"
    ]

    
    if user_input in exit_phrases:
        return random.choice(exit_responses)
    
    if "information about" in user_input or "tell me about" in user_input or "what is" in user_input:
        return get_wikipedia_summary(user_input)
    
    book_recommendations = [
        "To Kill a Mockingbird by Harper Lee",
        "1984 by George Orwell",
        "Pride and Prejudice by Jane Austen",
        "The Great Gatsby by F. Scott Fitzgerald",
        "Moby Dick by Herman Melville"
    ]

    movie_recommendations = [
        "Inception",
        "The Shawshank Redemption",
        "The Dark Knight",
        "Forrest Gump",
        "The Matrix",
        "Pulp Fiction",
        "Fight Club",
        "The Godfather",
        "The Lord of the Rings: The Fellowship of the Ring",
        "Interstellar"
    ]

    compliments = [
        "You have a fantastic smile!",
        "You're an amazing person!",
        "You're doing a great job!",
        "You have a wonderful sense of humor!",
        "You're very talented!",
        "You're incredibly kind!",
        "You have a great personality!",
        "You are very creative!",
        "You have a positive energy!",
        "You're a great friend!"
    ]

    daily_activities = [
        "How about trying something new, like a hobby you've always wanted to pursue or a book you've been meaning to read?",
        "Maybe you can go for a walk or a run and enjoy the fresh air.",
        "You could try cooking a new recipe.",
        "How about spending some time with family or friends?",
        "You could watch a movie or a series you've been wanting to see.",
        "Why not try some relaxation exercises or meditation?",
        "You could work on a personal project or hobby.",
        "How about reading a book or listening to a podcast?",
        "You could do some gardening or take care of your plants.",
        "Maybe you can write in a journal or start a blog.",
        "You could explore a nearby park or museum.",
        "Why not try a new sport or physical activity?",
        "You could volunteer for a local community service.",
        "How about learning a new language or skill?",
        "You could organize or redecorate your living space.",
        "Why not try painting or drawing?",
        "You could listen to some new music or create a playlist.",
        "How about doing some yoga or stretching exercises?",
        "You could visit a friend or family member you haven't seen in a while.",
        "How about taking a day trip to a nearby town or city?"
    ]
    patterns_responses = [
        (["good morning"],
         ["Good morning! How can I assist you today?"]),

        (["good afternoon"],
         ["Good afternoon! How can I assist you today?"]),

        (["good evening"],
         ["Good evening! How can I help you?"]),

        (["hi", "hello", "hey", "g'day", "hi there", "what's up", "yo", "how's it going", "hey there"],
         ["Hello! How can I assist you today?",
          "Hey there! What can I do for you?",
          "Hi! How can I help you?"]),

        (["how are you", "how's it going", "how are you doing", "how's everything",
          "how's life treating you", "what's happening"],
         ["I'm just a bunch of code, but I'm here to help you!",
          "I'm doing well! How about you?",
          "Feeling good! How can I assist you today?"]),

        (["thanks", "thank you", "thanks a lot", "thank you so much"],
         ["You're welcome!",
          "No problem!",
          "Anytime!"]),

        (["help", "help me", "can you help me"],
         ["Of course! What do you need assistance with?",
          "Sure thing! What can I assist you with?"]),

        (["your name", "who are you", "what are you called", "can i know your name",
          "what should i call you", "tell me your name"],
         ["I'm a chatbot here to assist you with your queries.",
          "I'm your friendly chatbot created to help you out.",
          "I'm an AI assistant designed to answer your questions."]),

        (["time", "what's the time", "tell me the time", "do you have the time",
          "could you tell me the time"],
         ["Sure! " + get_current_time()]),

         (["recommend me a book", "suggest a book", "PP"],
         [f"Sure! How about '{random.choice(book_recommendations)}'?"]),

        (["recommend me a movie", "suggest a movie", "movie recommendation"],
         [f"How about watching '{random.choice(movie_recommendations)}'?"]),

        (["give me a compliment"], [random.choice(compliments)]),

        (["what should i do today"], [random.choice(daily_activities)]),

        (["give me some advice", "advice", "i need some advice"],
         ["Always believe in yourself and keep pushing forward, no matter the obstacles."]),

        (["what is your favorite food", "favorite food", "your favorite food"],
         ["As a bot, I don't eat, but I've heard pizza is a favorite for many people!"]),

        (["what are your hobbies", "hobbies", "do you have hobbies"],
         ["I don't have hobbies, but I love helping people with their questions!"]),

        (["joke", "tell me a joke", "say something funny", "make me laugh"],
         [pyjokes.get_joke()])
    ]

    for patterns, responses in patterns_responses:
        for pattern in patterns:
            if pattern == user_input:
                return random.choice(responses)

    return "I'm not sure how to respond to that. Can you try asking something else?"


def get_wikipedia_summary(query):
    query = query.replace('information about', '').replace('tell me about', '').replace('what is', '').strip()
    
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"Here's what I found on Wikipedia about {query.capitalize()}: {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"The query '{query}' may refer to multiple things: {e.options}"
    except wikipedia.exceptions.PageError:
        return f"Sorry, I couldn't find any information on {query.capitalize()} on Wikipedia."
    except Exception as e:
        return f"An error occurred: {e}"

    
def get_current_time():
    current_time_utc = datetime.utcnow()
    ist_offset = timedelta(hours=5, minutes=30)  
    current_time_ist = current_time_utc + ist_offset
    
    current_hour = current_time_ist.hour
    period = "AM" if current_hour < 12 else "PM"
    current_hour = current_hour if current_hour <= 12 else current_hour - 12
    current_time_formatted = current_time_ist.strftime(f"%I:%M:%S {period} on %d-%m-%Y")
    
    return f"The current time is {current_time_formatted}"

def get_user_input():
    user_input = input_field.get("1.0", "end-1c").strip()
    
    if user_input:
        response = get_response(user_input)
        output_field.config(state=tk.NORMAL)  # Enable editing of output_field
        
        # Add user message in a colored box on the left (white background, black text)
        output_field.tag_configure("left", justify='left', foreground='black', background='white')
        output_field.insert(tk.END, "You:\n", "left")
        output_field.insert(tk.END, user_input + "\n\n", "left")
        
        # Add bot message in a colored box on the left (white background, black text)
        output_field.tag_configure("left", justify='left', foreground='black', background='white')
        output_field.insert(tk.END, "Bot:\n", "left")
        output_field.insert(tk.END, response + "\n\n", "left")
        
        output_field.config(state=tk.DISABLED)  # Disable editing of output_field
        input_field.delete("1.0", tk.END)  # Clear input field after sending message
        
   
        output_field.yview(tk.END)

root = tk.Tk()
root.title("ChatBot")

output_label = tk.Label(root, text="Conversation:")
output_label.pack()

output_field = scrolledtext.ScrolledText(root, width=60, height=20)
output_field.pack()
output_field.config(state=tk.DISABLED)  

message_label = tk.Label(root, text="Enter your message:")
message_label.pack()

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_field = scrolledtext.ScrolledText(input_frame, width=50, height=3)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=get_user_input)
send_button.pack(side=tk.RIGHT)

output_label.pack(anchor=tk.CENTER)
output_field.pack(anchor=tk.CENTER)
message_label.pack(anchor=tk.CENTER)
input_frame.pack(anchor=tk.CENTER)

root.mainloop()

def chatbot():
    print("Hello! I'm your friendly chatbot. How can I help you today?")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        response = get_response(user_input)

        exit_responses = [
        "Goodbye! Have a great day!","See you later!","Take care!","Farewell! Stay safe!","Catch you later!","It was nice chatting with you. Goodbye!",
        "Adios! Have a good one!","Bye! Come back soon!","Take it easy!","Catch you next time!","Goodbye! Hope to see you again!",
        "Stay safe and take care!","So long! Have a good day!","Good night! Rest well!","Bye bye! Take care!","I'm signing off now. Goodbye!",
        "Hasta la vista!","Sayonara! Until next time!","Cheerio! Have a great day!","Au revoir! See you soon!","Godspeed! Stay well!",
        "Until next time, take care!","I'm checking out. Bye!","Catch you soon! Stay safe!","Goodbye! Best wishes!",
        "I'm off now. Take care!","Gotta run! Bye!","I'm out of here. Take care!"
    ]
        if response in exit_responses:
            print(f"Chatbot: {response}")
            break
        else:
            print(f"Chatbot: {response}")

chatbot()