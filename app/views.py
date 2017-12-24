from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,JsonResponse,HttpResponseForbidden
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.decorators import login_required
import django_excel as excel
from app.forms import UploadFileForm,AddInfoForm
from app.models import Info,Total
from datetime import datetime,date
import xlsxwriter

def index(request):
	if request.user.is_superuser:
		context_dict = {}
		a = Total.objects.get(name="A")
		inc = Info.objects.filter(ttype="income").order_by('-date')
		exp = Info.objects.filter(ttype="expense").order_by('-date')
		context_dict["inc"] = inc
		context_dict["exp"] = exp
		context_dict["texpense"] = a.texpense
		context_dict["tincome"] = a.tincome
		context_dict["totalamount"] = a.totalamount
		return render(request, 'app/index.html', context_dict)
	else :
		return HttpResponseRedirect("/app/login/")

def add(request):
	if request.user.is_superuser:
		context_dict={}
		if request.method == 'POST':
			a = Total.objects.get(name="A")
			try:
				form = AddInfoForm(request.POST)
				if form.is_valid():
					user = form.save(commit=False)
					user.date = request.POST.get('date')
					if user.ttype =="income":
						a.totalamount += user.amount
						a.tincome += user.amount
					else :
						a.totalamount -= user.amount
						a.texpense += user.amount
					a.save()
					user.save()
					context_dict["success"] = "Added!"
					form = AddInfoForm()
					context_dict["form"] = form
					return render(request, 'app/add.html', context_dict)
			except Exception as e:
				context_dict["error"] = "Error occured" + str(e)
				return render(request, 'app/add.html', context_dict)
		else:
			form = AddInfoForm()
			context_dict["form"] = form
			return render(request, 'app/add.html', context_dict)
	else :
		return HttpResponseRedirect("/app/login/")		

def upload(request):
	if request.user.is_superuser:
		context_dict={}
		if request.method == 'POST' and request.FILES['file']:
			try:
				form = UploadFileForm(request.POST,request.FILES)
				if form.is_valid():
					def choice_func(row):
						if(str(row[0]).lower().startswith("inc")):
							row[0] = "income"
						else :
							row[0] = "expense"
						try:
							info = Info.objects.get(name=str(row[1]),date=str(row[3]))
							if (info.amount == row[2]):
								return None
							else :
								info.delete()
							return (row)
						except:
							return row
					request.FILES['file'].save_to_database(
						model=Info,
						initializer=choice_func,
						mapdict=['ttype','name','amount','date']
						)
					done=1
					update()
					form = UploadFileForm()
					context_dict["form"] = form
					context_dict["success"] = "Succesfully Uploaded!!"
					return render(request, 'app/upload.html', context_dict)
			except Exception as e:
				print (e)
				form = UploadFileForm()
				context_dict["form"] = form
				context_dict["error"] = e
				return render(request, 'app/upload.html', context_dict)
		else:
			form = UploadFileForm()
			context_dict["form"] = form
			context_dict["error"] = "No file uploaded"
			return render(request, 'app/upload.html', context_dict)
	else :
		return HttpResponseRedirect("/app/login/")

def updatetotal(request):
	if request.user.is_superuser:
		update()
		return HttpResponseRedirect("/app/")
	else :
		return HttpResponseRedirect("/app/login/")

def download(request):
	if request.user.is_superuser:
		context_dict = {}
		c = datetime.now()
		a = Total.objects.get(name="A")
		allinfo = Info.objects.all().order_by('-date')
		workbook = xlsxwriter.Workbook('media/wallet'+str(c)+'.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.set_column('A:A', 15)
		worksheet.set_column('B:B', 25)
		worksheet.set_column('C:C', 20)
		worksheet.set_column('D:D', 15)
		bold = workbook.add_format({'bold': 1})
		worksheet.write('A1', 'Type', bold)
		worksheet.write('B1', 'Name', bold)
		worksheet.write('C1', 'Amount', bold)
		worksheet.write('D1', 'Date', bold)
		row = 1
		col = 0
		for i in allinfo:
			worksheet.write_string(row,col,str(i.ttype))
			worksheet.write_string(row,col+1,str(i.name))
			worksheet.write_string(row,col+2,str(i.amount))
			worksheet.write_string(row,col+3,str(i.date))
			row+=1
		worksheet.write_string(row,col+1,"Total Income",bold)
		worksheet.write_string(row,col+2,str(a.tincome),bold)
		row+=1
		worksheet.write_string(row,col+1,"Total Spent",bold)
		worksheet.write_string(row,col+2,str(a.texpense),bold)
		row+=1
		worksheet.write_string(row,col+1,"Total Fund",bold)
		worksheet.write_string(row,col+2,str(a.totalamount),bold)
		row+=1
		workbook.close()
		return HttpResponseRedirect('/media/wallet'+str(c)+'.xlsx')
	else :
		return HttpResponseRedirect("/app/login/")

def loginuser(request):
	context_dict={}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user and user.is_superuser:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/app/')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			context_dict['error']="Invalid login details supplied."
			return render(request, 'app/login.html',context_dict)

	else:
		return render(request, 'app/login.html',context_dict)

def logoutuser(request):
	logout(request)
	return HttpResponseRedirect('/app/login')
	
def update():
	a = Total.objects.get(name="A")
	inc = Info.objects.filter(ttype="income")
	exp = Info.objects.filter(ttype="expense")
	tinc=texp=0
	for i in inc:
		tinc += i.amount
	for i in exp:
		texp += i.amount
	totalamount = tinc - texp
	a.totalamount = totalamount
	a.tincome = tinc
	a.texpense = texp
	a.save()
