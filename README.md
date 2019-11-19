 [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
 [![Generic badge](https://img.shields.io/badge/Status-Developing-yellow)](https://shields.io/)
# Mapeathor: One mapping to rule them all.
#### Mapeathor transalate your mappings from an abstrac language based in spreadsheets to any mapping language.  
###### Right now is under development, the only supported languages are **RML** **YARRRML** and **R2RML** and the Functions are not implemeted.  
## How it works:  
**Mapeathor it's a simple spreadSheet parser that identifies the basic structures of the mappings and create a new file in a specific mapping language.**  
![WorkFlow Image](./imgs/general_schema.png)    
## Example:    
### First Step: Fill the xlsx template with your own information.  
The template has four mandatory sheets, *Prefixes, LogicalSource, SubjectMap and PredicateObjectMap*, and it can include an additional optional sheet, *Functions*.
#### Prefixes:  
![Prefixes img](./imgs/sheet_prefix.png)  
  
 #### Source:  
![Source img](./imgs/sheet_source.png)  
  
 #### Subject:  
![Subject img](./imgs/sheet_subject.png)  
  
 #### PredicateObjectMaps:  
![PredicateObjectMaps img](./imgs/sheet_pom.png)  
  
 #### Functions:
![Function img](./imgs/sheet_function.png)

### Second Step: Choose the output language that you prefer. 
Here you can see the [Available Languages](./templates).

### Third Step: Execute these commands:
```BASH
$ git clone https://github.com/oeg-upm/Mapeathor
$ cd Mapeathor/code/
$ pip3 install -r dependencies.txt
$ python3 main.py -i /PATH/OF/YOUR/XLSX/FILE -l MappingLanguageNameChoosed
$ python3 main.py -h #Shows The Help Menu
#Example:
$ python3 main.py -i ../data/default.xlsx -l yarrrml
```
