# Degree Visualizer


- [Requirements](#requirements)
- [Application Architecture](#application-architecture)
- [Data Model](#data-model)
- [Backend Development](#backend-development)
- [Frontend Development](#frontend-development)




### Requirements

### Application Architecture

Due to the complexity of degree programs and the number of variables to consider, we decided to store course and degree plan data in a JSON format. This allowed for easy changes of schema and modifying invalid fields; however, in the future we would likely port this structure to a NoSQL store such as MongoDB. 

Courses are organized by department and are stored as a collection, along with a GUID, description, title, and prerequisites. Prerequisites consist of an array of GUIDs for courses which are dependencies. In order to simplify the process, we decided not to include detailed prerecs such as "sophomore standing". In the event multiple courses can be a prerec, we took only the first (lowest) course entry. 

- Courses: 
!["Course data model"](docs/coursesdata.png "Course data model")

Degrees were difficult to model do to their complex structure. To model required courses and in-major electives, we created a query structure in which courses are randomly selected from a list up to a predefined count value. We didn't have time to include out of major requirements since this is even more complicated and would require including many more classes in the course catalog.


- Degrees
!["Degrees data model"](docs/degreesdata.png "Degrees data model")

### Backend Development

### Frontend Development