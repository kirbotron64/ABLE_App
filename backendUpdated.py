import pandas
import openpyxl
import os
#from pypdf import PdfReader, PdfWriter
import PyPDF2




class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self)->None:

        self.dataFilePath = ""
        self.pdfTemplatePath = ""
        self.excelData = pandas.DataFrame()
        self.excelWorkshopDict = {}


    def buildDataStructures(self) -> None:
        """Build dataframe members using excel file provided"""

        # Need to add error handling for a non excel file path
        # Need to add error handling if sheet names are different or if sheets do not exist
        # Need to verify that all columns are present or throw and error (Workshop ID, Room, & Presenter)
        self.excelData = pandas.read_excel(self.dataFilePath)
        excelWedData = pandas.read_excel(self.dataFilePath, "Wednesday workshops")
        excelThuData = pandas.read_excel(self.dataFilePath, "Thursday workshops")
        excelWorkshopData = pandas.concat([excelWedData, excelThuData])
        # self.excelWorkshopDict = pandas.Series([excelWorkshopData['Room location'].values,
        #                                         excelWorkshopData['Presenter'].values],
        #                                         excelWorkshopData['workshopID'].values).to_dict()
        self.excelWorkshopDict = excelWorkshopData.set_index('workshopID').T.to_dict('list')


    # def createWorkshopDictionary(self, data : pandas.DataFrame) -> dict:
    #     columnID = data.columns.get_loc("workshopID")
    #     columnRoom = data.columns.get_loc("Room location")
    #     columnPresenter = data.columns.get_loc("Presenter")
    #     dataframeDictionary = pandas.Series([data['Room location'].values, data['Presenter'].values], data['workshopID'].values).to_dict()

    #     return dataframeDictionary


    # def buildDictionaries(self) -> None:
    #     self.dictWedData = self.CreateWorkshopDictionary(self.excelWedData)
    #     self.dictThuData = self.CreateWorkshopDictionary(self.excelThuData)

    
    # def getColumnHeaders(self)->list[str]:
    #     """ Get header info from Dataframe object """
        
    #     excelHeaders = self.excelData.columns
    #     return excelHeaders
    
    
    def buildBadges(self) -> bool:
        """Uses pdf template provided, data sets provided, and selected columns to construct
        the complete pdf document containing all badges for values in the data set. PDF doc
        has 4 values per badges per page and will be saved to the same location as the template
        document appended with '_Complete'."""


        # # Feature add - userSelectedFields:list[str]
        # # Create smaller DF with user selected columns
        # self.userSelectedData = self.excelData(userSelectedFields)

        # Create pdf objects (template and new blank doc)
        pdfTemplate = PyPDF2.PdfReader(self.pdfTemplatePath)
        pdfFilled = PyPDF2.PdfWriter()


        # Set initial variables for looping
        page = 0
        count_per_page = 4
        #pdfFilled.append(pdfTemplate)
        template_page = pdfTemplate.pages[0]

        #Loop through all items in dataframe
        for index, row in self.excelData.iterrows():
            
            # set value for field in pdf (0 - 3) - should reset every 4th value and use page
            field_index = index - (page * count_per_page)

            if pandas.isnull(row['wed_morning']): row['wed_morning'] = "WK0"
            if pandas.isnull(row['wed_afternoon']): row['wed_afternoon'] = "WK0"
            if pandas.isnull(row['thurs_morning']): row['thurs_morning'] = "WK0"
            if pandas.isnull(row['thurs_afternoon']): row['thurs_afternoon'] = "WK0"

            # Set pdf fields to values from dataframe (references dict for workshop details)
            template_page = pdfFilled.update_page_form_field_values(
                template_page,
                {f"name_{field_index}"      : row['badge_name'],
                 f"college_{field_index}"   : row['institution'],
                 f"c2r2_{field_index}"      : self.excelWorkshopDict[row['wed_morning']][2],
                 f"c3r2_{field_index}"      : self.excelWorkshopDict[row['wed_morning']][1],
                 f"c2r3_{field_index}"      : self.excelWorkshopDict[row['wed_afternoon']][2],
                 f"c3r3_{field_index}"      : self.excelWorkshopDict[row['wed_afternoon']][1],
                 f"c2r4_{field_index}"      : self.excelWorkshopDict[row['thurs_morning']][2],
                 f"c3r4_{field_index}"      : self.excelWorkshopDict[row['thurs_morning']][1],
                 f"c2r5_{field_index}"      : self.excelWorkshopDict[row['thurs_afternoon']][2],
                 f"c3r5_{field_index}"      : self.excelWorkshopDict[row['thurs_afternoon']][1],
                }
                )
            
            # if all four blocks on pdf filled out, reset field index and add new page
            if field_index >= 3:
                page += 1
                pdfFilled.add_page(updated_page)

        # Save complete pdf to folder with provided template
        save_path = os.path.dirname(self.pdfTemplatePath)
        output_stream = open(save_path + "/_complete.pdf", "wb")
        pdfFilled.write(output_stream)

        return True