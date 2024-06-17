# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from routes.linkedinRouter import router as status_router
from models.linkedin import TextInput
from controllers import linkedinControler
from controllers.companyScrapper import Company

# Initialize FastAPI app
main_app = FastAPI(docs_url="/", debug=True)

def convert_to_dict(obj):
    """
    Convert an object to a dictionary if it is an instance of a known class.
    Args:
        obj (object): The object to convert.    
    Returns:
        dict: The dictionary representation of the object.   
    Raises:
        TypeError: If the object is not an instance of a known class.
    """
    if isinstance(obj, Company):
        return obj.to_dict()
    # Add other conversions if necessary
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# Adding a CORS middleware
def add_cors_middleware(application: FastAPI) -> None:
    """
    Add CORS middleware to the FastAPI application.
    This function adds CORS (Cross-Origin Resource Sharing) middleware to the given
    FastAPI application, allowing specified origins, credentials, methods, and headers.
    Args:
        application (FastAPI): The FastAPI application instance to which the middleware will be added.  
    Returns:
        None
    """
    origins = [
        "http://localhost:3000",
        "http://localhost:3125",
        "http://0.0.0.0",
        "http://0.0.0.0:8000",
        "http://127.0.0.1:8000"
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

# Building the app
def build_app() -> FastAPI:
    """
    Build and configure the FastAPI application.
    This function creates a FastAPI application, adds CORS middleware, and includes
    the necessary routers.
    
    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    # Initialize the main FastAPI application instance
    add_cors_middleware(main_app)
    
    # Include the status router
    main_app.include_router(status_router)
    
    return main_app

# Initialize the app
main_app = build_app()

# API Endpoints
@main_app.post("/clients")
def get_potential_customers(text: TextInput):
    """
        Endpoint to get potential customers based on text input.
        
        This function logs into LinkedIn, lists companies, evaluates and filters them, 
        scrapes and selects employees, and saves the results locally.
        
        Args:
            text (TextInput): The input text containing requirements.
            
        Returns:
            dict: A dictionary containing parsed databases and selected entities.
    """
    # login
    driver = linkedinControler.login()
    print("Logged in")
    # Listing all companies
    print("Listing companies")
    companies_url = linkedinControler.company_listing(driver=driver, n_pages=20)
    # Scrapping, evaluating and filtering companies based on a given threshold
    print("Starting company evaluation")
    companies_db, selected_companies = linkedinControler.company_orchestrator(driver=driver, companies=companies_url, requirements=text.text, threshold=0.6)
    # Scraping, evaluating and selecting right employees to contact
    print("Starting employee evaluation")
    employees_db, selected_employees = linkedinControler.employee_orchestrator(driver=driver, selected_companies=selected_companies, threshold=0)
    # Saving everything locally for evaluation
    os.makedirs('tests', exist_ok=True)
    # Parsing data
    companies_db_parsed = {cmp: linkedinControler.company_parser(companies_db[cmp]) for cmp in companies_db}
    selected_companies_parsed = {cmp: linkedinControler.company_parser(selected_companies[cmp]) for cmp in selected_companies}
    employee_db_parsed = {
    cmp: {emp_name: linkedinControler.person_parser(employee) for emp_name, employee in employees_db[cmp].items()}
        for cmp in employees_db
    }
    selected_employee_parsed = {
        cmp: [linkedinControler.person_parser(employee) for employee in selected_employees[cmp]]
        for cmp in selected_employees
    }

    # Saving locally
    with open(os.path.join('tests', 'companies_db.json'), 'w', encoding='utf-8') as f:
        json.dump(companies_db_parsed, f, ensure_ascii=False, indent=4, default=convert_to_dict)
    with open(os.path.join('tests', 'selected_companies.json'), 'w', encoding='utf-8') as f:
        json.dump(selected_companies_parsed, f, ensure_ascii=False, indent=4, default=convert_to_dict)
    with open(os.path.join('tests', 'employees_db.json'), 'w', encoding='utf-8') as f:
        json.dump(employee_db_parsed, f, ensure_ascii=False, indent=4, default=convert_to_dict)
    with open(os.path.join('tests', 'selected_employees.json'), 'w', encoding='utf-8') as f:
        json.dump(selected_employee_parsed, f, ensure_ascii=False, indent=4, default=convert_to_dict)

    # Stop driver
    driver.quit()

    return {"selected_companies": selected_companies_parsed, "selected_employees": selected_employee_parsed}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8000)