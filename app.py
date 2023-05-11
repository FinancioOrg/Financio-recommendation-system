import pika
import json
from sentence_transformers import SentenceTransformer, util
from ArticleDAL import retrieveData
from ArticleDAL import retrieveArticle
from ArticleGraphDAL import insert_record_to_neo4j
from ArticleGraphDAL import connect_articles

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

model = SentenceTransformer('./stsb-roberta-base_offline')

# Declare the queue
channel.queue_declare(queue='article_created')

# Define a callback function to process messages
def callback(ch, method, properties, body):
    try:
        # Get a message
        message = json.loads(body.decode())
        # Create a node in Neo4j
        print("hello")
        insert_record_to_neo4j(message["Id"], message["Title"])
        # Semantic analysis
        articles = retrieveData(message["Id"])
        target = retrieveArticle(message['Text'])
        for article in articles:
            embeddings = model.encode([article.body, target], convert_to_tensor=True)
            cosine_scores = util.pytorch_cos_sim(embeddings[0], embeddings[1])
            similarity_score = cosine_scores.item()
            print(similarity_score)
            if similarity_score > 0.5:
                # Connect articles in the graph
                print(article.id, message["Id"])
                connect_articles(article.id, message["Id"])  # Replace connect_articles with your graph connection function

    except Exception as e:
        print("Error occurred:", str(e))
        # Re-queue the message
        ch.basic_nack(delivery_tag=method.delivery_tag)
    else:
        # Message processed successfully, acknowledge it
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages
channel.basic_consume(queue='article_created', on_message_callback=callback, auto_ack=False)
print("Listening for messages. To exit, press CTRL+C")
channel.start_consuming()
