FROM staphb/freyja:1.5.2-11_25_2024-01-52-2024-11-25

WORKDIR /opt/

RUN pip3 install cyvcf2==0.31.1
RUN wget https://github.com/sigven/vcf2tsvpy/archive/refs/tags/v0.6.1.tar.gz
RUN tar -xvf v0.6.1.tar.gz

WORKDIR /opt/vcf2tsvpy-0.6.1
RUN python3 setup.py install

COPY ./references /root/references
COPY ./freyjaSupport /root/freyjaSupport
COPY ./*.py /root

CMD python3 /root/main.py