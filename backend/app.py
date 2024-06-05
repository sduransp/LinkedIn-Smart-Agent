# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.linkedinRouter import router as status_router
from models.linkedin import TextInput
from controllers import linkedinControler

# Initialize FastAPI app
main_app = FastAPI(docs_url="/", debug=False)

# Adding a CORS middleware
def add_cors_middleware(application:FastAPI) -> None:
    origins = [
        "http://localhost",
        "http://localhost:3125",
        "http://0.0.0.0"
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
    add_cors_middleware(main_app)
    main_app.include_router(status_router)
    return main_app

# Initialize the app
main_app = build_app()

# API Endpoints
@main_app.post("/clients")
def get_potential_customers(text: TextInput):
    # login
    driver = linkedinControler.login()
    print("Logged in")
    # Listing all companies
    print("Listing companies")
    companies_url = linkedinControler.company_listing(driver=driver, n_pages=1)
    # Scrapping, evaluating and filtering companies based on a given threshold
    print("Starting company evaluation")
    companies_db, selected_companies = linkedinControler.company_orchestrator(driver=driver, companies=companies_url, requirements=text.text, threshold=0.6)
    print(f"The selected companies are: {selected_companies}")
    # Scraping, evaluating and selecting right employees to contact
    print("Starting employee evaluation")
    employees_db, selected_employees = linkedinControler.employee_orchestrator(driver=driver, selected_companies=selected_companies, threshold=0)
    print(f"The selected employees are: {selected_employees}")
    return {"companies_db": companies_db, "selected_companies": selected_companies, "employees_db": employees_db, "selected_employees": selected_employees}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8000)