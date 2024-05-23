import pandas
import openpyxl
import PyPDF2


class MultipleErrors(Exception):
    def __init__(self, errors):
        self.errors = errors


class ExcelDataframe():
    """ Class which creates Dataframe from given file """

    def __init__(self)->None:

        self.dataFilePath = ""
        self.pdfTemplatePath = ""
        self.excelData = pandas.DataFrame()
        self.excelWorkshopDict = {}
        self.presenter_index = 0
        self.location_index = 0


    def set_dataFilePath(self, path: str):
        """sets file path field for data file"""

        if path == "":
            return
        if not (path.lower().endswith('xls') or 
                path.lower().endswith('xlsx') or 
                path.lower().endswith('xlsm')):
            raise MultipleErrors([ValueError("Incorrect data file type provided")])
        else:
            self.dataFilePath = path
            self.buildDataStructures()

    def set_pdfTemplatePath(self, path: str):
        """sets file path field for pdf template file"""

        if path == "":
            return
        if not path.lower().endswith('pdf'):
            raise ValueError("Incorrect pdf file type provided")
        else:
            self.pdfTemplatePath = path

    
    def buildDataStructures(self) -> None:
        """Build dataframe members using excel file provided"""

        errors = []

        # Build dataframes from excel worksheets
        try:
            self.excelData = pandas.read_excel(self.dataFilePath, "Registrations")
        except:
            try:
                self.excelData = pandas.read_excel(self.dataFilePath, "registrations")
            except ValueError as e:
                errors.append(e)
        
        try:
            excelWedData = pandas.read_excel(self.dataFilePath, "Wednesday Workshops")
        except:
            try:
                excelWedData = pandas.read_excel(self.dataFilePath, "Wednesday workshops")
            except:
                try:
                    excelWedData = pandas.read_excel(self.dataFilePath, "wednesday Workshops")
                except:
                    try:
                        excelWedData = pandas.read_excel(self.dataFilePath, "wednesday workshops")
                    except ValueError as e:
                        errors.append(e)
        
        try:
            excelThuData = pandas.read_excel(self.dataFilePath, "Thursday Workshops")
        except:
            try:
                excelThuData = pandas.read_excel(self.dataFilePath, "Thursday workshops")
            except:
                try:
                    excelThuData = pandas.read_excel(self.dataFilePath, "thursday Workshops")
                except:
                    try:
                        excelThuData = pandas.read_excel(self.dataFilePath, "thursday workshops")
                    except ValueError as e:
                        errors.append(e)

        if errors:
            raise MultipleErrors(errors)
        

        # Preprocess column names to lowercase
        self.excelData.columns = map(str.lower, self.excelData.columns)
        excelWedData.columns = map(str.lower, excelWedData.columns)
        excelThuData.columns = map(str.lower, excelThuData.columns)
        self.excelData['pronouns'] = self.excelData['pronouns'].fillna('')

        
        #Verify data existence in workshop dataframes
        if not "workshopid" in excelWedData.columns:
            errors.append(ValueError("Column \'workshopID\' not found in the \'Wednesday workshops\' worksheet"))
        if not "presenter" in excelWedData.columns:
            errors.append(ValueError("Column \'presenter\' not found in the \'Wednesday workshops\' worksheet"))
        if not "location" in excelWedData.columns:
            errors.append(ValueError("Column \'location\' not found in the \'Wednesday workshops\' worksheet"))
        if not "workshopid" in excelThuData.columns:
            errors.append(ValueError("Column \'workshopID\' not found in the \'Thursday workshops\' worksheet"))
        if not "presenter" in excelThuData.columns:
            errors.append(ValueError("Column \'presenter\' not found in the \'Thursday workshops\' worksheet"))
        if not "location" in excelThuData.columns:
            errors.append(ValueError("Column \'location\' not found in the \'Thursday workshops\' worksheet"))

        if errors:
            raise MultipleErrors(errors)


        #Concat workshop dataframes, index columns, and create dictionary
        excelWorkshopData = pandas.concat([excelWedData, excelThuData])
        excelWorkshopData['presenter'] = excelWorkshopData['presenter'].fillna('None')
        excelWorkshopData['location'] = excelWorkshopData['location'].fillna('None')
        self.presenter_index = excelWorkshopData.columns.get_loc("presenter") - 1
        self.location_index = excelWorkshopData.columns.get_loc("location") - 1
        self.excelWorkshopDict = excelWorkshopData.set_index('workshopid').T.to_dict('list')



    
    def buildBadges(self) -> bool:
        """Uses pdf template provided, data sets provided, and selected columns to construct
        the complete pdf document containing all badges for values in the data set. PDF doc
        has 4 values per badges per page and will be saved to the same location as the template
        document appended with '_Complete'."""


        # Create pdf objects (template and new blank doc)
        pdfTemplate = PyPDF2.PdfReader(self.pdfTemplatePath)
        pdfFilled = PyPDF2.PdfWriter()


        # Set initial variables for looping
        page = 0
        count_per_page = 3
        pdfFilled.append(pdfTemplate)

        #Loop through all items in dataframe
        for index, row in self.excelData.iterrows():
            
            # set value for field in pdf (0 - 3) - should reset every 4th value and use page
            field_index = index - (page * count_per_page)

            if pandas.isnull(row['wed_morning']): row['wed_morning'] = "WK0"
            if pandas.isnull(row['wed_afternoon']): row['wed_afternoon'] = "WK0"
            if pandas.isnull(row['thurs_morning']): row['thurs_morning'] = "WK0"
            if pandas.isnull(row['thurs_afternoon']): row['thurs_afternoon'] = "WK0"


            val_name = row['badge_name']
            val_pronoun = row['pronouns']
            val_institution = row['institution']
            val_wedmornpres = self.excelWorkshopDict[row['wed_morning']][self.presenter_index]
            val_wedmornroom = self.excelWorkshopDict[row['wed_morning']][self.location_index]
            val_wedaftrpres = self.excelWorkshopDict[row['wed_afternoon']][self.presenter_index]
            val_wedaftrroom = self.excelWorkshopDict[row['wed_afternoon']][self.location_index]
            val_thumornpres = self.excelWorkshopDict[row['thurs_morning']][self.presenter_index]
            val_thumornroom = self.excelWorkshopDict[row['thurs_morning']][self.location_index]
            val_thuaftrpres = self.excelWorkshopDict[row['thurs_afternoon']][self.presenter_index]
            val_thuaftrroom = self.excelWorkshopDict[row['thurs_afternoon']][self.location_index]


            # Set pdf fields to values from dataframe (references dict for workshop details)
            pdfFilled.update_page_form_field_values(
                pdfFilled.pages[page],
                {f"name_{field_index}"      : val_name,
                 f"pronoun_{field_index}"   : val_pronoun,
                 f"institution_{field_index}"   : val_institution,
                 f"W_AM_Pres_{field_index}"      : val_wedmornpres,
                 f"W_AM_Room_{field_index}"      : val_wedmornroom,
                 f"W_PM_Pres_{field_index}"      : val_wedaftrpres,
                 f"W_PM_Room_{field_index}"      : val_wedaftrroom,
                 f"T_AM_Pres_{field_index}"      : val_thumornpres,
                 f"T_AM_Room_{field_index}"      : val_thumornroom,
                 f"T_PM_Pres_{field_index}"      : val_thuaftrpres,
                 f"T_PM_Room_{field_index}"      : val_thuaftrroom,
                }
                )
            
            # if all four blocks on pdf filled out, reset field index and add new page
            if field_index >= count_per_page - 1:
                self._pdf_suffix_fields(pdfFilled.pages[page], page)
                pdfFilled.reset_translation(pdfTemplate)
                page += 1
                pdfFilled.append(pdfTemplate)


        # Save complete pdf to folder with provided template
        # save_path = os.path.dirname(self.pdfTemplatePath)
        # output_stream = open(save_path + "/_complete.pdf", "wb")
        save_path = self.pdfTemplatePath[:-4]
        output_stream = open(save_path + "_complete.pdf", "wb")
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