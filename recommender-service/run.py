# recommender-service/run.py
import uvicorn

if __name__ == "__main__":
    # Apunta a tu archivo main.py y a la variable 'app'
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)