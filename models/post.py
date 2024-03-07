from tortoise import fields
from tortoise.models import Model

class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.User", related_name="posts")

    def __str__(self):
        return self.title
