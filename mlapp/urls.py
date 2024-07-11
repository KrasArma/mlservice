from django.urls import path
from .views import PredictionView, TrainModelView, ListModelsView

urlpatterns = [
    path('models/<str:model_id>/prediction/', PredictionView.as_view(), name='model-prediction'),
    path('models/<str:model_id>/train/', TrainModelView.as_view(), name='model-train'),
    path('models/all/', ListModelsView.as_view(), name='model-list'),
]