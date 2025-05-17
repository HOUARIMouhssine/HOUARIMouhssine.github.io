# Welcome to MkDocs::NFS

Pour toute la documentation, rendre visite à  [mkdocs.org](http://doc.5.196.93.233.nip.io/).

Afin de mettre en place un cluster Ceph il faut installer les deux composants: 

- Ceph Operator
- Ceph Cluster


#Rook-ceph Operator

On devait installer rook-ceph operator via Helm en utilisant la commande suivante: 

Ceph-Operator est dédié pour faire un watch de tout le cluster ceph et c'est lui qui va installer tous les CRDs

```
helm repo add rook-release https://charts.rook.io/release

helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph -f values.yaml

```

Le fichier values.yaml contient les valeurs suivant: 

```
csi:
  enableCephfsDriver: true
  enableRbdDriver: false

```

Maintenant , dans le namespace **rook-ceph** on voit le pod Operator qui est en phase Running 

```
kubectl get pods -n rook-ceph

rook-ceph-operator-5f4c57f467-2m6v5               1/1     Running     1 (4d16h ago)   7d23h
```

## Ceph Cluster 

Avant d'installer le cluster ceph, nous devons créer des disque sur virtualbox sur nos différents VM. 


Nous installons cephcluster avec Helm avec l'application du fichier values.yaml comme suite: 

``` 
helm repo add rook-release https://charts.rook.io/release

helm install --create-namespace --namespace rook-ceph rook-ceph-cluster \

   --set operatorNamespace=rook-ceph rook-release/rook-ceph-cluster -f values.yaml

```

Le fichier values est comme suite: 

``` 
 apiVersion: ceph.rook.io/v1

 kind: CephCluster

 metadata:

   name: rook-ceph

   namespace: rook-ceph

 spec:

   cephVersion:

     image: quay.io/ceph/ceph:v18.2.2

   cleanupPolicy:

     sanitizeDisks: {}

   crashCollector: {}

   dashboard:

     enabled: true

   dataDirHostPath: /var/lib/rook

   disruptionManagement: {}

   external: {}

   healthCheck:

     daemonHealth:

       mon: {}

       osd: {}

       status: {}

   logCollector: {}

   mgr:

     count: 2

   mon:

     count: 3

   monitoring: {}

   storage:

     deviceFilter: sdb

     nodes:

     - name: ah101

       resources: {}

     - name: ah102

       resources: {}

     - name: ah103

       resources: {}

     useAllDevices: false

kind: List

metadata:

 resourceVersion: ""

```

## CephFileSystem 

Sur mon cluster, on va utiliser une solution basé sur partage de fichier de système (FS), pour cela , il faut appliquer la CRD  **Cephfilesystem** qui va permettre de créer un pool qui s'appelle **replicated** qui sera utiliser comme la source qui va être utiliser par les OSD afin d'offire une solution de disque de type Ceph FS 

```
apiVersion: v1
items:
- apiVersion: ceph.rook.io/v1
  kind: CephFilesystem
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"ceph.rook.io/v1","kind":"CephFilesystem","metadata":{"annotations":{},"name":"myfs","namespace":"rook-ceph"},"spec":{"dataPools":[{"failureDomain":"host","name":"replicated","replicated":{"size":3}}],"metadataPool":{"failureDomain":"host","replicated":{"size":3}},"metadataServer":{"activeCount":1,"activeStandby":true,"annotations":null,"placement":null,"resources":null},"preserveFilesystemOnDelete":true}}
    creationTimestamp: "2024-10-23T16:03:08Z"
    finalizers:
    - cephfilesystem.ceph.rook.io
    generation: 2
    name: myfs
    namespace: rook-ceph
    resourceVersion: "1085330"
    uid: 3d660751-477b-4df5-be92-52bb0b3be3d1
  spec:
    dataPools:
    - application: ""
      erasureCoded:
        codingChunks: 0
        dataChunks: 0
      failureDomain: host
      mirroring: {}
      name: replicated
      quotas: {}
      replicated:
        size: 3
      statusCheck:
        mirror: {}
    metadataPool:
      application: ""
      erasureCoded:
        codingChunks: 0
        dataChunks: 0
      failureDomain: host
      mirroring: {}
      quotas: {}
      replicated:
        size: 3
      statusCheck:
        mirror: {}
    metadataServer:
      activeCount: 1
      activeStandby: true
      placement: {}
      resources: {}
    preserveFilesystemOnDelete: true
    statusCheck:
      mirror: {}
  status:
    observedGeneration: 2
    phase: Ready
kind: List
metadata:
  resourceVersion: ""
``` 
Finalement nous pouvons créer notre Storageclasse qui portera le nom de rook-cephfs et qui sera utiliser pour toute demande de volume 


Attention: tout type de demande du PVC devrai être de mode ReadWriteMany pour un type de FS


```
apiVersion: v1
items:
- allowVolumeExpansion: true
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"allowVolumeExpansion":true,"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{},"name":"rook-cephfs"},"mountOptions":null,"parameters":{"clusterID":"rook-ceph","csi.storage.k8s.io/controller-expand-secret-name":"rook-csi-cephfs-provisioner","csi.storage.k8s.io/controller-expand-secret-namespace":"rook-ceph","csi.storage.k8s.io/node-stage-secret-name":"rook-csi-cephfs-node","csi.storage.k8s.io/node-stage-secret-namespace":"rook-ceph","csi.storage.k8s.io/provisioner-secret-name":"rook-csi-cephfs-provisioner","csi.storage.k8s.io/provisioner-secret-namespace":"rook-ceph","fsName":"myfs","pool":"myfs-replicated"},"provisioner":"rook-ceph.cephfs.csi.ceph.com","reclaimPolicy":"Delete"}
    creationTimestamp: "2024-10-23T16:06:43Z"
    name: rook-cephfs
    resourceVersion: "518644"
    uid: 1a98809f-20c1-439e-aa5f-4bf2a34a4d5a
  parameters:
    clusterID: rook-ceph
    csi.storage.k8s.io/controller-expand-secret-name: rook-csi-cephfs-provisioner
    csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
    csi.storage.k8s.io/node-stage-secret-name: rook-csi-cephfs-node
    csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
    csi.storage.k8s.io/provisioner-secret-name: rook-csi-cephfs-provisioner
    csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
    fsName: myfs
    pool: myfs-replicated
  provisioner: rook-ceph.cephfs.csi.ceph.com
  reclaimPolicy: Delete
  volumeBindingMode: Immediate
kind: List
metadata:
  resourceVersion: ""
```

## Création d'un PVC 
Un exemple d'un PVC est comme suivant: 
 
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rbd-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: rook-cephfs
```
