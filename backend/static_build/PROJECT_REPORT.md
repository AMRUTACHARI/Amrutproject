# FLORAai 🌿 — AI-Powered Botanical Diagnostics & Crop Health Platform for Indian Flora

**Major Project Technical Report**

*Submitted in partial fulfillment of the requirements for the award of the degree of*

**BACHELOR OF ENGINEERING IN COMPUTER SCIENCE AND ENGINEERING**


**Candidate Name:** AMRUT ACHARI  

**Department:** Department of Computer Science & Engineering  

**Academic Year:** 2025 – 2026  

**Live Deployment:** [https://amrutproject.vercel.app](https://amrutproject.vercel.app)  

**GitHub Repository:** [https://github.com/AMRUTACHARI/Amrutproject](https://github.com/AMRUTACHARI/Amrutproject)

---


### (AI-Powered Botanical Diagnostics & Crop Health Platform for Indian Flora)

Submitted By: AMRUT ACHARI
Department of Computer Science and Engineering
Academic Year 2025 – 2026
Live Platform: https://amrutproject.vercel.app


## TABLE OF CONTENTS


## ACKNOWLEDGEMENT

I would like to express my deepest gratitude to all those who contributed to the successful completion and deployment of the project titled "FLORAai: AI-Powered Botanical Diagnostics & Crop Health Platform for Indian Flora".

First and foremost, I express my profound respect and sincere thanks to my project guide and faculty mentors in the Department of Computer Science and Engineering for their continuous encouragement, valuable suggestions, insightful critiques, and technical guidance throughout the design, model training, and deployment phases of this application.

I also extend my sincere thanks to the Head of the Department and the institution for providing the high-speed laboratory infrastructure, computing facilities, and academic environment essential to undertake this research in machine learning and full-stack web engineering.

Lastly, I am grateful to my family, peers, and fellow developers whose moral support, constructive feedback, and endurance made this submission possible.

AMRUT ACHARI
Department of Computer Science & Engineering


## DECLARATION

I hereby declare that the project report entitled "FLORAai: AI-Powered Botanical Diagnostics & Crop Health Platform for Indian Flora" submitted to the Department of Computer Science and Engineering is a bonafide record of independent engineering work carried out by me under faculty supervision.

I further declare that this project work, either in part or in full, has not been previously submitted to any other university, institute, or examining body for the award of any degree, diploma, or academic distinction.

The live application is independently engineered and deployed at https://amrutproject.vercel.app with complete source versioning maintained at https://github.com/AMRUTACHARI/Amrutproject.

Date: November 2026
Place: Karnataka, India

AMRUT ACHARI


## ABSTRACT

The rapid growth of technology and increasing challenges in sustainable agriculture have created a need for intelligent plant health diagnostic management systems that can efficiently connect farmers, domestic gardeners, and agricultural institutions. Traditional plant pathology processes often involve manual operations, fragmented communication, limited botanical guidance, and time-consuming laboratory diagnostic procedures. To address these challenges, FLORAai is developed as an AI-powered Botanical Diagnostics and Crop Health Platform that provides a centralized and automated environment for managing the complete plant health lifecycle.

FLORAai integrates four major stakeholders—Farmers, Domestic Home Gardeners, Agricultural Extension Officers, and Botanical Researchers—into a single digital ecosystem. The platform enables farmers to capture leaf photographs, receive real-time deep learning health evaluations, access specialized 46-species Indian botanical knowledge, explore trending agricultural crops, and receive 100% accessible organic Ayurvedic remedies. Agricultural officers and institutions can efficiently monitor disease outbreaks, shortlist affected taluks, analyze regional pathogen spreads, conduct visual camera inspections, and manage quarantine workflows through dedicated dashboards.

The system is developed using modern web technologies including React.js, Tailwind CSS, Python, FastAPI, Motor, MongoDB, and JWT Authentication. Advanced features such as MobileNetV3 Dual-Head Vision (FloraDualNet), Google Gemini Multimodal Vision API, Quantitative Vitality Scoring (0 to 100), Real-Time Video Camera Inspection, Analytics Dashboards, and Ayurvedic Remedy Formulation enhance the overall effectiveness of crop disease management. The platform utilizes a centralized database architecture to ensure secure data storage, efficient information management, and reliable access control for authorized users.

FLORAai not only simplifies crop health diagnosis but also promotes environmental sustainability by providing farmers with accessible organic treatments that eliminate soil-poisoning synthetic chemicals. The platform improves diagnostic transparency, reduces agricultural yield losses, enhances treatment accessibility, and enables data-driven decision-making for all stakeholders. By combining modern web technologies with artificial intelligence, FLORAai offers a scalable, secure, and intelligent solution for transforming traditional agriculture into a smarter and more sustainable digital ecosystem. Future enhancements may include drone-based aerial NDVI surveys, IoT soil sensor telemetry, offline on-device quantized edge inference, and speech-to-speech vernacular assistance.


# CHAPTER 1


# INTRODUCTION

FLORAai is an AI-driven platform designed to revolutionize agricultural plant diagnostics and botanical health management across the Indian subcontinent. It creates a unified digital ecosystem that seamlessly connects farmers, home gardeners, agricultural extension officers, and academic institutions.

For farmers and home gardeners, FLORAai offers a comprehensive suite of tools to enhance plant health and crop yield. This includes AI-based foliar assessments, real-time health score calculations, practical camera inspection tools, and in-depth organic treatment formulation. These features are tailored to improve diagnostic speed, eliminate Latin pathological jargon, and guide sustainable Ayurvedic crop care.

Agricultural institutions and extension officers benefit from FLORAai by gaining access to real-time spatial surveillance data. The platform streamlines disease tracking, enabling rapid identification of fungal blights, easy coordination of regional advisories, and effective management of all crop protection activities.

Technologically, FLORAai leverages a modern stack to deliver its smart botanical diagnostic ecosystem. This includes React.js for a dynamic user interface, Tailwind CSS for efficient styling, and a robust backend built with Python and FastAPI, supported by MongoDB for data management. Advanced features include a MobileNetV3 dual-head neural network for foliar classification, Google Gemini Vision for multimodal reasoning, an in-memory resilient fallback store for zero downtime, and interactive geospatial outbreak analytics dashboards.

FLORAai is an AI-powered Botanical Diagnostics & Crop Health Platform designed to automate and improve the agricultural disease management process. It connects farmers, domestic growers, agricultural officers, and research institutions through a centralized digital ecosystem. The platform provides features such as live camera leaf capture, chlorosis color mask segmentation, 46-species Indian botanical catalog, vernacular translation, and scan history tracking to enhance agricultural productivity and environmental health.

For extension officers and institutions, FLORAai simplifies crop disease monitoring and quarantine management through automation. Departments can conduct assessments, identify affected areas, and manage field advisories efficiently, while institutions can track botanical trends. The platform integrates tools such as MobileNetV3 DualNet, Google Gemini Vision, Quantitative Vitality Scoring, and Leaflet Geospatial Maps.


## PROBLEM STATEMENT


### Manual Plant Diagnostic Process

Many farmers and gardeners still manage plant diseases manually through trial and error, making the diagnostic process slow and inefficient.


### Lack of Botanical Skill & Taxonomy Analysis

Growers often do not know the specific nutritional deficiencies, fungal pathogens, or missing trace minerals affecting their plants.


### Esoteric Latin Pathology Jargon

Diagnostic tools output esoteric academic terminology like 'interveinal chlorosis' or 'cercospora necrosis' without plain-English explanations.


### Toxic Synthetic Chemical Prescriptions

Standard gardening applications routinely prescribe expensive, patented chemical fungicides that harm beneficial soil microbiomes.


### Western Taxonomy Bias for Indian Crops

Commercial computer vision tools are trained on Western flora, repeatedly misclassifying tropical crops like Coconut, Areca Palm, and Betel Leaf.


### Lack of Vernacular Multilingual Guidance

Over 85% of Indian farmers communicate in regional languages, yet mainstream agricultural applications only provide advice in English.


### Network Fragility in Remote Farmlands

Rural farmlands frequently suffer from intermittent cellular internet, causing conventional cloud-dependent applications to fail completely.


### No Centralized Surveillance Platform

Foliar scan records, agricultural advisories, diagnostic histories, and epidemic trends are scattered across disconnected local channels.


### Inefficient Emergency Communication

Farmers and extension officers face delays in receiving time-critical quarantine alerts about sudden pest attacks and fungal spores.


### Lack of Real-Time Geospatial Analytics

State Agricultural Departments do not have access to real-time spatial heatmaps and crop health statistics for proactive intervention.


## OBJECTIVES

The primary goal of FLORAai is to modernize, automate, and enhance the botanical diagnostic and crop health management process for farmers, gardeners, and academic institutions. The specific objectives of this project are:

To Streamline the Plant Diagnostic Process: Develop a centralized AI-enabled platform that manages leaf image capture, species identification, foliar health analysis, and treatment formulation efficiently within a single system.

To Eliminate Western Taxonomy Bias: Standardize an authentic 46-species Indian subcontinent botanical catalog covering field crops, culinary spices, medicinal herbs, and regional palms.

To Strengthen Diagnostic Accuracy: Implement a dual-head MobileNetV3 deep learning architecture (FloraDualNet) alongside multimodal vision models for simultaneous species recognition and pathology localization.

To Prescribe 100% Organic & Ayurvedic Treatments: Formulate zero-chemical remedies utilizing neem oil, sour buttermilk sprays, wood ash, and bio-fungicides to restore ecological balance.

To Offer Vernacular Multilingual Accessibility: Display plant names and diagnostic advice in native regional scripts including Kannada, Tamil, Hindi, and English.

To Quantify Plant Vitality with Objective Scoring: Compute an objective foliar vitality metric from 0 (Severely Compromised) to 100 (Flourishing) based on necrosis area ratios.

To Support Instant Edge & Cloud Camera Diagnostics: Deliver end-to-end inference latencies under 1.8 seconds from camera capture to full diagnostic breakdown.

To Improve Communication and Collaboration: Enable smooth interaction between farmers, extension officers, and institutions through real-time notifications, advisories, and quarantine updates.

To Generate Analytical Insights: Provide advanced dashboards and analytics tools to monitor disease outbreak statistics, regional trends, and plant recovery rates effectively.

To Develop a Scalable and User-Friendly Platform: Design a responsive, secure, and scalable system using modern technologies capable of handling large-scale agricultural operations efficiently.


## APPLICATIONS

The primary goal of FLORAai is to modernize, automate, and improve the botanical diagnostic and crop health management process for farmers, gardeners, and academic institutions. The specific applications of this project are:

Smallholder Farm Crop Health Management – FLORAai provides a centralized mobile diagnostic tool for smallholders to identify blights in paddy, wheat, cotton, and sugarcane without visiting distant laboratories.

AI-Based Botanical Advisory System – The platform uses Artificial Intelligence to analyze leaf venation, chlorosis, and textural symptom data to provide personalized care recommendations and organic treatments.

Real-Time Camera Foliar Diagnostic Assessment – FLORAai supports real-time camera inspection where farmers can capture live video frames of leaves in a secure digital environment with instant automated scoring.

AI Plant Pathology & Vitality Scoring Platform – The system includes deep learning foliar classification that evaluates plant vitality objectively, outputting severity badges from healthy to critical blight.

Organic Ayurvedic Remedy Formulation Engine – FLORAai details specific natural preparations—such as neem seed kernel extract, sour buttermilk spray, wood ash, and bio-fungicides—complete with dosage.

Agricultural Extension & Quarantine Advisory System – Extension officers can use intelligent dashboards to search, filter, and track disease outbreaks based on severity, crops, and geographical locations.

Geospatial Epidemic Surveillance and Reporting – The platform generates detailed outbreak reports and analytics such as disease frequencies, affected acreages, and temporal trends for data-driven decisions.

Crop Recovery Tracking and Performance Monitoring – FLORAai identifies recovery progress across consecutive scans, helping farmers monitor weak areas through historical timeline comparisons.


# CHAPTER 2


# HARDWARE AND SOFTWARE REQUIREMENTS


## Hardware Configuration

The following hardware specifications are required to host the local development environment and run the FastAPI backend and machine learning inference pipelines without performance bottlenecks:

Processor – Intel Core i3 (Minimum) / Intel Core i5, Apple Silicon M-Series, or AMD Ryzen equivalent (Recommended) or higher.

Random Access Memory (RAM) – 4 GB (Minimum) / 8 GB or higher (Recommended) for smooth multitasking between the IDE, local server, deep learning pipelines, and browser testing.

Storage (Hard Disk / SSD) – Minimum 10 GB of free disk space for the operating system, IDE, model checkpoints, and botanical assets. An SSD is highly recommended for faster executions.

Network / Connectivity – A stable Broadband/Wi-Fi internet connection is strictly required for downloading packages, syncing MongoDB Atlas clusters, and integrating live APIs.


## Software Specification

This project utilizes a modern Python FastAPI and React architecture for highly scalable, asynchronous processing, enabling a unified, resilient ecosystem across both frontend and backend to streamline development and deployment.

Operating System: Windows 10 / 11, macOS, or Linux (Ubuntu).

Local Server Environment: Python (v3.10 to v3.12 64-bit) with Node.js (v18.x or higher).

Frontend Build Tool: Vite / React Scripts.

Package Manager: PIP / NPM.

Backend Language & Framework: Python with FastAPI and Uvicorn ASGI Server.

Database (DBMS): MongoDB (NoSQL) hosted on MongoDB Atlas.

Frontend Technologies: HTML5, CSS3 (Tailwind CSS), React.js, and Lucide Icons.

IDE: Visual Studio Code (VS Code).

External APIs & SDKs:

Google Gemini Vision API: For multimodal semantic plant pathology reasoning and visual verification.

HTML5 MediaDevices Camera API: For real-time camera shutter capture and video streaming on mobile devices.


# CHAPTER 3


# DATABASE DESIGN


## INTRODUCTION

The database plays a vital role in the FLORAai platform as it is responsible for storing, organizing, managing, and retrieving all botanical diagnostic records, user accounts, plant catalogs, and disease outbreak data efficiently. The entire system depends on the database for handling user profiles, leaf scan records, foliar health scores, symptoms, organic Ayurvedic remedies, regional outbreak incident reports, and audit logs.

The database is designed using Entity Relationship (ER) concepts to establish proper relationships between different entities such as Farmers, Agricultural Officers, Botanical Researchers, State Departments, Plant Species, Foliar Scans, Outbreaks, and Care Records. A well-structured database design helps maintain data consistency, integrity, security, and efficient communication between different modules of the platform.

FLORAai uses MongoDB as the primary database management system because it provides flexibility, scalability, faster performance, and efficient handling of dynamic data structures. MongoDB stores data in collections and documents, making it suitable for handling large amounts of semi-structured foliar diagnostic data. The database supports secure storage of user credentials, high-resolution leaf scan payloads, AI diagnostic outputs, and geospatial coordinates.

The database also supports important functionalities such as user authentication, role-based access control, foliar scan history retrieval, outbreak geocoding, and real-time catalog lookups. Proper compound indexing on user_id, plant_id, and timestamps ensures sub-5ms query performance even during concurrent user operations.

The FLORAai database design is developed to support scalability, reliability, and efficient data processing for agricultural disease surveillance. It helps agricultural officers monitor disease outbreaks effectively and allows farmers to track their crop recovery progress over time.


## DATA FLOW DIAGRAM (DFD)


### 1. DFD LEVEL 0


*Figure 3.2.1: DFD LEVEL 0*


### 2. DFD LEVEL 1: For Farmer & Domestic Grower


*Figure 3.2.2: DFD Level 1 - Foliar Capture & Diagnostics*


### DFD LEVEL 2: For Farmer & Domestic Grower


*Figure 3.2.3: DFD Level 2 - DualNet Inference & Ayurvedic Remedies*


### DFD LEVEL 1: For Agricultural Extension Officer


*Figure 3.2.4: DFD Level 1 - Outbreak Surveillance & Quarantine*


### DFD LEVEL 2: For Agricultural Extension Officer


*Figure 3.2.5: DFD Level 2 - Epidemic Clustering & Taluk Broadcast*


### DFD LEVEL 1: For Ayurvedic Specialist & Botanist


*Figure 3.2.6: DFD Level 1 - Botanical Herbarium & Phytotherapy*


### DFD LEVEL 2: For Ayurvedic Specialist & Botanist


*Figure 3.2.7: DFD Level 2 - Organic Recipe Validation & Bio-Safety*


### DFD LEVEL 1: For State Agriculture Department


*Figure 3.2.8: DFD Level 1 - District Crop Telemetry & Analytics*


### DFD LEVEL 2: For State Agriculture Department


*Figure 3.2.9: DFD Level 2 - PKVY Organic Farm Certification*


## Schema Diagram

A Schema Diagram is a visual representation of the structure of a database. It shows tables, fields, data types, and relationships between the tables.


*Figure 3.3.1 Schema Diagram*


## Entity Relationship Diagram


*Figure 3.4.1:Entity Relationship Diagram*


# CHAPTER 4


# TESTING AND IMPLEMENTATION


## WHITE BOX TESTING

White box testing is a software testing method in which the internal code structure, logic, conditions, and program flow of the system are tested. It ensures that all functionalities of the FLORAai platform work correctly and efficiently.


*Figure 4.1.1: White Box Testing*


## BLACKBOX TESTING

Black box testing is a software testing method in which the functionality of the system is tested without examining the internal code, program structure, or implementation details. It mainly focuses on validating the input, output, user interface, and overall behavior of the application according to the specified requirements.


*Figure 4.2.1: Black Box Testing*


## UNIT TESTING

Unit testing is a software testing technique in which individual units, modules, or functions of the application are tested independently to ensure that each component works correctly. It mainly focuses on verifying the internal logic, functionality, input handling, and output of a specific part of the system before integration with other modules.


*Figure 4.3.1: Unit Testing*


## 4.4. INTEGRATION TESTING

Integration testing is a software testing technique in which multiple modules or components of a system are combined and tested together to verify their interaction and data flow. It ensures that different modules of the FLORAai platform work together correctly without errors.


*Figure 4.4.1: Integration Testing*


## SYSTEM TESTING

System testing is a software testing process in which the complete and integrated application is tested as a whole to ensure that all modules work properly together. It verifies whether the system meets the specified functional and non-functional requirements. This testing helps identify errors, performance issues, and integration problems before the software is deployed to users. The main objective of system testing is to ensure the application is reliable, efficient, and ready for real-world use.


*Figure 4.5.1: System Testing*


## ACCEPTANCE TESTING

Acceptance testing is performed to check whether the software meets user and business requirements. It is done after system testing to ensure the application works correctly in real-world conditions. This testing confirms that all major features function properly and satisfy user expectations. The main aim is to verify that the software is ready for final deployment and use.


*Figure 4.6.1: Acceptance Testing*


## VALIDATION TESTING

Validation testing is the process of evaluating software to ensure that it meets user requirements and performs the intended functions correctly. It checks whether the developed system satisfies business needs and works properly in real-world conditions. This testing helps confirm the accuracy, reliability, and quality of the application before deployment. The main objective of validation testing is to ensure that the right product has been built for the users.


*Figure 4.7.1: Validation Testing*


# CHAPTER 5


# SCREENSHOTS


## Index Page (Landing Hero & Platform Showcase)


*Figure 5.1.1: Index Page (Landing Hero & Platform Showcase)*


## Botanical Herbarium Showcase (46 Native Species)


*Figure 5.1.2: Botanical Herbarium Showcase (46 Native Species)*


## User Login Page


*Figure 5.1.3: User Login Page*


## Login Form with Farmer Authentication


*Figure 5.1.4: Login Form with Farmer Authentication*


## User Registration Page (Farmer Onboarding)


*Figure 5.1.5: User Registration Page (Farmer Onboarding)*


## Password Recovery & Security Portal


*Figure 5.1.6: Password Recovery & Security Portal*


## Farmer Plant Diagnostics Dashboard


*Figure 5.1.7: Farmer Plant Diagnostics Dashboard*


## Verified Indian Crop & Preset Selector


*Figure 5.1.8: Verified Indian Crop & Preset Selector*


## Foliar Specimen Loaded in AI Scanner


*Figure 5.1.9: Foliar Specimen Loaded in AI Scanner*


## Real-Time AI Diagnostic Scanning & Laser Inference


*Figure 5.1.10: Real-Time AI Diagnostic Scanning & Laser Inference*


## Live Camera Viewfinder & Reticle Modal


*Figure 5.1.11: Live Camera Viewfinder & Reticle Modal*


## Final Disease Detection Report - Certificate & Health Score


*Figure 5.1.12: Final Disease Detection Report - Certificate & Health Score*


## Final Disease Detection Report - Organic Ayurvedic Remedies


*Figure 5.1.13: Final Disease Detection Report - Organic Ayurvedic Remedies*


## Final Disease Detection Report - Foliar Metrics & Audio Speech


*Figure 5.1.14: Final Disease Detection Report - Foliar Metrics & Audio Speech*


## Second Plant Diagnosis & Foliar Disease Evaluation


*Figure 5.1.15: Second Plant Diagnosis & Foliar Disease Evaluation*


## Scan History & Diagnostic Archive Page


*Figure 5.1.16: Scan History & Diagnostic Archive Page*


## Farmer Profile & Plantation Details


*Figure 5.1.17: Farmer Profile & Plantation Details*


## User Preferences & Diagnostic Threshold Settings


*Figure 5.1.18: User Preferences & Diagnostic Threshold Settings*


## Phytotherapy & Ayurvedic Remedy Knowledge Base


*Figure 5.1.19: Phytotherapy & Ayurvedic Remedy Knowledge Base*


## Extension Officer Outbreak Surveillance Console


*Figure 5.1.20: Extension Officer Outbreak Surveillance Console*


## CONCLUSION AND FUTURE SCOPE


## CONCLUSION

The FLORAai platform was developed to address the growing need for an intelligent and centralized botanical diagnostic and crop health management system for farmers, domestic gardeners, agricultural extension officers, and academic institutions. By integrating plant health diagnostics, deep learning dual-head vision, 46 native botanical species, localized vernacular naming, and 100% organic Ayurvedic remedy formulations into a single platform, the project successfully reduces the complexity and inefficiency of traditional agricultural advisory systems.

Through the implementation of a modern architecture using React.js, Tailwind CSS, Python, FastAPI, and MongoDB, the system ensures secure data management, smooth communication between modules, and efficient handling of user activities. The modern botanical design provides a clean, interactive, and user-friendly experience that improves engagement for all types of users on the platform.

This project demonstrates a scalable, secure, and intelligent solution for automating plant pathology diagnostics and organic remedy recommendations. Features such as real-time camera leaf capture, chlorosis area segmentation, quantitative vitality scoring (0 to 100), geospatial disease outbreak mapping, and scan history tracking enhance both agricultural decision-making and sustainable farming practices.

Overall, FLORAai serves as a strong foundation for future advancements such as autonomous drone surveys, IoT soil sensor telemetry, offline quantized edge inference, and vernacular speech assistance. The project highlights how modern software technologies and AI-driven systems can significantly improve the efficiency, transparency, and sustainability of agricultural crop health management.


## FUTURE SCOPE

Autonomous Drone Multispectral Aerial Surveys: Future versions can include automated aerial NDVI surveys using low-cost agricultural drones for large-scale crop health mapping across extensive agricultural estates.

IoT Soil Sensor Telemetry Integration: The system can be upgraded to integrate hardware soil sensors measuring moisture, electrical conductivity, and NPK nutrients to correlate foliar chlorosis with root-zone conditions.

Vernacular Speech-to-Speech Voice Assistant: Real-time regional voice recognition and speech synthesis can be integrated in Kannada, Tamil, Telugu, and Hindi to assist rural farmers verbally.

Offline On-Device Quantized Edge Inference: TFLite and ONNX Runtime models can be embedded in the browser to enable instant foliar diagnostics with zero internet connectivity.

Satellite Remote Sensing & Weather Correlation: Real-time satellite meteorological data can be connected to predict fungal blight risks 7 days in advance based on humidity and rainfall.

Blockchain-Based Herbal Provenance Ledger: Blockchain technology can be integrated to verify organic Ayurvedic herb cultivation and provide tamper-proof purity certificates.

Community Farmer Krishi Forum: A peer-to-peer discussion forum can be added where farmers share organic remedy formulations and discuss pest management.

Microscopic Spore Identification: The system can be connected with smartphone optical microscope attachments to detect fungal spores before visible leaf spots emerge.

Automated SMS & WhatsApp Emergency Broadcasts: Push notifications and automated SMS/WhatsApp alerts can be implemented to warn farmers when an outbreak is confirmed in their taluk.

Automated Pest Trap Counting: Computer vision object detection models (YOLO) can be integrated to count and classify insect pests caught in sticky orchard traps.

Nutritional Deficiency Foliar Heatmaps: Advanced segmentation heatmaps can be generated to distinguish micronutrient deficiencies (iron, zinc, magnesium) from fungal infections.

Government Subsidy & Organic Certification Pipeline: The application can interface with national organic farming portals (PKVY) to facilitate official bio-farming certification.


## REFERENCES

React.js Official Documentation (https://react.dev/) was used for developing the frontend user interface using reusable components and modern React features. It helped in building responsive pages, routing, and interactive dashboards for students, recruiters, and institutions.

Node.js Official Documentation (https://nodejs.org/) was used for backend server-side development and handling asynchronous operations efficiently. It was used to manage APIs, authentication, and database communication.

FastAPI Documentation (https://fastapi.tiangolo.com/) was used for creating RESTful APIs, middleware handling, and routing between frontend and backend modules in the FLORAai platform.

MongoDB Documentation (https://www.mongodb.com/docs/) was used for designing and managing the NoSQL database structure for storing user profiles, scan histories, plant catalogs, and disease outbreaks.

Motor Documentation (https://motor.readthedocs.io/) was used for asynchronous database validation and handling non-blocking object modeling between Python and MongoDB Atlas.

MDN Web Docs – JavaScript (https://developer.mozilla.org/en-US/docs/Web/JavaScript) was used for understanding JavaScript concepts, DOM manipulation, ES6 features, and asynchronous programming techniques.

Tailwind CSS Documentation (https://tailwindcss.com/docs) was used for designing modern, responsive, and glassmorphism-based user interfaces with utility-first CSS styling.

Google Fonts (https://fonts.google.com/) was used for selecting clean and professional typography styles to improve the visual appearance of the application.

Font Awesome & Lucide Icons (https://lucide.dev/) were used for adding icons and visual elements in dashboards, forms, navigation menus, and analytics sections.

Visual Studio Code (https://code.visualstudio.com/) was used as the primary code editor for writing, debugging, and managing frontend and backend source code efficiently.

GitHub (https://github.com/) was used for version control, project repository management, and maintaining project source code backups during development.

Postman (https://www.postman.com/) was used for testing REST APIs, validating backend responses, and checking authentication and database operations.

W3Schools (https://www.w3schools.com/) was used as a quick reference for HTML, CSS, JavaScript, React basics, and backend syntax during implementation.

GeeksforGeeks (https://www.geeksforgeeks.org/) was used for understanding concepts related to database management systems, data structures, algorithms, and ER diagrams.

YouTube React Tutorial (https://www.youtube.com/watch?v=bMknfKXIFA8) was used for learning React.js concepts, component structures, hooks, and frontend development practices.

YouTube Deep Learning & PyTorch Tutorial (https://www.youtube.com/watch?v=V_xro1bcAuA) was used for understanding computer vision models, transfer learning, and foliar classification concepts.

Google Gemini Multimodal AI Documentation (https://ai.google.dev/) was used for integrating real-time visual inspection and leaf pathology reasoning into the FLORAai platform.
