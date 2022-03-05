from math import modf

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

PRODUCT_CATEGORY = (
    ('fruits', "Fruits"),
    ("clothes", "Clothes"),
    ("other", "Other"),
    ('household', 'Household'),
    ('toys', 'Toys'),
)


class Product(models.Model):
    name = models.CharField(max_length=63, verbose_name='Name')
    category = models.CharField(max_length=63, choices=PRODUCT_CATEGORY, default=PRODUCT_CATEGORY[2][0],
                                verbose_name='Categories')

    description = models.TextField(max_length=300, verbose_name='Description', null=True, blank=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Image of product')

    def __str__(self):
        return self.name

    @property
    def mid_rating(self):
        mid_grade = 0
        review = Review.objects.filter(product__name=self.name).filter(product__category=self.category).filter(
            product__description=self.description)
        for i in review:
            mid_grade += i.grade
        if mid_grade:
            mid_grade = mid_grade / len(review)
        a, b = modf(mid_grade)
        return a, range(int(b))

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Review(models.Model):
    author = models.ForeignKey(User, verbose_name='Author', related_name='review_user', on_delete=models.PROTECT)
    product = models.ForeignKey('Product', related_name='review_product', verbose_name='Product',
                                on_delete=models.CASCADE)
    review_text = models.TextField(max_length=511, verbose_name='Review text:')
    grade = models.PositiveIntegerField(default=5,
                                       validators=[
                                           MaxValueValidator(5),
                                           MinValueValidator(1)
                                       ])

    @property
    def get_range(self):
        return range(self.grade)