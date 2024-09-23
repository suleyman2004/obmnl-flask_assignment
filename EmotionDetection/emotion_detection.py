import requests
import json


def emotion_detector(text_to_analyze):
    """
    Sends a request to the Watson Emotion API to analyze the provided text.

    Args:
        text_to_analyze (str): The text for which to detect emotions.

    Returns:
        dict: A dictionary containing emotion predictions or None for each emotion if the request fails.
    """
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=myobj, headers=header)
    formatted_response = json.loads(response.text)

    if response.status_code == 200:
        return formatted_response
    elif response.status_code == 400:
        formatted_response = {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
        return formatted_response


def emotion_predictor(detected_text):
    """
    Processes the detected emotions and returns the emotions with their scores,
    along with the dominant emotion.

    Args:
        detected_text (dict): The dictionary containing emotion predictions.

    Returns:
        dict: A dictionary containing the scores for each emotion and the dominant emotion.
    """
    if all(value is None for value in detected_text.values()):
        return detected_text
    if detected_text.get('emotionPredictions') is not None:
        emotions = detected_text['emotionPredictions'][0]['emotion']
        anger = emotions['anger']
        disgust = emotions['disgust']
        fear = emotions['fear']
        joy = emotions['joy']
        sadness = emotions['sadness']
        max_emotion = max(emotions, key=emotions.get)
        formatted_dict_emotions = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': max_emotion
        }

        return formatted_dict_emotions
