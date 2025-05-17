# Welcome to MkDocs::DNS

Pour toute la documentation, rendre visite à  [mkdocs.org](http://doc.5.196.93.233.nip.io/).
#### Explication fichier **/etc/named.conf**
```
options {
  listen-on port 53 { 127.0.0.1 ; 192.168.0.1; };
  directory       "/var/named";
  pid-file        "/run/named/named.pid";
  dump-file       "/var/named/data/cache_dump.db";
  statistics-file "/var/named/data/named_stats.txt";
  memstatistics-file    "/var/named/data/named_mem_stats.txt";
  //allow-query           { localnets ; };
  allow-query     { any; };
  forwarders {
    8.8.8.8 ;
    8.8.4.4 ;
  };
};

zone "ahouari" {
  type master;
  file "/var/named/ahouari.db";
};

zone "0.168.192.in-addr.arpa" {
  type master;
  file "/var/named/0.168.192.db";
};

```


* `listen-on port 53`: cela, veut dire que notre serveur de bind écoute en localhost et sur l'adresse 192.168.0.1 sur le port 53

* `dump-file`: Ce fichier, explique l'emplacement dont le DNS serveur va stocker le cache de son contenue

* `statistics-file`: Ce fichier, représente les informations statistiques stocker par le serveur bind pour ses opérations

* `memstatistics-file`: Représente les informations statistiques relié à la mémoire (RAM)

* `allow-query`: représente une/plusieurs adresses IP qui ont le droit pour lancer des requetes pour ce DNS serveur

* `zone "ahouari"`: création d'une zone nommée ahouari et que zone est master et son fichier est dans **/var/named/ahouari.db**
* `zone "0.168.192.in-addr.arpa"`: Cette partie est la zone reverse PTR de la zone ahouari pour l'adresse réseau 192.168.0.0, c'est indiqué que cette zone est la zone reverse de la zone master ahouari et son fichier de configuration est localisé sur **/var/named/0.168.192.in-addr-arpa** 

- Cette configuration définit la partie zone DNS sur un réseau qui écoute dans le port 53 TCP/UDP, ce serveur autorise les queries DNS depuis n'importe quel serveur et il  les forwardes vers les DNS de google
- les autres machines dans le réseau peuvent spécifier l'adresse ip de ce dns serveur afin de faire des requêtes DNS


### Explication de fichier **/var/named/ahouari.db
```
$ORIGIN .
$TTL 10800      ; 3 hours
ahouari                 IN SOA  ah200.ahouari. admin.ah200.ahouari. (
                                2013022757 ; serial
                                3600       ; refresh (1 hour)
                                3600       ; retry (1 hour)
                                604800     ; expire (1 week)
                                38400      ; minimum (10 hours 40 minutes)
                                )
                        NS      ah200.ahouari.
$ORIGIN ahouari.
ah200                   A       192.168.0.1
ah201                   A       192.168.0.2
ah100                   A       192.168.0.10
ah101                   A       192.168.0.11
ah102                   A       192.168.0.12
```
### Explication de fichier ** /var/named/0.168.192.db **
``` 

