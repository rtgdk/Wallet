from django.db import models
from datetime import datetime,date
# Create your models here.
transtype = (('income','income'),('expense','expense'))

class Info(models.Model):
	ttype = models.CharField("Type",choices=transtype,db_index=True,max_length=16,default='expense') #transaction type
	name = models.CharField("Name",db_index=True,max_length=32,blank=False)
	date = models.DateField("Date",db_index=True,default=datetime.now,blank=True,null=True)
	amount = models.FloatField("Amount",default=0.0,null=False)
	lastedited = models.DateTimeField("Last editing Date",default=datetime.now, blank=False,null=True)
	addeddate = models.DateTimeField("Date Added on",default=datetime.now, blank=False,null=True)
	comments = models.CharField("Other",max_length=128,default="",blank=True,null=True)
	class Meta:
		unique_together = ('name', 'date','amount') ##add meal
	def __str__(self):
		return self.name

class Total(models.Model):
	name = models.CharField("Name",max_length=16,default='A')
	totalamount = models.FloatField("Funds left",default=0.0,null=False)
	tincome = models.FloatField("Total Earned",default=0.0,null=False)
	texpense = models.FloatField("Total Spent",default=0.0,null=False)
	def __str__(self):
		return str(self.totalamount)