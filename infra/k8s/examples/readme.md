minikube -> in a single VM -> single binary local and single node
microk8s -> in a single VM

kubeadm -> beta but vendor neutral

kubectl -> main command
pod networks
 1. Flannel -> easiest to setup
 2. Calico
 3. Weave
 4. Cilium

GKE,CKE,EKS

$Home/.kube/config


What is a context in kubernetes?
A context is a combination of clusters and user credentials.
$ kubectl config use-context foobar
kubectl get nodes
I insalled kubernates by the instruction from their website and using the root privilagees.
A package was available for k8s.

$kubectl cluster-info
1. control plane
2. dns

kubeadm has community focus and it's stable now\dots
kubeadm is added in k+s 1.4. 

Using apt hold to prevent upgrading kubeadm
$ sudo apt-mark hold kubeadm

We can create a cluster using kubeadm. and install control plane and pod netweeok.
We need to install a container rn time
usefull commands
```
iproute show
```
control plane is etcd and api server.

```
minicube get nodes
kube v 1.31

cp -> control plane

Run kubeadm ini on the cp node
Create a network for IP per pod
kubeadm join on the worker node

keys will be returned by kubeadm init also able to the same with resource manifet in kubectl.
$ kubectl create -f https://git.io/weave-kube-1.4

$ kubeadn uograde
1. plan
2. apply
3. diff
4. node

POD networking
CNI - container network interface
Weave net
Flannel -> Layer 3
Calico
Cilium

kube the hardway -> kelsey hightower -> kube walk thtough

k8s components
1. API Server
2. Controler
3. Scheduler
4. Kubelet
5. Kube proxy
Can I configure HA on my headnores

for deployment
1/ single-node
2/ single node multiple workes
3/ multiple head nodes with multiple workers

# install help
disable swap
load modules
modprove overlay
modprobe be_netfiltter

install containerd.io
apt-mark kunes packages
apt markkube