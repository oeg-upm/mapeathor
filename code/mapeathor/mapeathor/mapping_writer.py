import os
import go_template
import json

import global_config
import utils


def writeValues(data, path):
    """
    Redirects the data to the specific functions to write the 'data' into the file 'path'
    """
    if not os.path.isdir(global_config.tmpDir):
        os.mkdir(global_config.tmpDir)

    writePrefix(data,path)
    for triplesmap in data['TriplesMap']:
        writeTriplesMap(triplesmap, path)
        writeSubject(data['TriplesMap'][triplesmap]['Subject'], path)
        writeSource(data['TriplesMap'][triplesmap]['Source'], path)
        writePredicateObjects(data['TriplesMap'][triplesmap]['Predicate_Object'], path)

    # Functions implemented only in RML
    if global_config.templatesDir[-5:-1] == '/rml':
        for function in data['Function']:
            writeFunctionMap(function, path)
            writeFunctionPOM(data['Function'][function]['Predicate_Object'], path)
            writeFunctionSource(data['Function'][function]['Source'], path)


def writePrefix(data, path):
    """
    Writes the prefixes temporal file from the template with the information in 'data' into the path 'path'
    """
    for prefix in data['Prefix']:
        f = open(path + 'Prefix.yml', 'a+')
        f_base = open(path + 'Base.yml', 'a+')

        if ':' in str(prefix['Prefix']):
            re.sub(':', '', str(prefix['Prefix']))
        elif prefix['Prefix'] == 'nan' or prefix['URI'] == 'nan':
            continue

        if prefix['Prefix'] == '@base':
            f_base.write('URI' + ': ' + str(prefix['URI']) + '\n')
            f_base.close()
            go_template.render_template(global_config.templatesDir + 'Base.tmpl',global_config.tmpDir + 'Base.yml', global_config.tmpDir + 'Base.txt')
            writeResult('', 'Base')

        else:
            f.write('Prefix' + ': ' + str(prefix['Prefix']) + '\n')
            f.write('URI' + ': ' + str(prefix['URI']) + '\n')
            f.close()
            go_template.render_template(global_config.templatesDir + 'Prefix.tmpl',global_config.tmpDir + 'Prefix.yml', global_config.tmpDir + 'Prefix.txt')
            writeResult('', 'Prefix')

        #for element in prefix:
        #    if element == 'Prefix' and ':' in str(prefix[element]):
        #        prefix[element] = re.sub(':', '', str(prefix[element]))
            #if element == 'Prefix' and str(prefix[element] == '@base'):
        #    f.write(str(element) + ': ' + str(prefix[element]) + '\n')


def writeTriplesMap(data, path):
    """
    Writes the triples map temporal file from the template with the information in 'data' into the path 'path'
    """
    f = open(path + 'TriplesMap.yml', 'a+')
    f.write('ID: ' + str(data) + '\n')
    f.close()
    go_template.render_template(global_config.templatesDir + 'TriplesMap.tmpl',global_config.tmpDir + 'TriplesMap.yml', global_config.tmpDir + 'TriplesMap.txt')
    writeResult(str(data), 'TriplesMap')


def writePredicateObjects(data, path):
    """
    Writes the Predicate_Object temporal file from the template with the information in 'data' into the path 'path'
    """
    for key in data:
        if(len(data[key]) > 0):
            for predicateObjects in data[key]:
                f = open(path + key + '.yml', 'a+')
                predicateObjects['Object'] = utils.replaceVars(str(predicateObjects['Object']), str(predicateObjects['ObjectType']), str(predicateObjects['TermType']))
                predicateObjects['Predicate'] = utils.replaceVars(str(predicateObjects['Predicate']), str(predicateObjects['PredicateType']), 'nan')
                if( 'InnerRef' in predicateObjects.keys() and 'OuterRef' in predicateObjects.keys()):
                    predicateObjects['InnerRef'] = utils.replaceVars(str(predicateObjects['InnerRef']), 'join_condition', 'nan')
                    predicateObjects['OuterRef'] = utils.replaceVars(str(predicateObjects['OuterRef']), 'join_condition', 'nan')

                for element in predicateObjects:
                    f.write(str(element) + ': \'' + predicateObjects[element] + '\'\n')
                f.close()
                go_template.render_template(global_config.templatesDir + key + '.tmpl',global_config.tmpDir + key + '.yml', global_config.tmpDir + key + '.txt')
                writeResult(data[key][0]['ID'], key)


def writeSource(data, path):
    """
    Writes the source temporal file from the template with the information in 'data' into the path 'path'
    """
    f = open(path + 'Source.yml', 'a+')
    config  = json.loads(open(global_config.templatesDir + 'config.json').read())
    if(data['Iterator'] != ''):
        data['Iterator'] = str(config['iterator']['before']) + str(data['Iterator']) + str(config['iterator']['after'])
    for element in data:
        f.write(str(element) + ': \'' + data[element] + '\'\n')
    f.close()

    if('Query' in data.keys()):
        go_template.render_template(global_config.templatesDir + 'SourceQuery.tmpl',global_config.tmpDir + 'Source.yml', global_config.tmpDir + 'Source.txt')
    else:
        go_template.render_template(global_config.templatesDir + 'Source.tmpl',global_config.tmpDir + 'Source.yml', global_config.tmpDir + 'Source.txt')

    writeResult(data['ID'], 'Source')


