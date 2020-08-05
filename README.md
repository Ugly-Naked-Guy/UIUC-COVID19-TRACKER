# UIUC COVID-19 Tracker

## Description

The UIUC COVID-19 Tracker is a web application for students of University of Illinois at Urbana-Champaign to self-reports the test results and estimates the infection probability and the risk level based on temperature, symptoms, and activities they provided. This platform also helps administrators to better manage suspected cases, assign test indicators, and track students’ health situation around campus. 

## Usefulness

Similar websites/applications
1. Where COVID-19 (by CyberGIS Center for Advanced Digital and Spatial Studies at the University of Illinois at Urbana-Champaign)
2. Healthlynked COVID-19 tracker

Differences

1. A prediction model is developed in our platform, which outputs the probability of disease infection and the emergency level of newly reported cases. Such evaluation allows the users to have a better judgment of his risks and the health system to better prioritize medical resources, such as the COVID-19 test and clinical slot, for those patients in need.
2. With the mission of protecting the UIUC community in mind, our data attributes, user’s input options, and data visualization are specially customized for the UIUC community. For example, the hotspot places like Grainger library, Illini Union are incorporated in our hazard map and user interaction system.
3. A user interaction system is developed. Users are not only able to communicate with each other, but will also receive alarm messages from our AI back-end engine which keeps monitoring newly reported cases and clustering patterns.

## Realness and Data Sources

1. The sources of the data can be divided into two types. One is provided by WOLFRAM DATA REPOSITORY, which can be accessed from the following URL: https://datarepository.wolframcloud.com/resources/Patient-Medical-Data-for-Novel-Coronavirus-COVID-19. The name of the dataset is COVID-19 cases with information like age, gender, symptoms is Patient Medical Data for Novel Coronavirus COVID-19. It contains the medical records of patients infected with novel coronavirus COVID-19. Patient record attributes include age, sex, location, date of onset, symptoms, travel history, chronic diseases, and date of discharge or death.
2. The other part of the data is planned to be inserted by the user, which aims to be the student of the University of Illinois. Students are required to report their health conditions & symptoms, places they’ve visited, and tests & cases related information.
- Health conditions and symptoms
    - body temperature
    - whether you have shortness of breath
    - whether you have a cough
    - whether you have a fever
- Places visited
    - whether you’ve been to public places (restaurant, pub, bank, and etc.)
    - if so, whether you wear a face covering 
    - The places you visited today 
- Tests & Cases related information
    - whether you’ve been tested
    - whether you’ve been tested positive for COVID
    - whether you are Close contacts of confirmed COVID-19 Patients
Functionality

## Basic Functions

- INSERT:
    - User can create a record of his/her health condition and travel history 
    - Once the user has a positive test result, his travel history will be added to the high-risk area table.
- UPDATE: 
    - Once the user has a test result, his/her record will be updated as positive/negative cases.
    - Once there is a confirmed case, the 
- DELETE:  
    - The platform will delete the outdated(earlier than 14 days) health condition record of the user.
    - Show how to search the database and list or print returned results. You need to show a few different interesting queries over your database. 
- SEARCH:
    - For searching by location, the platform will show both users and administrators confirmed cases in a particular location.
    - For searching by symptom, the platform can give administrators the record of suspected cases based on symptoms from confirmed cases.
    - Based on users’ symptoms and travel history, the platform will give the priority of the users for the COVID-19 test.

## Advanced Functions

- Alert system

Within each user’s account, users can subscribe for specific locations to receive latest alert when someone nearby got confirmed. It is useful for students to notice the high risk areas and avoid being there. It might be challenging in real-time implementation when the data becomes scalable. 

- Estimation for infection probability 

The estimation for infection probability is based on the data collected from both country level and county level (from self-reported local cases). The patient's characteristics such as demography and symptoms are jointly considered. Prevalent machine learning models including logistic regression and random forests will be implemented in our platform.

## Local Development Enviroment Setup
To run the demo framework successfully in local computers. Please follow the follow the following steps including setting up MySql and Flask environments, configuring the Mysql server, importing demo-database into project folder, and etc. 

### Step1 
Install python and MySQL on your machine

### Step2
Go to terminal and install some relevant packages

    pip3 install flask
    pip3 install flask_mysqldb

### Step3 
You can either import the dataset into MySQL by

- installing MySQLWorkbench and using GUI 
![](https://paper-attachments.dropbox.com/s_8FAC4FB9CCE959A552D0F02E5B31F79A253F8478393075D30983A037BA96ED52_1595217144730_image.png)

- or using the following cmd

    ```
    // mysql.server start
    // mysqladmin -u root password 'yourpassword'
    // mysql –u root –p
    mysql -uroot -p crud > crud.sql
    
### Step 4 
Open your project in IDE (for example, VS Code) and start working!

### Step 5
go to termial and `cd` to your work dirctory:

    python3 __init__.py
    

    
## Remote server setup:

We also tried to set up the server remotely using C-Panel. 
(URL: http://gameofthread.web.illinois.edu/UIUC_COVID19) 

![](https://lh4.googleusercontent.com/NZJA3GYhX6MO7MHRwRNO_U0QTXYlu27NV0_7IMXALXsC5mfOMSklTHqUMd5A-WFuQy0_NSpvELoWP0udiVX6sidW9C5uzEfyComEKjr3lKUdQ5sl67wmOifq58kUPqxwKAaj7LA)

The detailed steps shows as follow, 
 
### Step 1
Register a domain in University of Illinois cPanel Web Hosting Service

![](https://lh4.googleusercontent.com/aegaEBEMDHePbvaCNgkOc-rD6NLbyBXD06L67yvqf3oyKS_lksCZTQwaUnJ_OK3qsrfOA2WvbaGQWp_iwK_1Li2KSqTKrJFmZPKiP6cUiWlpMF6dHLzH-2_uJzrAgFiBXe9aII8)

### Step 2
Create Python application in cPanel
 
![](https://lh3.googleusercontent.com/A5I0DJfindWMx6TtOThFowdMFV_soczNLk3lAlvYYIAFtCh7VwXeLSrTwN3MaPkZrbbrK6-Ih9ddMX9LvoV1D8PZU3df6hZRKDnopbXqM6ZsxR0KsBz8SLpezByq7W-74xYQ7F4)

Notes: The tutorial we follow for deploying flask application at cPanel is at https://www.youtube.com/watch?v=xFxL7Mvut6g
### Step 3
Upload files to File Manager’

### Step 4
Create database and add user

Notes: We follow the tutorial here https://www.youtube.com/watch?v=CHwxXGPnw48
  
## Remote database setup:

1. We use MySQL as our relational database.
2. To Import real data, we first create databases and users with MySQL® Database Wizard provided by cPanel, and then import data with phpMyAdmin provided by cPanel. 

## Reference:
The theme of website is referenced from https://github.com/parwiz123/flask-crud-application-with-mysql

The script logistics regression borrows some idea from https://zhuanlan.zhihu.com/p/41132059

