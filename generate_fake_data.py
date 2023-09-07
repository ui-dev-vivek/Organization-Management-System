import os
import django
from faker import Faker
from django.contrib.auth import get_user_model
# from subsidiaries.models import Subsidiaries

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dyrevolution_center.settings")
django.setup()

from employees.models import Employees
from clients.models import Clients
from subsidiaries.models import Organizations, Subsidiaries, Budgets  # Replace with your actual app name and models


fake = Faker()
User = get_user_model()

def create_fake_data():
    # Create 2 organizations
    for _ in range(2):
        organization = Organizations.objects.create(
            name=fake.company(),
            slug=fake.slug(),
            description=fake.text(),
        )
        # Create 10 subsidiaries for each organization
        for _ in range(10):
            subsidiary = Subsidiaries.objects.create(
                organization=organization,
                name=fake.company(),
                slug=fake.slug(),
                description=fake.text(),
            )
            # Create 10 budgets for each subsidiary
            for _ in range(10):
                Budgets.objects.create(
                    subsidiary=subsidiary,
                    year=fake.random_int(min=2023, max=2030),  # Example year range
                    amount=fake.random_int(min=10000, max=1000000),  # Example amount range
                )

def create_fake_users():
    for _ in range(10):
        username = fake.user_name()
        password = fake.password()
        User.objects.create_user(username=username, password=password)
        print(f"Username: {username}, Password: {password}")
        

def create_fake_employees():
    subsidiaries = Subsidiaries.objects.all()

    for subsidiary in subsidiaries:
        for _ in range(5):  # Change the number of employees as needed
            user = User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
            )

            Employees.objects.create(
                user=user,
                subsidiary=subsidiary,
                phone_no=fake.unique.random_int(min=1000000000, max=9999999999),
                emp_type=fake.random_element(elements=('full_time', 'part_time', 'freelancer')),
            )

def create_fake_clients():
    subsidiaries = Subsidiaries.objects.all()

    for subsidiary in subsidiaries:
        for _ in range(5):  # Change the number of clients as needed
            user = User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
            )

            Clients.objects.create(
                user=user,
                subsidiary=subsidiary,
                phone_no=fake.unique.random_int(min=1000000000, max=9999999999),
                organization_name=fake.company(),
            )


if __name__ == "__main__":
    # create_fake_users()
    # create_fake_data()
    create_fake_employees()
    # create_fake_clients()





# Username: erin40, Password: u7qOqB!6+3
# Username: debrarodriguez, Password: *97aQuxQC9
# Username: johnathanodonnell, Password: (aNn6D0iVs
# Username: steven77, Password: (cT9Vr@04g
# Username: wangmichelle, Password: k#!3FDaeQv
# Username: taylorisaiah, Password: tn11A0q9&n
# Username: lisawilson, Password: _H*(Vliuq5
# Username: cblackwell, Password: R)V_a4Lhtc
# Username: srodriguez, Password: 4PXXd5sh^)
# Username: patelmary, Password: RzA25ZYl!y