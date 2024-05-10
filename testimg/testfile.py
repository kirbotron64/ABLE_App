import pandas

def test():
    dfValues = {'col1': ['A'    , 'B'     , 'C'     ],
                'col2': [11     , 22      , 33      ],
                'col3': ['apple', 'banana', 'cherry']}
    dfMock = pandas.DataFrame(dfValues)
    for index, ind in dfMock.iterrows():
        print(ind['col2'])


test()