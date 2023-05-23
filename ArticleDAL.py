from neo4j import GraphDatabase
from azure.storage.blob import BlobServiceClient
from bs4 import BeautifulSoup
import re

class Article:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body

def retrieveData(exclude_id):
  
    # Create a connection to the Neo4j database
    neo4j_uri = "bolt://localhost:7687"  # Update with the appropriate Neo4j URI
    neo4j_username = "neo4j"  # Update with your Neo4j username
    neo4j_password = "password"  # Update with your Neo4j password
    neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

    # Connect to Azure Blob Storage
    blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=financiostorage;AccountKey=iEodRKrn8zoeBZF9KJ6Exdc4ZcyKVcB21T39tMUHt1yrzKanP4fcoM+LyYVSngfxpxQs9Sz2ifqo+ASt+UUVbQ==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)

    articles = []

    with neo4j_driver.session() as session:
        # Retrieve all records from Neo4j
        # Retrieve all records from Neo4j excluding the specified ID
        neo4j_query = "MATCH (n:Record) WHERE n.nodeID <> $id_value RETURN n"
        neo4j_result = session.run(neo4j_query, id_value=exclude_id)

        for neo4j_record in neo4j_result:
            neo4j_id = neo4j_record['n']['nodeID']
            neo4j_title = neo4j_record['n']['name']

            # Fetch the blob from Azure Blob Storage based on the Neo4j ID
            container_name = "data"  # Update with your Azure Blob Storage container name
            blob_name = neo4j_id
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_content = blob_client.download_blob().content_as_text()

            # Remove HTML elements from the article body
            soup = BeautifulSoup(blob_content, 'html.parser')
            pure_text = soup.get_text()
            clean_text = re.sub(r'\s+', ' ', pure_text).strip()

            # Create an Article instance and append it to the articles list
            article = Article(neo4j_id, neo4j_title, clean_text)
            articles.append(article)

    # Close the database connection
    neo4j_driver.close()
    print("retrieveData")
    return articles


def retrieveArticle(uri):
    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=financiostorage;AccountKey=iEodRKrn8zoeBZF9KJ6Exdc4ZcyKVcB21T39tMUHt1yrzKanP4fcoM+LyYVSngfxpxQs9Sz2ifqo+ASt+UUVbQ==;EndpointSuffix=core.windows.net')
    container_name, blob_name = uri.split('/')[-2:]
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    article_body = blob_client.download_blob().content_as_text()
    soup = BeautifulSoup(article_body, 'html.parser')
    pure_text = soup.get_text()
    clean_text = re.sub(r'\s+', ' ', pure_text).strip()
    print("retrieveArticle")
    return clean_text