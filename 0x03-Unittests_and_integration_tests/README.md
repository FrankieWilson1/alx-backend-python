# 0x03-Unittests_and_integration_tests Project Overview 

This project focuses on demonstrating fundamental concepts of Unit Testing and Integration Testing in Python. It involves creating a GithubOrgClient class to interact with the GitHub API and thoroughly testing its functionality using various mocking techniques. 

The primary goal is to showcase best practices in testing, including: 
1. Writing comprehensive unit tests for individual components.
2. Implementing integration tests to verify interactions with external services (mocked here).
3. Utilizing Python's unittest module effectively.
4. Leveraging the unittest.mock library for isolating code during testing.
5. Employing parameterized for data-driven tests.

Key Concepts Demonstrated 

- **Unit Testing**: Testing isolated functions and methods (e.g., access_nested_map, GithubOrgClient.org). 
- **Integration Testing**: Testing the interaction between GithubOrgClient and a mocked external dependency (requests.get). 
- **Mocking**: Using unittest.mock.patch, Mock, and PropertyMock to simulate external API calls and control dependencies. 
- **Parameterization**: Writing a single test method that can be run with multiple sets of inputs and expected outputs using parameterized. 
- **Memoization**: (Implemented in utils.py) Caching results of expensive function calls. 

Project Structure 

- **client.py**: Contains the GithubOrgClient class that interacts with GitHub organization data. 
- **utils.py**: Provides utility functions like get_json, access_nested_map, and memoize. 
- **test_client.py**: Contains all the unit and integration tests for the GithubOrgClient class. 
- **test_utils.py**: Contains unit tests for the functions in utils.py. 
- **fixtures.py**: (Optional/Dynamic) Holds test data (payloads, expected results) used in integration tests. 

Setup and Installation 

To get this project running locally, follow these steps: 
1. Clone the repository:  
   Bash 
   ```bash
   git clone https://github.com/FrankieWilson1/alx-backend-python.git
   cd 0x03-Unittests_and_integration_tests 
