<!-- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/ -->
# Manuall Install kubernates
`curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"`
sha validation is required.
v1.32.3 is stable at the moment.

`
## Install it.
``` install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl```

## Verify the installation
```kubectl version --client```
```kubectl version --client --output=yaml```
# Insatll using deb package
` apt-get install -y apt-transport-https ca-certificates curl gnupg`
keys
```
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key |  gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
 chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg # allow unprivileged APT programs to read this keyring
```
Add the repo
```
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' |  tee /etc/apt/sources.list.d/kubernetes.list

chmod 644 /etc/apt/sources.list.d/kubernetes.list   # helps tools such as command-not-found to work correctly
```
Install kubectl
``` apt-get install -y kubectl```


# sysctl params required by setup, params persist across reboots
cat <<EOF |  tee /etc/sysctl.d/k8s.conf
net.ipv4.ip_forward = 1
EOF

# Apply sysctl params without reboot
 sysctl --system

 https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/

apt install iproute2

install a container runtime
apt install docker.io kubeadm kubectl
