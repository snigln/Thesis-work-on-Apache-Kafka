# Thesis-work-on-Apache-Kafka
This repository is a both a guide on Apache Kafka and documentation of our thesis work on secure log management for apache kafka.
Our thesis is work is focues on how to securely manage a Apache Kafka based data streaming service.
This will include authentication with SSL-SASL and authorization with Kafkas built in ACL functions.
This will also include python producer and consumer script, these scipts will have SSS implemented aswell for segmentation and to allow two-factor authenticaiton.

## Download Apache Kafka

First download the latest version of Apache Kafka using the `wget` command, download [HERE](https://dlcdn.apache.org/kafka/).

Download the hash key aswell to ensure that the data is intact, this can either be a `md5` or a `sha` file.

Compare the the key to the tarball with the `gpg --print-md SHA256 downloaded_file` or `gpg --print-md md5 downloaded_file` command.

If they match the data is intact and you can extract the tarball with `tar -xzf downloaded_file` command

Change your working directory to the new Kafka directory with `cd`

### Start Kafka

First start the zookeeper server with the `bin/zookeeper-server-start.sh config/zookeeper.properties` command

Then start the broker with `bin/kafka-server-start.sh config/server.properties`

## Generating Certificates and Trust - Keystores

Please note that how the certificates and stores are generated should not be duplicated in a production envirourment!
Please refer to you company policies regarding certificates.

You will only need to create Key and Truststores for the Zookeeper client and the broker, since it is unable to use SASL to authenticate with it self.
Please note that whenever a name is promted, please input your hostname to avoid complications.

Download openSSL library with `sudo apt install openssl -y`

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

You can see in our server.properties file you can see that we have a super user called "kafka-admin".
This user is used to authenticate brokers with eachother and for interbroker communication.
To create more users we need to refer to to this user by refering to a the `admin.properties` file, which contains the credentials and certificates that the super user use.

But in a production envirorment this is not very secure, so in a production envirorment you should create a seperate admin user and add their credentials to the `admin.properties` file.

But to create this seperate admin user you will need to refer to the zookeeper client.

### Creating a user with Super user

`kafka-configs.sh --bootstrap-server hostname:9092 --command-config config/admin-properties --entity-type users --entity-name your-user --alter --add-config 'SCRAM-SHA-512=[password=your-password]'`

### Creating a user with Zookeeper client

`kafka-configs.sh --zookeeper hostname:2182 --zk-tls-config-file zookeeper-client.properties --entity-type users --entity-name kafka-admin --alter --add-config 'SCRAM-SHA-512=[password=your-password]'`

## Managing the cluster

Here you can see the commands which are used to create, restrict access, list and describe topics in the cluster.

### Create a topic

`kafka-topics.sh --bootstrap-server hostname:9092 --command-config admin.properties --create --topic topic-name`





