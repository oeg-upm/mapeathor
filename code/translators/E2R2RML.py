import sys


def write_triples_map(sheets, tm_name, out_path):

    filename = out_path + tm_name + ".r2rml.ttl"
    mapping_file = open(filename, 'w')

    # Prefixes
    write_prefixes(sheets['Prefixes'], mapping_file)

    for index, subject in sheets['SubjectMap'].iterrows():

        # Logical table
        write_logical_table(sheets['LogicalSource'], tm_name, mapping_file, index)

        # Subject map
        write_subject_map(sheets['SubjectMap'], mapping_file, index)

        # Predicate map
        write_predicate_object_maps(sheets['PredicateObjectMaps'], mapping_file, index)


def write_prefixes(prefixes_df, mapping_file):

    mapping_file.write("@prefix rr: <http://www.w3.org/ns/r2rml#> .\n")

    for index, row in prefixes_df.iterrows():
        mapping_file.write('@prefix ' + row['Prefix'] + ': <' + row['URI'] + "> .\n")


def write_logical_table(log_table_df, tm_name, mapping_file, index):

    mapping_file.write("\n<" + tm_name + str(index+1) + '>\n\n')
    mapping_file.write("\trr:logicalTable [\n")
    mapping_file.write("\t\t" + log_table_df['Logical source'][index] + " \"" + log_table_df['Value'][index] + "\"\n")
    mapping_file.write("\t];\n\n")


def write_subject_map(sbj_map_df, mapping_file, index):

    mapping_file.write("\trr:subjectMap [\n")
    mapping_file.write("\t\ta rr:Subject;\n")
    mapping_file.write("\t\trr:termType rr:IRI;\n")
    mapping_file.write("\t\trr:class " + sbj_map_df['Class'][index] + ";\n")
    mapping_file.write("\t\trr:template \"" + sbj_map_df['URI'][index] + "\";\n")
    mapping_file.write("\t];\n\n")


def write_predicate_object_maps(pred_obj_maps_df, mapping_file, sbj_index):

    for index, row in pred_obj_maps_df.iterrows():

        if row['Subject'] < (sbj_index + 1):
            continue
        elif row['Subject'] > (sbj_index + 1):
            break

        mapping_file.write("\trr:predicateObjectMap [\n")
        mapping_file.write("\t\trr:predicateMap\t[ rr:constant " + row['Predicate'] + " ];\n")

        if type(row['Object']) == str:
            mapping_file.write("\t\trr:objectMap\t[ rr:termType " + row['Term type'] + "; " + row['Object type'] +
                               " \"" + row['Object'] + "\"; ")
            if type(row['Data type']) == str:
                mapping_file.write("rr:datatype " + row['Data type'] + "; ];\n")
            else:
                mapping_file.write("];\n")
        elif type(row['Reference']) == str:
            mapping_file.write("\t\trr:objectMap\t[\n")
            mapping_file.write("\t\t\trr:parentTriplesMap <" + row['Reference'] + ">;\n")
            mapping_file.write("\t\t\trr:joinCondition [ rr:child \"" + row['Join-child'] + "\"; rr:parent \"" +
                               row['Join-parent'] + "\"; ];\n")
            mapping_file.write("\t\t];\n")

        mapping_file.write("\t];\n\n")

    mapping_file.write(".\n")
