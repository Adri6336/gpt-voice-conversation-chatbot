import openai
import faiss
import numpy as np
import os
from langchain.text_splitter import SpacyTextSplitter
from general_functions import info


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    try:
        return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
    except Exception as e:
        print(f"Error getting embedding for {text}: {e}")
        return None


class Neocortex:

    index = None  # This represents the vector database
    operational = False

    def __init__(self, key):
        """
        Make sure that a vector db is instantiated and save data
        from neocortex file to object.

        """
        openai.api_key = key
        self.operational = self.setup_vector_db()

    def load_memory(self, query: str) -> str:
        """
        This queries the vector db in the neocortex and
        returns the closest string.

        :param query: This is the question you're trying to answer, like user's age.
        :return: String containing most related info.
        """
        pass

    def save_memory(self, memory: str):
        """
        This saves a memory to a vector db. It breaks it apart with
        langchain and saves it.

        :param memory: This is the string text data you want to remember
        :return:
        """

        # Convert memory to embedding
        memory_data = get_embedding(memory)

        # add the embeddings to the index
        self.index.add(np.array(memory_data))

    def has_memories(self) -> bool:
        """
        This determines if a vector db file exists.

        :return: Bool representing if a vector file exists
        """
        pass

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
                # create a flat index with L2 distance and 1536 dimension
                self.index = faiss.IndexFlatL2(1536)

                # save the index to a file
                self.faiss.write_index(index, "neocortex.faiss")

            return True

        except Exception as e:
            info(f'Error: {e}', 'bad')
            return False


