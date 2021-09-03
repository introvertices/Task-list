import math
import os
import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from itertools import count, cycle
import json


#-------------------------------------------------------------------------------
#!--- VARS FOR QUESTY STUFF
# goat gifs
goat1 = "./goats/goat1.gif"
goat2 = "./goats/goat2.gif"
goat3 = "./goats/goat3.gif"
current_goat = goat1

# Import Json file to stats
with open("stats.json") as stats_file:
    stat_import = json.load(stats_file)
     
    current_level = stat_import["current_level"]
    current_xp = stat_import["current_xp"]
    needed_xp = stat_import["needed_xp"] * math.ceil(current_level/2)

    # Check goat clothes
    if current_level <=3:
        current_goat = goat1
    elif current_level >=4 and current_level <=6:
        current_goat = goat2
    else:
        current_goat = goat3
    
    #DEBUG print(current_goat)



#-------------------------------------------------------------------------------
#!--- ALLOW ANIMATED GIFS
class ImageLabel(tkinter.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)



#-------------------------------------------------------------------------------
#!--- FUNCTIONS

# Get correct list from selected dropdown option
def display_list(choice):
    choice = dropdown_var.get()
    print(choice)
    # Grab tasks from text file
    file_to_open ="lists/" + choice + ".txt"
    print(file_to_open)
    with open(file_to_open,"r") as tasklist_file:
        current_tasklist = tasklist_file.read().splitlines()
    task_list.delete(0,END)
    for i in current_tasklist:
        task_list.insert(END,"  " + i)

# Checks current experience gain against required XP to level
def check_xp():
    global current_level
    global current_xp
    global needed_xp
    global current_goat

    if current_xp >= needed_xp:
        current_level +=1
        current_xp = 0
        needed_xp = 5 + current_level * math.ceil(current_level/2)
        # Check goat clothes
        if current_level <=3:
            current_goat = goat1
        elif current_level >=4 and current_level <=6:
            current_goat = goat2
        else:
            current_goat = goat3
        # WOW THIS SUCKED TO FIX AND FIGURE OUT LMAO (kills the goat and rebirths the asshole with new clothes if needed)
        goat_img.configure(image=None)
        goat_img.configure(goat_img.load(current_goat))
        print(current_goat)

    print(current_level," ", current_xp," ",needed_xp)






#!--- BUTTON BEHAVIOURS
# Add a new task
def add_task():
    task = new_entry.get()
    # # WOW THIS SUCKED TO FIX AND FIGURE OUT LMAO
    # goat_img.configure(image=None)
    # goat_img.configure(goat_img.load(current_goat))

    if task != "":
        global current_xp
        current_xp +=1
        task_list.insert(END,"  " + task)
        new_entry.delete(0, "end")
        current_tasklist.append(task)

        check_xp()

        # Export stats to Json
        stat_export = {"current_level":current_level,"current_xp":current_xp,"needed_xp":needed_xp}
        with open("stats.json","w") as outfile:
            json.dump(stat_export, outfile)
        
    else:
        messagebox.showwarning("warning", "Please enter a task!")
    
    # Refresh stats canvas to show updated values
    stat_canvas.itemconfig(lvl_info,text=current_level)
    stat_canvas.itemconfig(xp_info,text=current_xp)
    stat_canvas.itemconfig(needed_info,text=needed_xp - current_xp)




# Delete highlighted task
def del_task():
    # Get the item the user is attempting to delete and store it in a var to remove from the initial list
    return_focus = task_list.get(task_list.curselection())
    task_list.delete(ANCHOR)
    current_tasklist[:] = [x for x in current_tasklist if return_focus not in x]        # Checks if return_focus is in the task list and removes it

# Save task list
def save_list():
    #print(current_tasklist)
    #list_to_save = task_list
    with open(file_to_open, "w") as tasks_to_save:
        for i in current_tasklist:
            tasks_to_save.write(i + "\n")







#-------------------------------------------------------------------------------
#!!!!!!!!!--- TKINTER LOOP FROM UNDER HERE
# Set up our main window
task_win = Tk()


