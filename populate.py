import os
import django

def main():
	a = Total.objects.get_or_create(name="A")

if __name__ == '__main__':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallet.settings')
	django.setup()
	from app.models import Total
	main()