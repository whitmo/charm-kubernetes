Kubernetes Minion Charm
=======================

[Kubernetes](https://github.com/googlecloudplatform/kubernetes) is an open
source  system for managing containerized applications across multiple hosts.
Kubernetes uses [Docker](http://www.docker.io/) to package, instantiate and run
containerized applications.  

The Kubernetes Juju charms enable you to run Kubernetes on all the cloud
platforms that Juju supports.

A Kubernetes deployment consists of several independent charms that can be
scaled to meet your needs

### etcd
The etcd charm is a key value store for Kubernetes.  All persistent master state
is stored in `etcd`.

### flannel
Is the networking component for Docker containers.

### kubernetes-master
Contains the API server, scheduler and other components to manage the
environment.

### kubernetes
Has the services necessary to run Docker containers and is managed by the master
system.

Usage
-----

To deploy a Kubernetes environment in Juju :


    juju deploy cs:~hazmat/trusty/etcd
    juju deploy cs:~hazmat/trusty/flannel
    juju deploy local:trusty/kubernetes-master
    juju deploy local:trusty/kubernetes

    juju add-relation etcd flannel
    juju add-relation etcd kubernetes
    juju add-relation etcd kubernetes-master
    juju add-relation kubernetes kubernetes-master


To interact with the kubernetes environment, either build or
[download](https://github.com/GoogleCloudPlatform/kubernetes/releases) the
[kubectl](https://github.com/GoogleCloudPlatform/kubernetes/blob/master/docs/kubectl.md)
binary (available in the releases binary tarball) and point it to the master with :


    $ juju status kubernetes-master | grep public
    public-address: 104.131.108.99
    $ export KUBERNETES_MASTER="104.131.108.99"

# Configuration
For you convenience this charm supports changing the version of kubernetes binaries.  
This can be done through the Juju GUI or on the command line:

    juju set kubernetes version=”v0.8.2”

If the charm does not already contain the tar file with the desired architecture 
and version it will attempt to download the kubernetes binaries using the gsutil 
command.

Congratulations you know have deployed a Kubernetes environment! Use the
[kubectl](https://github.com/GoogleCloudPlatform/kubernetes/blob/master/docs/kubectl.md) 
to interact with the environment.

# Kubernetes information

- [Kubernetes github project](https://github.com/GoogleCloudPlatform/kubernetes)
- [Kubernetes issue tracker](https://github.com/GoogleCloudPlatform/kubernetes/issues)
- [Kubernetes Documenation](https://github.com/GoogleCloudPlatform/kubernetes/tree/master/docs)
- [Kubernetes releases](https://github.com/GoogleCloudPlatform/kubernetes/releases)
