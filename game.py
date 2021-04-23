%pylab inline
import time
from __future__ import print_function
from pypot.creatures import PoppyErgoJr
from pypot.primitive.move import MoveRecorder, MovePlayer, Move

poppy = PoppyErgoJr()
motors=[poppy.m1, poppy.m2, poppy.m3, poppy.m4, poppy.m5, poppy.m6]
recorder = MoveRecorder(poppy, 50, motors)

options = []
thingsIknow = open("/home/poppy/notebooks/game/gameMemory.txt", "r") 
for tik in thingsIknow: 
    tik = tik.strip() 
    options.append(tik) 
amount = len(options) - 1 
thingsIknow.close() 

def play(positions): 
  for m in poppy.motors: 
      m.compliant=True 
  degree=10 
  for nr in range(80): 
    current=[m.present_position for m in poppy.motors] 
    count=0 
    for i in range(len(current)): 
        m=poppy.motors[i] 
        if abs(current[i]-positions[i])<degree: 
            m.led="green"
            count=count+1
        elif current[i]<positions[i]: m.led="yellow
        else: m.led="blue"
    time.sleep(0.5
    if count==6: break

  if count==6:
    for m in poppy.motors: m.led="white"
    time.sleep(5)
    for m in poppy.motors: m.led="green"
    print("Well done")
    return "Victory"
  else:
    for m in poppy.motors: m.led="red"
    return "Loss"

def addToMemory(name):
    thingsIknow = open("/home/poppy/notebooks/game/gameMemory.txt", "a"
    thingsIknow.write(str(name)+"\n") 
    thingsIknow.close() 
def show(choice):
    presentation = "/home/poppy/notebooks/game/" + choice + ".move" 
    for m in poppy.motors: 
        m.led='blue'
    with open(presentation, 'r') as fromMemory: 
        imported = Move.load(fromMemory) 
    player = MovePlayer(poppy, imported) 
    player.start() 
    time.sleep(10)
    positions=[m.present_position for m in poppy.motors
    poppy.rest_posture.start()
    time.sleep(5) 
    for m in poppy.motors: 
        m.compliant=False 
    return positions
def learn():
    while True: 
        poppy.rest_posture.start() 
        time.sleep(5) 
        for m in motors:
            m.compliant=True 
        for m in poppy.motors:
            m.led='green' 
        recorder.start() 
        time.sleep(5) 
        recorder.stop() 
        player = MovePlayer(poppy, recorder.move) 
        player.start() 
        time.sleep(5) 
        acceptable = raw_input("should I save this performance if not then we'll try again(y/n)") 
        if acceptable == "y" or acceptable == "Y": 
            return recorder 
        else: 
            for m in motors: 
                m.compliant=True 

activity = raw_input("are you ready?") 

if activity == "admin": 
    recorder = learn() 
    print("what shall we name this program?") 
    while True: 
        teaching = raw_input() 
        if teaching in options: 
            print("that name is already taken")
        else: 
            break 
    addToMemory(teaching) 
    teaching = "/home/poppy/notebooks/game/" + teaching + ".move" 
    with open(teaching, "w") as memory:
        recorder.move.save(memory) 
else: 
    gameType = random.randint(0, amount) 
    gameType = options[gameType] 
    while True: 
        positions = show(gameType) 
        state = play(positions) 
        if state == "Victory": 
            poppy.dance.start() 
            time.sleep(60) 
            poppy.dance.stop() 
            time.sleep(5) 
            break 
        else: 
            print("better luck next time")
