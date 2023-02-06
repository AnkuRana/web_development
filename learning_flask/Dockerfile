FROM python
# set the workinf directory to learning_flask
WORKDIR /learning_flask/
# copy local contents to container
ADD . /learning_flask/
#install all requirements
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]