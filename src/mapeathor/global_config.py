import tempfile
import pkgutil
import os


tmpDir = tempfile.TemporaryDirectory(prefix="mapeathor").name+"/"
baseTemplatesDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates') + '/'
dataTypesFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataTypes.json')
resultDir = tempfile.TemporaryDirectory(prefix="mapeathor").name+"/"
supportedLanguages = {'rml', 'rml2014', 'r2rml', 'yarrrml'}


def setMappingLanguage(lang):
    global templatesDir
    global language

    templatesDir = baseTemplatesDir + lang.lower() + "/"
    language = lang.lower()


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
   ],
   "BlankNode":[
      "blanknode",
      "blank node",
      "bn"
    ],
    "gYear":[
       "year",
       "gyear"
     ]
}