#!--- WINDOW WIDTH, HEIGHT, XPOS, YPOS, TITLE, AND DISABLE RESIZE ---
task_win.geometry('450x600+500+200')
task_win.title('Task Quest')
task_win.resizable(width = False, height = False)


#!--- BG UI GFX ---
ui_bg = PhotoImage(file="ui/ui_bg.png")
label1 = Label(task_win, image = ui_bg, borderwidth = 0)
label1.place(x = 0, y = 0)


#!--- DROPODOWN MENU ---
# Dropdown of lists
dirListing = os.listdir("lists/")
detected_files = []
for item in dirListing:
    if ".txt" in item:
        detected_files.append(item.replace(".txt",""))

#DEBUG print(detected_files)

# Create a new list with any underscores and file extensions stripped by this point
avail_lists = [s.replace("_"," ") for s in detected_files]

dropdown_var = StringVar(task_win)
dropdown_var.set(avail_lists[0])    # default dropdown value
dropdown_lists = OptionMenu(task_win, dropdown_var, *avail_lists,command=display_list)

# Dropdown Styling
dropdown_lists["highlightthickness"]=0
dropdown_lists["width"]=7

# Placement of element
dropdown_lists.place(x=19, y=112)


#!--- OPEN DEFAULT FILE
choice = dropdown_var.get()
file_to_open = "lists/" + choice + ".txt"
#DEBUG print(file_to_open)
with open(file_to_open,"r") as tasklist_file:
    current_tasklist = tasklist_file.read().splitlines()



#!--- MAIN FRAME SET UP FOR LIST BOX AND SCROLLBAR
frame = Frame(task_win)
frame.place(x=137,y=112)

#!--- LIST BOX 
# List box for our tasks to go live in
task_list = Listbox(frame,width=30,height=17,font=('Arial',12),bd=0,bg="#283189",fg="#FFFFFF",highlightthickness=0,selectbackground="#191e51",activestyle="none")
task_list.pack(side=LEFT,fill= BOTH)

# Insert tasks into list box from our task list created from the text file
for i in current_tasklist:
    task_list.insert(END,"  " + i)


#!--- SCROLLBAR
# Vertical scrollbar for longer to-do lists
tasklist_sb = Scrollbar(frame)
tasklist_sb.pack(side=RIGHT,fill=BOTH)

# Bind the scrollbar and list box together
task_list.config(yscrollcommand=tasklist_sb.set)
tasklist_sb.config(command=task_list.yview)


#!--- NEW ENTRIES
new_entry = Entry(task_win,font=("Arial",11),width=28)
new_entry.place(x=195,y=470)


#!--- BUTTONS
y_shift = 518
butt_width = 8

# Add task button
add_task_btn= Button(task_win,text='Add',font=("Arial",11),bg="#b4ea66",padx=2,pady=0,width=butt_width,command=add_task)
add_task_btn.place(x=133,y=y_shift)

# Delete task button
del_task_btn = Button(task_win,text='Delete',font=("Arial",11),bg="#940345",fg="white",padx=2,pady=0,width=butt_width,command=del_task)
del_task_btn.place(x=240,y=y_shift)

# Save tasks button
save_task_btn= Button(task_win,text='Save',font=("Arial",11),bg="#ffc96f",padx=2,pady=0,width=butt_width,command=save_list)
save_task_btn.place(x=347,y=y_shift)


#!--- GOAT MANAGEMENT <3
goat_x = 10
goat_y = 450
goat_img = ImageLabel(task_win,bd=0)
goat_img.place(x=goat_x,y=goat_y)

# Goat stats
stat_canvas = Canvas(task_win,width=107,height=150,bd=-2)
stat_canv_image = PhotoImage(file="./ui/stats_canv.png")
stat_canvas.place(x=7,y=300)
stat_canvas.create_image(0,0,image=stat_canv_image,anchor=NW)
lvl_info = stat_canvas.create_text(53,37,font=("Arial",14),fill="White",text=current_level)
xp_info = stat_canvas.create_text(53,82,font=("Arial",14),fill="White",text=current_xp)
needed_info = stat_canvas.create_text(53,123,font=("Arial",14),fill="White",text=needed_xp)

# Refresh the goat
goat_img.load(current_goat)




# Yay it works~
task_win.mainloop()