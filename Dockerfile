FROM python:3.6
# Add in the code ot the enviroment
RUN mkdir /App
WORKDIR /App
ADD . /App/
# Install UWSGI
RUN pip install --no-cache-dir uwsgi
# Install the base application requirements
RUN pip install --no-cache-dir -r requirements.txt 

# Envirment variables to modify settings
ENV IN_CONTAINER=1

# Start the celery queeus running
RUN celery -A OutletMeKnow worker -l info -S django
RUN celery -A OutletMeKnow beat -l info -S django

CMD [ "uwsgi", "--ini", "/app/uwsgi.ini" ]
