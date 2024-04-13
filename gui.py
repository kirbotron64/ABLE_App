#gui for badge creation using tkinter
#
#
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
# from backend import *

class Gui:
    def __init__(self, master):
        self.master = master
        master.title("ABLE Badge Creator")
        master.geometry("500x300")

        #variables to be accessed by backend, to produce pdfs
        self.file_name = ""
        self.field_names = []
        self.options = [ # replace with backend.field_list (backend will grab list of fields from csv's)
            "Time Slot",
            "Presenter",
            "Room"
        ]
        self.fields_dict = {} # holds combobox objects

        #FILE BROWSER
        self.label_file_explorer = Label(master,
                                         text = "No file selected")
        self.label_file_explorer.pack()
        self.button_explore = Button(master,
                                     text = "Browse Files",
                                     command= self.browseFiles)
        self.button_explore.pack()


        # NUM FIELDS LABEL & DROPDOWN
        self.num_fields_label = Label(master,
                                  text = "Select number of fields")
        self.num_fields_label.pack()

        self.n = IntVar()
        self.num_fields = ttk.Combobox(master,
                                       width = 8,
                                       textvariable = self.n,
                                       justify = "center")
        self.num_fields["values"] = [2,3,4,5]
        self.num_fields.bind("<<ComboboxSelected>>", self.createFields)
        self.num_fields.pack()


        # FIELD SELECTION DROPDOWNS
        self.field_select_label = Label(master, text="Field Selection:")
        self.field_select_label.pack()

        # CREATE BADGES BUTTON
        self.button_create = Button(master,
                                    text = "Click Here to Create Badges",
                                    command = self.createBadges)
        self.button_create.pack()

    # FILE BROWSER
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select a File",
                                              filetypes = (("Text files",
                                                            "*.txt*"),
                                                            ("all files",
                                                             "*.*")))
        self.label_file_explorer.configure(text = "File Selected: " + filename)
        self.file_name = filename

    def createFields(self, event):
        for i in range(len(self.fields_dict)):
            self.fields_dict[f"Field_box_{i + 1}"].pack_forget()
        self.fields_dict.clear()
        num_fields = int(self.num_fields.get())
        for i in range(num_fields):
            self.field = StringVar()
            box = ttk.Combobox(self.master,
                               width = 15,
                               textvariable = self.field,
                               values = self.options)
            self.fields_dict[f"Field_box_{i + 1}"] = box
        for i in range(len(self.fields_dict)):
            self.fields_dict[f"Field_box_{i + 1}"].pack()

    def createBadges(self):
        for i in range(len(self.fields_dict)):
            self.field_names.append(self.fields_dict[f"Field_box_{i + 1}"].get())
        print(self.field_names)
        print(self.file_name)
        
        

def main():
    root = Tk()
    gui = Gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()