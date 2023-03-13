from fastapi import FastAPI
import uvicorn
import logging
import io
from starlette.responses import StreamingResponse

from payload import request_body
from cartoongan.test_from_code import transform, transformAll

######## Log Start #######
# console logger
# logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)-4s]  %(message)s")
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-4s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
# Attach LoggingHandler to root logger
logging.getLogger().addHandler(consoleHandler)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)
######## Log End #######

# Declaring our FastAPI instance
app = FastAPI()

# Defining path operation for /predict endpoint
@app.post('/predict')
def predict(data : request_body):    
    logger.info("predict start")
    # Hosoda, Hayao, Shinkai, Paprika
    style = data.style
    input_path = data.file_path
    output_path = './output_images/'
    load_size = 300
    output = transform(style, input_path, output_path, load_size)
    logger.info("predict done")
    return { 'result' : output}
    # return StreamingResponse(io.BytesIO(output.tobytes()), media_type="image/png")

@app.post('/predictAllStyle')
def predictAllStyle(data : request_body):  
    logger.info("predictAllStyle start")  
    # Hosoda, Hayao, Shinkai, Paprika
    input_path = data.file_path
    output_path = './output_images/'
    load_size = 300
    output = transformAll(logger, input_path, output_path, load_size)
    logger.info("predictAllStyle done")  
    return { 'result' : output}
