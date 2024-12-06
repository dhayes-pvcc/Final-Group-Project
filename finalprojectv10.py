import os #allows for interaction with the os
from PIL import Image #imports pillow
from os import listdir #lets use functions for file management
import tkinter as tk # imports tkinter (GUI)
from tkinter import * #imports tkinter modules
from tkinter import messagebox #allows for popup messages
from PIL import Image, ImageTk #lets us use images with tkinter
import random #used for shuffling the cards
from tkinter import PhotoImage #also lets us use images with tkinter
from tkinter import filedialog #allows for the file browser look up function


def main(): 
    window = tk.Tk()    #main window
    window.title("FLashcard App") #title of window
    tk.Label(window, text="Enter Flashcard Set Name To Study:").pack() #display text
    entry = tk.Entry(window)  #allows for user input, assings it to a variable
    entry.pack()
    selected_option = tk.StringVar(value="Study")     #creates a base variable for the radiobutton
    tk.Radiobutton(window, text="Study", variable=selected_option, value="Study").pack()
    tk.Radiobutton(window, text="Add A New Flashcard Set to Study", variable=selected_option, value="Add").pack()  #radiobuttons for the two options
    def get_value():  #Calls the add or study function based on user input
        if selected_option.get() == "Add": #calls the add function if the add button was selected
            add()
        if selected_option.get() == "Study":
            flashcard_set_name = entry.get()  #gets the userinputted text for the name of the set
            if not flashcard_set_name.strip():
                messagebox.showerror("This Flashcard Set Does Not Exist") #shows error message when the flashcard set doenst exist
            else: #calls the study function for the flashcard set with the name given by the user input
                study(flashcard_set_name)
    button = tk.Button(window, text="Submit", command=get_value) #calls the getvalue function when the submit button is pressed
    button.pack()
    window.mainloop() #opens the window
def add():  #Add function for adding flashcards
    
    def select_folder(): #select folder function, called when the button is pressed
        folder_path = filedialog.askdirectory() #Opens file browser so the user can choose the folder containing their images.
        folder_label.config(text=f"Selected Folder: {folder_path}") #displays text that lets the user know what folder was selected
        folder_path_var.set(folder_path) 
    def create_flashcard_set(): #function that takes the images in the selected folder and saves the list on a text file 
        folder_path = folder_path_var.get() #gets the folder path from the user input and assigns it to a variable
        flashcard_set = flashcard_name_entry.get()#gets the user input for the flashcard set name and assigns it to a variable
        if not os.path.isdir(folder_path):  #Error message if folder doesn't exist
            print("This folder does not exist")
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
            if not images: #Error if there are no supported images in the folder.
                messagebox.showerror("Error", f"This Folder Contains No supported Images")
            else:
                messagebox.showinfo("Success", f"Flashcard set '{flashcard_set}' was succesfully created") #message to let the user know the set was created
                add_window.destroy() #closes the add window after the set has been created
    add_window = tk.Toplevel() #creates a new window
    add_window.title("Create Flashcard Set") #names the new window
    flashcard_name_label = tk.Label(add_window, text="What Would Your Like to Name Your Flashcard Set:") #adds text to the window
    flashcard_name_label.pack()
    flashcard_name_entry = tk.Entry(add_window) #allows for user input
    flashcard_name_entry.pack()
    folder_button = tk.Button(add_window, text="Select Your Folder Containing Your Images, only .jpg, .png, and .jpeg files are supported.", command=select_folder) #button to pick your folder, calls the select_folder function
    folder_button.pack()
    folder_path_var = tk.StringVar() #variable for the selected folder path
    folder_label = tk.Label(add_window, text="No folder selected")
    folder_label.pack()
    create_button = tk.Button(add_window, text="Create Flashcard Set", command=create_flashcard_set) #creates the flashcard set, calls the create_flashcard_set function
    create_button.pack()

