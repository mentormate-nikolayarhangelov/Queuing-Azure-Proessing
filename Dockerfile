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
	--queue-account="mmstorageacc" \
	--queue-key="HvcHprcC16hJ3+hQ4+Ad8JIS+l9Ht8IK5nogIwgvUS7Crv3etTnV3ZzU99JnF1De5op2KNDwc90B2EDnaXGbEw==" \
	--storage-endpoint="//mmstorageacc.file.core.windows.net/" \
	--storage-account="mmstorageacc" \
	--storage-key="HvcHprcC16hJ3+hQ4+Ad8JIS+l9Ht8IK5nogIwgvUS7Crv3etTnV3ZzU99JnF1De5op2KNDwc90B2EDnaXGbEw=="