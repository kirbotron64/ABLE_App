from pypdf import PdfReader, PdfWriter

#create pdfcreator objects to produce a page,
#repeat until list exhausted

class PdfCreator():
    def __init__(self, badge_dict):
        self.badge_dict = badge_dict

        self.reader = PdfReader("form_nested.pdf")
        self.writer = PdfWriter()

        page = self.reader.pages[0]
        fields = self.reader.get_fields()

        self.writer.append(self.reader)

        self.writer.update_page_form_field_values(
            self.writer.pages[0],
            {"name_0": f"{badge_dict[0][0]}",
            "college_0": f"{badge_dict[0][1]}",
            "c1r1_0": "Time Slot","c2r1_0": "Presenter","c3r1_0": "Room",
            "c1r2_0": "Wed Morn","c2r2_0": "Name1","c3r2_0": "York 1",
            "c1r3_0": "Wed Aft","c2r3_0": "Name2","c3r3_0": "York 2",
            "c1r4_0": "Thu Morn","c2r4_0": "Name3","c3r4_0": "York 3",
            "c1r5_0": "Thu Aft","c2r5_0": "Name4","c3r5_0": "York 4",
            "name_1": f"{badge_dict[1][0]}",
            "college_1": f"{badge_dict[1][1]}",
            "c1r1_1": "Time Slot","c2r1_1": "Presenter","c3r1_1": "Room",
            "c1r2_1": "Wed Morn","c2r2_1": "Name1","c3r2_1": "York 1",
            "c1r3_1": "Wed Aft","c2r3_1": "Name2","c3r3_1": "York 2",
            "c1r4_1": "Thu Morn","c2r4_1": "Name3","c3r4_1": "York 3",
            "c1r5_1": "Thu Aft","c2r5_1": "Name4","c3r5_1": "York 4",
            "name_2": f"{badge_dict[2][0]}",
            "college_2": f"{badge_dict[2][1]}",
            "c1r1_2": "Time Slot","c2r1_2": "Presenter","c3r1_2": "Room",
            "c1r2_2": "Wed Morn","c2r2_2": "Name1","c3r2_2": "York 1",
            "c1r3_2": "Wed Aft","c2r3_2": "Name2","c3r3_2": "York 2",
            "c1r4_2": "Thu Morn","c2r4_2": "Name3","c3r4_2": "York 3",
            "c1r5_2": "Thu Aft","c2r5_2": "Name4","c3r5_2": "York 4",
            "name_3": f"{badge_dict[3][0]}",
            "college_3": f"{badge_dict[3][1]}",
            "c1r1_3": "Time Slot","c2r1_3": "Presenter","c3r1_3": "Room",
            "c1r2_3": "Wed Morn","c2r2_3": "Name1","c3r2_3": "York 1",
            "c1r3_3": "Wed Aft","c2r3_3": "Name2","c3r3_3": "York 2",
            "c1r4_3": "Thu Morn","c2r4_3": "Name3","c3r4_3": "York 3",
            "c1r5_3": "Thu Aft","c2r5_3": "Name4","c3r5_3": "York 4"},
            auto_regenerate=True,
        )

        # write "output" to pypdf-output.pdf
        with open("filled-out.pdf", "wb") as output_stream:
            self.writer.write(output_stream)