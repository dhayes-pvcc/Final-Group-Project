import os
from PIL import Image
from PIL import ImageFilter
from os import listdir
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from tkinter import PhotoImage
from tkinter import filedialog

def get_value(selected_option, entry_widget):  #Calls the add or study function based on user input from the entrywidget
    value = entry_widget.get()
    if selected_option.get() == "Add":
        add()
    if selected_option.get() == "Study":
        study()
def main():
    window = tk.Tk()    
    window.title("FLashcard App")
    tk.Label(window, text="Enter Flashcard Set Name To Study:").pack()
    entry = tk.Entry(window)  
    entry.pack()
    selected_option = tk.StringVar(value="Study")     #creates a base variable for the radiobutton
    tk.Radiobutton(window, text="Study", variable=selected_option, value="Study").pack()
    tk.Radiobutton(window, text="Add A New Flashcard Set to Study", variable=selected_option, value="Add").pack()  #radiobuttons for the two options
    def get_value():  #Calls the add or study function based on user input
        if selected_option.get() == "Add":
            add()
        if selected_option.get() == "Study":
            flashcard_set_name = entry.get()  #gets the user input
            if not flashcard_set_name.strip():
                messagebox.showerror("This Flashcard Set Does Not Exist") #shows error message when the flashcard set doenst exist
            else: #calls the study function
                study(flashcard_set_name)
    button = tk.Button(window, text="Submit", command=get_value) #calls the getvalue function 
    button.pack()
    window.mainloop()
def add():  #Add function for adding flashcards
    
    def select_folder():
        folder_path = filedialog.askdirectory()
        folder_label.config(text=f"Selected FOlder: {folder_path}")
        folder_path_var.set(folder_path)
    def create_flashcard_set():
        folder_path = folder_path_var.get()
        flashcard_set = flashcard_name_entry.get()
        if not os.path.isdir(folder_path):  #Error message if folder doesn't exist
            print("This folder does not exist.")
        else:
            images = []   #Empty list to add images to
            save_file = flashcard_set + ".txt"  #Creates a text file using the flashcard set name
            with open(save_file, 'w') as f:    #opens the save file in write mode
                for filename in os.listdir(folder_path): #Iterates through each image in the folder
                    if filename.endswith(('.png', '.jpg', '.jpeg')):  #Makes sure it's a supported image file
                        img_path = os.path.join(folder_path, filename) #Adds the filename path to the folder path
                        f.write(img_path + '\n') #Writes each file path onto a new line in the save file
                        with Image.open(img_path) as img: #Adds each img to the list until there are no more img_path
                            images.append(img.copy())     
            if not images:
                messagebox.showerror("Error", f"This Folder Contains No supported Images")
    add_window = tk.Toplevel()
    add_window.title("Create Flashcard Set")
    flashcard_name_label = tk.Label(add_window, text="What Would Your Like to Name Your Flashcard Set:")
    flashcard_name_label.pack()
    flashcard_name_entry = tk.Entry(add_window)
    flashcard_name_entry.pack()
    folder_button = tk.Button(add_window, text="Select Your Folder Containing Your Images, only .jpg, .png, and .jpeg files are supported.", command=select_folder)
    folder_button.pack()
    folder_path_var = tk.StringVar()
    folder_label = tk.Label(add_window, text="No folder selected")
    folder_label.pack()
    create_button = tk.Button(add_window, text="Create Flashcard Set", command=create_flashcard_set)
    create_button.pack()

def load_image_paths(file_path): #loads image paths from the text file
    with open(file_path,'r') as f:
         paths = [line.strip() for line in f.readlines()]
    return paths
def load_images(image_paths): #adds the imagepaths to a list and opens them using pillow
    images = []
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            images.append(img)
        except IOError:
            print(f"Could not open image at: {img_path}")
    return images

class FlashcardApp: #this class organizes all the functions for the study function
    def __init__(self, master, image_paths):
        self.master = master
        self.image_paths = image_paths
        self.images = load_images(self.image_paths)
        self.current_images = list(self.images)
        self.shuffle_cards()
        self.image_label = tk.Label(master)
        self.image_label.pack()
        self.keep_button = tk.Button(master, text="Keep", command=self.keep_card)  #Button to keep the flashcard, calls the keep card function
        self.keep_button.pack(side=tk.LEFT)
        self.remove_button = tk.Button(master, text="Remove", command = self.remove_card)  #Button to remove a flashcard, calls the remove card function
        self.remove_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop) #Button to stop the program
        self.stop_button.pack(side=tk.LEFT)
        self.show_image()  #calls show image function
    def shuffle_cards(self):
        random.shuffle(self.current_images)

    def show_image(self):
        if not self.current_images: 
            if self.images:  #shuffles the cards after one instance of the flashcard set has been displayed
                self.current_images = list(self.images)
                self.shuffle_cards()
            else:  #ends the program if there are no cards left (remove function has removed them all)
                messagebox.showinfo("Info", "Congrats, You Have Learned this Flashcard Set")
                self.master.destroy()
                return
        img = self.current_images[0] 
        try:
            img_resized = img.copy()  #copies the image so we can resize it
            img_resized.thumbnail((400, 400))  #resizes the image
            self.tk_image = ImageTk.PhotoImage(img_resized) #converts pillow to photoimage for tk to use
            
            self.image_label.config(image=self.tk_image)  #makes the label the image
              # Store reference to avoid garbage collection
        except Exception as e:
            print(f"Error displaying image: {e}")
    def keep_card(self):
        if self.current_images:
            self.current_images.pop(0)  #moves on to the next image
        self.show_image()
    def remove_card(self):
        if self.current_images:
            current_image = self.current_images.pop(0) #moves onto the next image after removed the current one from the list
            self.images.remove(current_image)
        self.show_image()
    def stop(self): #quits the program
        self.master.destroy()

def study(flashcard_set_name):
    flashcard_set = flashcard_set_name + ".txt" #currently typed into the console need to add into tk #calls function
    if not os.path.isfile(flashcard_set):  #checks if the flashcard set exists and gives an error if it doesnt
        messagebox.showerror("Error", f"The flashcard set '{flashcard_set_name}' does not exist.")
        return
    image_paths = load_image_paths(flashcard_set)
    study_window = tk.Toplevel() #creates new flashcard study window
    study_window.title("Studying: {flashcard_set_name}")
    app = FlashcardApp(study_window, image_paths)
    study_window.mainloop()


main()
