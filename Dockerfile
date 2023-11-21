FROM python:3.10
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/streamlit_app.py .
COPY app/.env .
EXPOSE 8501
#HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run"]
CMD ["streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]