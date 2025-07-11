# Family Weight Tracker

A lightweight Flask web application to log and view daily weight entries for family members. Data is stored securely in a local Microsoft SQL Server database using Windows Authentication.

---

## 🧰 Features

- Input weight records for each family member (Ehsan, Mahtab, Leon)
- Display recent measurements in an easy-to-read table
- Flash messages confirm successful entries or show errors
- Local SQL Server integration with secure configuration

---

## 🏗️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML + inline CSS (using Jinja2 templates)
- **Database:** Microsoft SQL Server (accessed via `pyodbc`)
- **Libraries:** Flask, pyodbc, pandas, numpy

---

## 🖥️ Screenshots

![App UI - Input Form](./images/Screenshot%202025-07-08%20215518.png)

![App UI - Table View](./images/Screenshot%202025-07-08%20222304.png)


---

## 🧪 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt

