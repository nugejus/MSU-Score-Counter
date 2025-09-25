# Score Counter – MSU Cabinet Grade Parser

## 📌 Overview
This project was developed as a **personal skill-development project**.  

The application connects to the **MSU online cabinet**, logs in with user credentials, fetches the student’s grade data, parses the HTML structure, and then calculates GPA using different grading schemes.  
It also provides a **Tkinter-based GUI** to make the interaction more user-friendly.

---

## 🎯 Objectives
- Strengthen practical experience in **software architecture** (MVP pattern with adapters, use cases, presenters, views).
- Gain hands-on knowledge of **Selenium** and **BeautifulSoup** for web scraping.
- Practice building a **deployable desktop application** with **PyInstaller**.
- Collect user feedback on **usability, readability, and convenience**, and improve accordingly.

---

## 🛠 Features
- **Login automation** with Selenium.
- **Grade fetching and parsing** using BeautifulSoup.
- **Multiple GPA schemes** (5.0, 4.5, 4.3 scale).
- **GUI interface** (Tkinter) with:
  - Login screen (with Exit option).
  - Grade list and GPA view.
  - “Diploma only” filter option.
  - Loading screens and error dialogs for better UX.

- **User feedback survey** conducted to gather improvement points.

---

## 📂 Project Structure
score_counter/
├─ adapter/ # Selenium client & BeautifulSoup parser
├─ domain/ # Core models (grades, GPA calculation)
├─ usecase/ # Application use cases (login, fetch, compute GPA)
├─ presenters/ # Connect use cases ↔ views
├─ views/ # Tkinter UI components (Login, Grades, Loading)
├─ test/ # Unit tests
├─ config.py # Configuration (URLs, options)
├─ app.py # Application entrypoint
└─ requirements.txt

