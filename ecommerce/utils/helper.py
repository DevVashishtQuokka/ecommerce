import random

def generate_otp():
    return str(random.randint(100000, 999999))

def get_object_or_none(model, **kwargs):
    return model.objects.filter(**kwargs).first()