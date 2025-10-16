Stock Analisis AI

This library use 
CrewAI
AzureOpenAI

docker
docker build -t financial-analysis-api .

docker run -d -p 8000:8000 --env-file .env --name financial-app financial-analysis-api

curl -X POST "http://localhost:8000/analyze" \
-H "Content-Type: application/json" \
-d '{
  "stock_selection": "MELI"
}'

http://127.0.0.1:8000/analyze?stock_selection=MELI&date_analysis=2025-09-09


uvicorn main:app --host 0.0.0.0  --reload  --port 8000