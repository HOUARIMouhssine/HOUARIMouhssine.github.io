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


## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
