# Project



This repository contains files used to develop each project.
## Weather-APP

### How to Run Project

## Creating React Project

Run command `npx create-react-app <"name of app">` <br>
Unzip sourcefile and replace it with the source file in the created react app

## Install Packages:

Run in terminal (pointed at the folder with the react app)

- `npm install <"package name">` (Packages use in the weather application (requiring install) are listed bellow).

## Running Weather Application React Project:

Run in terminal (pointed at the folder with the react app) `npm start` to start local host deployment

# Project Information

## External Packages Used In Weather Application

For each run `npm install <"package name">`

 - axios
 - bootstrap
 - leaflet
 - react-bootstrap
 - react-burger-menu
 - react-icons
 - react-leaflet

## APIs Used In Weather Application

- [GeoNames](https://www.geonames.org/)
- [OpenWeather](https://openweathermap.org/)
- [Unsplash](https://unsplash.com)


## Blog-Portfolio

Run locally using 'MAMP' which connected to a database created in 'phpMyAdmin'.

Home page: <br>
<img align = "middle" width="500" alt="Index Page" src="https://github.com/Jdavid1204/projects/assets/88732045/64e1eb19-290e-4b4d-b2b7-62926b2a5278"> <br>
'phpMyAdmin' database <br>
<img align= "middle" width="500" alt="phpMyAdmin" src="https://github.com/Jdavid1204/projects/assets/88732045/c855550e-ee13-447f-b2ff-16d8ea6e1b2b">



## Platformer-Game
Make sure that you have installed [Python3](https://www.python.org/download/), and 'Pygame' library downloaded. 
```console
sudo apt install python3-dev
python -m pip install -U pygame==2.5.2 --user
```
## NHS-Table

Here's a breakdown of the purpose of each table and their relationships:

**department**: Stores information about different departments within the hospital, including their unique ID, name, and specialty. This is essential for organizing the hospital's services by medical specialty.

**person**: Acts as a generic table for storing basic personal information about individuals associated with the hospital, such as patients, clinicians, and possibly other staff. It includes details like name, date of birth (dob), age, gender, National Insurance (NI) number (a unique identifier in the UK), address, phone number, and email. The constraints ensure that each person has a unique NI number, and at least one contact method (phone or email) is provided.

**patient**: Contains specific information related to patients, linking them to the person table via person_id. It includes a patient's Medical Record Number (MRN) and employment status. The ON DELETE CASCADE clause ensures that if a person record is deleted, the corresponding patient record is also removed.

**clinician**: Stores information about medical clinicians, including their specialty, grade, and security level. It also links clinicians to the person table and optionally to a department. This setup allows tracking which clinicians belong to which department and their roles within the hospital.

**theatre**: Represents operating theatres within the hospital, linking each theatre to a department. The ON DELETE CASCADE policy indicates that if a department is deleted, its associated theatres are also removed.

**cases**: Manages medical cases, including their current status and associations with departments, clinicians, and patients. This table enables tracking of which clinician is handling which case, the department it belongs to, and the patient involved. The use of ON DELETE SET NULL and ON DELETE CASCADE ensures that cases can be reassigned or deleted appropriately based on changes in clinicians, departments, or patient records.

**operation**: Records details of surgical operations, including type, priority, status, scheduling, and associations with specific cases and theatres. This table is crucial for planning and managing surgical procedures within the hospital.

**waiting_list**: Manages waiting lists for operations, with entries including start and end times, and links to patient MRNs and specific cases. The constraints and foreign keys ensure data integrity and the relationship between waiting list entries and patients or cases.

**clinicians_performing_operation**: A junction table that links clinicians to operations they are performing. This many-to-many relationship allows recording multiple clinicians involved in a single operation.
