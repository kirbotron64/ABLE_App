from pdf_creator import PdfCreator

class BackEnd:
    def __init__(self, gui):
        self.gui = gui
        self.options = [
            "Time Slot",
            "Presenter",
            "Room"
        ]
        self.field_names = []
        self.badges_dict = {
            0: ["Matthew Kirby", "Western Governors University"],
            1: ["Zachary Coleman", "Cal Poly Pomona"],
            2: ["Jacob Gower", "Univeristy California Riverside"],
            3: ["Greg Lisk", "University Hard Knocks"]
        }

    def buildBadges(self):
        #build badges
        self.field_names.extend(self.gui.field_names)


        self.pdf_creator = PdfCreator(self.badges_dict)
        
        return True