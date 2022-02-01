import sys
import argparse

from . import global_config
from . import source
from . import mapping_generator
from ._version import __version__


def main():
    parser = argparse.ArgumentParser("mapeathor")
    parser.add_argument("-i", "--input_file", required=True, help="Input Excel file or Google SpreadSheet URL")
    parser.add_argument("-o", "--output_file", required=False, help="Name and path for output file", default="output")
    parser.add_argument("-l", "--language", required=True, help=("Supported Languages: " + str(global_config.supportedLanguages)))
    parser.add_argument("-v", "--version", help=("Version"), action="version", version="Mapeathor " + __version__)
    args = parser.parse_args()
    inputFile = ''

    # Local file
    if(source.checkFile(args.input_file)):
        inputFile = str(args.input_file)
    elif (args.input_file[0:8] != 'https://'):
        print('ERROR: File not found')
        sys.exit()

    # Google Spreadsheet file
    else:
        temp = source.gdriveToXMLX(args.input_file)
        if source.checkFile(temp):
            inputFile = temp
        else:
            print("ERROR: The downloaded document is not a spreadsheet")
            sys.exit()

    # Wrong language or not supported
    if(args.language.lower() not in global_config.supportedLanguages):
        print("ERROR: The selected Language is not supported by the moment.")
        print("Supporteds Languages: " + str(global_config.supportedLanguages))
        sys.exit()
    else: # Create mapping
        global_config.setMappingLanguage(args.language)
        print('Generating mapping file')
        outputFile = mapping_generator.generateMapping(inputFile, args.output_file)
        print("Your mapping file is in "+outputFile)

if __name__ == '__main__':
    main()
