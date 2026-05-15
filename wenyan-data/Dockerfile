FROM python:3.13-slim

WORKDIR /app

# 只装依赖，不拷贝代码（代码通过 volume 挂载）
RUN pip install --no-cache-dir flask

EXPOSE 8080

CMD ["python", "app.py"]
