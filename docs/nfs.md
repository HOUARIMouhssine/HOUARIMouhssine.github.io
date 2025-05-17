# Welcome to MkDocs::NFS

Pour toute la documentation, rendre visite à  [mkdocs.org](http://doc.5.196.93.233.nip.io/).

## Installation

Sur la machine principale, il faut installer les packages suivants et les démarrer via:  
```
dnf install nfs-utils -y
systemctl enable  nfs-server.service
systemctl start nfs-server.service

```

## Configuration de NFS 
```
cat /etc/exports

[root@ah200 etc]# cat /etc/exports

/data/nfs *(rw,sync,no_subtree_check)

```
et pour exporter ce folder on fait la commande suivant: 

```
exportfs -v

/data/nfs       <world>(sync,wdelay,hide,no_subtree_check,sec=sys,ro,secure,root_squash,no_all_squash)
```

**Pour être sûr que le folder est exporté** 
```
exportfs -s
/data/nfs  *(sync,wdelay,hide,no_subtree_check,sec=sys,ro,secure,root_squash,no_all_squash)

```

## Installation de provisionneur NFS dans le serveur principale

```
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/

helm repo update

helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \

  --set nfs.server=ah200.ahouari \

  --set nfs.path=/data/nfs


[root@ah200 nfs-psql]# kubectl get storageclass

NAME         PROVISIONER                                     RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE

nfs-client   cluster.local/nfs-subdir-external-provisioner   Delete          Immediate           true                   28d

[root@ah200 nfs-psql]# 
```


## Partie Client

**Prérequis**

* Il faut rajouter l'entrée **ah200.ahouari** sur la partie /etc/hosts de chaque machine
* Création du dossier **/data/nfs** dans chaque worker/master
* monté la partition **/data/nfs** sur chaque worker dans le fichier **/etc/fstab**
* Il est préférable d'installer les packages suivant:
``
dnf install nfs-utils nfs4-acl-tools -y
``
## Ajout de domaine name sur les workers

Pour ce faire, j'ai bénéficié du Playbook d'ansible kubespray pour lancer des commandes SHELL afin de rajouter la partie  

```
(python) [root@ah200 nfs] ansible kube_node -i inventory/mycluster/hosts.yaml -m shell  -a "echo 'ah200.ahouari:/data/nfs /mnt/nfs nfs defaults 0 0' >> /etc/fstab " -b --become-user=root --become-method=sudo

(python) [root@ah200 nfs] ansible kube_control_plane -i inventory/mycluster/hosts.yaml -m shell  -a "echo 'ah200.ahouari:/data/nfs /mnt/nfs nfs defaults 0 0' >> /etc/fstab " -b --become-user=root --become-method=sudo


```
## Création du dossier

```
(python) [root@ah200 nfs]ansible kube_control_plane -i inventory/mycluster/hosts.yaml -m command -a "mkdir -p /mnt/nfs" -b --become-user=root --become-method=sudo

(python) [root@ah200 nfs]ansible kube_node -i inventory/mycluster/hosts.yaml -m command -a "mkdir -p /mnt/nfs" -b --become-user=root --become-method=sudo


```
## Montage /mnt/nfs sur ah200.ahouari:/data/nfs

```
(python) [root@ah200 nfs] ansible kube_node -i inventory/mycluster/hosts.yaml -m shell  -a "mount -a" -b --become-user=root --become-method=sudo

(python) [root@ah200 nfs] ansible kube_control_plane -i inventory/mycluster/hosts.yaml -m shell  -a "mount -a" -b --become-user=root --become-method=sudo

(python) [root@ah200 nfs]ansible kube_node -i inventory/mycluster/hosts.yaml -m shell  -a "systemctl daemon-reload" -b --become-user=root --become-method=sudo

(python) [root@ah200 nfs]ansible kube_control_plane -i inventory/mycluster/hosts.yaml -m shell  -a "systemctl daemon-reload" -b --become-user=root --become-method=sudo

```

## Example création BDD avec storage class NFS


```
apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: nfs-storage

provisioner: nfs-subdir-external-provisioner

```

```
apiVersion: v1

kind: ConfigMap

metadata:

  name: psql-itwl-dev-01-cm

data:

  POSTGRES_DB: db

  POSTGRES_USER: ********* 

  POSTGRES_PASSWORD: ***********

  PGDATA: /var/lib/postgresql/data/k8s

---

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: psql-itwl-dev-01-pvc

spec:

  accessModes:

    - ReadWriteMany

  storageClassName: nfs-client 

  resources:

    requests:

      storage: 1Gi

apiVersion: apps/v1

kind: StatefulSet

metadata:

  name: psql-itwl-dev-01

  labels: 

    app: psql 

    ver: itwl-dev-01

spec:

  replicas: 1

  selector:

    matchLabels: 

      app: psql

      ver: itwl-dev-01

  serviceName: "itwl-dev-01"

  template: #For the creation of the pod      

    metadata:

      labels:

        app: psql

        ver: itwl-dev-01

    spec:

      containers:

        - name: postgres

          image: postgres:latest

          imagePullPolicy: "IfNotPresent"

          ports:

            - containerPort: 5432 

          envFrom:

            - configMapRef:

                name: psql-itwl-dev-01-cm          

          volumeMounts:

            - mountPath: /var/lib/postgresql/data

              name: pgdatavol

      volumes:

        - name: pgdatavol

          persistentVolumeClaim:

            claimName: psql-itwl-dev-01-pvc

---



apiVersion: v1

kind: Service

metadata:

  name: postgres-service-lb

spec:

  type: LoadBalancer

  selector:

    app: psql

  ports:

    - name: psql

      port: 5432 

      targetPort: 5432

      nodePort: 30101

      protocol: TCP

```
