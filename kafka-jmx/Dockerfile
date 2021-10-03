FROM wurstmeister/kafka:2.12-2.4.1
ADD kafka-jmx-config.yml /opt/kafka/libs/kafka-jmx-config.yml
ADD jmx_prometheus_javaagent-0.16.1.jar /opt/kafka/libs/jmx_prometheus_javaagent.jar
RUN chmod +r /opt/kafka/libs/jmx_prometheus_javaagent.jar
EXPOSE 7070
