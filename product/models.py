from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """
    Stores a product category that has a foreign key relation to
    Product class.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        """Automatically creaetes slug from entered name."""
        if not self.id:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)


class Team(models.Model):
    """
    Stores a F1 team that has a foreign key relation to Product class.
    """
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/team', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/team', blank=True, null=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/teams/{self.slug}/'

    def get_image(self):
        "Returns url to full size team logo."
        if self.image:
            return self.image.url
        else:
            return ''

    def get_thumbnail(self):
        "Returns url to team logo thumbnail."
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, heigth=400):
        "Creates team logo thumbnail from given picture."
        img = Image.open(self.image)
        hpercent = (heigth/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))

        img = img.resize((wsize, heigth), Image.Resampling.LANCZOS)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG')
        thumbnail = File(thumb_io, name=self.image.name)
        return thumbnail

    def save(self, *args, **kwargs):
        """Automatically creaetes slug from entered name."""
        if not self.id:
            self.slug = slugify(self.name)

        super(Team, self).save(*args, **kwargs)


class Product(models.Model):
    """
    Stores a single product instance, related to :model:`Category` and :model:`Team`.
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)
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
        "Returns url to full size team logo."
        if self.image:
            return self.image.url
        else:
            return ''

    def get_thumbnail(self):
        "Returns url to team logo thumbnail."
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return ''

    def save(self, *args, **kwargs):
        """Automatically creaetes slug from entered name."""
        if not self.id:
            self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs)

    def make_thumbnail(self, image, heigth=400):
        "Creates team logo thumbnail from given picture."
        img = Image.open(self.image)
        hpercent = (heigth/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize, heigth), Image.Resampling.LANCZOS)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG')
        thumbnail = File(thumb_io, name=self.image.name)
        return thumbnail


class Review(models.Model):
    """
    Stores a single review entry, related to Product and Author models.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Review {self.body} by {self.author.username}'
