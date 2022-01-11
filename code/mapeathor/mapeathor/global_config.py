import tempfile
import pkgutil


tmpDir = tempfile.TemporaryDirectory(prefix="mapeathor").name+"/"
baseTemplatesDir = pkgutil.get_loader("mapeathor").get_filename().replace("__init__.py", "")+"templates/"
#baseTemplatesDir = '/home/aiglesias/Mapeathor/code/templates/'
dataTypesFile = pkgutil.get_loader("mapeathor").get_filename().replace("__init__.py", "")+"dataTypes.json"
resultDir = tempfile.TemporaryDirectory(prefix="mapeathor").name+"/"
supportedLanguages = {'rml', 'r2rml', 'yarrrml'}


def setMappingLanguage(language):
    global templatesDir
    templatesDir = baseTemplatesDir + language.lower() + "/"


defaultDataTypes = {

   "string":[
      "string",
      "nan",
      " ",
      ""
   ],
   "decimal":[
      "decimal"
   ],
   "float":[
      "float"
   ],
   "double":[
      "double"
   ],
   "integer":[
      "integer",
      "int",
      "number"
   ],
   "boolean":[
      "boolean",
      "bool"
   ],
   "date":[
      "date",
   ],
   "time":[
      "time"
   ],
   "dateTime":[
      "datetime"
   ],
   "anyURI":[
      "anyuri",
      "iri",
      "uri",
      "url"
   ]
}
