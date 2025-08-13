# CSRS Automated Assessment

> **Automated assessment platform** for programming coursework within the Coursework Submission and Review System (**CSRS**).  
> Built with **Next.js**, **Flask**, **SQLite**, and **Docker**, featuring an **autograder**, REST API, and responsive web UI.

---

## 📌 Overview

Marking programming assignments at scale is time-consuming and error-prone.  
**CSRS Automated Assessment** streamlines this process by:

- Automatically compiling and testing student submissions.
- Comparing submissions against skeleton code.
- Providing instant feedback and structured reports to markers.
- Integrating seamlessly into the existing CSRS platform.

The system supports configurable marking workflows, reducing manual work for staff and improving consistency across markers.

---

## 🚀 Features

- **Autograder Pipeline** — Automatically compile, run tests, and analyse submissions.
- **Next.js Frontend** — Interactive UI for markers and admins.
- **Flask API** — Backend service to manage submission processing and results.
- **SQLite Database** — Lightweight storage for test results and metadata.
- **Dockerised Deployment** — Reproducible environments for local dev and production.
- **Configurable Workflows** — Module organisers can define marking steps per assignment.
- **Feedback Reports** — Generate structured feedback alongside grades.

---

## 🛠 Tech Stack

| Layer        | Technology |
|--------------|------------|
| **Frontend** | Next.js (React), TypeScript |
| **Backend**  | Flask (Python) |
| **Database** | SQLite |
| **Container**| Docker |
| **CI/CD**    | GitHub Actions |
| **Testing**  | Pytest (backend), Jest (frontend) |

---

## 📂 Repository Structure

```plaintext
src/
  frontend/       # Next.js app
  backend/        # Flask API and grading logic
  tests/          # Unit & integration tests
Dockerfile
docker-compose.yml
requirements.txt
package.json
```

---

## 🖥️ Getting Started

### Prerequisites
- **Node.js** >= 18.x
- **Python** >= 3.10
- **Docker** & **Docker Compose**

### Clone the Repository
```bash
git clone https://github.com/shimson94/csrs-automated-assessment.git
cd csrs-automated-assessment
```

### Local Development (Docker)
```bash
docker-compose up --build
```

Frontend: http://localhost:3000  
Backend API: http://localhost:5000

### Local Development (Manual)
1. **Backend**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    flask run
    ```
2. **Frontend**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## 📸 Screenshots

*(Add `/docs/screenshots/` images here once ready)*

---

## 🧪 Running Tests

**Backend**
```bash
cd backend
pytest
```

**Frontend**
```bash
cd frontend
npm test
```

---

## 📈 Roadmap

- [ ] Multi-language grading support (Java, C++)  
- [ ] Role-based access control (RBAC)  
- [ ] Rich analytics dashboard for markers and admins  
- [ ] Integration with external LMS APIs  

---

## 🏗 Architecture

Initial high level system design
![image](https://github.com/user-attachments/assets/6cbc2086-60fe-47e4-ae61-758e78076dd8)
```
- **Student** uploads code via the submission handler.
- Submissions are stored in distributed storage.
- A **messaging queue** coordinates containerised execution engines.
- The **server** runs grading in isolated containers and stores results.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Muzammil Hashim Chaudry**  
[GitHub](https://github.com/shimson94) | [LinkedIn](https://www.linkedin.com/in/hashim-chaudry/)
