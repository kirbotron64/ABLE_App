import pandas
import openpyxl
from pypdf import PdfReader, PdfWriter


class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self, dataFilename: str)->None:
        self.dataFilename = dataFilename
        self.excelData = pandas.read_excel(self.dataFilename)

        self.userSelectedData = []


    def GetColumnHeaders(self)->list[str]:
        """ Get header info from Dataframe object """
        
        excelHeaders = self.excelData.columns
        return excelHeaders
    

    
    def BuildBadges(self, userSelectedFields:list[str], pdfFilename: str):

        # Pass in a list from gui 
        self.userSelectedFields = userSelectedFields

        pdfTemplate = PdfReader(pdfFilename)
        pdfFilled = PdfWriter()

        pdfFilled.append(pdfTemplate)

        # pdfFilled.update_page_form_field_values(pdfFilled.pages[0],
        #     {

        #     }                                    
        # )

    def CreateUserSelectedDataframe(self):
        """ Build a smaller dataframe from given data """
    
        dataList = self.excelData(self.userSelectedFields)