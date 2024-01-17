from openai import OpenAI
import json
from arcgpt.tools import call_tool


def get_chatgpt_response(agent, prompt):
    client = OpenAI(api_key=agent.OpenAIKey)

    agent.add_history(
        {'role': 'user','content': prompt}
    )
    
    response = client.chat.completions.create(
        model=agent.Model,
        temperature=0,
        messages=agent.message_history,
        tools=agent.tools,
        tool_choice="auto",
        timeout=30
    )
    response_message = response.choices[0].message
    agent.add_history(response_message)

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_params = json.loads(tool_call.function.arguments)
            function_response = call_tool(function_name, function_params, agent.Workspace)
            
            # add the function response to the chat history
            agent.add_history(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                }
            )

        response = client.chat.completions.create(
            model=agent.Model,
            messages=agent.message_history,
        )
        response_to_user = response.choices[0].message
        agent.add_history({'role': 'assistant','content': response_to_user.content})

        return response_to_user.content
                
    else:
        # no function to be called just respond normally
        return response_message.content