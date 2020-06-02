 [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
 [![Generic badge](https://img.shields.io/badge/Status-Developing-yellow)](https://shields.io/)
 [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/oeg-upm/Mapeathor/blob/master/LICENSE)
 [![version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)



# Mapeathor: One mapping to rule them all
#### Mapeathor translates your mapping rules specified in spreadsheets to any mapping language.  
###### Right now it is under development, the supported languages are **R2RML**, **RML** and **YARRRML**; the Functions are being implemented.  

## How it works:  
**Mapeathor is a simple spreadsheet parser that identifies the basic structures of the mappings and create a new file in a specific mapping language.**  

<p align="center"> 
 <img src="./imgs/general_schema.png" alt="workflow" width="600"/> 
</p>

## Example:    
### First Step: Fill the xlsx template with your own information.  
The template has four mandatory sheets, *Prefixes, Source, Subject and PredicateObjectMap*, and it can include an additional optional sheet, *Functions*.
#### Prefixes:   
<p align="center"> 
 <img src="./imgs/sheet_prefix.png" alt="prefixes" width="300"/> 
</p>

#### Source:  
<p align="center"> 
 <img src="./imgs/sheet_source.png" alt="source" width="370"/> 
</p>
 
#### Subject:    
<p align="center"> 
 <img src="./imgs/sheet_subject.png" alt="subject" width="460"/> 
</p>

#### PredicateObjectMaps:    
<p align="center"> 
 <img src="./imgs/sheet_pom.png" alt="pom" width="800"/> 
</p>

#### Functions:
![Function img](./imgs/sheet_function.png)
<p align="center"> 
 <img src="./imgs/sheet_function.png" alt="function" width="400"/> 
</p>

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
