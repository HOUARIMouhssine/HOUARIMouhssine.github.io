# Welcome to MkDocs::Vagrant

Pour toute la documentation, rendre visite à  [mkdocs.org](http://doc.5.196.93.233.nip.io/).
#### Installation
```
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/fedora/hashicorp.repo
sudo dnf -y install vagrant
```
on pourra après voir sa version via 
``
vagrant --version
``

#### Command utiles
* `vagrant init` : Pour initier vagrant file.
* `vagrant global-status` : Pour voir le status complet de tous les VMs crée si ils sont en mode running ou non.
* `vagrant up <Vagrantfile>` : Pour mettre en tension et démarrer une VM auprès un fichier vagrant.
* `vagrant  reload ` : redémarrer une VM vagrant
* `vagrant  halt ` : stop une VM vagrant
* `vagrant  suspend ` : mettre une VM vagrant en mode suspende en gardant son état
* `vagrant  destroy <machine id> -f  `: supprimer une machine vagrant sans confirmation
* `vagrant box list `: pour récupirer tous les OS et les box installés
 

### VagrantFile
```
Vagrant.configure("2") do |config|
  config.vm.box = "almalinux/9"
  config.vm.hostname = "ah100"
  config.vm.network :private_network, ip: "192.168.0.10", netmask:"255.255.252.0"
  config.vm.provider :virtualbox do |vb|
    vb.customize [
      "modifyvm", :id,
      "--cpuexecutioncap", "50",
      "--memory", "2048",
    ]
  end
end
```
Un autre example de mettre en place une VM almalinux9 avec une configuration ssh qui permet:

*  changer la partie **PermitRootLogin** to **YES** . 
*  changer le mot de passe de l'utilisateur root .  

```
Vagrant.configure("2") do |config|
  config.vm.box = "almalinux/9"
  config.vm.hostname = "ah101"
  config.vm.network :private_network, ip: "192.168.0.11", netmask: "255.255.252.0"
  config.vm.provider :virtualbox do |vb|
    vb.customize [
      "modifyvm", :id,
      "--cpuexecutioncap", "50",
      "--memory", "2048",
    ]
  end
  config.vm.provision "shell", inline: <<-SHELL
    # Set root password to 'your_password'
    echo 'root:your_password' | chpasswd
    # Enable PermitRootLogin in /etc/ssh/sshd_config
    sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    # Restart ssh service
    systemctl restart sshd
  SHELL
end
```
