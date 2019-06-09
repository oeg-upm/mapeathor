import re
import sys


def write_triples_map(sheets, tm_name, out_path):

    filename = out_path + tm_name + ".yml"
    mapping_file = open(filename, 'w')

    write_prefixes(sheets['Prefixes'], mapping_file)

    mapping_file.write("\nmappings:\n")

    for index, subject in sheets['SubjectMap'].iterrows():

        # Logical source
        mapping_file.write("  " + tm_name + str(index+1) + ":\n")
        write_logical_source(sheets['LogicalSource'], mapping_file)

        # Subject-Predicate-Object map
        write_spo_map(sheets['SubjectMap'], sheets['PredicateObjectMaps'], mapping_file, index, sheets)

        mapping_file.write("\n\n")


def write_prefixes(prefixes_df, mapping_file):

    mapping_file.write("prefixes:\n")
    mapping_file.write("  rr: http://www.w3.org/ns/r2rml#\n")
    mapping_file.write("  rml: http://semweb.mmlab.be/ns/rml#\n")
    mapping_file.write("  ql: http://semweb.mmlab.be/ns/ql#\n")

    for index, row in prefixes_df.iterrows():
        mapping_file.write('  ' + row['Prefix'] + ': ' + row['URI'] + "\n")


def write_logical_source(log_source_df, mapping_file):

    mapping_file.write("    sources:\n")

    for index, row in log_source_df.iterrows():

        if row['Logical source'] == "rml:referenceFormulation":
            mapping_file.write("      referenceFormulation: %s\n" % row['Value'][3:].lower())
        elif row['Logical source'] == "rml:source":
            mapping_file.write("      access: %s\n" % row['Value'])
        elif row['Logical source'] == "rml:iterator":
            mapping_file.write("      iterator: %s\n" % row['Value'])


def reformat_templates(field):
    field = re.sub('\{', '$(', field)
    field = re.sub('\}', ')', field)
    return field


def write_spo_map(sbj_map_df, pred_obj_maps_df, mapping_file, sbj_index, sheets):

    # Change template format from {} to $()
    sbj_map_df['URI'][sbj_index] = reformat_templates(sbj_map_df['URI'][sbj_index])

    # Write subject
    if sbj_map_df['URI'][sbj_index][0] != '<':
        mapping_file.write("    s: " + sbj_map_df['URI'][sbj_index] + "\n")
    else:
        mapping_file.write("    s:\n")
        mapping_file.write("      - ")
        write_function_map(sbj_map_df['URI'][sbj_index], sheets, mapping_file, "        ")

    # Write predicate-object
    mapping_file.write("    po:\n")
    mapping_file.write("      - [rdf:type, " + sbj_map_df['Class'][sbj_index] + "]\n")

    for index, row in pred_obj_maps_df.iterrows():

        if row['Subject'] < (sbj_index + 1):
            continue
        elif row['Subject'] > (sbj_index + 1):
            break

        # Change template format from {} to $()
        if row['Predicate type'] == 'rr:template':
            row['Predicate'] = reformat_templates(row['Predicate'])

        # Write object without references
        if type(row['Object']) == str:

            # Change template format from {} to $()
            if row['Object type'] == 'rr:template':
                row['Object'] = reformat_templates(row['Object'])
            elif row['Object type'] == 'rml:reference':
                row['Object'] = '$(' + row['Object'] + ')'

            if row['Predicate'][0] == '<' and row['Object'][0] != '<':
                mapping_file.write("      - p:\n")
                mapping_file.write("        - ")
                write_function_map(row['Predicate'], sheets, mapping_file, "          ")
                mapping_file.write("        o: %s\n" % row['Object'])

            elif row['Predicate'][0] != '<' and row['Object'][0] == '<':
                mapping_file.write("      - p: %s\n" % row['Predicate'])
                mapping_file.write("        o:\n")
                mapping_file.write("        - ")
                write_function_map(row['Object'], sheets, mapping_file, "          ")

            elif row['Predicate'][0] == '<' and row['Object'][0] == '<':
                mapping_file.write("      - p:\n")
                mapping_file.write("        - ")
                write_function_map(row['Predicate'], sheets, mapping_file, "          ")
                mapping_file.write("        o:\n")
                mapping_file.write("        - ")
                write_function_map(row['Object'], sheets, mapping_file, "          ")
            else:
                mapping_file.write("      - [%s, %s]\n" % (row['Predicate'], row['Object']))

        # Write object with references
        elif type(row['Reference']) == str:
            row['Join-child'] = reformat_templates(row['Join-child'])
            row['Join-parent'] = reformat_templates(row['Join-parent'])

            mapping_file.write("      - p: %s\n" % row['Predicate'])
            mapping_file.write("        o:\n")
            mapping_file.write("          - mapping: %s\n" % row['Reference'])
            mapping_file.write("            condition:\n")
            mapping_file.write("              function: equal\n")
            mapping_file.write("              parameters:\n")

            if row['Join-child'][0] == '<' and row['Join-parent'][0] != '<':
                mapping_file.write("                - parameter: str1\n")
                mapping_file.write("                  value:\n")
                mapping_file.write("                    ")
                write_function_map(row['Join-child'], sheets, mapping_file, "                  ")
                mapping_file.write("                - [str2, $(%s)]\n" % row['Join-parent'])
            elif row['Join-parent'][0] == '<' and row['Join-child'][0] != '<':
                mapping_file.write("                - [str1, $(%s)]\n" % row['Join-parent'])
                mapping_file.write("                - parameter: str2\n")
                mapping_file.write("                  value:\n")
                mapping_file.write("                    ")
                write_function_map(row['Join-parent'], sheets, mapping_file, "                  ")
            elif row['Join-parent'][0] == '<' and row['Join-child'][0] == '<':
                mapping_file.write("                - parameter: str1\n")
                mapping_file.write("                  value:\n")
                mapping_file.write("                    ")
                write_function_map(row['Join-child'], sheets, mapping_file, "                  ")
                mapping_file.write("                - parameter: str2\n")
                mapping_file.write("                  value:\n")
                mapping_file.write("                    ")
                write_function_map(row['Join-parent'], sheets, mapping_file, "                  ")
            else:
                mapping_file.write("                - [str1, $(%s)]\n" % row['Join-child'])
                mapping_file.write("                - [str2, $(%s)]\n" % row['Join-parent'])


def write_function_map(func_name, sheets, mapping_file, spaces):

    try:
        func_df = sheets[func_name]
    except KeyError:
        print("ERROR: The function sheet %s is not in the file." % func_name)
        sys.exit(1)

    func_dict = dict(zip(func_df['Predicate'], func_df['Object']))

    mapping_file.write("function: %s\n" % func_dict['fno:executes'])
    mapping_file.write(spaces + "parameters:\n")

    for index, row in func_df.iterrows():

        if row['Predicate'] == 'fno:executes':
            continue
        elif row['Object'][0] == '<':
            mapping_file.write(spaces + "  - parameter: %s \n" % row['Predicate'])
            mapping_file.write(spaces + "    value:\n")
            mapping_file.write(spaces + "      ")
            write_function_map(row['Object'], sheets, mapping_file, spaces+"      ")
        else:
            if row['Object type'] == 'rml:reference':
                mapping_file.write(spaces + "  - [%s, $(%s)]\n" % (row['Predicate'], row['Object']))
            elif row['Object type'] == 'rr:constant':
                mapping_file.write(spaces + "  - [%s, \"%s\"]\n" % (row['Predicate'], row['Object']))
