# Lisbon Search Engine

This repository presents the final project of programming seminar 2023 in master of Geospatial technologies.

# Introduction

As part of the advance of geolocalization, the identification and display position of representative places in the development of communities have meaningful importance currently, this project seeks to display facilities in the city of Lisbon through the use of the "Lisbon Search Engine".
The development of this tool was possible due to the creation of the ETL  to connect with the database of the project and then transfer the data to the API according to the request done by the users using the front end of the tool.

The tool allows to the user select specific facilities located in the city of Lisbon and display their main information such as name, address, email, phone, website, among others----

https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/assets/Captura%20de%20pantalla%202023-02-25%20120535.jpg






If it is necessary, you can create a lisbon_engine environment in Anaconda to run this application, running the code below:

    conda create -n lisbon_engine

    conda activate lisbon_engine

After it, you can install all the packages necessary for this application running the code below:

    conda install --file requirements.txt --channel conda-forge
  

Considering database used in this project, in the folder "database" are located 2 files to run it into PGAdmin considering all the configurations necessary.



