
# Project_ALV_2022

## LKM Configuration
1. Update current packages of the system to the latest version.
```bash
  sudo apt update && sudo apt upgrade -y
```
2. Download and install the essential packages to compile kernels.
```bash
  sudo apt install build-essential libncurses-dev libssl-dev libelf-dev bison flex -y
  sudo apt install linux-headers-$(uname -r)
```
3. Clean up your installed packages.
```bash
  sudo apt clean && sudo apt autoremove -y
```
4. Compile LKM
Go to Project_ALV_2022 > LKM Folder
```bash
  sudo make ARCH=$(arch) -j$(nproc)
  sudo make
```
5. Load LKM
```bash
  sudo insmod new_kernel.ko 
```
6. To check whether the LKM has loaded successfully or not
```bash
   lsmod
```
