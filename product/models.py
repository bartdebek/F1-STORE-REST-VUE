from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Team(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/team', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/team', blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/teams/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'https://orca-app-kgbd6.ondigitalocean.app/' + self.image.url
        else:
            return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'https://orca-app-kgbd6.ondigitalocean.app/' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'https://orca-app-kgbd6.ondigitalocean.app/' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, heigth=200):
        img = Image.open(self.image)
        hpercent = (heigth/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize,heigth), Image.Resampling.LANCZOS)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG')
        thumbnail = File(thumb_io, name=self.image.name)
        return thumbnail



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/product', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/product', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, heigth=200):
        img = Image.open(self.image)
        hpercent = (heigth/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize,heigth), Image.Resampling.LANCZOS)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG')
        thumbnail = File(thumb_io, name=self.image.name)
        return thumbnail
        