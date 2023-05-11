from neo4j import GraphDatabase

def insert_record_to_neo4j(id_value, name):
    # Create a connection to the Neo4j database (graph container)
    uri = "bolt://localhost:7697"  # Update with the appropriate URI
    username = "neo4j"  # Update with your username
    password = "password"  # Update with your password
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    with driver.session() as session:
        # Create a new record with the provided id value
        query = "CREATE (n:Record {nodeID: $id_value, name: $name})"
        session.run(query, id_value=id_value, name=name)
    
    # Close the database connection
    driver.close()

def connect_articles(article_id1, article_id2):
    # Connect to the Neo4j database
    neo4j_uri = "bolt://localhost:7697"  # Update with the appropriate Neo4j URI
    neo4j_username = "neo4j"  # Update with your Neo4j username
    neo4j_password = "password"  # Update with your Neo4j password
    neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

    with neo4j_driver.session() as session:
        print(article_id1, article_id2)
        # Create a relationship between the two articles
        neo4j_query = "MATCH (a:Record),(b:Record) WHERE a.nodeID = $id_a AND b.nodeID = $id_b CREATE (a)-[r:SIMILAR ]->(b) RETURN r"
        session.run(neo4j_query, id_a=article_id1, id_b=article_id2)

    # Close the database connection
    neo4j_driver.close()
