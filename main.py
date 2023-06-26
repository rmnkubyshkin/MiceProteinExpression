import os
from wsgiref import simple_server

from flask import Response, render_template, Flask
from flask_cors import cross_origin, CORS
import flask_monitoringdashboard as dashboard
from prediction import Prediction
from training import Training

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def train():
    try:
        training_model = Training()
        training_model.train()
    except ValueError as e:
        return Response(f'Error occurred! {e}')
    except KeyError as e:
        return Response(f'Error occurred! {e}')
    except Exception as e:
        return Response(f'Error occurred! {e}')
    return Response("Training successful!")


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    try:
        prediction_model = Prediction()
        prediction_model.predict()
    except ValueError as e:
        return Response(f'Error occurred! {e}')
    except KeyError as e:
        return Response(f'Error occurred! {e}')
    except Exception as e:
        return Response(f'Error occurred! {e}')
    return Response("Prediction successful!")


port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    host = "0.0.0.0"
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()

