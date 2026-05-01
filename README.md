# API Automation Testing Suite – FakeStore API

## What is this?

This project is an automated API testing suite built with Python, Pytest, and Requests, designed to validate the functionality and reliability of the [FakeStore API](https://fakestoreapi.com) — a public REST API that simulates an e-commerce platform.

---

## Product / Feature Under Test

The following endpoints of the FakeStore API were tested, covering login and token retrieval via authentication, and full CRUD operations — create, read, replace, and delete — across users, products, and carts.

![AUTH](https://img.shields.io/badge/AUTH-Login-purple)
![GET](https://img.shields.io/badge/GET-Fetch%20Data-brightgreen)
![POST](https://img.shields.io/badge/POST-Create%20Resource-00bcd4)
![PUT](https://img.shields.io/badge/PUT-Full%20Update-ffeb3b)
![DELETE](https://img.shields.io/badge/DELETE-Delete%20Resource-red)

Endpoints covered:
- `/auth/login` — Authentication
- `/users` — Users
- `/products` — Products
- `/carts` — Carts

---

## Objective

The objective of this project was to validate the correct behavior of the FakeStore API by testing its CRUD operations and authentication endpoint against both valid and invalid inputs.
A key focus was verifying that the API honors its contract — meaning that responses follow the expected structure, status codes, and data types. This matters because a broken contract between frontend and backend can silently introduce bad data into a system, leading to integrity issues and a poor user experience down the line.

The suite also evaluates how consistently and reliably the API handles the inputs passed to it — whether those come from an expected user flow or an edge case — and documents how the system behaves under conditions it may not handle gracefully

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

### Notes:
- `POST`, `PUT`, `PATCH`, and `DELETE` operations are simulated — FakeStore API returns mocked success responses without actually persisting changes. These endpoints were still tested to validate how the system responds to both valid and invalid inputs against those mocked behaviors.

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
- **Helper Layer** (`utils/helpers.py`): Contains auxiliary functions reused throughout the suite, including all assertions for response structure and content validation across each test case. This keeps test logic clean and avoids duplicating assertion code.
- **Session Config** (`conftest.py`): Handles session setup and base URL configuration for the entire suite.
- **Report** (`report.html`): Auto-generated HTML test report produced by `pytest-html` after each run.
- **Dependencies** (`requirements.txt`): Lists all required packages to run the project.

---

## Key Decisions

- **Retrieval was the top priority** (`GET`) — ensuring the system returns valid, well-structured data is the foundation of the suite. Responses were strictly validated against the documented API contract: if the structure, fields, or data types didn't match what the API promises, the test fails.
- **Creation was equally prioritized** (`POST`) — the contract must be strict in both directions. The API should accept and reflect back data exactly as documented, no more, no less.
- **Update operations were included** (`PUT`) but with more flexibility, as behavior showed discrepancies during testing. See the Results section for details.
- **Delete operations were tested with less rigor**, as the endpoint logic was straightforward — but it produced some of the most interesting and unexpected behaviors observed in the suite. See the Results section for details.

---

## Results

![Tests](https://img.shields.io/badge/Tests-198-blue)
![Passed](https://img.shields.io/badge/Passed-81-brightgreen)
![XFailed](https://img.shields.io/badge/Expected%20Failures-117-yellow)
![Failed](https://img.shields.io/badge/Failed-0-brightgreen)
![Errors](https://img.shields.io/badge/Errors-0-brightgreen)
![Duration](https://img.shields.io/badge/Duration-3m%2001s-lightgrey)

The suite ran 198 tests across all four endpoints with no unexpected failures or errors. The 117 expected failures (xfail) were intentionally marked to document known API limitations and inconsistencies — every test under xfail failed due to discrepancies in status codes, response formats, or unexpected server behavior. Rather than leaving them as hard failures that block the suite, xfail was used to keep the run clean while preserving full visibility into what broke and why, with each case documented individually in the report to provide context behind the decision.

### Bugs & Findings

- `/auth/login` — Most consistent endpoint, but with notable edge case failures.
  Overall, the auth endpoint performed well under normal conditions — valid credentials return a token in JSON format as expected. One minor discrepancy: the documentation states `200 OK` on successful login, but the API returns `201 Created` instead. Not critical, but worth noting.
    - More interesting were the undocumented error responses. The API returns detailed messages not mentioned anywhere in the docs:
`400 — "username and password are not provided in JSON format" for malformed input`
`401 — "username or password is incorrect" for valid format but non-existent credentials`
The documentation only states that `400 Bad Request` should be returned with no body — so finding verbose, descriptive error messages was unexpected.
    - Bug — Server crash on string payload (`524 error`)
Sending a plain string instead of a JSON object as the payload caused the server to return a `524 error` — a Cloudflare timeout indicating the origin server crashed. This is the most critical finding in the suite: a single malformed input to the authentication endpoint — the front door of the platform — is enough to bring it down entirely instead of returning a controlled `400 response`.
<img width="1832" height="889" alt="image" src="https://github.com/user-attachments/assets/3e2d773f-955d-4624-84cf-97ba75362da6" />


- `/users` — Functional on happy path, inconsistent everywhere else.
Fetching all users and fetching by ID worked flawlessly. We located and validated John (user ID 1) and his complete data without issues. Valid edge case IDs (1, 2, 9, 10) all returned correct user structures with non-empty fields.
   - **GET** inconsistencies:

      - The id path parameter accepts any data type across all methods. Floats return `200` with a `null` body instead of `400`. Passing "a", True, or None returns an undocumented error message: `{"status":"error","message":"user id should be provided"}`. Empty string "" returns `404` with broken `HTML` instead of `400` in `JSON`.
      - Out-of-range and invalid IDs (-1, 0) return `200` with a `null` body instead of `400`. Out-of-bounds ID (11) returns `200` with `null` instead of `404`.

   - **POST** inconsistencies:

      - On successful creation, the API returns only `{ "id": 1 }` instead of the full user object as documented — the contract is broken on the happy path itself.
      - Missing fields, empty payload, and wrong payload (e.g. sending a product object instead of a user) all return `201 Created` instead of `400 Bad Request`.
      - No field format enforcement — passing wrong types for any field (e.g. integer for username, integer for email) still results in `201 Created`.
      - Junk data returns `400` with a broken `HTML` body instead of `JSON`.

   - **PUT** inconsistencies:

      - Notable behavior: unlike products, `PUT` on `users` uses the id from the request body rather than the path parameter — the opposite of what /products does. The returned id will differ from the path parameter id.
      - Empty payload returns `200` with an empty body `{}` instead of `400`.
      - Missing fields, wrong payload, and invalid field formats all return `200` instead of `400` — same lack of validation as `POST`.
      - Invalid IDs (-1, 0) return `200` with the full payload instead of `400`. Out-of-bounds ID (11) returns `200` instead of `404`.

   - **DELETE** inconsistencies:

      - Every delete request — valid or not — returns the full user object instead of an empty body, mirroring a GET response.
      - <img width="1833" height="278" alt="image" src="https://github.com/user-attachments/assets/c34a610d-933c-437c-8d07-5358c2e78d6b" />
      - Invalid IDs (-1, 0) return `200` with a `null` body instead of `400`. Out-of-bounds ID (11) returns `200` with `null` instead of `404` — this case also doubles as attempting to delete a non-existent user.
      - Float ID (25.5) returns `200` with null instead of an error.
      - Passing "a", True, None, or a full payload object surfaces the undocumented error: `{"status":"error","message":"user id should be provided"}` — not necessarily a bug, but completely absent from the documentation.
      - Empty string "" returns `404` with broken `HTML` instead of `400` IN `JSON`.


- `/products` — Solid happy path, poor input validation.
Fetching all products and fetching by ID worked correctly. The price field accepts both integers and floats despite the documentation specifying integers only — minor inconsistency but worth noting.
   - `GET` inconsistencies:

       - The id path parameter accepts any data type. Floats, booleans, and None return `200` instead of `400`. Passing an empty string "" returns the full product list — same as `GET /products`. Strings return a broken HTML 400.
       - Out-of-range and invalid IDs (-1, 0, non-existent) return `200` with a `null` body instead of `400/404`.

   - **POST** inconsistencies:

      - Missing fields, empty body, and wrong payload all return `201` Created instead of `400` Bad Request. The API creates the product regardless of what it receives.
      - No field format enforcement — passing wrong types for any field still results in `201 Created`.
      - Junk data returns `400` in broken `HTML`.
      - On successful creation, the response body contains the full product object — consistent with documentation.

   - **PUT** inconsistencies:

      - Mirrors `POST` behavior across the board.
      - Notable behavior: the API ignores the id in the request body entirely and uses the path parameter id instead.
      - True and None as path parameter return an undocumented error: `{"status":"error","message":"something went wrong! check your sent data"}`.
      - Empty string "" as path parameter returns `404` with broken `HTML` instead of `400 JSON`.

   - **DELETE** inconsistencies:

      - Every delete request — valid or not — returns the full product object as if it were a `GET` response, instead of an empty body.
      - Invalid IDs (-1, 0) return `200` with `1` in the body instead of `400`.
      - Non-existent ID (21) doubles as a delete of already-deleted resource — returns `200` with `1` in body instead of `404`.
      - Passing "a", True, None, or a full payload object surfaces an undocumented error: `{"status":"error","message":"product id should be provided"}` — not a bug per se, but entirely undocumented.
      - Empty string "" returns `404` with broken `HTML` instead of `400` in `JSON`.
  <img width="1823" height="398" alt="image" src="https://github.com/user-attachments/assets/207caf26-7b04-49d8-9b20-390fd6cd69e1" />
<img width="1825" height="389" alt="image" src="https://github.com/user-attachments/assets/b35e06b3-8e29-4b02-a148-99fab13b251d" />
    
- **`/carts` — Functional but incomplete dataset, consistent validation failures**
  Fetching all carts and fetching by ID worked correctly for the first 7 carts. Two undocumented fields were found in the response body (`date` and `__v`) — not a bug, but worth noting. Products inside carts only contain `productId` and `quantity` instead of the full product object described in the documentation.

  A critical data inconsistency was discovered: the documentation states the API has 20 carts, but carts 8 through 20 return `200 OK` with a `null` body — meaning only 7 carts actually exist. This affects edge case validation for IDs 19 and 20, which were expected to return valid cart data but returned `null` instead.

  - **GET**
    - Invalid IDs (`-1`, `0`) return `200` with `null` instead of `400`. Out-of-bounds ID (`21`) returns `200` with `null` instead of `404`.
    - Float ID (`25.5`) returns `200` with `null` instead of `400`.
    - Empty string `""` returns the full cart list — same as `GET /carts` — instead of `400`.
    - `"a"`, `True`, and `None` return an undocumented error message: `{"status":"error","message":"cart id should be provided"}` with a `400` status — correct code, but completely absent from the documentation.

  - **POST**
    - On creation, the API returns `id: 11` instead of a value above 20, confirming only 7 carts exist despite the documentation claiming 20.
    - Missing `userId`, missing `products`, empty payload, and wrong payload all return `201 Created` instead of `400 Bad Request` — the API creates the cart regardless of what it receives.
    - Junk data returns `400` with a broken HTML body instead of JSON — status code is correct, but the format is not.

  - **PUT**
    - Happy path and valid edge cases (IDs 1, 2, 19, 20) work correctly — the API returns the updated cart with the correct structure.
    - Invalid IDs (`-1`, `0`) return `200` instead of `400`. Out-of-bounds ID (`21`) returns `200` instead of `404`.
    - Float ID (`25.5`) is treated as a valid integer and returns `200`.
    - Empty string `""` returns an error in HTML — inconsistent with the expected JSON format.
    - Empty payload and wrong schema both return `200` with `{ "id": 1 }` instead of `400`.
    - Junk data returns `400` in broken HTML — status is correct, format is not.
    - `"a"`, `True`, and `None` surface an undocumented error: `{"status":"error","message":"something went wrong! check your sent data"}` with a correct `400` status.

  - **DELETE**
    - Valid IDs 1 and 2 return the full cart object instead of an empty body. IDs 19 and 20 return `null` — consistent with the missing cart data issue found in GET.
    - Invalid IDs (`-1`, `0`) return `200` with `null` instead of `400`. Out-of-bounds ID (`21`) returns `200` with `null` instead of `404`.
    - Float ID (`25.5`) is treated as valid, returning `null` with `200`.
    - Empty string `""` returns a broken HTML error — not strictly a bug, but not JSON.
    - `"a"`, `True`, and `None` return the undocumented error: `{"status":"error","message":"cart id should be provided"}` with a correct `400` status.
    - Passing a full payload object as the ID also returns `400` with a valid JSON error — undocumented but arguably correct behavior.

---

## Documentation
The following test case and bug report serve as examples of how the full suite would be documented. Each test case and bug found during execution follows this same structure.

- Test cases (example)
  
<img width="1287" height="114" alt="image" src="https://github.com/user-attachments/assets/0087ce57-7535-4fa5-a3ec-1659026b1835" />


- Bug report (example)
  
<img width="702" height="780" alt="image" src="https://github.com/user-attachments/assets/04fdb70c-d2d8-461f-96f5-0150c7e3af74" />

---


## What Would I Improve Next?

The main thing I would improve is the debugging workflow. Manually adding `print(response.text)` to each test in order to inspect server responses was time-consuming given the volume of cases. Going forward, I would implement structured logging or a pytest fixture that automatically captures and logs responses, making it significantly faster to identify issues without having to instrument each test individually.

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
