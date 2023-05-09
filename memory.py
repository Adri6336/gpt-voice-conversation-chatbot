import openai
import faiss
import numpy as np
import pandas as pd
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter as RCTS
from general_functions import info


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")

    ct = 0
    errors = []

    while ct < 3:
        try:
            return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

        except Exception as e:
            errors.append(e)
            ct += 1

    print(f"Error getting embedding for {text}: {errors}")
    return None


class Neocortex:

    index = None  # This represents the vector database
    operational = False
    df = None  # This represents the plaintext database

    def __init__(self, key):
        """
        Make sure that a vector db is instantiated and save data
        from neocortex file to object.

        """
        openai.api_key = key
        self.operational = self.setup_vector_db()

    def load_memory(self, query_text: str) -> str:
        """
        This queries the vector db in the neocortex and
        returns the closest string.

        :param query_text: This is the question you're trying to answer, like user's age.
        :return: String containing most related info.
        """
        if self.df.empty:
            return 'Uncertain'

        query = get_embedding(query_text)

        # normalize the query vector
        query = query / np.linalg.norm(query)
        D, I = self.index.search(np.array([query]), 1)
        answer = self.df.loc[I[0][0], 'text']

        # change the threshold for similarity score
        info(f'D: {D}')
        info(f'MEM: {answer}')


        if D > 0.8:
            return answer
        else:
            return 'Uncertain'

    def save_memory(self, memory: str):
        """
        This saves a memory to a vector db. It breaks it apart with
        langchain and saves it.

        :param memory: This is the string text data you want to remember
        :return:
        """

        # Convert memory to embedding
        memory_embedding = get_embedding(memory)
        memory_embedding = memory_embedding / np.linalg.norm(memory_embedding)  # Normalize
        memory_data = np.array([memory_embedding])

        # add the embeddings to the index and df
        self.df = pd.concat([self.df, pd.DataFrame([memory, memory_data], index=self.df.columns).T], ignore_index=True)
        self.index.add(np.array(memory_data))

        # Save index and csv to disk
        self.df.to_csv("neocortex.csv", index=False)
        faiss.write_index(self.index, "neocortex.faiss")

    def split_and_save(self, memory: str):
        """
        Splits the memory string into chunks

        :param memory: A string you want to recall
        :return: None
        """
        splitter = RCTS(chunk_size=360, chunk_overlap=0)
        chunks = splitter.split_text(memory)

        for chunk in chunks:
            self.save_memory(chunk)

    def setup_vector_db(self) -> bool:
        """
        This attempts to create a vectordb on your machine.

        :return: Success state of file creation attempt
        """
        try:
            if os.path.exists("neocortex.faiss"):
                # load the index from the file
                self.index = faiss.read_index("neocortex.faiss")

            else:
                # create a flat index with cosine similarity and 1536 dimension
                self.index = faiss.IndexFlatIP(1536)

                # save the index to a file
                faiss.write_index(self.index, "neocortex.faiss")

            if os.path.exists("neocortex.csv"):
                self.df = pd.read_csv("neocortex.csv", header=0, names=['text', 'embedding'])
                self.df = self.df[self.df.embedding.notnull()]

            else:
                self.df = pd.DataFrame(columns=['text', 'embedding'])
                self.df.to_csv("neocortex.csv", index=False)

            # normalize the vectors in the dataframe
            self.df['embedding'] = self.df['embedding'].apply(lambda x: x / np.linalg.norm(x))

            return True

        except Exception as e:
            info(f'Error: {e}', 'bad')
            return False

