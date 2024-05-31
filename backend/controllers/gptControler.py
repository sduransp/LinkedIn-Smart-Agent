# importing libraries
import os
from openai import AzureOpenAI
import re
import yaml

def load_requirements(config_path='config/requirements.yaml'):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config['employee_requirements']

def extract_score(response):
    """
    Extracts the first floating-point number that appears in the response.
    Assumes the number is formatted as a decimal between 0 and 1.

    Parameters:
    response (str): The text response from which to extract the score.

    Returns:
    float: The first decimal number found in the response, or None if no match is found.
    """

    match = re.search(r'\b0?\.\d+\b', response)
    if match:
        return float(match.group())
    else:
        return None

def company_evaluation(requirements:str, company_description:str)-> float:
    """
        Evaluates how closely a company's LinkedIn description matches a given profile
        description using GPT-4 Turbo model provided by Azure.

        Parameters:
        requirements (str): The target profile description of the desired company.
        company_description (str): The actual LinkedIn description of the company to evaluate.

        Returns:
        float: A compatibility score between 0.0 and 1.0 indicating the match level.
    """

    client = AzureOpenAI(
        api_version = os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_KEY")
    )

    message_text=[{
        "role":"system",
        "content":(f"""
                    Given the desired company profile description and a specific company's description from LinkedIn, determine how well the company matches the desired profile. 
                   The input consists of two parts: the target profile description, which outlines the characteristics and qualities of the ideal company, and the actual company description from LinkedIn.

                    Input:

                    Target Profile Description: {company_description}
                    Actual Company Description: {requirements}

                    Task:
                    Evaluate how closely the actual company description matches the target profile description. Return a compatibility score ranging from 0 to 1, where 0 indicates no suitability and 1 indicates total suitability. 
                    In addition, return also a brief explanation of this decision.
                    Consider factors like industry relevance, company size, value alignment, and any specified attributes in your assessment.

                    Output:
                    A single floating-point number representing the compatibility score.

                   """
        )
    }]

    chat_completion = client.chat.completions.create(
        model="gpt4-turbo",
        messages = message_text,
        temperature=0.0
    )
    
    response = chat_completion.choices[0].message.content
    score = extract_score(response)

    return(score, response)

def employee_evaluation(employee_name: str, employee_position: str, employee_education: list) -> float:
    """
        Evaluates how closely an employee's profile matches a given target profile using GPT-4 Turbo model provided by Azure.

        Parameters:
        requirements (str): The target profile description of the desired employee.
        employee_name (str): The name of the employee.
        employee_position (str): The position/job title of the employee.
        employee_education (list): The educational background of the employee.

        Returns:
        float: A compatibility score between 0.0 and 1.0 indicating the match level.
    """
    # Load the requirements from the YAML configuration file
    client = AzureOpenAI(
        api_version = os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_KEY")
    )
    # Initialize the Azure OpenAI client
    employee_education_str = ", ".join(
        [f"{edu.institution_name}: {edu.degree}" for edu in employee_education]
    )
    # Format the employee's education details
    requirements = load_requirements()

    # Prepare the message for the GPT-4 model
    message_text = [{
        "role": "system",
        "content": (f"""
                    Given the desired employee profile description and a specific employee's details, determine how well the employee matches the desired profile. 
                    The input consists of two parts: the target profile description, which outlines the characteristics and qualities of the ideal employee, and the actual employee's details.

                    Input:

                    Target Profile Description: {requirements}
                    Actual Employee Details: 
                    - Name: {employee_name}
                    - Position: {employee_position}
                    - Education: {employee_education_str}

                    Task:
                    Evaluate how closely the actual employee details match the target profile description. Return a compatibility score ranging from 0 to 1, where 0 indicates no suitability and 1 indicates total suitability.
                    In addition, return a brief explanation of this decision.
                    Consider factors like job relevance, educational background, skills, and any specified attributes in your assessment.

                    Output:
                    A single floating-point number representing the compatibility score.
                   """
        )
    }]
    # Get the response from the GPT-4 model
    chat_completion = client.chat.completions.create(
        model="gpt4-turbo",
        messages=message_text,
        temperature=0.0
    )

    response = chat_completion.choices[0].message["content"]
    score = extract_score(response)

    return score, response
    

if __name__ == "__main__":

    company_requirements= "I am looking for a company related to the construction industry with a large reputation."
    company_description = """
        Our purpose is to improve society by considering social outcomes in everything we do, relentlessly focusing on excellence and digital innovation, transforming our clients’ businesses, our communities and employee opportunities.

        Partnering with our clients, we are solving the world's most intricate challenges. We search out the connections others fail to make, to unlock creativity and deliver better outcomes for the lives we touch every day.

        Website
        http://mottmac.com
        Industry
        Civil Engineering
        Company size
        10,001+ employees
        22,386 associated members LinkedIn members who’ve listed Mott MacDonald or its subsidiaries (Habtec Mott MacDonald, Cambridge Education, and 4 other companies) as their current workplace on their profile.
        Headquarters
        Croydon, London
        Specialties
        Buildings, Education, Environment, Health, Industry, Infrastructure finance, International development, Oil & gas, Transportation, Water & wastewater, Climate resilience, Urbanisation, Social outcomes, Digital transformation, Smart infrastructure, Renewable energy, Energy, and Infrastructure epidemiology

        """
    score,response = company_evaluation(requirements=company_requirements, company_description=company_description)
    print(score)
    