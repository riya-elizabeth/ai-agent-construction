import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

client = chromadb.Client()

ef = DefaultEmbeddingFunction()

collection = client.create_collection("test", embedding_function=ef)

collection.add(
    documents=["Fall protection is required above 6 feet.",
                "Hard hats must be worn on all construction sites."],
    ids=["doc1", "doc2"]
)

results = collection.query(query_texts=["What PPE is needed?"], n_results=1)
print("Query: What PPE is needed?")
print("Best match:", results['documents'][0][0])