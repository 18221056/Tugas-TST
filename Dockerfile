# Gunakan base image resmi Python
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements.txt ke dalam container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy seluruh konten proyek ke dalam container
COPY . /app

# Expose port yang akan digunakan oleh FastAPI
EXPOSE 8000

# Command untuk menjalankan aplikasi FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
