from openai import OpenAI
import os
import ast
import together

def writeMessageUsingLLM(apiKey: str, instructions: str, prompt: str, modelname="gpt-3.5-turbo", maxTokens=128) -> str:
    """
    """
    os.environ['OPENAI_API_KEY'] = apiKey
    client = OpenAI()
    response = client.chat.completions.create(
    model=modelname,
    messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": prompt
            }],
        temperature=0.2,
        max_tokens=maxTokens,
        top_p=1)
    result = response.choices[0].message.content.replace("\n","")
    return result
    

def classifyInputMessage(apiKey: str, inputMessage: str) -> dict:
    """
    Classify a given input message into predefined classes using OpenAI GPT-3.5-turbo.

    Parameters:
    - apiKey (str): The API key for accessing the LLM API.
    - inputMessage (str): The input message to be classified.

    Returns:
    A dictionary indicating the presence or absence of each class:
    {'meeting': 0, 'jobOrHelpOpportunity': 1, 'travelRelatedUpdate': 0, 'jobRelatedUpdate': 1 }
    If a particular class is present, its output is 1; otherwise, if it is absent, it is 0.
    """
    together.api_key = apiKey
    instructions = """ you are a natural language expert who classifies a given message into the following sequence of classes meeting, jobOrHelpOpportunity, travelRelatedUpdate, and jobRelatedUpdate, and then returns the JSON in the provided format: {'meeting': 0, 'jobOrHelpOpportunity': 1, 'travelRelatedUpdate': 0, 'jobRelatedUpdate': 1 } if a particular class is present its output is 1 otherwise if it is absent it is 0. meeting can be decided on the given definition, if the message is about seeking the other person's availability, if the message is about the sender or receiver having a meeting in the future even if it is not certain. jobOrHelpOpportunity is when the sender is seeking help with either hiring, or seeking help with an ongoing work related issue. travelRelatedUpdate is any update regarding travel that the sender is going to undertake in future. jobRelatedUpdate is when the sender joins a new company or is promoted within his company only."""
    inputMessage = inputMessage + "\n<bot>:"
    response = together.Complete.create(prompt = f"""<bot>: {instructions} \n <human>: {inputMessage}""",
                                      model = "mistralai/Mistral-7B-Instruct-v0.2",
                                      max_tokens = 512,
                                      temperature = 0.1,
                                      top_k = 60,
                                      top_p = 0.95,
                                      repetition_penalty = 1.1,
                                      stop = ['<human>', '\n\n'])
    result = response['output']['choices'][0]['text'].replace("\n","")
    result = ast.literal_eval(result)
    return result

def extractDetailsFromInputMessage(openaiKey: str, inputMessage: str, targetClasses: dict) -> dict:
    """
    
    """
    os.environ['OPENAI_API_KEY'] = openaiKey
    client = OpenAI()
    finalResult = {}
    if targetClasses["meeting"]==1:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "you are a personal assistant that extracts details from text messages I receive. For meetings you need to provide agenda of the meeting, and the time when the meeting is scheduled, if a detail is missing leave it empty. The output here should be just a JSON with the following structure {'agenda': 'put the extracted agenda here', 'time': 'put the extracted time here'}"
                },
                {
                    "role": "user",
                    "content": inputMessage
                }],
            temperature=0.0,
            max_tokens=128,
            top_p=1)
        result = response.choices[0].message.content.replace("\n","")
        result = ast.literal_eval(result)
        finalResult['meeting'] = result
    if targetClasses["jobOrHelpOpportunity"]==1:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "you are a personal assistant that extracts details from text messages I receive. For referrals you need to provide the desired high level skills asked for. The output here should be just a JSON with the following structure {'skills': 'put the extracted skills here'}"
                },
                {
                    "role": "user",
                    "content": inputMessage
                }],
            temperature=0.1,
            max_tokens=128,
            top_p=1)
        result = response.choices[0].message.content.replace("\n","")
        result = ast.literal_eval(result)
        finalResult['jobOrHelpOpportunity'] = result
    if targetClasses["travelRelatedUpdate"]==1:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "you are a personal assistant that extracts details from text messages I receive. For travel update you need to provide the agenda and location of travel if any, if no agenda is mentioned leave it empty. The output here should be just a JSON with the following structure {'agenda': 'put the extracted agenda here', 'location': 'put the city of extracted location here'}"
                },
                {
                    "role": "user",
                    "content": inputMessage
                }],
            temperature=0.1,
            max_tokens=128,
            top_p=1)
        result = response.choices[0].message.content.replace("\n","")
        result = ast.literal_eval(result)
        finalResult['travelRelatedUpdate'] = result
    if targetClasses["jobRelatedUpdate"]==1:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "you are a personal assistant that extracts details from text messages I receive. For work update you need to provide the new company, new position and new location, if any detail is missing leave it empty. The output here should be just a JSON with the following structure {'newCompany': 'put the extracted new company here', 'newPosition': 'put the extracted new position here','location': 'put the city of extracted location here'}"
                },
                {
                    "role": "user",
                    "content": inputMessage
                }],
            temperature=0.1,
            max_tokens=128,
            top_p=1)
        result = response.choices[0].message.content.replace("\n","")
        result = ast.literal_eval(result)
        finalResult['jobRelatedUpdate'] = result
    return finalResult