def writeSubjectTemp(data, path):
    """
    NOT IN USE
    Writes the subject temporal file from the template with the information in 'data' into the path 'path'
    """
    f = open(path + 'Subject.yml', 'a+')
    data['URI'] = utils.replaceVars(data['URI'], data['SubjectType'], 'nan')
    for element in data:
        if element != 'Class':
            f.write(element + ': ' + data[element] + '\n')
        else:
            for i in range(0, len(data[element])):
                f.write(element + str(i) + ': ' + data[element][i] + '\n')
    f.close()
    go_template.render_template(global_config.templatesDir + 'Subject.tmpl',global_config.tmpDir + 'Subject.yml', global_config.tmpDir + 'Subject.txt')
    writeResult(data['ID'], 'Subject')


def writeSubject(data, path):
    """
    Writes the subject temporal file from the template with the information in 'data' into the path 'path'
    """

    f = open(global_config.tmpDir + 'Subject.txt', 'a+')

    data['URI'] = utils.replaceVars(data['URI'], data['SubjectType'], 'nan')
    data['SubTermMap'] = utils.replaceTermMap(data['SubjectType'])

    if global_config.templatesDir[-8:-1] != 'yarrrml':
        f.write('rr:subjectMap [\n\ta rr:Subject;\n\trr:termType rr:IRI;\n\t' + data['SubTermMap'] + ' ' + data['URI'] + ';\n')
        for class_s in data['Class']:
            f.write('\trr:class ' + class_s + ';\n')
        f.write('];\n')
    else:
        f.write('s: ' + data['URI'] + '\npo:\n')
        for class_s in data['Class']:
            f.write('  - [a, ' + class_s + ']\n')

    f.close()
    writeResult(data['ID'], 'Subject')


def writeFunctionMap(data, path):
    """
    Writes the function map temporal file from the template with the information in 'data' into the path 'path'
    """
    f = open(path + 'FunctionMap.yml', 'a+')
    f.write('FunctionID: ' + str(data) + '\n')
    f.close()
    go_template.render_template(global_config.templatesDir + 'FunctionMap.tmpl', global_config.tmpDir + 'FunctionMap.yml', global_config.tmpDir + 'FunctionMap.txt')
    writeResult(str(data), 'FunctionMap')


def writeFunctionSource(data, path):
    """
    Writes the source of function temporal file from the template with the information in 'data' into the path 'path'
    """
    f = open(path + 'FunctionSource.yml', 'a+')
    config  = json.loads(open(global_config.templatesDir + 'config.json').read())
    if(data['Iterator'] != ''):
        data['Iterator'] = str(config['iterator']['before']) + str(data['Iterator']) + str(config['iterator']['after'])
    for element in data:
        f.write(str(element) + ': \'' + data[element] + '\'\n')
    f.close()
    go_template.render_template(global_config.templatesDir + 'FunctionSource.tmpl',global_config.tmpDir + 'FunctionSource.yml', global_config.tmpDir + 'FunctionSource.txt')
    writeResult(data['FunctionID'], 'FunctionSource')


def writeFunctionPOM(data, path):
    """
    Writes the Predicate_Object of function temporal file from the template with the information in 'data' into the path 'path'
    """
    for pom in data:
        f = open(path + 'FunctionPOM.yml', 'a+')
        if pom['Feature'] != 'fno:executes' and str(pom['Value'])[0] != '<':
            pom['Value'] = '\"' + pom['Value'] + '\"'
        for element in pom:
            f.write(str(element) + ': \'' + pom[element] + '\'\n')
        f.close()
        go_template.render_template(global_config.templatesDir + 'FunctionPOM.tmpl', global_config.tmpDir + 'FunctionPOM.yml', global_config.tmpDir + 'FunctionPOM.txt')
        writeResult(pom['FunctionID'], 'FunctionPOM')


def writeResult(ID, name):
    """
    Writes the temporal files assigning ID and names for the different parts of the mapping
    """
    delete = open(global_config.tmpDir + name + '.txt', 'r')
    final = open(global_config.resultDir + ID + '.' + name + '.' + 'result.txt', 'a+')
    final.writelines(delete.readlines())
    delete.close()
    final.close()

    try:
        os.remove(global_config.tmpDir + name + '.txt')
        os.remove(global_config.tmpDir + name + '.yml')
    except:
        pass


def writeFinalFile(path_, idTMList, idFList):
    """
    Gathers all the temporal files identified with 'idTMList' and 'idFList' and writes
    it in the final mapping file in 'path_'
    """
    data = json.loads(open(global_config.templatesDir  + 'structure.json').read())
    config = json.loads(open(global_config.templatesDir + 'config.json').read())

    if not path_.endswith(str(config['extension'])):
        path = path_ + '.' +  str(config['extension'])
    else:
        path = path_

    if os.path.isfile(path):
        os.remove(path)

    recursiveWrite(0,data['unique'], path, '')
    for id_ in idTMList:
        recursiveWrite(0, data['variable'], path, id_)
    for id_ in idFList:
        recursiveWrite(0, data['variable'], path, id_)
    return path


def recursiveWrite(tabs, parent, finalFile, id_):
    """
    Writes the temporal files in one recursively
    """
    for data in range(0, len(parent)):
        file_ = global_config.resultDir + id_ + '.' + parent[data]['file'] + '.result.txt'
        config = json.loads(open(global_config.templatesDir + 'config.json').read())
        exists = os.path.isfile(file_)
        if(exists):
            f = open(file_, 'r')
            final = open(finalFile, 'a+')
            if(str(parent[data]["before"]) != ""):
                final.write(parent[data]["before"] + '\n')
            for line in f.readlines():
                final.write(' ' * int(config['tab']['size']) * tabs + str(line))
            f.close()
            #os.remove(file_)
            final.close()
            if(len(parent[data]['childs']) > 0):
                recursiveWrite(parent[data]['tabs'], parent[data]['childs'], finalFile, id_)
            if(str(parent[data]["after"]) != ""):
                final = open(finalFile, 'a+')
                final.write(parent[data]["after"] + '\n')
                final.close()
