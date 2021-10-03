# Steps to deploy/provision/configure the environment

1) Install Vagrant *(https://www.vagrantup.com/downloads)*
2) Install VirtualBox *(https://www.virtualbox.org/wiki/Downloads)*
3) Clone this repository *(git clone https://github.com/santiagovarela86/sre-evolution-challenge)*
4) Run 'vagrant up' in the repository root folder

# How to visualize the Metrics

- Access Prometheus *(http://hostname:30900)*
- Access Grafana *(http://hostname:31000)* with "admin/admin" user/password combination. Then, you can either change the password or skip the password change screen and use Grafana
  - Go to the Dashboards Section *(http://hostname:31000/dashboards)*
  - Access the dashboards to see the different types of metrics
- Note: `hostname` could be `localhost` or `192.168.50.11` if you run this locally in your PC, or it could be the public IP of the Host (provided it has ports 30900 and 31000 exposed to the Internet).

# CLI into the Cluster

- Once the deployment has finished, you can run 'vagrant ssh k8s-master-1' in the repository root folder to log into the Master Node and run *kubectl* commands inside the Cluster (https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)

- To get a list of all the Cluster Nodes run the following command:

  - `kubectl get nodes -o wide` 

- To get a list of all the PODs run the following command:

  - `kubectl get pods --all-namespaces -o wide` 

- Consumer and Producer log their output to the console, you can take a look at the POD logs running the following commands: 

  - `kubectl logs -n applications consumer-xxxxxxxxxx-yyyyy -f` 
  - `kubectl logs -n applications producer-xxxxxxxxxx-yyyyy -f`

  Where `xxxxxxxxxx-yyyyy` is the dynamic ID of each POD, which you can get running the `kubectl get pods` command mentioned above.

# Discussions / Limitations

- This is a Single-Master Cluster ONLY. Multi-Master Cluster functionality is NOT implemented. If you set the `MASTER_NUM` variable in the Vagrantfile to more than 1, expect strange things to happen (It will create multiple Master Nodes but will join all the Worker Nodes only to the last created Master Node, leaving all the previous Master Nodes isolated).

- This is a Multi-Worker Cluster. You can configure the number of Worker Nodes using the `WORKER_NUM` variable in the Vagrantfile.

- There will be `WORKER_NUM` number of Zookeeper and Kafka instances, each one running on a Worker Node, with its own Local Persistent Volume, running on Stateful Sets.

- The Kafka topics will be replicated with a factor of `WORKER_NUM`.

- Grafana and Prometheus will only run on Worker 1, as they use Local Persistent Volume.

- The Private Docker Registry where Consumer, Producer, Kafka and Zookeeper images are pushed, runs on the Master Node, InMemory.

- Grafana, Prometheus, Docker Registry, Consumer and Producer run as Deployments with a replica count of 1.

- Kafka and Docker network traffic is not encrypted.

- This project uses "ansible_local" as provisioner. Meaning: each K8S Node is its own Ansible Host. One of the requirements was to only have Vagrant and VBox installed in the Host, which makes the use of the "ansible" provider not feasible because in that case Ansible needs to be installed on the Host. Also, we need to be able to run this on any operating system, another reason not to use the "ansible" provider, as Ansible doesn't run on Windows Hosts.<br>
*=> Alternative: deploy an additional VM, install Ansible on it, and use it to provision the environment remotely. Went for the "ansible_local" option instead, given its ease of use, i.e. the out-of-the-box setup of the SSH keys and eliminating the need for managing another VM. Also, for some Ansible modules I would have to install Python dependencies on the remote nodes either way.*

# Tested on the following Host and Operating System combinations

- Desktop PC + Windows 10 *(2 Cores/4 Threads + 16 GB)*
  - **Tested up to 1 Master and 3 Workers**
- Azure VM + Ubuntu 20.04 *(4 vCPUs + 16 GB)*
  - **Tested up to 1 Master and 3 Workers**
- Azure VM + Red Hat Linux 8.2 *(4 vCPUs + 16 GB)*
  - **Tested up to 1 Master and 3 Workers**
- Azure VM + Windows Server 2019 *(4 vCPUs + 16 GB)*
  - **Struggled even with just 1 Master and 1 Worker**
- 32 GB of Free Disk Space Recommended
- It takes around 45 minutes to deploy a 4 Node Cluster.

# Versions

- VirtualBox **v6.1.26**
- Vagrant **v2.2.18**
- Cluster Nodes OS **ubuntu/bionic64:18.04**
- Kubernetes **v1.22.2**
- Container Runtime **docker://20.10.8**
- Flannel **quay.io/coreos/flannel:v0.14.0**
- Docker Registry **registry:2**
- Kafka **wurstmeister/kafka:2.12-2.4.1**
- Zookeeper **k8s.gcr.io/kubernetes-zookeeper:1.0-3.4.10**
- JMX Prometheus Java Agent **jmx_prometheus_javaagent-0.16.1.jar**
- Consumer and Producer **python:3.7**
- Prometheus **prom/prometheus:v2.30.1**
- Grafana **grafana/grafana:7.5.2**

# References

- https://www.vagrantup.com/docs/provisioning/ansible_local
- https://www.itwonderlab.com/en/ansible-kubernetes-vagrant-tutorial/
- https://phoenhex.re/2018-03-25/not-a-vagrant-bug
- https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/
- https://app.vagrantup.com/ubuntu/boxes/bionic64
- https://docs.ansible.com/ansible/2.4/playbooks_loops.html
- https://stackoverflow.com/questions/43794169/docker-change-cgroup-driver-to-systemd
- https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/
- https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/
- https://kubernetes.io/docs/tutorials/stateful-application/zookeeper/
- http://cloudurable.com/blog/kubernetes_statefulset_zookeeper_part1/index.html
- https://medium.com/@anilkreddyr/kubernetes-with-flannel-understanding-the-networking-part-1-7e1fe51820e4
- https://stackoverflow.com/questions/47845739/configuring-flannel-to-use-a-non-default-interface-in-kubernetes
- https://itnext.io/kubernetes-journey-up-and-running-out-of-the-cloud-flannel-c01283308f0e
- https://dzone.com/articles/ultimate-guide-to-installing-kafka-docker-on-kuber
- https://rmoff.net/2018/08/02/kafka-listeners-explained/
- https://hub.docker.com/r/wurstmeister/kafka/
- https://stackoverflow.com/questions/47516355/multi-broker-kafka-on-kubernetes-how-to-set-kafka-advertised-host-name
- https://medium.com/kubernetes-tutorials/monitoring-your-kubernetes-deployments-with-prometheus-5665eda54045
- https://prometheus.io/docs/prometheus/latest/configuration/configuration/
- https://grafana.com/docs/grafana/latest/installation/kubernetes/
- https://github.com/danielqsj/kafka_exporter
- https://github.com/prometheus/jmx_exporter
- https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/preexisting-pd
- https://github.com/openshift/openshift-restclient-python/issues/230
- https://kafka-python.readthedocs.io/en/master/
- https://docs.docker.com/registry/insecure/
- https://docs.python.org/3/library/datetime.html
- https://elliot004.medium.com/getting-started-with-apache-kafka-and-prometheus-jmx-javaagent-on-windows-dockertoolbox-b1df3fe5fc7e
- https://github.com/prometheus/client_python
- https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- http://www.whiteboardcoder.com/2017/05/prometheus-jmx-and-zookeeper.html
- https://devopscube.com/setup-grafana-kubernetes/
- https://grafana.com/tutorials/provision-dashboards-and-data-sources/
- https://grafana.com/docs/grafana/latest/administration/provisioning/
- https://github.com/confluentinc/jmx-monitoring-stacks
