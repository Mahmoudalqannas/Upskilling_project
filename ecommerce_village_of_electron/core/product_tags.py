class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


class ProductTags(models.Model):
    tag_name = models.ManyToManyField(to='Tag')
    tag_product = models.ForeignKey(
        to='Item', on_delete=models.CASCADE, null=True, blank=True, unique=True)
