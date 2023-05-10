# Thesis work on Apache-Kafka security
This repository is a both a guide on Apache Kafka and documentation of our thesis work on secure log management for apache kafka.
Our thesis work focuses on how to securely manage a Apache Kafka based data streaming service.
This will include authentication with SSL-SASL and authorization with Kafkas built in ACL functions.
This will also include python producer and consumer script, these scipts will have SSS implemented aswell for segmentation and to allow multi-factor authenticaiton.

## Download Apache Kafka

First download the latest version of Apache Kafka using the `wget` command, download [HERE](https://dlcdn.apache.org/kafka/).

Download the hash key aswell to ensure that the data is intact, this can either be a `md5` or a `sha` file.

Compare the the key to the tarball with the `gpg --print-md SHA256 downloaded_file` or `gpg --print-md md5 downloaded_file` command.

If they match, that means that the data is intact and you can extract the tarball with `tar -xzf downloaded_file` command

Change your working directory to the new Kafka directory with `cd`

### Start Kafka

First start the zookeeper server with the `bin/zookeeper-server-start.sh config/zookeeper.properties` command

Then start the broker with `bin/kafka-server-start.sh config/server.properties`

## Generating Certificates and Trust - Keystores

Please note that how the certificates and stores are generated should not be duplicated in a production environment!
Please refer to you company policies regarding certificates.

You will only need to create Key and Truststores for the Zookeeper client and the broker, since it is unable to use SASL to authenticate with it self.
Please note that whenever a name is promted, please input your hostname to avoid complications.

Download openSSL library with `sudo apt install openssl -y`

The certificates and stores should be stored in a secure directory in a production environment but in our case we just stored in a directory in the kafka directory.

### Generate the Certificate Authority
`openssl req -new -x509 -keyout ca-key -out ca-cert -days 3650`
This will create a `ca-key` file and a `ca-cert` file.

### Generate Truststore
`keytool -keystore truststore-file-name.jks -alias ca-cert -import -file ca-cert`

### Generate Keystore
`keytool -keystore keystore-file-name.jks -alias your-alias -validity 3650 -genkey -keyalg RSA -ext SAN=dns:hostname`

### Sign the Keystore
`keytool -keystore keystore-file-name.jks -alias your-alias -certreq -file request-file-name`

`openssl x509 -req -CA ca-cert -CAkey ca-key -in request-file-name -out signed-file-name -days 3650 -CAcreateserial`

`keytool -keystore keystore-file-name.jks -alias ca-cert -import -file ca-cert`

`keytool -keystore keystore-file-name.jks -alias your-alias -import -file signed-file-name`



## Managing SASL users

You can see in our server.properties file you can see that we have a super user called "broker-admin".
This user is used to authenticate brokers with each other and for inter-broker communication.
To create more users we need to refer to to this user by refering to a the `admin.properties` file, which contains the credentials and certificates that the super user use.

But in a production environment this is not very secure, so in a production environment you should create a seperate admin user and add their credentials to the `admin.properties` file.

But to create this seperate admin user you will need to refer to the zookeeper client.

### Creating a user with Super user

`bin/kafka-configs.sh --bootstrap-server hostname:9092 --command-config config/admin-properties --entity-type users --entity-name your-user --alter --add-config 'SCRAM-SHA-512=[password=your-password]'`

### Creating a user with Zookeeper client

`bin/kafka-configs.sh --zookeeper hostname:2182 --zk-tls-config-file config/zookeeper-client.properties --entity-type users --entity-name kafka-admin --alter --add-config 'SCRAM-SHA-512=[password=your-password]'`

### Deleting a user

`bin/kafka-configs.sh --bootstrap-server hostname:9092 --command-config config/admin.properties --entity-type users --entity-name your-user --alter --delete-config 'SCRAM-SHA-512'`

### Describe a user

`bin/kafka-configs.sh --bootstrap-server hostname:9092 --command-config config/admin.properties --entity-type users --entity-name your-user --describe`

### List all users

`bin/kafka-configs.sh --bootstrap-server hostname:9092 --command-config config/admin.properties --entity-type users --describe`


## Managing the cluster

Here you can see the commands which are used to create, restrict access, list and describe topics in the cluster.

### Create a topic

`bin/kafka-topics.sh --bootstrap-server hostname:9092 --command-config config/admin.properties --create --topic topic-name`

### Descirbe a topic

`bin/kafka-topics.sh --bootstrap-server hostname:9092 --command-config config/admin.properties --describe --topic topic-name`

### List all topics

`bin/kafka-topics.sh --bootstrap-server hostname:9092 --command-config config/admin.properties --list`

### List ACLs tied ot the user

`bin/kafka-acls.sh --authorizer-properties zookeeper.connect=hostname:2182 --zk-tls-config-file zookeeper-client.properties --add --allow-principal User:your-user --operation WRITE --operation DESCRIBE --operation DESCRIBECONFIGS --topic topic-name`

### Grant Write access to topic (Producer)

`bin/kafka-acls.sh --authorizer-properties zookeeper.connect=hostname:2182 --zk-tls-config-file config/zookeeper-client.properties --add --allow-principal User:your-user --operation WRITE --operation DESCRIBE --operation DESCRIBECONFIGS --topic topic-name`

### Grant Read access to topic (Consumer)

`bin/kafka-acls.sh --authorizer-properties zookeeper.connect=hostname:2182 --zk-tls-config-file config/zookeeper-client.properties --add --allow-principal User:your-user --operation READ --operation DESCRIBE --topic topic-name`

`bin/kafka-acls.sh --authorizer-properties zookeeper.connect=hostname:2182 --zk-tls-config-file config/zookeeper-client.properties --add --allow-principal User:your-user --operation READ --group your-consumer-group`


## Python Scipts

There are two python scripts producer.py and consumer.py, the producer requires a user to authenticate before the script starts to produce to a topic.
It then generates 2 messages containing a string value and a random int value.
These messages are then segmented into two pieces with SSS and each one of the pair is sent to a different topic. This is to ensure that no user alone can reconstruct the intial messege.

The consumer script requires two users to authenticate before it starts to consume messages from the two topics, then the messages are reconstructed and prints to the screen.
The scripts however seem to fail every 3rd attempt, we do think it has something to do with the offsets of the messages and there beign more than one partition in the topics, but we will do further research about this.

To run the scripts the Kafka Client, developed and maintained by Confluent, must first be installed. This can be done with pip:
'pip install confluent-kafka'

Furthermore, the scripts require the fluix implementation of Shamir's secret sharing algorithm.
'pip3 install git+https://git.sr.ht/~fluix/sss'
