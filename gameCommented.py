%pylab inline
import time #lubab kasutada time lisamoodulit millega saab programmis määrata pause
from __future__ import print_function #kuna tegemist on python2 programmiga, siis see lubab võtta python3-st print käsu
from pypot.creatures import PoppyErgoJr #võimaldab robotile spetsiifilise käske anda
from pypot.primitive.move import MoveRecorder, MovePlayer, Move #võimaldab liigutusi salvestada

poppy = PoppyErgoJr() #defineerime roboti
motors=[poppy.m1, poppy.m2, poppy.m3, poppy.m4, poppy.m5, poppy.m6] #defineerime kõik kuus mootorit
recorder = MoveRecorder(poppy, 50, motors) #defineerime liigutuste salvesti

options = [] #algne tühi nimekirja kuhu laetakse sisse teada olevad liigutused
thingsIknow = open("/home/poppy/notebooks/game/gameMemory.txt", "r") #lae sisse fail kus on teada olevate liigutuste nimed
for tik in thingsIknow: #tsükkel mis käib läbi sisse laetud faili gameMemory.txt
    tik = tik.strip() #eemaldab sisse loetud nimest mitte vajalikud sümbolid
    options.append(tik) #lisab liigutuse nime nimekirja
amount = len(options) - 1 #loenda valikute arv kokku ning lahuta 1 kuna programm hakkab lugema nullist
thingsIknow.close() #sulgeb sisse laetud faili

def play(positions): #mängimis funktsioon
  for m in poppy.motors: #käi kõik mootorid läbi
      m.compliant=True #vabasta mootorid nii et inimene saaks neid liigutada
  degree=10 #määra eksimus kraadid
  for nr in range(80): #korruta tsüklit 80 korda
    current=[m.present_position for m in poppy.motors] #kontrolli kõikide mootorite asukohti
    count=0 #loendur väärtusega 0
    for i in range(len(current)): #käi läbi positsiooni andmed
        m=poppy.motors[i] #määra muutuja m sisse mootor i, i muutub ühe võrra suuremaks iga kord kui tsükkel läbi käib
        if abs(current[i]-positions[i])<degree:  #kontrolli kas mootor on õige nurga all, kui jah siis liigu edasi
            m.led="green" #muuda mootori värv roheliseks
            count=count+1 #lisa loendurile 1 juurde
        elif current[i]<positions[i]: m.led="yellow" #kui mootor on liialt vasakule kaldus, muuda led kollaseks
        else: m.led="blue" #kui mootor on liialt paremale kaldus, muuda siniseks
    time.sleep(0.5) #oota o.5 sekundit
    if count==6: break #kui kõik mootorid on rohelised, lõpeta tsükkel

  if count==6: #kui kõik mootorid said roheliseks
    for m in poppy.motors: m.led="white" #muuda mootorite led lambid valgeks
    time.sleep(5) #oota viis sekundit
    for m in poppy.motors: m.led="green" #muuda mootorite led lambid roheliseks
    print("Well done") #anna kasutajale teada et hästi tehtud
    return "Victory" #tagasta põhiprogrammi info et mängija võitis
  else: #kui kõik mootorid ei saanud paika
    for m in poppy.motors: m.led="red"  #muuda roboti led lambid punaseks
    return "Loss" #tagasta põhiprogrammi info et mängija kaotas

def addToMemory(name): #funktsioon liigutuse mällu lisamiseks
    thingsIknow = open("/home/poppy/notebooks/game/gameMemory.txt", "a") #ava fail kus on liigutuste nimed
    thingsIknow.write(str(name)+"\n") #kirjuta faili uue liigutuse nimi
    thingsIknow.close() #sulge fail
