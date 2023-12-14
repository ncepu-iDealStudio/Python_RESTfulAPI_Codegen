# set basic mirror: Centos7
FROM centos:7
ENV python_version=3.9.6
LABEL title="centos7_Python"${python_version}

# set local yum resource
RUN yum -y install wget
RUN cd /etc/yum.repos.d/ \
 && rm -rf /etc/yum.repos.d/*.repo \
&& wget  http://mirrors.aliyun.com/repo/Centos-7.repo \
&& yum clean all \
&& yum makecache

# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install Development Tools requiments
RUN yum -y groupinstall "Development Tools" \
&&  yum -y install openssl-devel bzip2-devel libffi-devel \
&&  rm -rf /var/cache/yum/* \
&&  yum clean all

#install Python
WORKDIR /usr/local
RUN mkdir python3
RUN wget https://www.python.org/ftp/python/${python_version}/Python-${python_version}.tgz
RUN tar xvf Python-${python_version}.tgz
WORKDIR /usr/local/Python-${python_version}
RUN ./configure --prefix=/usr/local/python3 && make && make install
RUN ln -s /usr/local/python3/bin/python3 /usr/bin/python3 \
&& ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3 && pip3 install --upgrade pip
RUN python3 --version

#Centos bugfix for python--根据操作系统的情况增加安装或者卸载软件包

#clean up
WORKDIR /usr/local
RUN rm -f Python-${python_version}.tgz && rm -rf /usr/local/Python-${python_version}
RUN yum -y groupremove "Development Tools"

#python3 [command]

# Setup the environment
ENV PYTHONIOENCODING=utf-8

# Build folder
RUN mkdir -p /deploy/app
WORKDIR /deploy/app

# copy requirements.txt.   othors will be mounted by -v
COPY ./requirements.txt /deploy/app/requirements.txt

# Create a virtual environment
RUN python3 -m venv venv \
&& source ./venv/bin/activate \
&& pip3 install -r /deploy/app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
&& pip3 install gunicorn==20.1.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# system bugfix
COPY ./deploy/werkzeug.py  /deploy/app/venv/lib/python3.8/site-packages/werkzeug/__init__.py
COPY ./deploy/flask_uploads.py /deploy/app/venv/lib/python3.8/site-packages/flask_uploads.py

CMD ["/bin/bash"]
