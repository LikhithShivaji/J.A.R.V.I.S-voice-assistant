import random
import json
import torch
from brain import NeuralNet
from NeuralNetwork import bag_of_words,tokenize

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r') as json_data:
    intents=json.load(json_data)

FILE="TrainData.pth"
data=torch.load(FILE)

input_size=data["input_size"]
hidden_size=data["hidden_size"]
output_size=data["output_size"]
all_words=data["all_words"]
tags=data["tags"]
model_state=data["model_state"]

model=NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

#--------------------------------------------------------------------------------------

Name="Jarvis"
from listen import Listen
from speak import Say
from task import NonInputExecution
from task import InputExecution
from task import wishMe
import pyfirmata

def Main():
    sentence=Listen()
    result=str(sentence)

    if sentence=="exit":
        exit()

    sentence=tokenize(sentence)
    X=bag_of_words(sentence,all_words)
    X=X.reshape(1,X.shape[0])
    X=torch.from_numpy(X).to(device)

    output=model(X)

    _ , predicted=torch.max(output,dim=1)
    
    tag=tags[predicted.item()]

    probs=torch.softmax(output,dim=1)
    prob=probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag==intent["tag"]:
                reply=random.choice(intent["responses"])

                if "time" in reply:
                    NonInputExecution(reply)

                elif "date" in reply:
                    NonInputExecution(reply)

                elif "day" in reply:
                    NonInputExecution(reply)

                elif "wikipedia" in reply:
                    InputExecution(reply,result)

                elif "google" in reply:
                    InputExecution(reply,result)

                elif "news" in reply:
                    InputExecution(reply,result)

                elif "calculate" in reply:
                    InputExecution(reply,result)

                elif "song" in reply:
                    InputExecution(reply,result)

                elif "weather" in reply:
                    InputExecution(reply,result)

                elif "temperature" in reply:
                    InputExecution(reply,result)

                elif "light" in reply:
                    InputExecution(reply,result)

                elif "fan" in reply:
                    InputExecution(reply,result)

                elif "shutdown" in reply:
                    InputExecution(reply,result)

                elif "remember that" in reply:
                    InputExecution(reply,result)

                elif "what do you remember" in reply:
                    InputExecution(reply,result)

                elif "pause" in reply:
                    InputExecution(reply,result)

                elif "play" in reply:
                    InputExecution(reply,result)

                elif "mute" in reply:
                    InputExecution(reply,result)

                elif "screenshot" in reply:
                    InputExecution(reply,result)

                elif "open" in reply:
                    InputExecution(reply,result)

                elif "translate" in reply:
                    InputExecution(reply,result)

                elif "volume up" in reply:
                    InputExecution(reply,result)

                elif "volume down" in reply:
                    InputExecution(reply,result)

                else:
                    Say(reply)
                
while True:
    Main()