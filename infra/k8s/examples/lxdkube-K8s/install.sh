# prepare the system for docker installation
apt-get install -y apt-transport-https ca-certificates curl gnupg

# add kuber mirror
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key -o /tmp/k8s.key
gpg --batch --yes --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg /tmp/k8s.key
rm -f /tmp/k8s.key
chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg # allow unprivileged APT programs to read this keyring
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' |  tee /etc/apt/sources.list.d/kubernetes.list
chmod 644 /etc/apt/sources.list.d/kubernetes.list   # helps tools such as command-not-found to work correctly
#install a container runtime
apt-get update
apt-get install -y kubeadm kubectl kubelet docker.io

# # Add Docker's official GPG key
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# # Add Docker repository
# add-apt-repository \
#    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#    $(lsb_release -cs) \
#    stable"

# # Install Docker
# apt-get update
# apt-get install -y docker-ce docker-ce-cli containerd.io


# sysctl
cat <<EOF |  tee /etc/sysctl.d/k8s.conf
net.ipv4.ip_forward = 1
EOF

# disable swap
swapoff -a
# kubeadm config images pull
kubeadm init
