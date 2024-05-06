import pandas
import openpyxl
import os
import PyPDF2




class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self)->None:

        self.dataFilePath = ""
        self.pdfTemplatePath = ""
        self.excelData = pandas.DataFrame()
        self.excelWorkshopDict = {}
        self.presenter_index = 0
        self.location_index = 0


    def set_dataFilePath(self, path: str) -> None:
        """sets file path field for data file"""

        #add handling for none selected
        if not (path.lower().endswith('xls') or 
                path.lower().endswith('xlsx') or 
                path.lower().endswith('xlsm')):
            raise Exception("Incorrect file type provided")
        else:
            self.dataFilePath = path
            self.buildDataStructures()

    def set_pdfTemplatePath(self, path: str) -> None:
        """sets file path field for pdf template file"""

        #add handling for none selected
        if not path.lower().endswith('pdf'):
            raise Exception("Incorrect file type provided")
        else:
            self.pdfTemplatePath = path

    
    def buildDataStructures(self) -> None:
        """Build dataframe members using excel file provided"""

        # Need to add error handling for a non excel file path
        # Need to add error handling if sheet names are different or if sheets do not exist
        # Need to verify that all columns are present or throw and error (Workshop ID, Room, & Presenter)

        # Build dataframes from excel worksheets
        try:
            self.excelData = pandas.read_excel(self.dataFilePath, "registrations")
        except:
            raise Exception("\'registrations\' worksheet not found in data file")
        
        try:
            excelWedData = pandas.read_excel(self.dataFilePath, "Wednesday workshops")
        except:
            raise Exception("\'Wednesday workshops\' worksheet not found in data file")
        
        try:
            excelThuData = pandas.read_excel(self.dataFilePath, "Thursday workshops")
        except:
            raise Exception("\'Thursday workshops\' worksheet not found in data file")
        
        #if any above are true then exit

        
        #Verify data existence in workshop dataframes+
        if not "workshopID" in excelWedData.columns:
            raise Exception("Column \'workshopID\' not found in the \'Wednesday workshops\' worksheet")
        if not "Presenter" in excelWedData.columns:
            raise Exception("Column \'Presenter\' not found in the \'Wednesday workshops\' worksheet")
        if not "Location" in excelWedData.columns:
            raise Exception("Column \'Location\' not found in the \'Wednesday workshops\' worksheet")
        if not "workshopID" in excelThuData.columns:
            raise Exception("Column \'workshopID\' not found in the \'Thursday workshops\' worksheet")
        if not "Presenter" in excelThuData.columns:
            raise Exception("Column \'Presenter\' not found in the \'Thursday workshops\' worksheet")
        if not "Location" in excelThuData.columns:
            raise Exception("Column \'Location\' not found in the \'Thursday workshops\' worksheet")
        
        #if any above are true raise exit (use variable fed by the above?)


        #Concat workshop dataframes, index columns, and create dictionary
        excelWorkshopData = pandas.concat([excelWedData, excelThuData])
        self.presenter_index = excelWorkshopData.columns.get_loc("Presenter") - 1
        self.location_index = excelWorkshopData.columns.get_loc("Location") - 1
        self.excelWorkshopDict = excelWorkshopData.set_index('workshopID').T.to_dict('list')



    
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
        pdfFilled.append(pdfTemplate)

        #Loop through all items in dataframe
        for index, row in self.excelData.iterrows():
            
            # set value for field in pdf (0 - 3) - should reset every 4th value and use page
            field_index = index - (page * count_per_page)

            if pandas.isnull(row['wed_morning']): row['wed_morning'] = "WK0"
            if pandas.isnull(row['wed_afternoon']): row['wed_afternoon'] = "WK0"
            if pandas.isnull(row['thurs_morning']): row['thurs_morning'] = "WK0"
            if pandas.isnull(row['thurs_afternoon']): row['thurs_afternoon'] = "WK0"

            # Set pdf fields to values from dataframe (references dict for workshop details)
            pdfFilled.update_page_form_field_values(
                pdfFilled.pages[page],
                {f"name_{field_index}"      : row['badge_name'],
                 f"college_{field_index}"   : row['institution'],
                 f"c2r2_{field_index}"      : self.excelWorkshopDict[row['wed_morning']][self.presenter_index],
                 f"c3r2_{field_index}"      : self.excelWorkshopDict[row['wed_morning']][self.location_index],
                 f"c2r3_{field_index}"      : self.excelWorkshopDict[row['wed_afternoon']][self.presenter_index],
                 f"c3r3_{field_index}"      : self.excelWorkshopDict[row['wed_afternoon']][self.location_index],
                 f"c2r4_{field_index}"      : self.excelWorkshopDict[row['thurs_morning']][self.presenter_index],
                 f"c3r4_{field_index}"      : self.excelWorkshopDict[row['thurs_morning']][self.location_index],
                 f"c2r5_{field_index}"      : self.excelWorkshopDict[row['thurs_afternoon']][self.presenter_index],
                 f"c3r5_{field_index}"      : self.excelWorkshopDict[row['thurs_afternoon']][self.location_index],
                }
                )
            
            # if all four blocks on pdf filled out, reset field index and add new page
            if field_index >= 3:
                self._pdf_suffix_fields(pdfFilled.pages[page], page)
                pdfFilled.reset_translation(pdfTemplate)
                page += 1
                pdfFilled.append(pdfTemplate)

        # Save complete pdf to folder with provided template
        save_path = os.path.dirname(self.pdfTemplatePath)
        output_stream = open(save_path + "/_complete.pdf", "wb")
        pdfFilled.write(output_stream)

        return True
    
    def _pdf_suffix_fields(self, page, sfx):
        """Adds a provided suffix to all fields on a provided pdf page"""
        fields = page.get('/Annots')
        if fields:
            for field_ref in fields:
                field = field_ref.get_object()
                field_name = field.get('/T') if '/T' in field else None
                if field_name:
                    # Append page number to field name
                    new_field_name = f"{field_name}_Page{sfx}"
                    field.update({
                        PyPDF2.generic.NameObject("/T"): PyPDF2.generic.TextStringObject(new_field_name)
                    })
