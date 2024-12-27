# Project
This repository contains files used to develop each project.

## Big Data Analytics Project

This project demonstrates the power of distributed computing for analysing large-scale datasets across diverse domains, including urban transportation, blockchain networks, and streaming log data. Developed using PySpark and related technologies, it showcases advanced data processing, visualisation, and real-time streaming techniques.

### Purpose
The project was designed to:
- Provide actionable insights from real-world datasets for urban planning, financial systems, and network analysis.
- Demonstrate scalable solutions for handling multi-million-record datasets using distributed computing frameworks.
- Apply advanced graph and streaming analytics for domain-specific challenges.

### Key Technologies
- **PySpark**: Distributed data processing.
- **GraphFrames**: Graph-based analysis.
- **Structured Streaming**: Real-time data processing.
- **AWS S3**: Cloud-based storage.
- **Matplotlib**: Data visualisation.

---

### Scripts

#### `nyc_taxi_data_analysis.py`
**Purpose**: Analyse NYC Yellow Taxi data to uncover tipping patterns, top routes, and borough-based insights.
- Processed 22+ million records.
- Calculated average tips per passenger and identified the top 10 routes based on tipping behavior.
- Enriched data with geospatial information using joins.

#### `ethereum_blockchain_analysis.py`
**Purpose**: Examine Ethereum blockchain data to explore miner activity, transaction fees, and daily block trends.
- Aggregated $1.2M+ in transaction fees for October 2015.
- Ranked top 10 miners by total block size.
- Performed date-based analyses for September and October transaction metrics.

#### `green_taxi_graph_analysis.py`
**Purpose**: Perform graph-based analysis on NYC Green Taxi data using GraphFrames.
- Created a graph with 195 vertices (zones) and edges (trips).
- Computed shortest paths and PageRank to evaluate network efficiency.
- Analysed connected zones within boroughs and service areas.

#### `nasa_log_streaming.py`
**Purpose**: Stream and analyse NASA log data in real-time.
- Implemented sliding windows for aggregating GIF requests with sub-3-second latency.
- Aggregated total bytes transferred by hostname and counted successful GET requests.
- Demonstrated the power of watermarking to handle late-arriving data efficiently.

#### `blockchain_activity_histograms.py`
**Purpose**: Visualise Ethereum blockchain activity.
- Generated histograms for daily block counts and unique senders in September 2015.
- Saved visualisations as PNG files for reporting.

#### `transaction_fee_histograms.py`
**Purpose**: Visualise transaction fees and block counts over time.
- Created bar charts for October 2015 transaction fees and block counts.
- Highlighted trends for blockchain metrics.

## Installation and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Jdavid1204/projects/big-data-analytics
   cd big-data-analytics
   ```

2. Set up a Python environment with required libraries:
   ```bash
   pip install pyspark matplotlib graphframes boto3
   ```

3. Configure AWS S3 credentials in your environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your-access-key
   export AWS_SECRET_ACCESS_KEY=your-secret-key
   export DATA_REPOSITORY_BUCKET=your-s3-bucket
   export S3_ENDPOINT_URL=your-s3-endpoint
   export BUCKET_PORT=port
   ```


## Embedded Systems Projects
### 1. Touch Sensor and LED Control (`touch_sensor_control.c`)
- **Description**: Implements a real-time touch-sensitive system that dynamically controls LED brightness and color. Uses CMSIS-RTOS for multi-threaded operation with event-driven architecture.
- **Features**:
  - Reads touch positions and maps them to specific actions.
  - Adjusts LED brightness incrementally based on touch regions.
  - Integrates event flags to handle multiple touch states.
- **Purpose**: Demonstrates multi-threading, event handling, and real-time user interaction.

### 2. ADC-Based LED Control (`adc_led_control.c`)
- **Description**: Utilises the ADC to measure voltage levels from two potentiometers (VR1 and VR2) and adjusts LED states accordingly. 
- **Features**:
  - Calibrates ADC for accurate measurements.
  - Dynamically changes LED behavior based on real-time voltage inputs.
  - Implements error handling for invalid input ranges.
- **Purpose**: Highlights analog-to-digital conversion and real-time signal processing.

### 3. PWM LED Brightness Control (`pwm_led_brightness.c`)
- **Description**: Controls the brightness of RGB LEDs using Pulse-Width Modulation (PWM). Allows users to toggle between different brightness change rates and patterns.
- **Features**:
  - Two modes for brightness adjustment: fast and slow.
  - Includes an additional LED pattern-switching feature (some functionality may require additional files).
  - Demonstrates advanced timer usage for precise control.
- **Purpose**: Demonstrates the use of PWM for efficient LED control and aesthetic pattern creation.

### 4. Reaction Timer (`reaction_timer.c`)
- **Description**: A reaction timing system that measures user response time with millisecond precision. 
- **Features**:
  - Waits for a random delay before triggering a "ready" state.
  - Records reaction time with hardware timers.
  - Includes error handling for early button presses.
- **Purpose**: Demonstrates event-driven programming, state transitions, and timing accuracy.

## Disclaimer

- **Missing Files**: Some supporting files (e.g., `rgb.c`, `clock.c`) may not be included in this repository. You can replace or replicate these functionalities by creating additional `.c` files or adapting the code to your needs.
- **Microcontroller Compatibility**: These projects are designed to run on the **FRDM-KL28Z board** using the **Keil µVision** IDE. Ensure all dependencies (e.g., CMSIS, board-specific drivers) are correctly set up in your development environment.
- **Adaptation**: While the provided scripts focus on specific use cases, they can be extended or modified for other microcontrollers or embedded platforms.


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
