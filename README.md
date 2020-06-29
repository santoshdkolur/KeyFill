# KeyFill

KeyFill is a word suggestion script built using keras, pyautogui and pynput.

##### Requirements:
  - Tensorflow 2.0
  - keras
  - pickle
  - pnput
  - pyautogui
  - pyperclip

## Current Build v0.01

  - Suggested words are'nt perfect. The model needs to be perfected a bit.
  - This is just the first working prototype.
  - The model was trained on a few english sentences.
 
##### Run: 
Download or clone the repo. 
Make sure you have all the dependencies installed. Check the requirements for the list of required libraries.
Unzip the files, open terminal inside the folder and run the following code.
``` 
$python run.py
```
Open any text editor and start typing. Whenevr you want a suggestion for the next word, press L_SHIFT + '+' keys. You'll get a pop up with three suggested words.

##### Contents:
1. Text Prediction.ipynb  : This file contains the code that was used to train the model. 
2. Text_pred_trained: This folder contains the trained model and it's respective tokenizer.
3. run. py :  This file contains to code to load the pretrained model and display the suggested words.
4. final_data.txt : This is the dataset used to train the model. 
5. final_data_small.txt : I advise you to use this if your ran capacity is 8GB or less. 

#### Working:
The model works best when there are already atleast two sentences before prediction.

![Alt text](assets/Work.png)

