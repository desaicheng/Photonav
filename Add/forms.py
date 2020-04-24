from django import forms
from .models import photo


class newLandmark(forms.Form):
    landmarkImage = forms.ImageField()
# upload_to= settings.SHARE_IMAGE_UPLOAD_PATH


class ImageUpload(forms.ModelForm):
    class Meta:
        model = photo
        fields = ('img',)

        def save(self):
            image = super(ImageUpload, self).save()
            return image
