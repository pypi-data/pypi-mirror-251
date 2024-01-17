# ArcGPT
## Description
ArcGPT is intended to be used with ArcGIS Pro and be run within the python window. ArcGPT relies on ChatGPT function calling to call arcpy functions to perform various tasks in ArcGIS Pro using natural language prompts. It is essentially a collection of ChatGPT function call functions that call geoprocessing tools via arcpy.

## Dependencies
- ArcGIS Pro Desktop 2.9x or newer
- An OpenAI API Key
- Python 3.7x or newer
- arcpy (comes with your ArcGIS Pro installation)

## Getting Started
Follow the instructions on the below wiki page to setup your development environment.
https://dev.azure.com/ngisaus/RND-GENAI/_wiki/wikis/RND-GENAI.wiki/331/ArcGPT-Dev-Environment-Setup

Once your environment setup has been completed, if running a standalone script, you can call arcGPT using the method below.

```
import arcgpt

openaiKey = "[OPENAI KEY]"
llmModel= "gpt-3.5-turbo"
workspace = r"C:\temp"

reply = agent.query([USER INPUT COMMAND])

print(reply)
```

## Currently Supported Functions
ArcGPT uses the ChatGPT function calling feature to inform the ChatGPT model about all the supported functions. 
The functions are generally calls to arcpy geoprocessing tools. The currently implemented functions are listed below:

### Get Current Weather
**Description:** Get the current weather in a given location - CURRENTLY HARD CODED FOR DEMO PURPOSES

**ChatGPT Function:**
```
get_current_weather
``` 
**Example Query:**
```
"What is the weather in Perth today?"
```
**Limitations:** 
Currently configured for demo purposes only - hard coded values return the same weather conditions for any input location.

### Get Schools in Suburb
**Description:** Get the schools that exist in any Western Australian suburb - outputs a new feature class in the ArcGIS Pro project's default GDB. Queries SLIP map services to obtain a suburb boundary, then uses the boundary to find any contained schools. 

**ChatGPT Function:**
```
getSchoolsInSuburb
``` 
**Example Query:**
```
"Which schools are in Perth?"
```
**Limitations:** 
Currently only viable for WA suburbs, if a suburb contains no schools, the tool will fail.

## Additional Notes
- While the code is running, the ArcGPT agent will maintain a chat/message history, as per a normal chatGPT session. If multiple queries are sent to the agent, the message history will build and provide the agent with additional context.
- To retrieve the message history, you can use the method below.
```
messages = agent.message_history
```
- arcgpt will never delete or edit any data, it will only create new feature classes.
- all your commands are going to OpenAI to generate the responses so just be aware of that.
- arcgpt uses the gpt-3.5-turbo model by default, other models are available, see https://platform.openai.com/docs/models
- To update the model used to create a new agent, you can change the model parameter as below.
```
import arcgpt

openaiKey = "[OPENAI KEY]"
llmModel= "[MODEL NAME]" # e.g. gpt-4
workspace = r"C:\temp"

reply = agent.query([USER INPUT COMMAND])

print(reply)
```

