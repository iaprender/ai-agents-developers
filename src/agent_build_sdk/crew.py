from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# Importing crewAI tools
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
	CodeInterpreterTool
)

search_tool = SerperDevTool(
	
)
code_interpreter = CodeInterpreterTool()
website_tool = WebsiteSearchTool()


# Uncomment the following line to use an example of a custom tool
# from agent_build_sdk.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# llm = ChatOpenAI(model='gpt-3.5') # Loading GPT-3.5

@CrewBase
class AgentBuildSdkCrew():
	"""AgentBuildSdk crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def nodejs_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['nodejs_developer'],
			tools=[
				search_tool,
				website_tool,
				code_interpreter
			],
			verbose=True,
			allow_code_execution=True
		)

	@agent
	def csharp_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['csharp_developer'],
			tools=[
				search_tool,
				website_tool,
				code_interpreter
			],
			verbose=True,
			allow_code_execution=True
		)

	@task
	def nodejs_developer_task(self) -> Task:
		return Task(
			config=self.tasks_config['nodejs_developer_task'],
			agent=self.nodejs_developer(),
			output_file='app.js'
		)

	@task
	def csharp_developer_task(self) -> Task:
		return Task(
			config=self.tasks_config['csharp_developer_task'],
			agent=self.csharp_developer(),
			output_file='app.cs'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AgentBuildSdk crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)