from arcgpt.openai_services import get_chatgpt_response
from arcgpt.tools import get_tools

class Agent:
    def __init__(self, openAIKey, llmModel, workspace):
        self.OpenAIKey = openAIKey
        self.Model = llmModel
        self.Workspace = workspace

        self.tools = get_tools()
        self.context = "you are the arcgpt python library, a user is sending prompts to you from ArcGIS Pro, a desktop GIS application for visualising, creating, editing and performing analysis on spatial data. You have been provided with functions to call the ArcPy python library to perform GIS tasks in the users ArcGIS Pro client. Your role is to interpret the users natural language and translate that to the arcpy function calls that have been defined."
        self.message_history = [
            {
                "role": "system",
                "content": self.context
            }
        ]
    
    def query(self, userPrompt):
        reponse = get_chatgpt_response(self, userPrompt)
        return reponse
    
    def add_history(self, data):
        self.message_history.append(data)

