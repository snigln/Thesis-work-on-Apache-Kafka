from confluent_kafka import Consumer, KafkaError
import os

def prnt_header():
    print("-"*80)
    print("{:^80}".format("Kafka Consumer"))
    print("{:^80}".format("Hjalmars & Mirzas exjobb"))
    print("{:^80}".format("Basalt AB, Craton"))
    print("-"*80)

def prnt_recv_msg(msg):
    print(f"Received message: {msg.value()} on topic {msg.topic()} and partition {msg.partition()} with offset {msg.offset()}")

def main():
    prnt_header()
    username1 = input("First username >")
    password1 = input("Password >")
    username2 = input("Second username >")
    password2 = input("Password >")
    c = Consumer({
        'bootstrap.servers':'raspberrypi:9092',
        'security.protocol':'sasl_ssl',
        'sasl.mechanism':'SCRAM-SHA-512',
        'sasl.username':username1,
        'sasl.password':password1,
        'group.id':'ssl-consumer',
        'ssl.ca.location':'/home/exjobb/ssl/ca-cert',
        'auto.offset.reset':'latest'
        })

    c.subscribe(['sss-topic1'])

    c1 = Consumer ({
        'bootstrap.servers':'raspberrypi:9092',
        'security.protocol':'sasl_ssl',
        'sasl.mechanism':'SCRAM-SHA-512',
        'sasl.username':username2,
        'sasl.password':password2,
        'group.id':'sasl-consumer',
        'ssl.ca.location':'/home/exjobb/ssl/ca-cert',
        'auto.offset.reset':'latest'
        })
    
    c1.subscribe(['sss-topic2'])
    segments1 = []
    segments2 = []
    try:
        while True:
            msg = c.poll(1.0)
            msg1 = c1.poll(1.0)
            if msg is None or msg1 is None:
                continue
            if msg.error() or msg1.error():
                print(f"Error while consuming message: {msg.error()}")
            else:
                if msg:
                    prnt_recv_msg(msg)
                    msg_value = msg.value().decode('utf-8')
                    segments1.append(msg_value)
                if msg1:
                    prnt_recv_msg(msg1)
                    msg1_value = msg1.value().decode('utf-8')
                    segments2.append(msg1_value)

                if len(segments1) == 1 and len(segments2) == 1:
                    # Recover the secret using sss rec and the 4 event logs
                    command = 'sss rec "{}" "{}"'.format(segments1[0], segments2[0])
                    command = command.replace('"', '')
                    print(command)
                    cmd = os.popen(command)
                    output = cmd.read()
                    secret = output.strip()
                    # Do something with the recovered secret
                    print("The secret message is:", secret)
                    # Clear segments lists for next messages
                    segments1 = []
                    segments2 = []

    except KeyboardInterrupt:
        print("\nInterrupted, exiting...")

    finally:
        c.close()
        c1.close()

if __name__ == "__main__":
    main()

