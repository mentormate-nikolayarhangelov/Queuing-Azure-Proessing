# Queuing Long Running Tasks on Azure - Proessing Demo
This repository is used for a sample client, which demonstrates the architectural pattern
mentioned in the [Queuing Long Running Tasks on Azure](TODO) blog post.
## Demo
The demo client is a sample Python application, which will get messages from the Pending queue and handle them.
If the JSON message specifies a share, the app will try to mount the share to its file system and will list the contents of the Azure share.
## Steps
1. Log into your Docker on Ubuntu server.
3. Execute  the following commands in the repository folder:
    ```
    $ docker build -t "mentormate-azure-processing" .
    $ docker run --privileged -it mentormate-azure-processing
    ```

**Note:** The *mount* command requires elevated permissions. That is why the *--privileged* parameter is added to *docker run*.

## Mounting Azure Shares
The Azure file shares use a CIFS file system. For Ubuntu you first need to install the CIFS utils.
```
$ sudo apt-get install cifs-utils
```
The mounting is done with the following command:
```
 $ mount -t cifs <source_url> <destination_folder> -o vers=3.0,user=<user>,password=<password>
```
