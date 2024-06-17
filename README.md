# linkedin-agent

This is an AI agent for identifying and contacting potential clients on LinkedIn. It automates the process of navigating through LinkedIn search result pages, extracting company and employee information, and allowing users to send messages to potential clients.

## Features

- **Automated Search**: Automatically searches for companies on LinkedIn based on user input.
- **Pagination Handling**: Navigates through multiple pages of search results.
- **Data Extraction**: Extracts company and employee information including name, position, and LinkedIn profiles.
- **Company Evaluation**: Evaluates each company based on the company description and the search criteria, selecting the most suitable companies for contacting.
- **Employee Evaluation**: Evaluates employees deciding whether it is a suitable employee for contacting.
- **Messaging**: Provides functionality to send messages to potential clients directly from the app.

## Installation

To set up and run the LinkedIn agent locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/linkedin-agent.git
    cd linkedin-agent
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory of your project and add the following variables:
    ```
    LINKEDIN_USERNAME=your_linkedin_username
    LINKEDIN_PASSWORD=your_linkedin_password
    ```

4. **Run the application**:
    ```sh
    python app.py
    ```

## Usage

1. **Search for Companies**:
    - Enter a description of your target company in the search bar and click the search icon.
    - The application will navigate through LinkedIn search results, extracting relevant data.

2. **View Results**:
    - Click on a company card to view detailed information about the company.
    - Click on employee cards within the company details to view detailed information about the employees.

3. **Send Messages**:
    - Use the "Send Message" button within the employee details modal to send a message directly.

## Development

### Prerequisites

- Python 3.x
- Node.js and npm (for frontend development)
- Selenium WebDriver

### Setting up the Development Environment

1. **Install Frontend Dependencies**:
    ```sh
    cd frontend
    npm install
    ```

2. **Run the Frontend Development Server**:
    ```sh
    npm start
    ```

3. **Run the Backend Development Server**:
    ```sh
    python app.py
    ```

### Running Tests

To run tests for the application, use the following command:
```sh
pytest
