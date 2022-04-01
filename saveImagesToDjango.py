""" Copy this Script to Django Shell"""

import os

from plants.models import Plant
from django.core.files.uploadedfile import UploadedFile

for file in os.listdir('/home/moritz/voynich/voynich-image-collector/data'):
     if not os.path.isdir(os.path.join('/home/moritz/voynich/voynich-image-collector/data',file)):
            myPlant = Plant()
            myPlant.page = file.split('.')[0]
            myPlant.page_image.save(file, UploadedFile(file=open(os.path.join('/home/moritz/voynich/voynich-image-collector/data',file),'rb'), content_type='image/jpg'))
            myPlant.svg.save(file, UploadedFile(file=open(os.path.join('/home/moritz/voynich/voynich-image-collector/data',file),'rb'), content_type='image/jpg'))
            myPlant.save()