# set basic mirror you can select suitable python version
FROM python:3.9.18-slim-bullseye


# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Build folder
RUN mkdir -p /deploy/app
WORKDIR /deploy/app
COPY ./api.experiment.ncepu.edu.cn/. /deploy/app

# copy requirements.txt.   othors will be mounted by -v
COPY ./api.experiment.ncepu.edu.cn/requirements.txt /deploy/app/requirements.txt

# Create a virtual environment
RUN pip install -r /deploy/app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

RUN sed -i 's/from werkzeug import secure_filename, FileStorage/from werkzeug.datastructures import FileStorage\nfrom werkzeug.utils import secure_filename/g' /usr/local/lib/python3.9/site-packages/flask_uploads.py
