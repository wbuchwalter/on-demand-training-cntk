First we will need to create a custom VM image. This will allow our future deployments to be much faster by not having to download and install every component every time.

### Create a template image
Create a new VM, here are the important parameters:

Base Image: Ubuntu 16.04 LTS
Disk: HDD (you can't access the new N-Series if using SSD for the time being)
Location: South Central US, or other regions supporting N-seires
Size: NC* or NV*

### Install prerequisites on the VM

__Basics__
```bash
sudo apt-get update
sudo apt-get install gcc
sudo apt-get install make
``` 

__Docker__  
If you use a different version of Ubuntu, check the [official documentation](https://docs.docker.com/engine/installation/) instead.
```
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
sudo apt-get install docker-engine
sudo service docker start
```

__Optional__  
Pre-pull heavy docker images.  
CNTK's docker images is quite heavy so pulling it can be relatively long. By pulling it now, we will save a lot of time every time we re-deploy.
Note that the [official CNTK image](https://hub.docker.com/r/microsoft/cntk/tags/) is currently outdated, so we are using another one in the mean time.
```bash
sudo docker pull alfpark/cntk:2.0beta4-gpu-openmpi
```
__NVIDIA Driver & nvidia-docker__  
Download NVIDIA drivers and nvidia-docker package, but don't install them yet (otherwise there will be issues with the generalized image):
```
sudo mkdir /tools
sudo wget -P /tools http://us.download.nvidia.com/XFree86/Linux-x86_64/375.20/NVIDIA-Linux-x86_64-375.20.run
sudo wget -P /tools https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.0-rc.3/nvidia-docker_1.0.0.rc.3-1_amd64.deb
```

The driver and nvidia-docker will be installed automatically when the VM is created through a custom extensions.

### Capture the VM

Follow Step 1 and 2 of [Capture a Linux virtual machine running on Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-linux-capture-image?toc=%2fazure%2fvirtual-machines%2flinux%2ftoc.json)
If you are using the new Azure CLI (`az`), just replace `azure` by `az`, the commands are mostly the same.

### Update ARM template

In the ARM template (`template.json`), replace the `storageProfile` from the virtual machine resource by the one outputed by the `az vm capture` command.


### Create a new VM

To make sure everything is working fine, we are going to create a new VM based on our captured image

Start by creating a new resource group (if you choose a different location, make sure it offers N-Series)
`az resource group create -l southcentralus -n <group-name>`

Let's deploy our template in our new group:
`az resource group deployment create -g <group-name> --template-file template.json --parameters "{\"adminPassword\": {\"value\": \"<password>\"}}"`

SSH into the newly created VM (you can find the public IP in the portal):
`ssh agent@xx.xx.xx.xx`

Test that everything is running correctly:
`sudo nvidia-docker run --rm nvidia/cuda nvidia-smi`

That should display some information on your GPU from inside a docker container:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 375.20                 Driver Version: 375.20                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K80           Off  | B9EB:00:00.0     Off |                    0 |
| N/A   46C    P8    28W / 149W |    121MiB / 11471MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```


### Cleaning up
You can now delete everything in your original resource group that was used to capture the VM **except** the storage account, since that's where the VHD is stored.
