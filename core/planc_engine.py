from google import genai
from pydantic import BaseModel, Field
from core import utils
import asyncio
from pathlib import Path
from typing import Optional
import json

# GEMINI_API_KEY = utils.get›_gemini_api_key()
TEST_MODEL = "gemini-2.0-flash-lite"
PARSE_MODEL = "gemini-2.0-flash"
RESUME_TEXT_PATH = utils.get_resume_text_path()

class Test(BaseModel):
    response: str

class education(BaseModel):
    """ Represents an education entry in the resume """
    degree: str
    institution: str
    gpa: Optional[str]    ## GPA is optional, can be None if not applicable
    start_date: str
    end_date: str

class career(BaseModel):
    """ Represents a career entry in the resume """
    title: str
    company: str
    start_date: str
    end_date: str
    description: str

class projects(BaseModel):
    title: str
    description: str
    url: Optional[str] = None  # url is optional, can be None if not applicable)

class Resume(BaseModel):
    """ Represents a resume with various fields """
    name: str
    email: list[str]
    phone: list[str]
    skills: list[str]
    education: list[education]
    career: list[career]
    accomplishments: list[str]
    projects: list[projects]

class CoverLetter(BaseModel):
    date: str
    company: str
    address: str
    hiring_manager: str = Field(
        default="Dear Hiring Manager",
        description="Full salutation (e.g., 'Dear Ms. Johnson') if known. Else, use 'Dear Hiring Manager'."
    )
    body: str
    user_name: Optional[str] = Field(
        default=None,
        description="User's full name. Leave blank (None) if not available — DO NOT fabricate."
    )
    user_email: str
    user_phone: str

class JobDescription(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[str] = Field(
        default=None,
        description="The job type such as Full-time, Part-time, Contract, or Internship. Can be inferred from context."
    )
    responsibilities: list[str]
    qualifications: list[str]
    preferred_qualifications: Optional[list[str]] = None
    skills_required: list[str] = Field(
        ...,
        description="Explicitly mentioned hard or soft skills. Should not include generic qualities unless clearly labeled as skills."
    )
    experience_level: Optional[str] = Field(
        default=None,
        description="Required experience level (e.g., '3+ years', 'Senior', 'Entry-level'). Often phrased variably in JD."
    )
    salary_range: Optional[str] = Field(
        default=None,
        description="Salary details as-is from the JD (e.g., '$90K–$120K', 'Competitive'). Leave None if not present."
    )
    benefits: Optional[list[str]] = None
    application_deadline: Optional[str] = Field(
        default=None,
        description="Deadline for applying (e.g., 'Apply by July 12', 'Closes in 2 weeks')."
    )
    job_posting_url: Optional[str] = None
    summary: Optional[str] = Field(
        default=None,
        description="summary of the job description in plain language. Includes role, top responsibilities, and alignment hints."
    )



def get_gemini_client():
    api_key = utils.get_gemini_api_key()
    return genai.Client(api_key=api_key)

def load_prompt(path: str, **kwargs) -> str:
    prompt_template = Path(path).read_text()
    return prompt_template.format(**kwargs)

def load_resume_text() -> str:
    return RESUME_TEXT_PATH.read_text() if RESUME_TEXT_PATH.exists() else "NO DATA PROVIDED"

def test_gemini():
    client = get_gemini_client()
    response = client.models.generate_content(
        model= TEST_MODEL,
        contents="This is a test for response, Please respond with \"Up and running\"",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Test],
        },
    )
    # Use the response as a JSON string.
    # print(response.text)

    # Use instantiated objects.
    test_response : list[Test] = response.parsed
    if not test_response:
        raise ValueError("No response received from Gemini API.")
    return test_response[0].response


def parse_resume(resume_text: str) -> Resume:
    if not resume_text:
        raise ValueError("Path provided seems to be empty, please check the file path and try again.\n If the issue persists, run setup again.")
    
    client = get_gemini_client()
    response = client.models.generate_content(
        model= PARSE_MODEL,
        contents= load_prompt(
            "patterns/resume_data_extraction.md",
            resume_text = resume_text
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": Resume,
        },
    )

    # Use instantiated objects.
    structured_response : list[Test] = response.parsed
    if not structured_response:
        raise ValueError("No response received from Gemini API.")
    return structured_response.model_dump(exclude_none=True)

def parse_job(job_data: str) -> JobDescription:
    if not job_data:
        raise ValueError("Input Data provided seems to be empty, please check the input and try again.\n If the issue persists, restart Terminal.")
    
    client = get_gemini_client()
    response = client.models.generate_content(
        model= PARSE_MODEL,
        contents= load_prompt(
            "patterns/job_data_extraction.md",
            job_data = job_data
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": JobDescription,
        },
    )

    # Use instantiated objects.
    structured_response : list[Test] = response.parsed
    if not structured_response:
        raise ValueError("No response received from Gemini API.")
    return structured_response.model_dump(exclude_none=True)

def create_coverletter(job_data, resume_data) -> CoverLetter:
    if not job_data or not resume_data:
        raise ValueError("Input Data provided seems to be empty, please check the input and try again.\n If the issue persists, restart Terminal.")
    
    client = get_gemini_client()
    response = client.models.generate_content(
        model= PARSE_MODEL,
        contents= load_prompt(
            "patterns/coverletter_generation.md",
            job_data = job_data,
            resume_data = resume_data
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": CoverLetter,
        },
    )

    # Use instantiated objects.
    structured_response : list[Test] = response.parsed
    if not structured_response:
        raise ValueError("No response received from Gemini API.")
    return structured_response.model_dump(exclude_none=True)

def create_tailored_resume(job_data, resume_data) -> Resume:
    if not job_data or not resume_data:
        raise ValueError ("Input Data provided seems to be empty, please check the input and try again.\n If the issue persists, restart Terminal.")
    client = get_gemini_client()
    response = client.models.generate_content(
        model= PARSE_MODEL,
        contents= load_prompt(
            "patterns/custom_resume_generation.md",
            job_data = job_data,
            resume_data = resume_data
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": Resume,
        },
    )

    # Use instantiated objects.
    structured_response : list[Test] = response.parsed
    if not structured_response:
        raise ValueError("No response received from Gemini API.")
    return structured_response.model_dump(exclude_none=True)


# print(load_prompt("patterns/resume_data_extraction.md", resume_text=load_resume_text()))
# res = (parse_resume(Path(RESUME_TEXT_PATH).read_text()))
# print(json.dumps(res, indent=2))


