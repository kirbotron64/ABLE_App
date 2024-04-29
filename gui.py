from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os
from backendUpdated import ExcelDataframe
from enum_filetypes import FileType

class Gui:
    def __init__(self, window):
        self.window = window
        self.window.title("ABLE Badge Creator")
        self.window.geometry("")
        # self.window.geometry("465x165")

        self.backend = ExcelDataframe()
        self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        # self.data_file_name = ""
        # self.template_file_name = ""
        self.data_file_name = "C:/Users/zacha/Documents/Repos/ABLE_App/registrations_April_24.xlsx"
        self.pdf_file_name = "C:/Users/zacha/Documents/Repos/ABLE_App/form_nested.pdf"

        # To be included in future feature update
        ###self.field_names = []
        ###self.options = self.backend.options
        ###self.fields_dict = {} # holds combobox objects

    def createInterfaceObjects(self):
        #Create buttons and labels
        self.button_datafile = Button(self.window, text = "Browse for data file", command=lambda:  self.browseFiles(FileType.DATAFILE), height=1)
        self.button_pdffile = Button(self.window, text = "Browse for pdf template", command=lambda:  self.browseFiles(FileType.PDF), height=1)
        self.button_create = Button(self.window, text = "Create Badges", command = self.createBadges, width= 15)
        self.label_datafile = Label(self.window, text = "No file selected", wraplength= 500, justify='left')
        self.label_pdffile = Label(self.window, text = "No file selected", wraplength= 500, justify='left')

        # Create grid structure for window
        self.window.rowconfigure((0,2,6), minsize= 15)
        self.window.rowconfigure((1,3,4,5), minsize= 30)
        self.window.columnconfigure((0,4), minsize= 10)
        self.window.columnconfigure(2, minsize= 200, )
        self.window.columnconfigure((1,3), minsize= 100)

        # Place buttons and labels within the grid
        self.button_datafile.grid(column=1,row=1,sticky='ew')
        self.button_pdffile.grid(column=1,row=3,sticky='ew')
        self.button_create.grid(column=3,row=5,sticky='ns')
        self.label_datafile.grid(column=2,row=1,columnspan=2)
        self.label_pdffile.grid(column=2,row=3,columnspan=2)



    # FILE BROWSER
    def browseFiles(self, type):
        """File browser for gui - requires parameter spicifying what file type should be searched for using the appropirate enum"""

        filename = filedialog.askopenfilename(initialdir = self.desktop_path,
                                              title = "Select a File",
                                              filetypes = type.value)
        if filename != "":
            match type:
                case FileType.PDF:
                    self.label_pdffile.configure(text = "File Selected: " + filename)
                    self.pdf_file_name = filename
                case FileType.DATAFILE:
                    self.label_datafile.configure(text = "File Selected: " + filename)
                    self.data_file_name = filename
                case _:
                    # Add error handling
                    pass
        print(filename)
            

    def createBadges(self):
        # for i in range(len(self.fields_dict)):
        #     self.field_names.append(self.fields_dict[f"Field_box_{i + 1}"].get())
        self.backend.dataFilePath = self.data_file_name
        self.backend.pdfTemplatePath = self.pdf_file_name
        self.backend.buildDataStructures()


        if self.backend.buildBadges() == True:
            tkinter.messagebox.showinfo("Badge Creation Status","Badge creation completed!")
            quit()


    # def labelFields(self):    
    #     # NUM FIELDS LABEL & DROPDOWN
    #     self.num_fields_label = Label(master,
    #                               text = "Select number of fields:")
    #     self.num_fields_label.grid(row=2,column=0,padx=2,pady=2)

    #     self.n = IntVar()
    #     self.num_fields = ttk.Combobox(master,
    #                                    width = 8,
    #                                    textvariable = self.n,
    #                                    justify = "center")
    #     self.num_fields["values"] = [2,3,4,5]
    #     self.num_fields.bind("<<ComboboxSelected>>", self.createFields)
    #     self.num_fields.grid(row=3,column=0,padx=2,pady=2)


    #     # FIELD SELECTION DROPDOWNS
    #     self.field_select_label = Label(master, text="Field Selection:")
    #     self.field_select_label.grid(row=4,padx=2,pady=2)



    # def createFields(self, event):
    #     for i in range(len(self.fields_dict)):
    #         self.fields_dict[f"Field_box_{i + 1}"].grid_forget()
    #     self.fields_dict.clear()
    #     num_fields = int(self.num_fields.get())
    #     for i in range(num_fields):
    #         self.field = StringVar()
    #         box = ttk.Combobox(self.master,
    #                            width = 15,
    #                            textvariable = self.field,
    #                            values = self.options)
    #         self.fields_dict[f"Field_box_{i + 1}"] = box
    #     for i in range(len(self.fields_dict)):
    #         self.fields_dict[f"Field_box_{i + 1}"].grid(row=4,column=i+1,padx=2,pady=2)

        
        
def main():
    root = Tk()
    gui = Gui(root)
    gui.createInterfaceObjects()
    root.mainloop()

if __name__ == "__main__":
    main()