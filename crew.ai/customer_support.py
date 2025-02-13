import dotenv
from crewai import Agent, Task, Crew

import os

dotenv.load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
# os.environ["OPENAT_MODEL_NAME"] = "gpt-4.0-mini"
# os.environ["OPENAT_MODEL_NAME"] = "o3-mini"
os.environ["OPENAT_MODEL_NAME"] = "gpt-3.5-turbo"

support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful support representative in the company",
    backstory=(
                "You work at Stoerk-tronic GmbH (https://stoerk-tronic.com) and "
                "are now working on providing support to a B2B {customer}, "
                "a super important customer of the company. "
                "You need to make sure that you provide the best support!"
                "You are very knowledgeable about the SToerk-tronic's product. You're the go-to person "
                "for difficult customer issues and you always go above and beyond "
                "to make sure the customer is satisfied."
                "Make sure to provide full complete answers"
                "and make no assumptions."
    ),
    allow_delegation=False,
    verbose=True
)

# Quality assurance agent
# Can do its own work and delegate back to other agent because
# allows_delegation is set to True per default.

support_quality_assurance_agent = Agent(
	role="Support Quality Assurance Specialist",
	goal="Get recognition for providing the "
    "best support quality assurance in your team",
	backstory=(
		"You work at Stoerk-tronic GmbH (https://stoerk-tronic.com) and "
        "are now working with your team "
		"on a request from {customer} ensuring that "
        "the support representative is "
		"providing the best support possible. "
		"You need to make sure that the support representative "
        "is providing full "
		"complete answers, and make no assumptions."
    ),
	verbose=True
)

from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool, \
                         PDFSearchTool

#docs_scrape_tool = ScrapeWebsiteTool("https://www.stoerk-tronic.com/fileadmin/erp/dokumente/datenblaetter/de/900320_001.pdf")

docs_scrape_tool = PDFSearchTool("https://www.stoerk-tronic.com/fileadmin/erp/dokumente/datenblaetter/de/900320_001.pdf")

inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
	    "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
		"Make sure to use everything you know "
        "to provide the best support possible."
		"You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
	    "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
		"leaving no questions unanswered, and maintain a helpful and friendly "
		"tone throughout."
    ),
	tools=[docs_scrape_tool],
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
		"thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
		"Don't be too formal, we are a chill and cool company "
	    "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
)

crew = Crew(
  agents=[support_agent, support_quality_assurance_agent],
  tasks=[inquiry_resolution, quality_assurance_review],
  verbose=2,
  memory=True
)

inputs = {
    "customer": "Schaefer.AI",
    "person": "Siegfried Schaefer",
    "inquiry": "I need help with adjusting the hysterisis "
               "of the temperature alarm in a ST121 controller "
               "Can you provide guidance?"
}

result = crew.kickoff(inputs=inputs)

print(result)

