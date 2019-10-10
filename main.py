import pygame as pg
import pygame.midi as midi
import pyautogui
import threading
import subprocess

class midiController:
    def __init__(self):
        self.pads = []
        list.append(self.pads, key(48))
        list.append(self.pads, key(49))
        list.append(self.pads, key(50))
        list.append(self.pads, key(51))

        self.counter = 0

class key:
    def __init__(self, noteNumber):
        self.status = 0
        self.noteNumber = noteNumber
        self.noteVelocity = 0



mpk2mini = midiController()  # global
def pollMidi():
    deviceCount = pg.midi.get_count()
    print(deviceCount)
    for i in range(0, deviceCount):
        print(pg.midi.get_device_info(i))

    midi_in = pg.midi.Input(1)  # id = 1
    

    while True:
        if midi_in.poll():
            midiData = midi_in.read(1)

            if midiData[0][0][0] == 144:  # note on
                for i in range(0, len(mpk2mini.pads)):
                    if midiData[0][0][1] == mpk2mini.pads[i].noteNumber:
                        mpk2mini.pads[i].status = 1
            elif midiData[0][0][0] == 128:  # note off
                for i in range(0, len(mpk2mini.pads)):
                    if midiData[0][0][1] == mpk2mini.pads[i].noteNumber:
                        mpk2mini.pads[i].status = 0


def startAudacity():
    subprocess.Popen([r"C:\Program Files (x86)\Audacity\audacity.exe"])


def initAll():
    startAudacity()
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = True

    pg.init()
    pg.midi.init()

    if pg.midi.get_init(): 
        print("success")
    else: print( "NO SUCCESS")
    


def controlFunction():
    btnState = 0  #  static, button state of last loop
    try:
        while True:
                #while(midi_in.poll()):
                #    midi_in.read(1000)  # flush buffer

                text = ""
                for i in range(0, len(mpk2mini.pads)):
                    text = text + str(mpk2mini.pads[i].status)
                print(text)

                if mpk2mini.pads[2].status == 0:
                    btnState = 0
                elif mpk2mini.pads[2].status == 1 and btnState == 0:
                    btnState = 1
                    if mpk2mini.counter == 0:
                        pyautogui.press('r')  # record
                        pg.time.wait(500)
                        mpk2mini.counter = mpk2mini.counter + 1
                    elif mpk2mini.counter == 1:
                        pyautogui.press('space')  # stop recording
                        pg.time.wait(300)
                        pyautogui.hotkey('shift', 'space') # replay
                        pg.time.wait(200)
                        mpk2mini.counter = mpk2mini.counter + 1
                    elif mpk2mini.counter == 2:
                        pyautogui.press('space')  # stop recording
                        pg.time.wait(300)
                        pyautogui.press('y') # delete
                        mpk2mini.counter = 0
                        pg.time.wait(200)
                if mpk2mini.pads[0].status == 1:  # stop
                    pyautogui.press('space')  # stop recording
                    pg.time.wait(500)

                #midi_in.read(1000)
                #pg.time.wait(00)

                '''
                elif mpk2mini.pads[2].status == 1:  # replay
                    pyautogui.hotkey('shift', 'space')

                elif mpk2mini.pads[1].status == 1:  # stop
                    pyautogui.press('space')  # stop recording

                elif mpk2mini.pads[0].status == 1:  # delete
                    pyautogui.press('y') 
                '''

    except KeyboardInterrupt:
        print("\nkeyboard interrupt")

        


if __name__ == "__main__":
    initAll()
    pollThread = threading.Thread(target=pollMidi)
    pollThread.start()
    controlThread = threading.Thread(target=controlFunction)
    controlThread.start()
    