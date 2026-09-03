# Public Transit Agency Management System

A web application developed to model and manage core operations of a public transit agency, including passenger services, route scheduling, pricing, user management, and administrative workflows.

The project was built as an academic software engineering exercise focused on backend development, modular architecture, database integration, and web application design.

---

## 🚍 Main Features

### Passenger Module
- User registration and authentication
- View available transportation services
- Consult routes and schedules
- View pricing information
- Register service purchases
- Access personal service history

### Administration Module
- Administrative access
- Passenger activity monitoring
- Service price management
- Route and service administration

### Service Scheduling
- Create and manage transportation services
- Assign vehicles and schedules
- Manage available routes
- Retrieve active vehicles from the database

---

## 🏗️ Architecture

The application is organized into a main web application and supporting service modules.

```text
DS_PublicTransitAgency/
├── main.py
├── logic/
│   ├── db.py
│   ├── usuario.py
│   └── MSpasajeros.py
├── MS-Programacion/
│   └── MSprogramacion.py
├── MS-mantenimiento/
│   └── MSmantenimiento.py
├── templates/
├── static/
└── requirements.txt
