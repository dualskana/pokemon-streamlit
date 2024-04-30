# Dockerfile

# 使用官方 Python 3.12 slim 镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制代码
COPY . /app

# 安装 poetry
RUN pip install poetry

# 安装项目依赖
RUN poetry install --no-dev

# 暴露端口
EXPOSE 8081

# 检查
HEALTHCHECK CMD curl --fail http://localhost:8081/_stcore/health

# 运行
ENTRYPOINT ["poetry","run", "streamlit", "run", "app.py", "--server.port=8081", "--server.address=0.0.0.0"]