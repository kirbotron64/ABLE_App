import pandas
import openpyxl
from pypdf import PdfReader, PdfWriter


class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self, dataFilename: str)->None:
        self.dataFilename = dataFilename
        self.excelData = pandas.read_excel(self.dataFilename)
        self.excelWedData = pandas.read_excel(self.dataFilename, "Wednesday workshops")
        self.excelThuData = pandas.read_excel(self.dataFilename, "Thursday workshops")

        self.userSelectedData = []

        self.dictWedData = self.CreateWorkshopDictionary(self.excelWedData)
        self.dictThuData = self.CreateWorkshopDictionary(self.excelThuData)



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

    def CreateWorkshopDictionary(self, data : pandas.DataFrame) -> dict:
        columnID = data.columns.get_loc("workshopID")
        columnRoom = data.columns.get_loc("Room location")
        columnPresenter = data.columns.get_loc("Presenter")
        dataframeDictionary = pandas.Series(data['Room location'].values, data['workshopID'].values).to_dict()

        return dataframeDictionary



