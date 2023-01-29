import tkinter
from subprocess import call

from navigation_direction import current_location_address

YELLOW = "#f7f5dd"
GREEN = "#32CD32"
FONT_NAME = "Courier"
CYAN = "cyan"
FONT_NAME_2 = "Helvetica"
PALE_GREEN = "#98FB98"
RED = "#FF0000"
POWDER_BLUE = "#B0E0E6"
E_YELLOW = "#ffde34"
black="#000000"
count = 5
t = 0
emoji_text = "😎"
global canvas


def calling_voice_commands():
    call(["python", "voice_commands.py"])


##############################TKINTER_GUI INTERFACE##########################################


window = tkinter.Tk()
window.config(padx=100, pady=50, bg=YELLOW)
window.title("Blind Navigation Application")
canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = tkinter.PhotoImage(file="data.png")
canvas.create_image(100, 112, image=tomato_image)
text1 = canvas.create_text(100, 130, text="", fill="BLACK", font=(FONT_NAME, 15, "bold"))
canvas.grid(row=3, column=3)

label3 = tkinter.Label(text="Navigation System", bg=YELLOW, fg=black, font=(FONT_NAME_2, 20, "bold"))
label3.grid(row=0, column=3, columnspan=7)

label4 = tkinter.Label(text="", bg=YELLOW, fg=E_YELLOW, font=(FONT_NAME_2, 20, "bold"))
label4.grid(row=1, column=3, columnspan=7)

button1 = tkinter.Button(text="Voice", fg="black", bg=YELLOW, highlightthickness=0, highlightbackground=YELLOW,
                         command=calling_voice_commands
                         )
button1.grid(row=5, column=2)

button2 = tkinter.Button(text="Live Location", fg="black", bg=YELLOW, command=current_location_address)
button2.config(padx=2, pady=2)
button2.grid(row=5, column=4, columnspan=3)

button3 = tkinter.Button(text="Run application", bg=YELLOW)
button3.grid(row=5, column=3, columnspan=2)

window.iconbitmap(r"icon.ico")
######################TKINTER MAIN WINDOW LOOP#################################################
window.mainloop()
