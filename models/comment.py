from tortoise import fields
from tortoise.models import Model

class Comment(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    author = fields.ForeignKeyField("models.User", related_name="comments")

    def __str__(self):
        return self.content
