from django.db import models

# Ckeditor
#from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
DEFAULT_STATUS = "draft"
STATUS = (
    ('draft', 'Taslak'),
    ('published', 'Yayinlandi'),
    ('deleted', 'Silindi'),
)


TYPE_CHOICE = (
    ('men', 'Erkek'),
    ('women', 'Kadın'),
    ('unisex', 'Unisex'),
    ('slider', 'Slider'),
    ('slider2', 'Slider2'),
    ('category', 'Kategory'),
)


# Category
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        default="",
    )
    cover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='category',
    )
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    )
    type = models.CharField(
        max_length=8,
        default="general",
        choices=TYPE_CHOICE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{1000 + self.pk } - {self.type} - {self.title}"


# Product
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,

    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        default="",
    )
    content = models.TextField()
    cover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='products',
    )
    hover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='products',
    )
    price = models.FloatField()
    salePrice = models.FloatField()

    stock = models.PositiveSmallIntegerField(default=0)
    is_home = models.BooleanField(
        default=False,
    )
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Yorum
class Comment(models.Model):
    productPost = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200, verbose_name='Ad Soyad')
    content = models.TextField(max_length=200, verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def str(self):
        return self.name