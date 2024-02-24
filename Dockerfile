FROM quay.io/pypa/manylinux2014_x86_64
# make and connect local machine to /myvol
RUN mkdir /myvol
VOLUME /myvol


# There are no alias for python and pip 
# so set eviroment variable to location
ENV PIP_PATH_37=/opt/python/cp37-cp37m/bin/pip
ENV PY_PATH_37=/opt/python/cp37-cp37m/bin/python

ENV PIP_PATH_38=/opt/python/cp38-cp38/bin/pip
ENV PY_PATH_38=/opt/python/cp38-cp38/bin/python

ENV PIP_PATH_39=/opt/python/cp39-cp39/bin/pip
ENV PY_PATH_39=/opt/python/cp39-cp39/bin/python

ENV PIP_PATH_310=/opt/python/cp310-cp310/bin/pip
ENV PY_PATH_310=/opt/python/cp310-cp310/bin/python

WORKDIR /opt
# install the Lingo API
RUN yum -y install wget 
RUN  wget https://www.lindo.com/downloads/LAPI-LINUX-64x86-15.0.tar.gz
RUN tar -xvzf LAPI-LINUX-64x86-15.0.tar.gz
ENV LINDOAPI_HOME=/opt/lindoapi


RUN git clone https://github.com/lindosystems/lindoapi-python /lindoapi-python
WORKDIR /lindoapi-python
    # Build 3.7
RUN ${PY_PATH_37} -m build;                    \                   
    # Build 3.8
    ${PY_PATH_38} -m build;                     \
    # Build 3.9
    ${PY_PATH_39} -m build;                     \
    # Build 3.10
    ${PY_PATH_310} -m build;                    
 

      # convert to manylinux
 CMD auditwheel repair /lindoapi-python/dist/*cp37*.whl  &&\
     auditwheel repair /lindoapi-python/dist/*cp38*.whl  &&\
     auditwheel repair /lindoapi-python/dist/*cp39*.whl  &&\
     auditwheel repair /lindoapi-python/dist/*cp310*.whl;  \
     # install the manylinux .whl files for testing
     ${PIP_PATH_37} install  /lindoapi-python/wheelhouse/*cp37*.whl;      \
     ${PIP_PATH_38} install  /lindoapi-python/wheelhouse/*cp38*.whl;      \
     ${PIP_PATH_39} install  /lindoapi-python/wheelhouse/*cp39*.whl;      \
     ${PIP_PATH_310} install /lindoapi-python/wheelhouse/*cp310*.whl;     \  
     # copy manylinux .whl files to local directory
     cp /lindoapi-python/wheelhouse/*cp37*.whl /myvol;                   \ 
     cp /lindoapi-python/wheelhouse/*cp38*.whl /myvol;                   \     
     cp /lindoapi-python/wheelhouse/*cp39*.whl /myvol;                   \
     cp /lindoapi-python/wheelhouse/*cp310*.whl /myvol;                  \
     cd samples;\
     # test each .whl file
     echo "Testing 3.7"           >  /myvol/test.txt;    \
     echo "=============================================================" >>  /myvol/test.txt;    \
     ${PY_PATH_37} -m lindo_test  >> /myvol/test.txt;    \
     ${PY_PATH_37} lp.py  >> /myvol/test.txt;    \
     ${PY_PATH_37} mip.py  >> /myvol/test.txt;    \
     ${PY_PATH_37} nlp.py  >> /myvol/test.txt;    \
     ${PY_PATH_37} qp.py  >> /myvol/test.txt;    \
     ${PY_PATH_37} sp.py  >> /myvol/test.txt;    \
     echo "Testing 3.8"           >> /myvol/test.txt;    \
     echo "=============================================================" >>  /myvol/test.txt;    \
     ${PY_PATH_38} -m lindo_test  >> /myvol/test.txt;    \
     ${PY_PATH_38} lp.py  >> /myvol/test.txt;    \
     ${PY_PATH_38} mip.py  >> /myvol/test.txt;    \
     ${PY_PATH_38} nlp.py  >> /myvol/test.txt;    \
     ${PY_PATH_38} qp.py  >> /myvol/test.txt;    \
     ${PY_PATH_38} sp.py  >> /myvol/test.txt;    \
     echo "Testing 3.9"           >> /myvol/test.txt;    \
     echo "=============================================================" >>  /myvol/test.txt;    \
     ${PY_PATH_39} -m lindo_test  >> /myvol/test.txt;    \
     ${PY_PATH_39} lp.py  >> /myvol/test.txt;    \
     ${PY_PATH_39} mip.py  >> /myvol/test.txt;    \
     ${PY_PATH_39} nlp.py  >> /myvol/test.txt;    \
     ${PY_PATH_39} qp.py  >> /myvol/test.txt;    \
     ${PY_PATH_39} sp.py  >> /myvol/test.txt;    \
     echo "Testing 3.10"          >> /myvol/test.txt;    \
     echo "=============================================================" >>  /myvol/test.txt;    \
     ${PY_PATH_310} -m lindo_test >> /myvol/test.txt;                        \
     ${PY_PATH_310} lp.py  >> /myvol/test.txt     \
     ${PY_PATH_310} mip.py  >> /myvol/test.txt;    \
     ${PY_PATH_310} nlp.py  >> /myvol/test.txt;    \
     ${PY_PATH_310} qp.py  >> /myvol/test.txt;    \
     ${PY_PATH_310} sp.py  >> /myvol/test.txt;    


