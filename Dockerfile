FROM sd2e/python3 as pfish-base

RUN pip3 install \
    cliff \
    pydent
 
RUN mkdir /script
WORKDIR /script

COPY ./pxfish .

RUN mkdir /wd
WORKDIR /wd
ENTRYPOINT [ "python3", "/script/pyfish.py"]