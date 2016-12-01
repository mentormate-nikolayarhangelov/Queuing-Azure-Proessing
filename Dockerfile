FROM ubuntu:latest
MAINTAINER Nikolay Arhangelov MentorMate

# Install packages
RUN apt-get update && apt-get install -y \
	cifs-utils \
	python-pip
RUN pip install azure

# Add the client files
ADD client.py /mentormate/azure-processing-client/

# Run with the appropriate Azure environment settings
CMD python /mentormate/azure-processing-client/client.py \
	--queue-account="<queue-storage-account>" \
	--queue-key="<queue-storage-key>" \
	--storage-endpoint="<share-storage-endpoint>" \
	--storage-account="<share-storage-key>" \
	--storage-key="<share-storage-password>"
