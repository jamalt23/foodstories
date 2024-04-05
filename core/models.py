from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    text = models.TextField(max_length=1000)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('Tag', verbose_name=("Tags"))
    created_at = models.DateTimeField(auto_now_add=True)    

    def get_tags(cls):
        taglist = []
        for tag in cls.tags.all():
            tag.title = tag.title.title()
            tag.save()
            taglist.append(tag.title)
        return taglist

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Comment(models.Model):
    author = models.CharField(max_length=50)
    text = models.TextField(max_length=1000)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author} - {self.text}"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class Tag(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=300)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name

class Subscribe(models.Model):
    email = models.EmailField(max_length=300)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Subscribe"
        verbose_name_plural = "Subscribes"

