import pandas
import sys
import argparse
import translators.E2RML as rml
import translators.E2YARRRML as yarrrml
import translators.E2R2RML as r2rml


def check_template(file):

    # Check that the excel file exists and is an excel file
    try:
        sheet_names = sorted(pandas.ExcelFile(file).sheet_names)
    except FileNotFoundError:
        print("ERROR: File doesn't exist.")
        sys.exit(1)
    except:
        print("ERROR: File is not in excel format.")
        sys.exit(1)

    # Check if the sheets in the excel file are correct
    mandatory_sheets = ['LogicalSource', 'PredicateObjectMaps', 'Prefixes', 'SubjectMap']
    if not set(mandatory_sheets).issubset(set(sheet_names)):
        print('ERROR: The sheets contained in the excel file are wrong.')
        print("The mandatory sheets are 'Prefixes', 'LogicalSource', 'SubjectMap' and 'PredicateObjectMap'.")
        sys.exit(1)
    else:
        sheets = {}
        for sheet in sheet_names:
            sheets[sheet] = pandas.read_excel(file, sheet_name=sheet)

    # Check if the columns in each sheet are correct
    if sorted(list(sheets['Prefixes'])) != ['Prefix', 'URI']:
        print('ERROR: The column names of the sheet \'Prefixes\' are wrong. Please check the docs or use the template.')
        sys.exit(1)
    elif sorted(list(sheets['LogicalSource'])) != ['Logical source', 'Value']:
        print('ERROR: The column names of the sheet \'LogicalSource\' are wrong. Please check the docs or use the template.')
        sys.exit(1)
    elif sorted(list(sheets['SubjectMap'])) != ['Class', 'URI']:
        print('ERROR: The column names of the sheet \'SubjectMap\' are wrong. Please check the docs or use the template.')
        sys.exit(1)
    elif sorted(list(sheets['PredicateObjectMaps'])) != ['Data type', 'Join-child', 'Join-parent', 'Object', 'Object type', 'Predicate', 'Predicate type', 'Reference', 'Subject', 'Term type']:
        print('ERROR: The column names of the sheet \'PredicateObjectMaps\' are wrong. Please check the docs or use the template.')
        sys.exit(1)

    return sheets


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", required=True, help="Input excel file")
    parser.add_argument("-o", "--output_path", required=True, help="Output path to create the output file")
    parser.add_argument("-n", "--name_triples_map", required=True, help="Name of the new triples map")
    parser.add_argument("-l", "--language", required=True, help="Mapping language to translate to, RML or YARRRML")

    args = parser.parse_args()

    # Check if the excel file is right for using and get the sheets contained as data frames
    sheets = check_template(args.input_file)

    # Translate template
    try:
        if args.language.lower() == 'rml':
            rml.write_triples_map(sheets, args.name_triples_map, args.output_path)
        elif args.language.lower() == 'yarrrml':
            yarrrml.write_triples_map(sheets, args.name_triples_map, args.output_path)
        elif args.language.lower() == 'r2rml':
            r2rml.write_triples_map(sheets, args.name_triples_map, args.output_path)
        else:
            print("ERROR: Language nor recognized. Possibilities are 'RML', 'R2RML' and 'YARRRML'.")
    except TypeError:
        print('ERROR: One or more cells are empty. Please make sure all the required fields are filled.')
        sys.exit(1)

if __name__ == '__main__':

    main()
