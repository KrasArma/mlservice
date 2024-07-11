from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Prediction
from .serializers import PredictionSerializer
from minio import Minio
from keras.models import load_model
from django.conf import settings
import xgboost as xgb
import pandas as pd
import numpy as np
import joblib
from .utils import preprocess_text, tfidf_vectorizer, label_encoder
import json
from .minio_client import download_file, client
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical


class PredictionView(APIView):
    def post(self, request, model_id):
        input_data = request.data.get('input')
        user_id = request.data.get('user_id')

        if model_id == "1":
   
            local_file_path = "spell_classifier_model_v1_0.h5"
            download_file("models", local_file_path, local_file_path)
            model = load_model(local_file_path)
            
      
            processed_text = preprocess_text(input_data['text'])
            text_tfidf = tfidf_vectorizer.transform([processed_text])
            text_seq = pad_sequences(text_tfidf.toarray(), maxlen=500)
            prediction = model.predict(text_seq)
            predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])
            output_data = json.dumps(predicted_label[0])
        
        elif model_id == "2":
       
            local_file_path = "catboost_model_v1.cbm"
            download_file("models", local_file_path, local_file_path)
            model = xgb.Booster()
            model.load_model(local_file_path)
      
            df = pd.DataFrame([input_data])
            print(df.dtypes)
            dmatrix = xgb.DMatrix(df.drop(columns='CLIENT_ID', axis=0))
            print(dmatrix)
            prediction = model.predict(dmatrix)
            output_data = prediction[0]

        print('Данные получены')
        prediction_record = Prediction(user_id=user_id, input_data=json.dumps(input_data), output_data=output_data, model_id=model_id)
        prediction_record.save()

        return Response({'prediction': output_data}, status=status.HTTP_200_OK)

class TrainModelView(APIView):
    def post(self, request, model_id):
        data = json.loads(request.body)
        texts = data['texts']
        labels = data['labels']
        
        if model_id == "1":
            local_file_path = "spell_classifier_model_v1_0.h5"
            download_file("models", local_file_path, local_file_path)
            spell_classifier = load_model(local_file_path)
            
      
            processed_texts = [preprocess_text(text) for text in texts]
            text_tfidf = tfidf_vectorizer.transform(processed_texts)
            text_seq = pad_sequences(text_tfidf.toarray(), maxlen=500)
            numeric_labels = label_encoder.transform(labels)
            
        
            num_classes = len(label_encoder.classes_)
            categorical_labels = to_categorical(numeric_labels, num_classes=num_classes)

   
            spell_classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

            spell_classifier.fit(text_seq, categorical_labels, epochs=5, batch_size=32)
            
            spell_classifier.save(local_file_path)
            client.fput_object('models', local_file_path, local_file_path)

            return Response({'message': 'Model trained successfully'}, status=status.HTTP_200_OK)
        
        elif model_id == "2":
            local_file_path = "catboost_model_v1.cbm"
            download_file("models", local_file_path, local_file_path)
            model = xgb.Booster()
            model.load_model(local_file_path)

            df = pd.DataFrame(texts)
            print(df.drop(columns='CLIENT_ID', axis=0))
            dmatrix = xgb.DMatrix(df.drop(columns='CLIENT_ID', axis=0), label=labels)
            params = model.attributes()
            xgb_train = xgb.train(params, dmatrix, xgb_model=model)
            xgb_train.save_model('catboost_model_v1.cbm')
            return Response({'message': 'Model trained successfully'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'message': 'Invalid model ID'}, status=status.HTTP_400_BAD_REQUEST)

class ListModelsView(APIView):
    def get(self, request):

        models_list = [
            {"model_id": "1", "name": "Keras Spell Classifier"},
            {"model_id": "2", "name": "XGBoost Client Model"}
        ]
        return Response(models_list, status=status.HTTP_200_OK)

