import json
import transitions

trans = []

with open("fsm.json") as f:
    data = json.load(f)
    for i in data["state"]:
        state = {"trigger":0,"source":0,"dest":0}
        for j in i:
            if j == "trigger":
                state["trigger"] = i[j]
            if j == "source":
                state["source"] = i[j]
            if j == "dest":
                state["dest"] = i[j]
        trans.append(state)
            

from transitions.extensions import GraphMachine
from transitions import Machine
from functools import partial
import cv2

class Model(object):
    
    def __init__(self, states,initial):
        self.machine = Machine(model=self, states=states, initial=initial)
        
def create_fsm():
    model = Model(data["states"],data["init"])

    for i in trans:
        model.machine.add_transition(i["trigger"],i["source"],i["dest"])
    return model
def create_fsm_graph(model):
    machine = GraphMachine( model=model,
                            states=data["states"],
                            transitions=trans,
                            initial=data["init"],
                            auto_transitions=False,
                            show_conditions=True,)
model = create_fsm()
create_fsm_graph(model)
model.get_graph().draw('my_fsm.png', prog='dot')

'''model = create_fsm()
create_fsm_graph(model)
model.get_graph().draw('my_fsm.png', prog='dot')
img = cv2.imread('my_fsm.png')
cv2.imshow("img",img)
cv2.waitKey(0)'''
    