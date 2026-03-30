# 🚗 Carpool Platform – Private Car Sharing System  
*Full-stack ride-sharing platform with real-time communication & role-based access*

## Overview  
This project is a comprehensive **private carpooling system** designed to connect drivers and passengers for efficient, eco-friendly travel. Built with a client‑server architecture, the platform supports three user roles—**passengers, drivers, and administrators**—with fine‑grained permission controls. It enables drivers to publish trips, passengers to search and book seats, real‑time messaging between matched users, and full administrative oversight.

The system addresses urban traffic congestion and low vehicle utilization by promoting shared mobility. It incorporates robust validation, secure authentication, and an intuitive mobile interface to deliver a reliable and user‑friendly experience.

## Tech Stack  
| Layer          | Technology                                                              |
|----------------|--------------------------------------------------------------------------|
| Frontend       | UniApp (Vue.js), HBuilderX                                               |
| Backend        | Java 17, Spring Boot, Spring Security, JWT, WebSocket                    |
| Database       | MySQL 5.7+, MyBatis                                                      |
| Testing        | JUnit, Selenium, Apifox, Locust                                          |
| Environment    | Windows 11, IntelliJ IDEA, VS Code                                       |

## Core Features  

### Passenger  
- 🔐 **Account Registration & Login** – Secure phone‑based registration, password encryption (MD5 + salt).  
- 👤 **Profile Management** – View and edit personal information, manage historical orders and trips.  
- 🔍 **Trip Search** – Search trips by origin, destination, and departure time; smart matching algorithm prioritizes nearby routes.  
- 📝 **Booking** – Request seats on selected trips; receive driver confirmation.  
- 📋 **Order Management** – Track order status (pending, confirmed, completed, cancelled).  
- 💬 **Real‑Time Chat** – Communicate with drivers via WebSocket after booking confirmation.  
- ⭐ **Review & Feedback** – Rate drivers and submit complaints or suggestions.

### Driver  
- 🔐 **Account Registration & Login** – Same secure authentication; additional real‑name and driver’s license verification.  
- 🚗 **Vehicle Management** – Add, edit, delete vehicles; vehicles must be approved by admin before use.  
- 🚀 **Trip Publishing** – Create trips with origin, destination, departure time, price, available seats, and selected vehicle.  
- 📊 **Trip Management** – View published trips and manage passenger booking requests.  
- ✅ **Order Handling** – Accept or reject booking requests; confirm orders to finalize trips.  
- 💬 **Real‑Time Chat** – Communicate with passengers after booking confirmation.

### Administrator  
- 👥 **User Management** – View all users; enable or disable accounts.  
- 🚘 **Vehicle Verification** – Review and approve driver‑submitted vehicle information.  
- 📅 **Trip Oversight** – Monitor and remove non‑compliant trips.  
- 📢 **Complaint Handling** – Process user complaints and update user credit records.

## System Architecture  
The system follows a classic three‑tier architecture:
```
Frontend (UniApp) ──HTTP Request──► Controller Layer (REST API)
│
▼
Service Layer (Business Logic)
│
▼
Repository Layer (Data Access)
│
▼
MySQL Database (15+ tables)
```

- **Presentation Layer** – UniApp mobile client, handles UI and user interaction.  
- **Business Logic Layer** – Spring Boot services for authentication, trip matching, order processing, and real‑time messaging.  
- **Data Access Layer** – MyBatis with MySQL, ensuring data consistency and integrity.

## Database Design  
The database consists of **15+ relational tables** normalized to 3NF:

| Table | Description |
|-------|-------------|
| `user` | Stores user credentials, roles, and personal info |
| `car` | Vehicle details owned by drivers (with audit status) |
| `trip` | Trip information: route, time, price, available seats |
| `carpool_order` | Orders linking passengers to trips |
| `chat_message` | Real‑time chat history per order |
| `complaint` | User complaints linked to orders |
| `review` | Ratings and feedback after trip completion |

Foreign key constraints enforce referential integrity, and indexes are applied to high‑frequency query fields.

## Development & Runtime Environment  

### Frontend  
- Open the UniApp project in **HBuilderX**.  
- Run directly on Android emulator or real device (Android 7.0+).

### Backend  
1. Clone the repository and import into **IntelliJ IDEA**.  
2. Configure MySQL in `application.yml` (database name, username, password).  
3. Run `CarpoolBackendApplication.java` to start the Spring Boot server (default port: 8080).

## How to Run  

1. **Start Backend** – Launch Spring Boot application.  
2. **Start Frontend** – Run UniApp project in HBuilderX.  
3. **Access the App** – Use the login screen to register or sign in.

## Testing & Quality Assurance  

### Unit Testing (JUnit)  
- **UserService** – 16 test cases covering registration, login, profile updates, and password changes.  
- **TripService** – 17 test cases for trip publishing, searching, and status transitions.  
- **ValidationUtils** – 46 test cases for input validation (phone, ID card, password strength, etc.).

### Functional Testing (Selenium)  
Automated browser tests simulate user flows: login, registration, trip search, and navigation across modules.

### Interface Testing (Apifox)  
All RESTful APIs were tested with mock data, covering success paths, edge cases, and error handling.

### System Testing (Locust)  
Concurrency test: 5 users, 1 request/second for 20 seconds; failure rate under 15%, confirming baseline stability.

<img width="781" height="853" alt="image" src="https://github.com/user-attachments/assets/96ca34e9-8241-4b11-884f-0e8310f03ffd" />

<img width="793" height="866" alt="image" src="https://github.com/user-attachments/assets/0edbc525-8817-4d8c-9d23-ef38e61d4334" />

<img width="800" height="876" alt="image" src="https://github.com/user-attachments/assets/35c31ea8-25c7-48f1-a931-a87d428c64c4" />

## Project Structure  
```
carpool-platform/
├── backend-springboot/
│ ├── src/main/java/com/carpool/
│ │ ├── controller/ # REST API endpoints
│ │ ├── service/ # Business logic
│ │ ├── repository/ # MyBatis data access
│ │ ├── model/ # Entity classes
│ │ ├── dto/ # Data transfer objects
│ │ └── config/ # CORS, WebSocket config
│ └── src/test/java/ # Unit tests
├── frontend-uniapp/ # UniApp mobile client
├── selenium_tests/ # Functional test scripts
└── locust_tests/ # Load testing scripts
```

## Acknowledgments  
This project was developed as part of a Software Engineering course. It demonstrates the full lifecycle of a real‑world application—from requirements analysis and UML modeling to implementation, testing, and documentation. Special thanks to the team for their collaboration and dedication.
