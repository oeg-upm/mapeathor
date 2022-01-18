import json
import re

from .global_config import *


def replaceVars(element, type_, termtype_):
    """
    Writes the objects 'element' correctly according to their type 'type_' and termtype 'termtype_', returns the
    corrected object
    """
    config = json.loads(open(global_config.templatesDir + 'config.json').read())
    # Add "" to the constant literal objects in YARRRML
    if(global_config.templatesDir[-8:-1] == 'yarrrml' and type_ == 'constant' and termtype_ == 'Literal'):
        result = str(config['variable'][type_]['before']) + element + str(config['variable'][type_]['after'])

    # Replace '{' and '}' in all but constant objects according to the config.json file of each language
    elif(type_ != 'constant' and str(config['variable'][type_]['before']) != '{' and str(config['variable'][type_]['after']) != '}'):
        result = element.replace("{", str(config['variable'][type_]['before'])).replace("}", config['variable'][type_]['after'])

    elif(((termtype_ != 'IRI' and type_ == 'constant') or type_ == 'template') and (global_config.templatesDir[-4:-1] == 'rml' or global_config.templatesDir[-6:-1] == 'r2rml')):
        result = "\"" + element + "\""

    else:
        result = element
    return result


def replaceTermMap(type_):
    config = json.loads(open(global_config.templatesDir + 'config.json').read())
    result = config['variable'][type_]['termMap']
    return result


def dataTypeIdentifier(element):
    """
    Identifies the datatype of the object 'element' and returns it
    """
    # Load the json with some xsd datatypes predefined

    try:
        data = open(global_config.dataTypesFile).read()
        dataTypes = json.loads()
    except:
        dataTypes = global_config.defaultDataTypes

    for key in dataTypes.keys():
        if element.lower().strip() in dataTypes[key]:
            return key

    print('WARNING: datatype not recognized (' + element + '), check XSD datatypes')
    return element


def termTypeIdentifier(element, dataType):
    """
    Identifies the termtype of the object 'element' based on itself and its datatype 'dataType' and returns it
    """
    if(len(str(element).split(":")) == 2 or "http" in str(element) or dataType == "anyURI"):
        return 'IRI', '~iri'
    else:
        return 'Literal', ''


def predicateTypeIdentifier(element):
    """
    Identifies the type of the predicate, distinguishing between constant, reference and template, and returns it
    """
    # For constant
    if(len(str(element).split(":")) == 2 and "{" not in str(element) and "}" not in str(element)):
        return 'constant'
    # For reference
    elif(str(element)[:1] == '{' and str(element)[-1:] == '}' and len(str(element).split(" "))  == 1):
        return 'reference'
    # For template
    elif(bool(re.search("{.+}.+", str(element))) or bool(re.search(".+{.+}", str(element)))):
        return 'template'
    # Constant when not recognized
    else:
        print("WARNING: type not identified for predicate '" + element + "', 'constant' assigned")
        return 'constant'


def cleanDir(path):
    """
    Cleans the results directory
    """
    dir = os.listdir(path)
    for f in dir:
        os.remove(path + f)
