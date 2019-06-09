import sys


def write_triples_map(sheets, tm_name, out_path):

    filename = out_path + tm_name + ".rml.ttl"
    mapping_file = open(filename, 'w')

    # Prefixes
    write_prefixes(sheets['Prefixes'], mapping_file)

    for index, subject in sheets['SubjectMap'].iterrows():

        # Logical source
        mapping_file.write("\n<" + tm_name + str(index+1) + ">\n\n")
        write_logical_source(sheets['LogicalSource'], mapping_file)

        # Subject map
        write_subject_map(sheets['SubjectMap'], mapping_file, index)

        # Predicate map
        write_predicate_object_maps(sheets['PredicateObjectMaps'], mapping_file, index, sheets)

        mapping_file.write(".\n\n")


def write_prefixes(prefixes_df, mapping_file):

    mapping_file.write("@prefix rr: <http://www.w3.org/ns/r2rml#> .\n")
    mapping_file.write("@prefix rml: <http://semweb.mmlab.be/ns/rml#> .\n")
    mapping_file.write("@prefix ql: <http://semweb.mmlab.be/ns/ql#> .\n")
    mapping_file.write("@prefix fnml: <http://semweb.mmlab.be/ns/fnml#> .\n")

    for index, row in prefixes_df.iterrows():
        mapping_file.write('@prefix ' + row['Prefix'] + ': <' + row['URI'] + "> .\n")


def write_logical_source(log_source_df, mapping_file):

    mapping_file.write("\trml:logicalSource [\n")

    for index, row in log_source_df.iterrows():

        if row['Logical source'] == "rml:referenceFormulation":
            mapping_file.write("\t\t" + row['Logical source'] + " " + row['Value'] + " ;\n")
        else:
            mapping_file.write("\t\t" + row['Logical source'] + " \"" + row['Value'] + "\" ;\n")

    mapping_file.write("\t];\n\n")


def write_subject_map(sbj_map_df, mapping_file, sbj_index):

    mapping_file.write("\trr:subjectMap [\n")
    mapping_file.write("\t\ta rr:Subject;\n")
    mapping_file.write("\t\trr:termType rr:IRI;\n")
    mapping_file.write("\t\trr:class " + sbj_map_df['Class'][sbj_index] + ";\n")
    mapping_file.write("\t\trr:template \"" + sbj_map_df['URI'][sbj_index] + "\";\n")
    mapping_file.write("\t];\n\n")


def write_predicate_object_maps(pred_obj_maps_df, mapping_file, sbj_index, sheets):

    for index, row in pred_obj_maps_df.iterrows():

        if row['Subject'] < (sbj_index + 1):
            continue
        elif row['Subject'] > (sbj_index + 1):
            break

        # Write predicate
        mapping_file.write("\trr:predicateObjectMap [\n")

        if row['Predicate'][0] == '<':
            mapping_file.write("\t\trr:predicateMap\t[\n")
            write_function_map(row['Predicate'], sheets, mapping_file, "\t\t\t")
            mapping_file.write("\t\t];\n")
        elif row['Predicate type'] == 'rr:constant':
            mapping_file.write("\t\trr:predicateMap\t[ rr:constant " + row['Predicate'] + " ];\n")
        elif row['Predicate type'] == 'rr:template':
            mapping_file.write("\t\trr:predicateMap\t[ rr:template \"" + row['Predicate'] + "\" ];\n")

        # Write object without references
        if type(row['Object']) == str:

            # Write function map
            if row['Object'][0] == '<':
                mapping_file.write("\t\trr:objectMap\t[\n")
                write_function_map(row['Object'], sheets, mapping_file, "\t\t\t")
                mapping_file.write("\t\t];\n")

            # Normal object
            else:
                # TermType
                mapping_file.write("\t\trr:objectMap\t[ rr:termType " + row['Term type'] + "; ")
                # Object
                mapping_file.write(row['Object type'] + " \"" + row['Object'] + "\"; ")
                # Data type if it's defined
                if type(row['Data type']) == str:
                    mapping_file.write("rr:datatype " + row['Data type'] + "; ];\n")
                else:
                    mapping_file.write("];\n")

        # Write object with references
        elif type(row['Reference']) == str:
            mapping_file.write("\t\trr:objectMap\t[\n")
            mapping_file.write("\t\t\trr:parentTriplesMap <" + row['Reference'] + ">;\n")
            mapping_file.write("\t\t\trr:joinCondition [ rr:child \"" + row['Join-child'] + "\"; rr:parent \"" +
                               row['Join-parent'] + "\"; ];\n")
            mapping_file.write("\t\t];\n")

        mapping_file.write("\t];\n\n")


def write_function_map(func_name, sheets, mapping_file, tabs):

    try:
        func_df = sheets[func_name]
    except KeyError:
        print("ERROR: The function sheet %s is not in the file." % func_name)
        sys.exit(1)

    mapping_file.write(tabs + "fnml:functionValue [\n")

    for index, row in func_df.iterrows():
        mapping_file.write(tabs + "\trr:predicateObjectMap [\n")
        mapping_file.write(tabs + "\t\trr:predicateMap " + row['Predicate'] + " ;\n")

        if row['Object'][0] == '<':
            mapping_file.write(tabs + "\t\trr:objectMap\t[\n")
            write_function_map(row['Object'], sheets, mapping_file, tabs=(tabs + "\t\t\t"))
            mapping_file.write(tabs + "\t\t];\n")
        elif row['Predicate'] == 'fno:executes':
            mapping_file.write(tabs + "\t\trr:objectMap [ " + row['Object type'] + " " + row['Object'] + " ];\n")
        else:
            mapping_file.write(tabs + "\t\trr:objectMap [ " + row['Object type'] + " \"" + row['Object'] + "\" ];\n")

        mapping_file.write(tabs + "\t];\n")

    mapping_file.write(tabs + "];\n")
