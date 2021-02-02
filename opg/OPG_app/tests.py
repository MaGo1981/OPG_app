from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Opg, ProductCategory, Product, Profile


class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.logout_url=reverse('logout')
        self.user={
            'username': 'ime2@domena.com',
            'email': 'ime2@domena.com',
            'password': 'Datulja2222',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'opg_name': 'opg_name',
            'address': 'address',
            'phone': 'phone',
        }
        # Create Product Category.
        c1 = ProductCategory.objects.create(name="MLIJECNI PROIZVODI")
        c2 = ProductCategory.objects.create(name="VOĆE")
        c3 = ProductCategory.objects.create(name="POVRĆE")

        # Create Product
        p1 = Product.objects.create(name='Sir', category=c1)
        p2 = Product.objects.create(name='Jabuka', category=c2)
        p3 = Product.objects.create(name='Brokula', category=c3)

        # Create user.
        u1 = User.objects.create_user(first_name="Admin", username='admin', email='admin@admin.com', password='admin')


        return super().setUp()


class OpgTest(BaseTest):

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)


    def test_can_login_user(self):
        reg_response = self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(reg_response.status_code, 302)
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        login_response=self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(login_response.status_code,302)



    def test_can_logout_user(self):
        reg_response = self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(reg_response.status_code, 302)
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        login_response=self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(login_response.status_code,302)
        logout_response = self.client.post(self.logout_url, self.user, format='text/html')
        self.assertEqual(logout_response.status_code, 200)

    def testOPGCreated(self):
        reg_response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(reg_response.status_code, 302)
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        login_response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(login_response.status_code, 302)
        opg = Opg.objects.filter(name="opg_name")
        self.assertEqual(opg.count(), 1)


    def testProductsPage(self):
        c = Client()
        response = c.get("/product_list")
        self.assertEqual(response.status_code, 200)

    def testProfile(self):
        c = Client()
        response = c.get("/profile")
        self.assertEqual(response.status_code, 200)


    def testAddProduct(self):
        c = Client()
        response = c.post('/login', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)

        response = c.get("/product_list")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 3)
        c1 = ProductCategory.objects.create(name="MLIJECNI PROIZVODI")
        p4 = Product.objects.create(name='Jogurt', category=c1)
        response = c.get("/product_list")
        self.assertEqual(response.context["products"].count(), 4)



    def testEditProduct(self):
        c = Client()
        response = c.post('/login', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)

        response = c.get("/product_list")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 3)
        c1 = ProductCategory.objects.create(name="MLIJECNI PROIZVODI")
        p4 = Product.objects.create(name='Jogurt', category=c1)
        response = c.get("/product_list")
        self.assertEqual(response.context["products"].count(), 4)
        c2 = ProductCategory.objects.create(name="VOĆE")
        Product.objects.filter(name='Jogurt').update(category=c2)
        self.assertEqual(Product.objects.filter(category=c2).count(), 1)



    def testEditProfile(self):
        reg_response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(reg_response.status_code, 302)
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        login_response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(login_response.status_code, 302)
        profile = Profile.objects.filter(address="address").update(phone='555999')
        self.assertEqual(Profile.objects.filter(phone='555999').count(), 1)
