import pandas
import openpyxl
from pdf_creator import PdfCreator


class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self, filename: str)->None:
        self.filename = filename
        self.excelData = pandas.read_excel(self.filename)


    def GetColumnHeaders(self)->list[str]:
        """ Get header info from Dataframe object """
        
        excelHeaders = self.excelData.columns
        return excelHeaders