def show(choice): #ette näitamise funktsioon
    presentation = "/home/poppy/notebooks/game/" + choice + ".move" #otsi üles liigutuse andmed
    for m in poppy.motors: #käi läbi kõik mootorid
        m.led='blue' #muuda led lambid siniseks
    with open(presentation, 'r') as fromMemory: #ava fail kus on liikumis andmed
        imported = Move.load(fromMemory) #loe andmed sisse nii et programm nendest aru saaks
    player = MovePlayer(poppy, imported) #lae need andmed muutujasse
    player.start() #alusta liigutuse presenteerimist
    time.sleep(10) #oota 10 sekundit
    positions=[m.present_position for m in poppy.motors] #jäta mootorite lõpp positsioonid meelde
    poppy.rest_posture.start() #vii robot tagasi puhke positsiooni
    time.sleep(5) #oota 5 sekundit
    for m in poppy.motors: #käi läbi kõik mootorid
        m.compliant=False #lukusta mootorid
    return positions #tagasta lõpp positsiooni informatsioon
def learn(): #õppimis funktsioon
    while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
        poppy.rest_posture.start()  #tagasta lõpp positsiooni informatsioon
        time.sleep(5) #oota 5 sekundit
        for m in motors: #käi läbi kõik mootorid
            m.compliant=True #vabasta mootorid et inimesne saaks neid liigutada
        for m in poppy.motors:#käi läbi kõik mootorid
            m.led='green' #muuda led lambid roheliseks
        recorder.start() #alusta liigutuse salvestamist
        time.sleep(5) #oota 5 sekundit
        recorder.stop() #lõpeta liigutuse salvestamine
        player = MovePlayer(poppy, recorder.move) #lisa salvestatud andmed muutujasse
        player.start() #presenteeri liigutus
        time.sleep(5) #oota 5 sekundit
        acceptable = raw_input("should I save this performance if not then we'll try again(y/n)") #küsi kas kasutajale meeldis liigutus, anna teada et vastata kas y või n
        if acceptable == "y" or acceptable == "Y": #kui vastus on kas y või Y, siis liigu edasi
            return recorder #saada salvestatud info tagasi põhi programmi
        else: #kui vastati midagi mis ei ole y või Y
            for m in motors: #käi läbi kõik mootorid
                m.compliant=True #vabasta mootorid et inimesne saaks neid liigutada

activity = raw_input("are you ready?") #küsi kasutajalt kas ta on mänguks valmis

if activity == "admin": #kui kasutaja kirjutab vastuseks sõna admin
    recorder = learn() #alusta õppimis funktsiooni
    print("what shall we name this program?") #anna teada et kasutja võib programmi nimetada
    while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
        teaching = raw_input() #siin saab sisestada kasutaja nime
        if teaching in options: #kui see nimi juba eksisteerib
            print("that name is already taken") #see nimi on juba võetud
        else: #kui seda nime pole olemas
            break #lõpeta tsükkel
    addToMemory(teaching) #liigu mällu lisamis funktsiooni
    teaching = "/home/poppy/notebooks/game/" + teaching + ".move" #lisa muutujasse vastave liigutuse jaoks asukoht
    with open(teaching, "w") as memory: #ava just lisatud asukoht
        recorder.move.save(memory) #kirjuta sinna uus fail koos andmetega
else: #kui kasutaja vastas midagi peale sõna admin
    gameType = random.randint(0, amount) #vali suvaline number vahemikus 0 ning eelnevalt saadud amount vahel
    gameType = options[gameType] #suvaliselt valitud numbri järgi saadakse liigutus mängu jaoks
    while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
        positions = show(gameType) #sisesta muutujasee liigutuse nimi
        state = play(positions) #alusta mängu koos liigutuse nimega
        if state == "Victory": #kui mängija võitis
            poppy.dance.start() #robot hakkab tantsima
            time.sleep(60) #oota 60 sekundit
            poppy.dance.stop() #lõpeta tantsimine
            time.sleep(5) #oota 5 sekundit
            break #lõpeta tsükkeö
        else: #kui kasutaja kaotas
            print("better luck next time") #soovi paremt õnne tulevastes mängudes
            #siia võib sisestada sõna break. Kui see sinna lisada, siis program lõpetab töö pärast kaotust.
