
query_sys_prompt = """You are a bot that converts questions into effective search queries for a vector database that uses cosine similarity. Essentially, your query will be compared to the data in this database and the most similar datum will be returned to you. Thus, your searches must be designed to maximize the chance of finding information that is similar to it. 

For example, the database could have something like, "The user likes the book Dune.". You can acquire this datum with the query, "book user like single".

Whenever you receive a question, return only the most effective search query."""

def get_initial_prompt(model: str):
    '''
    Placeholder function. In time will be fleshed out so
    that users can take advantage of different models' 
    capabilites with more expansive prompts. GPT-3 models
    have less token allowance than GPT-4, so their prompts 
    are necessarily smaller. GPT-4 prompts will be more 
    expansive.
    '''
    pass

def get_memories(model: str):
    '''
    Placeholder function. Will work with memories
    in a way that depends on the model. For example,
    GPT-4 will have a larger memory text prompt.
    '''
    pass