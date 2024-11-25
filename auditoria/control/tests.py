from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Auditor, Control, Encabezado, Pregunta, ValidacionDiseño


class control_test(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.auditor = Auditor.objects.create(
            nombre_completo="Test Auditor",
            usuario=self.user,
        )
        self.url = reverse("control_list")

    def test_should_return_200_user_logged_in(self):
        self.client.login(username="testuser", password="testpass")

        session = self.client.session
        session["ano"] = 2024
        session["testing"] = "Semestre 1"
        session["user_id"] = self.user.id
        session.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_no_logged_user_should_redirect(self):
        url = reverse("control_list")
        response = self.client.get(url)
        self.assertRedirects(response, "/?next=/control/")


class AddEncabezadoControlTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.auditor = Auditor.objects.create(
            nombre_completo="Test Auditor",
            usuario=self.user,
        )
        self.control = Control.objects.create(
            nombre="Control Test",
            codigo="C001",
            auditor=self.auditor,
            año=2024,
        )

        ValidacionDiseño.objects.create(
            control=self.control,
            fecha_ejecucion=date.today(),  # Proporcionar una fecha válida
        )

        self.url = reverse(
            "add_encabezado_control", kwargs={"control_id": self.control.id}
        )

    def test_should_redirect_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"/?next=/control/add_encabezado_control/{self.control.id}"
        )

    def test_should_return_200_when_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ControlByIdTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.auditor = Auditor.objects.create(
            nombre_completo="Test Auditor",
            usuario=self.user,
        )
        self.control = Control.objects.create(
            nombre="Control Test",
            codigo="C001",
            auditor=self.auditor,
            año=2024,
        )
        self.url = reverse("control", kwargs={"control_id": self.control.id})

    def test_should_redirect_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/?next=/control/control/{self.control.id}")

    def test_should_return_200_when_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class AddValidacionDisenoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.auditor = Auditor.objects.create(
            nombre_completo="Test Auditor",
            usuario=self.user,
        )
        self.control = Control.objects.create(
            nombre="Control Test",
            codigo="C001",
            auditor=self.auditor,
            año=2024,
        )
        self.url = reverse(
            "add_validacion_diseno", kwargs={"control_id": self.control.id}
        )

    def test_should_redirect_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"/?next=/control/add_validacion_diseno/{self.control.id}"
        )

    def test_should_return_200_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
