import pandas
import openpyxl
from pypdf import PdfReader, PdfWriter


class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self, dataFilename: str)->None:

        #Need to add error handling for a non excel file path
        self.dataFilename = dataFilename

        self.buildDataFrames()

        #Don't like that parameter requires first item to succeed
        self.excelWorkshopDict = self.CreateWorkshopDictionary(self.excelWorkshopData)
        

    def buildDataFrames(self) -> None:
        """Build dataframe members using excel file provided"""
        self.excelData = pandas.read_excel(self.dataFilename)

        #Need to add error handling if sheet names are different or if sheets do not exist
        #Need to verify that all columns are present or throw and error (Workshop ID, Room, & Presenter)
        excelWedData = pandas.read_excel(self.dataFilename, "Wednesday workshops")
        excelThuData = pandas.read_excel(self.dataFilename, "Thursday workshops")
        self.excelWorkshopData = pandas.concat([excelWedData, excelThuData])


    # def buildDictionaries(self) -> None:
    #     self.dictWedData = self.CreateWorkshopDictionary(self.excelWedData)
    #     self.dictThuData = self.CreateWorkshopDictionary(self.excelThuData)

    
    def GetColumnHeaders(self)->list[str]:
        """ Get header info from Dataframe object """
        
        excelHeaders = self.excelData.columns
        return excelHeaders
    
    
    def BuildBadges(self, userSelectedFields:list[str], pdfFilename: str):

        # # Create smaller DF with user selected columns
        # self.userSelectedData = self.excelData(userSelectedFields)

        # Create pdf objects (template and new blank doc)
        pdfTemplate = PdfReader(pdfFilename)
        pdfFilled = PdfWriter()


        # Set initial variables for looping
        page = 0
        count_per_page = 4
        pdfFilled.append(pdfTemplate)

        #Loop through all items in dataframe
        for index, row in self.excelData.iterrows():
            
            # set value for field in pdf (0 - 3) - should reset every 4th value and use page
            field_index = index - (page * count_per_page)

            # Set pdf fields to values from dataframe (references dict for workshop details)
            pdfFilled.update_page_form_field_values(
                pdfFilled.pages[page],
                {f"name_{field_index}"      : row['badge_name'],
                 f"college_{field_index}"   : row['institution'],
                 f"c2r2_{field_index}"      : self.excelWorkshopDict[row['wed_morning'][0]],
                 f"c3r2_{field_index}"      : self.excelWorkshopDict[row['wed_morning'][1]],
                 f"c2r3_{field_index}"      : self.excelWorkshopDict[row['wed_afternoon'][0]],
                 f"c3r3_{field_index}"      : self.excelWorkshopDict[row['wed_afternoon'][1]],
                 f"c2r4_{field_index}"      : self.excelWorkshopDict[row['thurs_morning'][0]],
                 f"c3r4_{field_index}"      : self.excelWorkshopDict[row['thurs_morning'][1]],
                 f"c2r5_{field_index}"      : self.excelWorkshopDict[row['thurs_afternoon'][0]],
                 f"c3r5_{field_index}"      : self.excelWorkshopDict[row['thurs_afternoon'][1]],
                },auto_regenerate=True
                )
            
            # if all four blocks on pdf filled out, reset field index and add new page
            if field_index >= 3:
                page += 1
                pdfFilled.append(pdfTemplate)

        # Change to save in same desitination as template with same name & "_complete" appended
        # Save complete pdf to folder with provided template
        with open("filled-out.pdf", "wb") as output_stream:
            pdfFilled.write(output_stream)





        # pdfFilled.update_page_form_field_values(pdfFilled.pages[0],
        #     {

        #     }                                    
        # )


    def CreateWorkshopDictionary(self, data : pandas.DataFrame) -> dict:
        columnID = data.columns.get_loc("workshopID")
        columnRoom = data.columns.get_loc("Room location")
        columnPresenter = data.columns.get_loc("Presenter")
        dataframeDictionary = pandas.Series(data['Room location'].values, data['workshopID'].values).to_dict()

        return dataframeDictionary



