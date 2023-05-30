from neo4j import GraphDatabase
import os

def insert_record_to_neo4j(id_value, name):
    # Create a connection to the Neo4j database (graph container)
    neo4j_uri = os.environ.get('neo4j_uri')
    neo4j_username = os.environ.get('neo4j_username')  # Update with your Neo4j username
    neo4j_password = os.environ.get('neo4j_password')  # Update with your Neo4j password
    neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    
    with neo4j_driver.session() as session:
        # Create a new record with the provided id value
        query = "CREATE (n:Record {nodeID: $id_value, name: $name})"
        session.run(query, id_value=id_value, name=name)
    
    # Close the database connection
    neo4j_driver.close()
    print("insert_record_to_neo4j")

def connect_articles(article_id1, article_id2):
    # Connect to the Neo4j database
    neo4j_uri = os.environ.get('neo4j_uri')
    neo4j_username = os.environ.get('neo4j_username')  # Update with your Neo4j username
    neo4j_password = os.environ.get('neo4j_password')  # Update with your Neo4j password
    neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

    with neo4j_driver.session() as session:
        print(article_id1, article_id2)
        # Create a relationship between the two articles
        neo4j_query = "MATCH (a:Record),(b:Record) WHERE a.nodeID = $id_a AND b.nodeID = $id_b CREATE (a)-[:SIMILAR]->(b), (b)-[:SIMILAR]->(a)  RETURN a, b"
        session.run(neo4j_query, id_a=article_id1, id_b=article_id2)

    # Close the database connection
    neo4j_driver.close()
    print("connect_articles")


    

