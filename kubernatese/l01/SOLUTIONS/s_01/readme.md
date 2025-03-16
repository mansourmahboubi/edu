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
