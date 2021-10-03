# Input Parameters
MASTERS_NUM = 1 # Single Master Cluster ONLY # Multimaster Cluster NOT implemented
MASTERS_CPU = 2 
MASTERS_MEM = 2048

WORKERS_NUM = 1
WORKERS_CPU = 2
WORKERS_MEM = 2048

IMAGE_NAME = "ubuntu/bionic64"
VM_PROVIDER = "virtualbox"
NETWORK_TYPE = "private_network"
PROVISION_ANSIBLE = "ansible_local"
PROVISION_RUN = "always"
BOOT_TIMEOUT = 600

K8S_NAME = "k8s-cluster"
MASTER_PREFIX = "k8s-master-"
WORKER_PREFIX = "k8s-worker-"
ADMIN_USER = "vagrant"
ADMIN_GROUP = "vagrant"
NODE_IP_BASE = "192.168.50."
LAST_OCTET_BASE_IP = 10
POD_NETWORK_CIDR = "172.16.0.0/12"

ZOOKEEPER_NUM = WORKERS_NUM
KAFKA_BROKER_NUM = WORKERS_NUM
KAFKA_TOPICS = "input:1:#{KAFKA_BROKER_NUM}, output:1:#{KAFKA_BROKER_NUM}" # "TOPICNAME:PARTITIONS:REPLICAS"
KAFKA_VOLUME_NAME = "kafka_volume"
KAFKA_VOLUME_SIZE = "5GB"
KAFKA_MOUNT_PATH = "/mnt/kafka"
ZOOKEEPER_VOLUME_NAME = "zookeeper_volume"
ZOOKEEPER_VOLUME_SIZE = "5GB"
ZOOKEEPER_MOUNT_PATH = "/mnt/zookeeper"
GRAFANA_VOLUME_NAME = "grafana_volume"
GRAFANA_VOLUME_SIZE = "5GB"
GRAFANA_MOUNT_PATH = "/mnt/grafana"
PROMETHEUS_VOLUME_NAME = "prometheus_volume"
PROMETHEUS_VOLUME_SIZE = "5GB"
PROMETHEUS_MOUNT_PATH = "/mnt/prometheus"
PROMETHEUS_PORT = 30900
GRAFANA_PORT = 31000

ANSIBLE_PLAYBOOK = "ansible/roles/k8s.yml"

VAGRANT_DISABLE_VBOXSYMLINKCREATE = 1
VAGRANT_VERSION = 2
ENV['VAGRANT_EXPERIMENTAL'] = "disks"

