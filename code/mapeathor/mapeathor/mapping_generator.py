import pandas
import sys
import os
import json
import re
import copy

from .global_config import *
from .mapping_writer import *
from .utils import *

def generateJson(path):
    """
    The input excel file 'path' is translated into JSON format, returns the json
    """
    data = pandas.ExcelFile(path, engine='openpyxl')
    json = {}
    for sheet_ in data.sheet_names:
        sheet = str(sheet_)
        json[sheet] = {}
        json[sheet] = generateJsonCols(data.parse(sheet))
    return json


def generateJsonCols(data):
    """
    Arranges correctly the input pandas dataframe into a json, which is returned as output
    """
    rng = len(data[data.columns[0]])
    result = []
    for row in range(0, rng):
        element = {}
        for col_ in data.columns:
            col = str(col_)
            element[col] = str(data[col][row])
        result.append(element)
    return result


def organizeJson(data):
    """
    Rearranges the data in JSON format into the desired structure, returns the resulting json
    """
    json = {}
    json['Prefix'] = data['Prefix']
    json['TriplesMap'] = {}
    formated_subjects = reFormatSubject(data['Subject'])
    for subject in formated_subjects:
        json['TriplesMap'][subject['ID']] = findChilds(data, subject['ID'])
        json['TriplesMap'][subject['ID']]['Subject'] = subject
        json['TriplesMap'][subject['ID']]['Subject']['SubjectType'] = utils.predicateTypeIdentifier(subject['URI'])
        json['TriplesMap'][subject['ID']]['Source'] = reFormatSource(json['TriplesMap'][subject['ID']]['Source'])
        json['TriplesMap'][subject['ID']]['Predicate_Object']  =  reFormatPredicateObject(json['TriplesMap'][subject['ID']]['Predicate_Object'])
    json['Function'] = reFormatFunction(data['Function'], json)
    return json


def reFormatSubject(data):
    """
    Reorganize subjects in case there is more than one class per ID
    """
    id_class = {}
    for element in data:
        if element['ID'] == 'nan':
            continue
        elif element['ID'] in id_class:
            id_class[element['ID']].append(element['Class'])
        else:
            id_class[element['ID']] = [element['Class']]

    subjects = []
    for element in data:
        if element['ID'] in id_class:
            element['Class'] = id_class[element['ID']]
            del id_class[element['ID']]
            subjects.append(element)

    return(subjects)


def findChilds(data, ID):
    """
    Finds the Predicate_Object and Source in 'data' of the given 'ID' and returns it
    """
    result = {}
    keys = sorted(data.keys())
    keys.remove('Subject')
    keys.remove('Prefix')
    keys.remove('Function')

    for key in keys:
        result[key] =  []
        for element in data[key]:
            if(element['ID'] == ID):
                result[key].append(element)
    return result


def reFormatFunction(data_function, data):
    """
    Rearranges the data of functions 'data_function' into the desired structure and adds the source of each function
    with 'data'. The rearranged json is returned.
    """
    # Empty sheet
    if data_function == []:
        return({})
    elif data_function[0]['Feature'] == 'nan' and data_function[0]['Value'] == 'nan':
        return({})

    result = {}
    for element in data_function:
        # Blank rows
        if element['FunctionID'] == 'nan':
            continue

        element['FunctionID'] = str(element['FunctionID'])[1:-1]
        if element['FunctionID'] not in result.keys():
            result[element['FunctionID']] = {'Predicate_Object':[], 'Source':[]}
            FID = element['FunctionID']

        if element['FunctionID'] == FID:
            if("{" not in str(element['Value']) and "}" not in str(element['Value']) and '<' != str(element['Value'])[0]):
                element['ValueType'] = 'rr:constant'
            elif(str(element['Value'])[:1] == '{' and str(element['Value'])[-1:] == '}'):
                element['Value'] = str(element['Value'])[1:-1]
                element['ValueType'] = 'rml:reference'
            elif(str(element['Value'])[:1] == '<' and str(element['Value'])[-1:] == '>'):
                element['Value'] = '<#' + str(element['Value'])[1:]
                element['ValueType'] = ''
            else:
                print('WARNING: Wrong element in Function', FID)
                element['ValueType'] = 'rr:constant'
            result[element['FunctionID']]['Predicate_Object'].append(element)

    for fun in result:
        result[fun]['Source'] = find_source(fun, data, result)
        result[fun]['Source']['FunctionID'] = fun
        #print(result['Fun1']['Source'])
    return(result)


def find_source(function_key, data, functions):
    """
    Finds the source of the 'function_key' in 'data' or in 'functions', and returns it
    """
    for tm in data['TriplesMap']:
        if len(data['TriplesMap'][tm]['Predicate_Object']['Function']) != 0:
            for fun in data['TriplesMap'][tm]['Predicate_Object']['Function']:
                if fun['Object'] == function_key:
                    #data['TriplesMap'][tm]['Source']['FunctionID'] = function_key
                    #print(data['TriplesMap'][tm]['Source'])
                    return(data['TriplesMap'][tm]['Source'])
    for fun in functions:
        if len(functions[fun]['Source']) != 0:
            for element in functions[fun]['Predicate_Object']:
                if element['Value'][2:-1] == function_key:
                    functions[function_key]['Source'] = functions[fun]['Source'].copy()
                    #functions[function_key]['Source']['FunctionID'] = function_key
                    return(functions[function_key]['Source'])


