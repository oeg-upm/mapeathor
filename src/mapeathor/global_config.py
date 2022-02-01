import tempfile
import pkgutil
import os


tmpDir = tempfile.TemporaryDirectory(prefix="mapeathor").name+"/"
baseTemplatesDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates') + '/'
dataTypesFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataTypes.json')
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
