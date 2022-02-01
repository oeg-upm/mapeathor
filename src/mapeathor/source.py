import pandas
import tempfile
import re
import sys
import requests


def checkFile(path):
    """
    Checks if the input 'path' is an excel file an can be correctly read, returns a boolean
    """
    try:
        data = pandas.ExcelFile(path, engine='openpyxl')
        return True
    except:
        return False


def gdriveToXMLX(url):
    temp = tempfile.NamedTemporaryFile(prefix="mapeathor-gdrive", delete=False, suffix=".xlsx")

    m = re.search(r'(?:file|spreadsheets)\/d\/(.*)\/', url)

    if not m:
        raise Exception("Malformed Google Spreadsheets URL")
        sys.exit()

    docid = m.groups()[0]

    url = 'https://docs.google.com/spreadsheets/d/'+docid+'/export?exportFormat=xlsx'

    r = requests.get(url)
    temp.write(r.content)
    return temp.name
