from angle_emb import AnglE, Prompts
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
from pymongo import MongoClient
import json
import zuni
from bson import json_util
import ast


class NeuralSearcher:
    def __init__(self, qdrantURL, qdrantAPI, collectionName):
        self.collectionName = collectionName
        self.model = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()
        self.model.set_prompt(prompt=Prompts.C)
        self.qdrant_client = QdrantClient(qdrantURL,api_key=qdrantAPI)
    
    def search(self, text, location=None):
        vector = self.model.encode({'text': text}, to_numpy=True)[0].tolist()

        if location is not None:
            filter = Filter(**{
            "must": [{
                "key": "currentlocation.city",
                "match": {
                    "value": location
                }
            }]})
            search_result = self.qdrant_client.search(
                collection_name=self.collectionName,
                query_vector=vector,
                query_filter=filter, 
                limit=5
            )
            payloads = [hit.payload for hit in search_result]
        else:
            search_result = self.qdrant_client.search(
                collection_name=self.collectionName,
                query_vector=vector,
                limit=5
            )
            payloads = [hit.payload for hit in search_result]
        nameOfPeople = []
        for payload in payloads:
            nameOfPeople.append(payload["_id"])
        return nameOfPeople
    
def rankPeople(personIds, detailJson, keyOpenAI, mongoDbURL, mongoDbName, mongoDbCollectionName):
    '''
    The current ranking pipeline takes user description, people description and tries to assign score to them on the basis of similarity.
    Basic assumption: Even with referral people with similar work and non work interests would align together (for example: person A who is looking for front end engineers might prefer someone who has similar interests as him.)
    '''
    mongoClient = MongoClient(mongoDbURL)
    mongoDatabase = mongoClient.get_database(mongoDbName)
    mongoDatabaseCollection = mongoDatabase.get_collection(mongoDbCollectionName)
    detailsSelectedPeople = {}
    for personId in personIds:
        for document in mongoDatabaseCollection.find():
            jsonString = json_util.dumps(document)
            jsonObject = json.loads(jsonString)
            if jsonObject["_id"]==personId:
                detailsSelectedPeople[personId["$oid"]] = jsonObject["descriptions"]
    userName = detailJson["firstName"]
    instructions = f"You are a hiring manager who works for {userName} and should match the user with details of the people provided. You will be provided with a description of the user in a dictionary format with key being userid and value being the user description. Your goal is to assign the people a single value score out of 10. The scores should be in a json format with key being userid as provided in input and the value being score. The output should only be a json with key as personid and value as score, do not add any other text, if the two descriptions are about the same person keep the score as -1."
    prompt = "My description is as follows: " + detailJson["descriptions"] + "The person description of the people you should score are as follows: " + str(detailsSelectedPeople) + ". Now assign them all a score as you have been instructed and only return the score json."
    outputScores = zuni.llmBasedFeatures.writeMessageUsingLLM(keyOpenAI, instructions, prompt, modelname='gpt-4-0613', maxTokens=128)
    result = ast.literal_eval(outputScores)
    sortedResult = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    return sortedResult