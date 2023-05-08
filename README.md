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
