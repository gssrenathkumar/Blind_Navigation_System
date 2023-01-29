
from time import sleep
from subprocess import call
from multiprocessing import Process

def calling_open_cv():
    call(["python","object_distance_detector.py"])

def calling_navigation_direction():
    call(["python","navigation_direction.py"])

def calling_voice_commands():
    call(["python","voice_commands.py"])

def calling_gui():
    call(["python","tkinter_application.py"])

if __name__ == "__main__":
    my_process1 = Process(target=calling_gui)
    my_process2 = Process(target=calling_navigation_direction)
    my_process3 = Process(target=calling_open_cv)
    my_process1.start()
    my_process3.start()
    my_process2.start()
    my_process1.join()
    my_process2.join()
    my_process3.join()


