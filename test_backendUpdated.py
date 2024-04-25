import unittest
from backendUpdated import ExcelDataframe
import pandas

class TestBackendMethods(unittest.TestCase):

    dfValues = {'col1': ['A'    , 'B'     , 'C'     ],
                'col2': [11     , 22      , 33      ],
                'col3': ['apple', 'banana', 'cherry']}
    dfMock = pandas.DataFrame(dfValues)
    
    def testInitialization(self):
        #class in instantiated
        self.assertRaises(something, ExcelDataframe.buildDataFrames)
        EDF = ExcelDataframe('teststring')
        #string not provided
        #file is not an excel/csv file
        #file does not have 'registrations' tab
        #file does not have 'Wednesday workshops' tab
        #file does not have 'Thursday workshops' tab


        #self.assertIsInstance()
        pass

    def testBuildDataFrames(self):
        self.assertIs(ExcelDataframe.buildDataFrames, pandas.DataFrame)

    
