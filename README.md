# MCDataVis
To learn how to use the code and understand the data in this project head over to the github pages site. These scripts pull and anazlye data pretaining to MightyCoders students from the MightyCoders site. Data was scrapped using seleiumn and visauls were generated with matplotlib.  
## Python Scripts for MightyCoders Data Vis
3 .py files in total:   
- StudentDataVis, Containts data anylais functions and the visualizations for students/ MightyCoder trends 
- StudentObjectSerializer, contains read and write json methods, and student class definition, used in StudentDataVis.py  
- WebScrapper, used to pull dates from the LMS originally not needed anymore as all the data is in the JSON files    
## JSON files related to project 
- students, dictionary key: "student name", value: student object containing all the stats used for data visualization  
- studentMCDataMaster, dictinoary containing all data both kirkland and bothell campuses, key: "student name", value: list of dates (lesson start dates) 
- studentMCdata, dictionary of Bothell students and lesson dates 
- studentMCdataKirkland, dictionary of Kirkland students and lesson dates  
