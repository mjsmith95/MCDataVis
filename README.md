# MCDataVis
To learn how to use the code and understand the data in this project head over to the [github pages site](https://mjsmith95.github.io/MCDataVis/). These scripts pull and anazlye data pretaining to MightyCoders students from the MightyCoders site. Data was scrapped using seleiumn and visauls were generated with matplotlib.  
## Python Scripts for MightyCoders Data Vis
5 Python files in total:   
- `StudentDataVis.py`, Containts data anylais functions and the visualizations for students/ MightyCoder trends 
- `StudentObjectSerializer.py`, contains read and write json methods, and student class definition, used in StudentDataVis.py  
- WebScrapper, used to pull dates from the LMS originally not needed anymore as all the data is in the JSON files  
- `SOSExample.py`, an example to demostrate the functionality of `StudentObjectSerializer.py` 
- `DataVisExample.py`, an example to demostrate the functionality of `StudentDataVis.py` 
## JSON files related to project 
- `students.json`, dictionary key: "student name", value: student object containing all the stats used for data visualization  
- `studentMCDataMaster.json`, dictinoary containing all data both kirkland and bothell campuses, key: "student name", value: list of dates (lesson start dates) 
- `studentMCdata.json`, dictionary of Bothell students and lesson dates 
- `studentMCdataKirkland.json`, dictionary of Kirkland students and lesson dates  
## TODO:
- [ ] Add trend line optional param to lesson timeline
- [ ] Add covid indicator to lesson timeline 
- [ ] Finish type hinting 
- [ ] Finish doc strings 
- [ ] Add nav elements to the github pages site 
- [ ] Add side bar elements to the github pages site 
- [ ] Hyperlink key elements of the documentation 
- [ ] Improve rank histogram function, not consistent with other histogram functions in terms of flexiability 
- [ ] Finish documenting SOS  
