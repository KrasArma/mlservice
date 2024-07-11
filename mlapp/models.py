from django.db import models

class Prediction(models.Model):
    user_id = models.IntegerField()
    input_data = models.TextField()
    output_data = models.TextField()
    model_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)