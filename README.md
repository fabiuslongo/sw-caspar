# sw-caspar

This is the repository of the Python (3.7+) implementation of SW-CASPAR (Semantic Web-Cognitive Architecture System Planned and Reactive), which
is an alternative version of [CASPAR](https://github.com/fabiuslongo/pycaspar) able to make reasoning on the Semantic Web.

![Image 1](https://github.com/fabiuslongo/sw-caspar/blob/master/images/sw-caspar.JPG)

# Installation

---------------

This repository has been tested on Python 3.7.3 64bit on Windows 10, with the following packages versions:

* [Phidias](https://github.com/corradosantoro/phidias) (release 1.3.4.alpha) 
* [spaCy](https://spacy.io/) (ver. 2.2.4)
* [Natural Language Toolkit](https://www.nltk.org/) (ver. 3.5)
* [Owlready2](https://pypi.org/project/Owlready2/) (ver. 0.30)
* [pyttsx3 (Text-to-Speech)](https://pyttsx3.readthedocs.io/en/latest/) 

### Phidias

---------------

```sh
> git clone https://github.com/corradosantoro/phidias
> python setup.py install
> python -m pip install pyreadline
> python -m pip install parse
```

### spaCy

---------------

```sh
> python -m pip install spacy
> python -m spacy download en_core_web_lg
```


### Natural Language Toolkit

---------------

from prompt:
```sh
> python -m pip install nltk
```
from python console:
```sh
> import nltk
> nltk.download('wordnet')
```

### Owlready2 

---------------

from prompt:
```sh
> python -m pip install owlready2
```



### pyttsx3 (Text-to-Speech)

---------------

from prompt:
```sh
> python -m pip install pyttsx3
```



# Testing
This cognitive architecture is designed to implement more intelligent agents and also 
is an agent itself. Before starting the agent, Entities and Speech-To-Text Interfaces must be defined.

### Entities definition

---------------

Entities involved in reasoning must be defined in the Smart Environment Interface (smart_env_int.py).

### Speech-To-Text Interfaces

---------------

STT Interfaces (for both hotword and utterances) must be defined inside the Instances Sensors 
(sensors.py).
 

### Starting agent

---------------

First of all, you must create the ontology. In order to do that, you must follow three preliminar steps:

* Choose the owl file name, by setting the variable FILE_NAME (within AGENT) in the config.ini (test.owl for instance)
* Execute sw-caspar.py

```sh
Creating new test.owl file...

Please Re-Run SW-Caspar.

Process finished with exit code 0
```

* Re-execute sw-caspar

```sh
Loading existing test.owl file...

NLP engine initializing. Please wait...

	PHIDIAS Release 1.3.4.alpha (deepcopy-->clone,micropython,py3)
	Autonomous and Robotic Systems Laboratory
	Department of Mathematics and Informatics
	University of Catania, Italy (santoro@dmi.unict.it)


eShell: main > go()
eShell: main > Starting SW-Caspar...

Starting Hotword detection...

eShell: main > 
```

Now sw-caspar is ready.
Unless you delete the owl file or choose to create another ontology, the agent will try to load every time the file specified in confi.ini.


### IoT commands and routines

---------------

For this section the developer is referred to [CASPAR](https://github.com/fabiuslongo/pycaspar).



### Ontology Learning

---------------

Considering the following sentences:

* _Colonel West is American_
* _Cuba is a hostile nation_
* _missiles are weapons_
* _the Colonel West sells missiles to Cuba_
* _When an American sells weapons to a hostile nation, that American is a criminal_

SW-Caspar will model the ontology in order to infer the further natural language assertion:

* _Colonel West is a criminal_


```sh
eShell: main > +FEED("Colonel West is American")
eShell: main > +FEED("Cuba is a hostile nation")
eShell: main > +FEED("missiles are weapons")
eShell: main > +FEED("the Colonel West sells missiles to Cuba")
eShell: main > +FEED("When an American sells weapons to a hostile nation, that American is a criminal")
```

Here is all taxonomic relations (by opening the ontology file with Protege) after the such assertions:
 
![Image 2](https://github.com/fabiuslongo/sw-caspar/blob/master/images/west-taxo.JPG)