def load_image_paths(file_path): #loads image paths from the text file
    with open(file_path,'r') as f: #opens the file in read mode
         paths = [line.strip() for line in f.readlines()] #reads each line and strips all empty white space
    return paths #returns list of image paths
def load_images(image_paths): #adds the imagepaths to a list and opens them using pillow
    images = [] #creates empty list
    for img_path in image_paths:
        try:
            img = Image.open(img_path) #opens each image with pillow and adds it to the images list
            images.append(img)
        except IOError: #error if pilloe cant open the image
            print(f"Could not open image at: {img_path}")
    return images #returns list of opened images

class FlashcardApp: #class for the study function
    def __init__(self, master, image_paths):
        self.master = master 
        self.image_paths = image_paths #paths list
        self.images = load_images(self.image_paths) #loads the images from image_paths list
        self.current_images = list(self.images) #creates a copy of the list so it can be shuffled
        self.shuffle_cards() #shuffles the flashcards
        self.image_label = tk.Label(master) #widget for displaying the images
        self.image_label.pack()
        self.keep_button = tk.Button(master, text="Keep", command=self.keep_card)  #Button to keep the flashcard, calls the keep card function
        self.keep_button.pack(side=tk.LEFT)
        self.remove_button = tk.Button(master, text="Remove", command = self.remove_card)  #Button to remove a flashcard, calls the remove card function
        self.remove_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop) #Button to stop the program
        self.stop_button.pack(side=tk.LEFT)
        self.show_image()  #calls show image function,displays the first image
    def shuffle_cards(self): #shuffles the flashcards
        random.shuffle(self.current_images)

    def show_image(self): #displays the current flashcard
        if not self.current_images: #checks if there are any cards left 
            if self.images:  #shuffles the cards after one instance of the flashcard set has been displayed
                self.current_images = list(self.images) #copies the original list 
                self.shuffle_cards() #calls shuffle function to shuffle the copy of the original list
            else:  #ends the program if there are no cards left (remove function has removed them all)
                messagebox.showinfo("Info", "Congrats, You Have Learned this Flashcard Set")
                self.master.destroy() #closes the window
                return
        img = self.current_images[0] #variable for the first image in the list
        try:
            img_resized = img.copy()  #copies the image so we can resize it
            img_resized.thumbnail((400, 400))  #resizes the image
            self.tk_image = ImageTk.PhotoImage(img_resized) #converts pillow to photoimage for tk to use
            
            self.image_label.config(image=self.tk_image)  #makes the label the image
        except Exception as e: #debug for image display issues
            print(f"Error displaying image: {e}")
    def keep_card(self): #moves onto the next card without removed it from the list
        if self.current_images: #checks if there are cards left in the deck
            self.current_images.pop(0)  #removes the current card from the 0 spot
        self.show_image() #displays the next card
    def remove_card(self): #removes the current flashcard from the list
        if self.current_images: #checks if there are any cards left
            current_image = self.current_images.pop(0) #removes the current card from the shuffled list
            self.images.remove(current_image) #removes the current card from the original list so it isn't shuffled back in
        self.show_image() #displays the next card
    def stop(self): #quits the program
        self.master.destroy() #closes the window

def study(flashcard_set_name): #study function, studies the flashcard set name that was entered 
    flashcard_set = flashcard_set_name + ".txt" #ctakes the name and adds .txt so we can use the txt file that was created for it
    if not os.path.isfile(flashcard_set):  #checks if the flashcard set exists and gives an error if it doesnt
        messagebox.showerror("Error", f"The flashcard set '{flashcard_set_name}' does not exist.")
        return
    image_paths = load_image_paths(flashcard_set) #loads the image paths from the text file
    study_window = tk.Toplevel() #creates new flashcard study window
    study_window.title("Studying: {flashcard_set_name}") #title of flashcard app, uses the user inputted name
    app = FlashcardApp(study_window, image_paths) #starts the flashcard app with the image paths given
    study_window.mainloop() #opens the window


main() #starts the program