# VirtualBox VMs Setup
Vagrant.configure(VAGRANT_VERSION) do |config|
  config.ssh.insert_key = false

  (1..MASTERS_NUM).each do |i|      
    config.vm.define "#{MASTER_PREFIX}#{i}" do |master|
      master.vm.boot_timeout = BOOT_TIMEOUT
      master.vm.box = IMAGE_NAME
      master.vm.network NETWORK_TYPE, ip: "#{NODE_IP_BASE}#{i + LAST_OCTET_BASE_IP}"
      master.vm.hostname = "#{MASTER_PREFIX}#{i}"
      master.vm.network "forwarded_port", guest: PROMETHEUS_PORT, host: PROMETHEUS_PORT # Exposing Prometheus
      master.vm.network "forwarded_port", guest: GRAFANA_PORT, host: GRAFANA_PORT # Exposing Grafana
      master.vm.provider VM_PROVIDER do |v|
        v.memory = MASTERS_MEM
        v.cpus = MASTERS_CPU
        v.name = "#{MASTER_PREFIX}#{i}"
      end            
      master.vm.provision PROVISION_ANSIBLE, run: PROVISION_RUN do |ansible|
        ansible.playbook = ANSIBLE_PLAYBOOK
        ansible.extra_vars = {
          k8s_cluster_name: K8S_NAME,                    
          k8s_master_admin_user:  ADMIN_USER,
          k8s_master_admin_group: ADMIN_GROUP,
          k8s_master_apiserver_advertise_address: "#{NODE_IP_BASE}#{i + LAST_OCTET_BASE_IP}",
          k8s_master_pod_network_cidr: POD_NETWORK_CIDR,
          k8s_master_node_name: "#{MASTER_PREFIX}#{i}",
          k8s_node_public_ip: "#{NODE_IP_BASE}#{i + LAST_OCTET_BASE_IP}",
          k8s_master_public_ip: "#{NODE_IP_BASE}#{LAST_OCTET_BASE_IP + 1}",
          worker_prefix: WORKER_PREFIX,
          zookeeper_num: ZOOKEEPER_NUM,
          zookeeper_mount_path: ZOOKEEPER_MOUNT_PATH,
          zookeeper_volume_size: ZOOKEEPER_VOLUME_SIZE.chomp("B").concat("i"),
          kafka_broker_num: KAFKA_BROKER_NUM,
          kafka_mount_path: KAFKA_MOUNT_PATH,
          kafka_volume_size: KAFKA_VOLUME_SIZE.chomp("B").concat("i"),
          kafka_topics: KAFKA_TOPICS,
          grafana_mount_path: GRAFANA_MOUNT_PATH,
          grafana_volume_size: GRAFANA_VOLUME_SIZE.chomp("B").concat("i"),
          prometheus_mount_path: PROMETHEUS_MOUNT_PATH,
          prometheus_volume_size: PROMETHEUS_VOLUME_SIZE.chomp("B").concat("i"),
          prometheus_port: PROMETHEUS_PORT,
          grafana_port: GRAFANA_PORT
        }
      end
    end
  end

  (1..WORKERS_NUM).each do |j|
    config.vm.define "#{WORKER_PREFIX}#{j}" do |node|
      node.vm.boot_timeout = BOOT_TIMEOUT
      node.vm.box = IMAGE_NAME
      node.vm.network NETWORK_TYPE, ip: "#{NODE_IP_BASE}#{j + LAST_OCTET_BASE_IP + MASTERS_NUM}"
      node.vm.hostname = "#{WORKER_PREFIX}#{j}"
      node.vm.disk :disk, size: ZOOKEEPER_VOLUME_SIZE, name: ZOOKEEPER_VOLUME_NAME
      node.vm.disk :disk, size: KAFKA_VOLUME_SIZE, name: KAFKA_VOLUME_NAME
      if j == 1 then # Only create Grafana and Prometheus Volumes on the first Worker
        node.vm.disk :disk, size: GRAFANA_VOLUME_SIZE, name: GRAFANA_VOLUME_NAME
        node.vm.disk :disk, size: PROMETHEUS_VOLUME_SIZE, name: PROMETHEUS_VOLUME_NAME
      end
      node.vm.provider VM_PROVIDER do |v|
        v.memory = WORKERS_MEM
        v.cpus = WORKERS_CPU
        v.name = "#{WORKER_PREFIX}#{j}"
      end      
      node.vm.provision PROVISION_ANSIBLE, run: PROVISION_RUN do |ansible|
        ansible.playbook = ANSIBLE_PLAYBOOK
        ansible.extra_vars = {
          k8s_cluster_name: K8S_NAME,
          k8s_node_admin_user:  ADMIN_USER,
          k8s_node_admin_group: ADMIN_GROUP,
          k8s_node_public_ip: "#{NODE_IP_BASE}#{j + LAST_OCTET_BASE_IP + MASTERS_NUM}",
          k8s_master_public_ip: "#{NODE_IP_BASE}#{LAST_OCTET_BASE_IP + 1}",
          zookeeper_mount_path: ZOOKEEPER_MOUNT_PATH,
          kafka_mount_path: KAFKA_MOUNT_PATH,
          grafana_mount_path: GRAFANA_MOUNT_PATH,
          prometheus_mount_path: PROMETHEUS_MOUNT_PATH,
          worker_prefix: WORKER_PREFIX
        }
      end
    end
  end
end
