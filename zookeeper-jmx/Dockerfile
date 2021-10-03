FROM k8s.gcr.io/kubernetes-zookeeper:1.0-3.4.10
ADD zookeeper-jmx-config.yml /opt/zookeeper/lib/zookeeper-jmx-config.yml
ADD jmx_prometheus_javaagent-0.16.1.jar /opt/zookeeper/lib/jmx_prometheus_javaagent.jar
RUN chmod +r /opt/zookeeper/lib/jmx_prometheus_javaagent.jar
EXPOSE 7070
