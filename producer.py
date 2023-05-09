from confluent_kafka import Producer
from faker import Faker
from random import randint
import os
import json


def delivery_conf(err, msg):
    if err:
        print (f"Failed to produce to broker: {str(err)}")
    else:
        print (f"Successfully produced to broker partion {msg.partition()} with the offset {msg.offset()}")
        print (f"{msg.value()}")

def main():
    try:
        print ("_"*80)
        print ("{:^80}".format("Kafka Producer"))
        print ("{:^80}".format("Hjalmars & Mirzas exjobb"))
        print ("{:^80}".format("Basalt AB, Craton"))
        print ("Please submit username and password")
        username = input("Username >")
        password = input("Password >")
        p = Producer({"bootstrap.servers":"raspberrypi:9092","security.protocol":"sasl_ssl",
"sasl.mechanism":"SCRAM-SHA-512","sasl.username":username,"sasl.password":password,
"ssl.ca.location":"/home/exjobb/ssl/ca-cert","acks":"-1",
"partitioner":"consistent_random"})
        os.system("clear")
        print ("Login Success")
        print ("Producer ID:",p)
        for i in range(0,2):
            print(i)
            admin1_topic=[]
            admin2_topic=[]
            sid = randint (0,100)
            msg_value = str({"Very secret data": sid})
            command = 'sss gen -n 2 -k 2 "{}"'.format(msg_value)
            cmd = os.popen(command)
            output = cmd.read()
            lines = [line for line in output.splitlines()[1:-2] if line]
            shares = list(lines)
            for e in range(len(shares)):
                print(len(shares))
                print(shares)
                if i % 2 == 0:
                    admin1_topic.append(shares[e])
                else:
                    admin1_topic.append(shares[e])
            if admin1_topic:
                p.produce(topic="sss-topic1", value=admin1_topic[0], on_delivery=delivery_conf)
                p.produce(topic="sss-topic2", value=admin1_topic[1], on_delivery=delivery_conf)

    except KeyboardInterrupt:
        print ("Exiting...")
    finally:
        p.flush()


if __name__ == "__main__":
    main()
