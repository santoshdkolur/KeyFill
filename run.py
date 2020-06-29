import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import pyperclip
from pynput import keyboard
import pyautogui
import time

from tensorflow.keras.models import load_model
model=load_model('Text_pred_trained/model_bidirectional_v3_final_max_seq_102.h5')

with open('Text_pred_trained/tokenizer_bidirectional_v3_final_maxseq_102.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
max_sequences=102

def suggest(predicted,num=3):                 #Get n number of suggestions
    suggested=[]
    for _ in range(num):
        suggested.append(np.argmax(predicted))
        predicted[0][np.argmax(predicted)]=0
    return suggested


def complete(seed):                         #Get n suggested words from the seed text.
    if(len(seed.split(' '))>20):
        seed=' '.join(seed.split(' ')[-20])
    token_list=tokenizer.texts_to_sequences([seed])[0]
    token_list=np.array(pad_sequences([token_list],maxlen=max_sequences-1,padding='pre'))
    predicted=model.predict(token_list,verbose=0)
    rev={v:k for k,v in dict(tokenizer.word_index).items()}
    suggested_words=[rev[ele] for ele in suggest(predicted)]
    return suggested_words

#complete('Today was busy but')

#Try to get the next n words to complete a sentence.
def predict_sentence(seed_text="Today was a",next_words=10):  
    next_words=20
    for _ in range(next_words):
        token_list=tokenizer.texts_to_sequences([seed_text])[0]
        token_list=np.array(pad_sequences([token_list],maxlen=max_sequences-1,padding='pre'))
        predicted=model.predict_classes(token_list,verbose=0)
        output_word=""
        for word,index in tokenizer.word_index.items():
            if index==predicted:
                output_word=word
                break
        seed_text+=' '+output_word
    return seed_text



#predict_sentence("Why is it so stupid to")


def auto():
#Purpose: pedict the suggested words and complete the sentence.
#Author : Santosh Kolur

    #Hotkey Shift + '+'
    COMBINATIONS = {keyboard.Key.shift,keyboard.KeyCode(char='+')} 
    current = set()
    text=''
    #Function predicts and diplays the suggested words
    def execute():
        global text
        next_word=''
        pyautogui.press('right',presses=1)
        pyautogui.press('backspace',presses=1)
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        pyautogui.press('right',presses=2)
        text=pyperclip.paste()
        text=text.replace(',', ' , ')
        text=text.replace('.',' . ')
        text=' '.join(text.split(' ')[-10:])
        #print("Text:  "+text)
        if(text[-1]!=' '):
            next_word=' '
        next_word+=str(pyautogui.confirm(text='Choose one of the suggested',title='Suggested Words',buttons=complete(text)))+' '
        if('None' not in next_word):
            if('.' in text[-3:]):
                if(next_word[0]!=' '):
                    next_word=next_word[0].upper()+next_word[1:]
                else:
                    next_word=next_word[0:2].upper()+next_word[2:]
            keyboard.Controller().type(next_word)
            time.sleep(0.2)
        pyperclip.copy('')
        text=''
    #This fucnction runs when the script detects the hotkey
    def on_press(key):
        if key in COMBINATIONS:
            current.add(key)
            if all(k in current for k  in COMBINATIONS):
                execute()

    def on_release(key,text=text):
        if key in COMBINATIONS:
            current.remove(key)
        if key == keyboard.Key.esc:
        # Stop listener
            return False
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


print("\n\nEnter 1 to start the service: ")
choice=int(input())
if(choice==1):
    print("\nPress Shift and + keys to automatically fill the next word.\nPress esc key to stop the script\n")
    auto()
else:
    print('Wrong choice. Exiting:')
    exit()