def reFormatPredicateObject(data):
    """
    Rearranges the json contained in 'data' for the Triple Object Maps, and returns it
    """
    result = {'Join':[], 'Function':[], 'POM':[]}
    nullValues =  {'', 'NaN', ' ', 'nan', 'NAN'}
    for element in data:
        element['PredicateType'] = utils.predicateTypeIdentifier(element['Predicate'])
        element['PredTermMap'] = utils.replaceTermMap(element['PredicateType'])
        element['DataType'] = utils.dataTypeIdentifier(element['DataType'])
        element['TermType'], element['isIRI'] = utils.termTypeIdentifier(element['Object'], element['DataType'])

        # Populate Join key
        if(str(element['Object'])in nullValues and str(element['InnerRef']) not in nullValues and str(element['OuterRef']) not in nullValues):
            element['ObjectType'] = 'reference'
            result['Join'].append(element)
        # Populate Function key
        elif(str(element['Object'])[:1] == '<' and str(element['Object'])[-1:] == '>'):
            element['ObjectType'] = 'reference'
            element['Object'] = str(element['Object'])[1:-1]
            result['Function'].append(element)
        # Populate Constant key
        elif("{" not in str(element['Object']) and "}" not in str(element['Object'])):
            element['ObjectType'] = 'constant'
            element['ObjTermMap'] = utils.replaceTermMap(element['ObjectType'])
            result['POM'].append(element)
        # Populate Template key
        elif(bool(re.search("{.+}.+", str(element['Object']))) or bool(re.search(".+{.+}", str(element['Object'])))):
            element['ObjectType'] = 'template'
            element['ObjTermMap'] = utils.replaceTermMap(element['ObjectType'])
            result['POM'].append(element)
        # Populate Reference key when none of the conditions above are fulfilled
        else:
            element['ObjectType'] = 'reference'
            element['ObjTermMap'] = utils.replaceTermMap(element['ObjectType'])
            result['POM'].append(element)
    return result


def reFormatSource(data):
    """
    Rearranges the format of the 'Source' sheet in 'data' and returns it
    """
    result = {}
    for element in data:
        if(element['Feature'].lower() == 'source'):
            result['Source'] = str(element['Value'])
        elif(element['Feature'].lower() == 'format'):
            result['Format'] = str(element['Value'])
            if result['Format'].lower() == 'json':
                result['Format'] = 'JSONPath'
            elif result['Format'].lower() == 'xml':
                result['Format'] = 'XPath'
            elif result['Format'].lower() == 'xquery':
                result['Format'] = 'XQuery'
            elif result['Format'].lower() == 'csv':
                result['Format'] = 'CSV'

            if global_config.templatesDir[-8:-1] == 'yarrrml':
                result['Format'] = str(result['Format']).lower()

        elif(element['Feature'].lower() == 'iterator'):
            result['Iterator'] = str(element['Value'])
        elif(element['Feature'].lower() == 'table'):
            result['Table'] = str(element['Value'])
        elif(element['Feature'].lower() == 'query'):
            result['Query'] = str(element['Value'])
        elif(element['Feature'].lower() == 'sqlversion'):
            result['SQLVersion'] = str(element['Value'])
        else:
            print("ERROR: " + element + " feature not recognized. The recognized values for the \
                column 'Feature' in the sheet 'Source' are 'source', 'format', 'iterator', \
                'table', 'query' and 'SQLVersion")
            sys.exit()

    if('Iterator' not in result.keys()):
        result['Iterator'] = ''
    if('SQLVersion' not in result.keys()):
        result['SQLVersion'] = 'SQL2008'
    if('Source' not in result.keys() and 'Table' in result.keys()):
        result['Source'] = result['Table']
        if ('Format' not in result.keys()):
            result['Format'] = result['SQLVersion']


    result['ID'] = data[0]['ID']
    return result


def generateMapping(inputFile, outputFile=None):
    """
    General function with the flow of the script to generate and organize the JSON file with the data from
    'inputFile', and write it in the mapping file
    """
    if os.path.isdir(global_config.resultDir):
        utils.cleanDir(global_config.resultDir)
    else:
        os.mkdir(global_config.resultDir)

    if outputFile is None:
        outputFile = global_config.resultDir + re.findall(r'\/?([\w\-\_\[\]\(\)]+)\.',inputFile)[0]  ## wider option \/?([^\.\/]+)\.

    ## Without try/except
    #json = generateJson(inputFile)
    #json = organizeJson(json)

    try:
        json = generateJson(inputFile)
        #print("First JSON: ")
        #print(str(json).replace('\'', '\"'))
        json = organizeJson(json)
        #print("Second JSON: ")
        #print(str(json).replace('\'', '\"'))
        # sys.exit()
    except KeyError:
        print("ERROR: The spreadsheet template is not correct. Check the sheet and column names are correct.")
        sys.exit()

    mapping_writer.writeValues(json,global_config.tmpDir)

    outputFile = mapping_writer.writeFinalFile(outputFile, json['TriplesMap'].keys(), json['Function'].keys())
    return outputFile
