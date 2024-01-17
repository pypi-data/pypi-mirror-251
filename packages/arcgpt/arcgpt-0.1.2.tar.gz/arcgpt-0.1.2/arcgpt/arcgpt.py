from .agent import Agent

def CreateAgent(openAIKey, llmModel, workspace):
    return Agent(openAIKey, llmModel, workspace)
