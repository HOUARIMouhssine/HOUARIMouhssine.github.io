# Welcome to MkDocs::VboxManage

Pour toute la documentation, rendre visite à  [mkdocs.org](http://doc.5.196.93.233.nip.io/).
VboxManage est la partie CLI pour Oracle VM virtualbox, il permet de crée des interfaces réseaux, de les configurer, démarrer ou l'arreter
Dans notre example, il sera utiliser pour créer une interface réseau sur le réseau local dont lequel on va écouter


Pour spécifier le machine folder des VMs via VBoxManage 
``
VBoxManage setproperty machinefolder /data/virtualbox/VM
``
## Création une inteface
```
vboxmanage hostonlyif create
VBoxManage hostonlyif ipconfig vboxnet0 --ip=192.168.0.1 --netmask=255.255.252.0
```
Cette inteface fait partie de la zone dns **ahouari**

## Configuration de Haproxy 
```
frontend http               
    bind 5.196.93.233:80 
    use_backend %[req.hdr(Host),lower] 

frontend https                         
    bind 5.196.93.233:443 #ssl crt /etc/haproxy/cert/server.pem
    mode http                               
    option httplog                             
    use_backend %[req.hdr(Host),lower]
```
**Pour la partie backend (example: virtualbox)** 
```
backend virtualbox.5.196.93.233.nip.io
  balance roundrobin
  server server_virtualbox_1 5.196.93.233:8080 check
```

* `http Frontend`: cela, veut dire que notre serveur écoute toujour sur l'IP 5.196.93.233 dans le port 80  

* `use_backend %[req.hdr(Host),lower]`: Cette partie explique qu'on écoute de chaque backend en basant sur son **host header** qui est **case-insensitive**  et qui fait partie dans le dossier **conf.d**

* `mode http`: on écoute tous le traffic http sur SSL ( pas mode tcp)  

* `option httplog`: cela veut dire qu'on active le mode log pour la partie http 

Si on avait un fichier pem, dans ce cas là , on va utiliser le trafic http over SSL pour chiffrer le traffic en mode loadbalancing
* `backend virtualbox.5.196.93.233.nip.io`: le nom du backend utiliser, il revient vers un nom de **nip.io** qui est un DNS public donc la format est  : *nom.IP.nip.ip* , le nom de ce backend est **server_virtualbox_1**, ce backend va écouter sur le port 8080 avec l'IP public ( Image docker dèjà créer) et configurer



## Docker-compose file
```
version: "3.5"
services:
    vbox_http:
        container_name: vbox_http
        image: joweisberg/phpvirtualbox
        restart: always
        ports:
            - 8080:80
        environment:
            TZ="Europe/Paris"
            SRV1_HOSTPORT="5.196.93.233:18083"
            SRV1_NAME="Server1"
            SRV1_USER="root"
            SRV1_PW="*****"
            CONF_browserRestrictFolders="/home,/usr/lib/virtualbox,"
            CONF_noAuth="true"

```
Pour installer cette image de docker , il faut lancer la commande: 

```
docker-compose -f /data/docker-compose/phpvbox.yaml up  -d
```
Pour supprimer l'image docker 

```
docker-compose -f /data/docker-compose/phpvbox.yaml down
```


### Reset the password: 

Si on veut récupérer le mot de passe de l'utilisateur admin; il faut se connecter sur le container du docker qui est phpvbox et renommer le fichier recovery.php-disabled vers recovery.php 


Aprés il faut rédemmarer le service : `` vboxweb-service ``


### Restart DHCP Server

après avoir choisi le serveur dhcp via l'interface virtualbox, et des fois, il faut le rédemarrer pour prendre en compte le nouveau réseau , pour cela il faut lancer : `` VBoxManage dhcpserver restart  --interface=vboxnet1``
