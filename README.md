# Query Annotation Tool

## Motivation
One of the main challenges of Natural language processing (NLP) is converting unstructured data into a structured format. Structured data can then in turn be used to create knowledge graphs, train other machine learning models, etc. A widely used method for this is Named Entity Recognition (NER). It involves the identification and extraction of some particular entities of interest in the text. Many trained models available are able to extract names of people, places and organization with great accuracy. In our case we had a corpus of 600 research texts regarding the different types of coatings applied on Steel. Our task was to populate a domain model consisting of predefined entities like ingredients used, there quantities, the conditions under which the steel coating process took place, coating type, substrate, etc. We started by creating our own corpus to train a NER model that could identify some of the basic entities like occurrences of molecules, processes, conditions, actions and quantities. Using the trained model we implemented an Annotation tool cum Search tool where one could perform queries, that would perform search on the database and re- turn focused results. This enabled us to populate our domain model without training an NER for all entities

## How to run
look up `Query-Tool/user-guide.pdf`

## Annotation Tool
<img width="1276" alt="annotation tool ss" src="https://user-images.githubusercontent.com/34295094/140602986-ef0c1002-cafd-48d3-8c79-b0477e4e53f1.png">

## Search Tool
<img width="1275" alt="Query tool" src="https://user-images.githubusercontent.com/34295094/140602993-2c2eeabe-f87b-41c4-875b-a7b1d969a33c.png">

