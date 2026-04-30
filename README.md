# API Automation Testing Suite – FakeStore API

## What is this?

This project is an automated API testing suite built with Python, Pytest, and Requests, designed to validate the functionality and reliability of the [FakeStore API](https://fakestoreapi.com) — a public REST API that simulates an e-commerce platform.

---

## Product / Feature Under Test

The following endpoints of the FakeStore REST API were tested, covering authentication and full CRUD operations:

![AUTH](https://img.shields.io/badge/AUTH-Login-purple)
![GET](https://img.shields.io/badge/GET-Fetch%20Data-brightgreen)
![POST](https://img.shields.io/badge/POST-Create%20Resource-00bcd4)
![PUT](https://img.shields.io/badge/PUT-Full%20Update-ffeb3b)
![PATCH](https://img.shields.io/badge/PATCH-Partial%20Update-orange)
![DELETE](https://img.shields.io/badge/DELETE-Delete%20Resource-red)

Endpoints covered:
- `/auth/login` — Authentication
- `/users` — Users
- `/products` — Products
- `/carts` — Carts

---

## Objective

The objective of this project was to validate the correct behavior of the FakeStore API by testing its CRUD operations and authentication endpoint against both valid and invalid inputs.

This included verifying that the API honors its contract — meaning that responses follow the expected structure, status codes, and data types — since a broken contract between frontend and backend can silently introduce bad data into a system and cause serious issues down the line. Additionally, the suite was designed to probe the API's robustness when faced with unexpected inputs, missing fields, or edge case scenarios.

---

## Scope

### Included:
- Full CRUD testing (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) for `/users`, `/products`, and `/carts`
- Authentication testing via `/auth/login`
- Positive, negative, boundary, and exploratory test scenarios
- Validation of response status codes, response structure, and API contract consistency

### Not included:
- Products nested inside carts (`products` within `/carts`), since that behavior is already covered through the `/products` endpoint
- Deep authentication validation, as FakeStore API does not implement real authorization — any token is accepted regardless of validity
- Performance or load testing, as the scope was limited to functional validation only

---

## Project Structure / Artifacts
```
FakestoreAPI_automated_testing_suite/
├── tests/
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_products.py
│   └── test_carts.py
├── utils/
│   ├── api_client.py
│   ├── data.py
│   └── helpers.py
├── conftest.py
├── report.html
├── requirements.txt
└── .gitignore
```

The suite is organized in a modular way to keep responsibilities separated and make it easier to maintain and scale over time.

- **Test Layer** (`/tests`): Contains all test files, one per endpoint — `test_auth.py`, `test_users.py`, `test_products.py`, and `test_carts.py`. Each file covers its respective resource across multiple scenarios.
- **API Client Layer** (`utils/API_client.py`): Centralizes all HTTP requests using the Requests library. Rather than calling the API directly inside test files, all requests are wrapped into reusable methods.
- **Data Layer** (`utils/data.py`): Stores payloads and test data used across multiple test cases, keeping test files cleaner and easier to read.
- **Helper Layer** (`utils/helpers.py`): Contains auxiliary functions reused throughout the suite, reducing duplication and keeping test logic focused on behavior.
- **Session Config** (`conftest.py`): Handles session setup and base URL configuration for the entire suite.
- **Report** (`report.html`): Auto-generated HTML test report produced by `pytest-html` after each run.
- **Dependencies** (`requirements.txt`): Lists all required packages to run the project.

---

## Key Decisions

- **Creation and retrieval were prioritized** (`POST` and `GET`) because getting data into and out of the system correctly is fundamental. If the API accepts invalid data or returns an inconsistent structure, it breaks the contract with the frontend and can corrupt the system silently over time.
- **Update operations were also emphasized** (`PUT`/`PATCH`) due to their direct impact on data consistency and integrity.
- **Authentication testing was limited by design**, since FakeStore API doesn't implement real auth — the endpoint was tested for surface-level behavior and error handling rather than actual security validation.
- **Edge cases were included** to assess the API's robustness, though with less emphasis than the core CRUD flows. The goal was to document how the system behaves under unexpected conditions, not necessarily to assert correctness where the API has no defined behavior.
- **A modular project structure was adopted** to separate test logic from API calls and helper utilities, making the suite more maintainable and reducing code duplication.

---

## Results

![Tests](https://img.shields.io/badge/Tests-198-blue)
![Passed](https://img.shields.io/badge/Passed-81-brightgreen)
![XFailed](https://img.shields.io/badge/Expected%20Failures-117-yellow)
![Failed](https://img.shields.io/badge/Failed-0-brightgreen)
![Errors](https://img.shields.io/badge/Errors-0-brightgreen)
![Duration](https://img.shields.io/badge/Duration-3m%2001s-lightgrey)

The suite ran 198 tests across all four endpoints with no unexpected failures or errors. The 117 expected failures (`xfail`) were intentionally marked to document known API limitations and inconsistencies rather than block the suite.

### Bugs & Findings

**Bug 1 — Server crash on invalid auth payload**
Sending an incorrect credentials payload to `/auth/login` causes the server to crash with a 5xx error (524/527) instead of returning a `401 Unauthorized`. This suggests a lack of error handling at the server level.

**Bug 2 — Missing input validation on POST and PUT**
Most scenarios involving missing fields or incorrect data formats on resource creation and updates return `200 OK` instead of `400 Bad Request`. The API accepts and processes invalid data without any complaint.

**Bug 3 — Inconsistent DELETE responses**
When deleting a resource, the API returns the deleted object as if it were a `GET` response, instead of an empty body or a confirmation message — contradicting the documented behavior.

**Bug 4 — HTML responses instead of JSON**
In some instances, the API returns broken HTML instead of a JSON response, directly violating the expected API contract.

---

## What Would I Improve Next?

The main thing I would improve is the debugging workflow. Manually adding `print(response.text)` to each test in order to inspect server responses was time-consuming given the volume of cases. Going forward, I would implement structured logging or a pytest fixture that automatically captures and logs responses, making it significantly faster to identify issues without having to instrument each test individually.

---

## Tools Used

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-gray?style=flat)
![pytest--html](https://img.shields.io/badge/pytest--html-report-orange?style=flat)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white)

---

## Testing Types & Methodology

![Functional](https://img.shields.io/badge/Functional%20Testing-blue)
![Edge Cases](https://img.shields.io/badge/Edge%20Cases-blueviolet)
![Boundary](https://img.shields.io/badge/Boundary%20Testing-9cf)
![Negative](https://img.shields.io/badge/Negative%20Testing-red)
![Data Validation](https://img.shields.io/badge/Data%20Validation-yellow)
![Test Case Design](https://img.shields.io/badge/Test%20Case%20Design-lightgrey)
![Test Automation](https://img.shields.io/badge/Test%20Automation-darkgreen)
![Test Execution](https://img.shields.io/badge/Test%20Execution-lightblue)

---

## How to Run the Tests

1. Clone the repository:
```bash
   git clone https://github.com/alejandrog-gutierrez/FakestoreAPI_automated_testing_suite.git
   cd FakestoreAPI_automated_testing_suite
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run the test suite and generate the HTML report:
```bash
   pytest --html=report.html
```

The `report.html` file will be generated in the root of the project with the full test results.
