FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# تعيين متغيرات البيئة الافتراضية (سيتم تجاوزها بواسطة إعدادات Render)
ENV PORT=8000
ENV HOST="0.0.0.0"

# كشف المنفذ الذي سيستمع عليه التطبيق
EXPOSE 8000

# أمر بدء التشغيل
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
