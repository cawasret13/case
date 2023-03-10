from django.db import models

STATUS = {
    (0, 'Published'),
    (1, 'Expectation'),
    (2, 'Archive')
}


class item(models.Model):
    id_item = models.CharField(max_length=32)
    hash_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='items/images/')
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class cases(models.Model):
    id_case = models.CharField(max_length=16)

    icon = models.ImageField(upload_to ='case/images/')
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    amount_items = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS, default=1)
    old_price = models.IntegerField(default=0)
    show_old_price = models.BooleanField(default=False)

    items = models.JSONField(default=[])

    money = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    history = models.JSONField(default=[])

    testing_history = models.JSONField(default=[])
    coef_profit = models.FloatField(default=0)
    coef_compensation = models.FloatField(default=0)
    applayRules = models.BooleanField(default=False)
    rules = models.JSONField(default=[])

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return self.name

class HistoryCase(models.Model):
    name = models.CharField(max_length=200)
    img = models.CharField(max_length=500)

class Users(models.Model):
    token = models.CharField(max_length=32)
    tradeLink = models.TextField(null=True)
    name = models.CharField(max_length=200)
    img = models.CharField(max_length=500)
    money = models.FloatField(default=0)
    admin = models.BooleanField(default=False)
    replenishment = models.FloatField(default=0)
    inventory = models.TextField()

    def __str__(self):
        return self.name