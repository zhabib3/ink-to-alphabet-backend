import logging
import json
import base64
from pathlib import Path
import azure.functions as func
from fastai.vision import open_image, load_learner


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function processed a request.')
    # Get Image base64 uri and convert it to png
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Error: HTTP Request Body is empty", status_code=400)

    img_url = req_body['imgURL']
    path = Path.cwd()
    cnn_model = load_learner(path=path, file="model.pkl")
    if img_url:
        header, img_b64_data = img_url.split(",", 1)
        with open("alphabet.png", "wb") as f:
            try:
                f.write(base64.b64decode(img_b64_data))
            except Exception:
                return func.HttpResponse(f"Error: Unable to parse data url in request body", status_code=400)

        # Load up the image and predict alphabet
        img = open_image("alphabet.png")
        prediction = cnn_model.predict(img)
        class_idx = prediction[1].item()
        predicted_alpha = ALPHABETS[class_idx]
        logging.info(f"Predicted Alphabet: {ALPHABETS[class_idx]}")
    else:
        return func.HttpResponse(f"Error: Request body must have field `imgURL` that contains base64 image uri", status_code=400)

    res = {
        "Predicted Alphabet": predicted_alpha
    }
    headers = {"Access-Control-Allow-Origin": "*"}
    return func.HttpResponse(
        json.dumps(res),
        mimetype="application/json",
        headers=headers
    )


ALPHABETS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
