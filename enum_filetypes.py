from enum import Enum

class FileType(Enum):
    PDF = [('PDF Files', '.pdf')]
    DATAFILE = [('CSV/Excel Files', '.csv .xls*')]
