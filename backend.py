class BackEnd:
    def __init__(self, gui):
        self.gui = gui
        #POPULATE LIST WITH CSV
        self.options = [
            "Time Slot",
            "Presenter",
            "Room"
        ]
        self.field_names = []

    def buildBadges(self):
        #build badges
        self.field_names.extend(self.gui.field_names)
        return True