#gui for badge creation using tkinter
from tkinter import *
from tkinter import filedialog


class Gui:
    def __init__(self, master):
        self.master = master
        master.title("Able Badge Creator")
        master.geometry("500x500")

    
        self.file_name = ""
        self.options = [
            # Populate from file selection (list will populate from fields provided in file)
            "Time Slot",
            "Presenter",
            "Room"
        ]
        # data type of menu text
        self.clicked = StringVar()
        self.clicked.set( "Choose field" )
        self.drop = OptionMenu(master, self.clicked, *self.options )
        self.drop.pack()

        self.button = Button(master, text = "Click Me", command = self.show)
        self.button.pack()

        self.label = Label (master, text = " ")
        self.label.pack()

        self.label_file_explorer = Label(master,
                                         text = "No file selected")
        self.label_file_explorer.pack()
        self.button_explore = Button(master,
                                     text = "Browse Files",
                                     command= self.browseFiles)
        self.button_explore.pack()
        

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select a File",
                                              filetypes = (("Text files",
                                                            "*.txt*"),
                                                            ("all files",
                                                             "*.*")))
        self.label_file_explorer.configure(text = "File Selected: " + filename)
        self.file_name = filename

    def show(self):
        self.label.config(text = self.clicked.get())

def main():
    root = Tk()
    gui = Gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()