 [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
 [![Generic badge](https://img.shields.io/badge/Status-Developing-yellow)](https://shields.io/)
# Mapeathor: One mapping to rule them all
#### Mapeathor translates your mapping rules specified in spreadsheets to any mapping language.  
###### Right now it is under development, the supported languages are **R2RML**, **RML** and **YARRRML**; and the Functions are not implemented.  

## How it works:  
**Mapeathor is a simple spreadsheet parser that identifies the basic structures of the mappings and create a new file in a specific mapping language.**  

![WorkFlow Image](./imgs/general_schema.png)

## Example:    
### First Step: Fill the xlsx template with your own information.  
The template has four mandatory sheets, *Prefixes, Source, Subject and PredicateObjectMap*, and it can include an additional optional sheet, *Functions*.
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
With python:
```BASH
# Clone the repository
$ git clone https://github.com/oeg-upm/Mapeathor

# Install the needed packages
$ cd Mapeathor/code/
$ pip3 install -r requirements.txt

# How to execute it
$ python3 main.py -i /Mapeathor/data/YOURFILE -l [RML | R2RML | YARRRML]

# Help Menu
$ python3 main.py -h 

# Example
$ python3 main.py -i /Mapeathor/data/default.xlsx -l yarrrml
```
With docker:
```BASH
# Clone the repository
$ git clone https://github.com/oeg-upm/Mapeathor

# Install the docker image with docker-compose
$ docker-compose up -d

# Copy the XLSX files to data repository
$ cp yourfiles ./data/

# Execute it
$ docker exec -it mapeathor ./run.sh /Mapeathor/data/YOURFILE [RML | R2RML | YARRRML]

# Results will appear in result folder
```
### Publications
Iglesias-Molina, A., Chaves-Fraga, D., Priyatna, F., & Corcho, O. (2019). Towards the Definition of a Language-Independent Mapping Template for Knowledge Graph Creation. *In Proceedings of the Third International Workshop on Capturing Scientific Knowledge co-located with the 10th International Conference on Knowledge Capture (K-CAP 2019)* (pp. 33-36). [Online version](https://sciknow.github.io/sciknow2019/papers/SciKnow_2019_paper_4.pdf)

### Authors and contact
- [Ana Iglesias-Molina](https://github.com/anaigmo) (ana.iglesiasm@upm.es)
- [Luis Pozo](https://github.com/w0xter) (luis.pozo@upm.es)
