from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os
from backendUpdated import ExcelDataframe
from typing import Literal

class Gui:
    def __init__(self, window):
        self.window = window
        self.window.title("ABLE Badge Creator")
        self.window.geometry("")

        self.backend = ExcelDataframe()
        self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.data_file_name = ""
        self.template_file_name = ""


    def createInterfaceObjects(self):
        #Create buttons and labels
        self.button_datafile = Button(self.window, text = "Browse for data file", command=lambda:  self.setFilePath('excel'), height=1)
        self.button_pdffile = Button(self.window, text = "Browse for pdf template", command=lambda:  self.setFilePath('pdf'), height=1)
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
    def setFilePath(self, type: Literal['pdf', 'excel']):
        """File browser for gui - requires parameter spicifying what file type should be searched for using the appropirate enum"""

        try:
            match type:
                case 'pdf':
                    ###Talk to Josh about a better way to do this?
                    filename = self.fileBrowser([('PDF Files', '.pdf')])
                    try:
                        self.backend.set_pdfTemplatePath(filename)
                    except:
                        tkinter.messagebox.showinfo("Error!","Incorrect filetype chosen. Please try again.")
                    else:
                        self.pdf_file_name = filename
                        self.label_pdffile.configure(text = "File Selected: " + filename)
                case 'excel':
                    filename = self.fileBrowser([('Excel Files', '.xls*')])
                    try:
                        self.backend.set_dataFilePath(filename)
                    except:
                        tkinter.messagebox.showinfo("Error!","Incorrect filetype chosen. Please try again.")
                    else:
                        self.data_file_name = filename
                        self.label_datafile.configure(text = "File Selected: " + filename)
                case _:
                    pass
        except (ValueError) as e:
            tkinter.messagebox.showinfo(f"{e}")


    def fileBrowser(self, type: tuple[str, str]) -> str:
        filename = filedialog.askopenfilename(initialdir = self.desktop_path,
                                              title = "Select a File",
                                              filetypes = type)
        return filename
            

    def createBadges(self):
        if self.backend.buildBadges() == True:
            tkinter.messagebox.showinfo("Badge Creation Status","Badge creation completed!")
            quit()

        
        
def main():
    root = Tk()
    gui = Gui(root)
    gui.createInterfaceObjects()
    root.mainloop()

if __name__ == "__main__":
    main()