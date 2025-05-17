# Welcome to MkDocs::Documentation

Pour toute la documentation, rendre visite à  [mkdocs.org](http://doc.5.196.93.233.nip.io/).
#### Source de l'environnement
```
source /data/python/bin/activate
```
#### Entrer dans le répertoire 
```
cd /data/Documentation
git fetch
git init 
git add .
mkdocs gh-deploy -r https://github.com/HOUARIMouhssine/ahouari.github.io -b main
```
### Création d'un service

Pour que l'url du doc soit accessible en temps réel ( ce qui veut dire sans sourcer l'environnement à chaque fois et lancer le mkdocs serve), j'ai crée un fichier bash dédier pour faire ça.
```

[root@ah200 Documentation]# cat permanent_running.sh 
#!/bin/bash

# Source your virtual environment

source /data/python/bin/activate



# Run mkdocs serve

cd /data/Documentation && mkdocs serve
```
Pour que cette partie soit permanente, j'ai crée un fichier daemon sous forme du service  : 

```
[root@ah200 Documentation]# systemctl status mkdocs.service 

● mkdocs.service - MKDocs Service

     Loaded: loaded (/etc/systemd/system/mkdocs.service; disabled; preset: disabled)

     Active: active (running) since Mon 2024-02-12 16:50:31 UTC; 6 days ago

   Main PID: 902882 (permanent_runni)

      Tasks: 8 (limit: 203086)

     Memory: 33.5M

        CPU: 12min 40.005s

     CGroup: /system.slice/mkdocs.service

             ├─902882 /bin/bash /data/Documentation/permanent_running.sh

             └─902883 /data/python/bin/python /data/python/bin/mkdocs serve


[root@ah200 Documentation]# cat /etc/systemd/system/mkdocs.service 
[Unit]
Description=MKDocs Service
After=network.target
[Service]
Type=simple
ExecStart=/bin/bash -c '/data/Documentation/permanent_running.sh'
[Install]
WantedBy=multi-user.target
[root@ah200 Documentation]# 
```
