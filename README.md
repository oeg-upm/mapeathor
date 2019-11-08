# Mapeathor

Translator of mapping rules written in spreadsheets into R2RML, RML or YARRRML. 

## Guide

It is necessary to have Python 3.6.0 installed. Then, clone or download this repository and install the packages in requirements.txt:
```
pip install -r requirements.txt
```
In the code repository it's the file ready to run:

```
cd code/
python main_translator.py -i <input_file> -o <output_path> -n <triples_map_name> -l <mapping_language>
```
