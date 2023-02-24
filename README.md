# Lisbon Search Engine

This repository presents the final project of programming seminar 2023 in master of Geospatial technologies.

# Introduction

As part of the advance of geolocalization, the identification and display position of representative places in the development of communities have meaningful importance currently, this project seeks the display of facilities in the city of Lisbon through the use of "Lisbon Search Engine".
The development of this tool was possible due to the creation of an ETL  to connect with the database of the project and then transfer the data to the API according to the request done by the users  using the front-end of the tool.



If it is necessary, you can create a lisbon_engine environment in Anaconda to run this application, running the code below:

    conda create -n lisbon_engine

    conda activate lisbon_engine

After it, you can install all the packages necessary for this application running the code below:

    conda install --file requirements.txt --channel conda-forge
  

Considering database used in this project, in the folder "database" are located 2 files to run it into PGAdmin considering all the configurations necessary.



