import paho.mqtt.client as mqtt
import traceback
import psycopg2

broker_source = "192.168.0.27"
broker_source_port = 1883

client_source = mqtt.Client()

DatabaseName = 'sensordata'
DatabasePort = 5432

print("Connecting to database")
connection = psycopg2.connect("dbname=sensordata user=pi")

insert_statement = """"""

def insertIntoDatabase(message):
	"Inserts the mqtt data into the database"
	with connection.cursor() as cursor:
		print("Inserting data: " + str(message.topic) + ";" + str(message.payload)[2:][:-1] + ";" + str(message.qos))
		#cursor.callproc('InsertIntoMQTTTable', [str(message.topic), str(message.payload)[2:][:-1], int(message.qos)])
		table_name = message.topic.rsplit('/',2)[-1]
		print (table_name)
		cursor.execute("INSERT INTO " + table_name + " VALUES (" + str(message.payload)[2:][:-1]+")")
		connection.commit()

def on_message(client, userdata, message):
	"Evaluated when a new message is received on a subscribed topic"
	print("Received message '" + str(message.payload)[2:][:-1] + "' on topic '"
		+ message.topic + "' with QoS " + str(message.qos))
	insertIntoDatabase(message)
	
def setup():
	"Runs the setup procedure for the client"
	print("Setting up the onMessage handler")
	client_source.on_message = on_message
	print("Connecting to source")
	client_source.connect(broker_source, broker_source_port)
	client_source.subscribe("#", qos=1)
	print("Setup finished, waiting for messages...")

try:
	setup()
	client_source.loop_forever()
except Exception as e:
	traceback.print_exc()
finally:
	connection.close()