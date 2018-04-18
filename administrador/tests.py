from django.test import TestCase
from django.urls import reverse
from administrador.models import User
from torneo.models import *
from equipo.models import Equipo
from jugadora.models import Jugadora
from coaches.models import PreRegistro

class UserTestCase(TestCase):
    def test_create_user_correct_username(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Carlos", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().username, "croman")

    def test_create_user_correct_first_name(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Carlos", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "Carlos")

    def test_create_user_correct_email(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Carlos", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().email, "carlosromanrivera@hotmail.com")

    def test_create_user_existing_username(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Primero", "username": "croman", "email":"primero@hotmail.com"})
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Segundo", "username": "croman", "email":"segundo@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "Primero")

    def test_create_user_existing_email(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Primero", "username": "primero", "email":"carlosromanrivera@hotmail.com"})
        self.client.post('/administrador/agregar_administrador/', {"first_name": "Segundo", "username": "segundo", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "Primero")

    def test_create_user_without_name(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().first_name, "")

    def test_create_user_default_password(self):
        self.client.post('/administrador/agregar_administrador/', {"first_name": "", "username": "croman", "email":"carlosromanrivera@hotmail.com"})
        self.assertEqual(User.objects.last().check_password("temporal"), True)

    def test_PreRegistro(self):

        usuario1 = User.objects.create_user(username='testuser2', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser2', password='12345')

        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="1995",
            fechaInicio='2010-12-12',
            costo=int(12.12),
            fechaJunta='1995-11-11',
            costoCredencial=12
        )

        a =PreRegistro.objects.create(
            Nombre="Ale",
            Correo="Notas",
            Notas="Aqui va las notas",
            torneo=t1
        )

        b = PreRegistro.objects.create(
            Nombre="Ale",
            Correo="gmail",
            Notas="Aqui va las notas",
            torneo=t1
        )

        a.save()
        b.save()

        resp = self.client.get('/administrador/lista_PreRegistro/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(a, b in resp.context['PreRegistros'])

        # Eliminar uno que no existe
        resp = self.client.get('/administrador/eliminar_PreRegistro/123123123/')
        self.assertEqual(resp.status_code, 404)

        # Eliminar uno correcto
        resp = self.client.get('/administrador/eliminar_PreRegistro/'+str(b.id)+'/')
        resp = self.client.get('/administrador/lista_PreRegistro/')
        self.assertTrue(a in resp.context['PreRegistros'])
        self.assertTrue(b not in resp.context['PreRegistros'])

        # Aceptar Un preregostr incorrecto
        resp = self.client.get('/administrador/aceptar_PreRegistro/123/')
        resp = self.client.get('/administrador/lista_PreRegistro/')
        c = PreRegistro.objects.get(id=a.id)
        self.assertTrue(c.codigo == None)


        # Aceptar Un preregostr correcto
        resp = self.client.get('/administrador/aceptar_PreRegistro/' + str(a.id) + '/')
        resp = self.client.get('/administrador/lista_PreRegistro/')
        c = PreRegistro.objects.get(id=a.id)
        self.assertFalse(c.codigo == None)



class ValidarPreRegistroEquipoCase(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')
        t1 = Torneo.objects.create(
            id=2,
            nombre="Torneo PRueba",
            categoria="1995",
            categoriaMax="1997",
            fechaInicio='2010-12-12',
            costo=int(12.12),
            fechaJunta='1995-11-11',
            costoCredencial=12,
            activo=True
        )
        t1.save()
        ea = Equipo.objects.create(
            nombre = 'Equipo A',
           representante = 'Juan A',
           telefono = '4426483003',
           correo = 'rr100@live.com.mx',
           colorLocal  = 1,
           colorVisitante = 2,
           cancha = 'Estadio Azteca',
           dia = 1,
           hora = '13:05',
           activo = False
           )
        ea.save();
        for equipo in Equipo.objects.all():
            estadistica = Estadisticas(equipo=equipo, torneo=t1)
            estadistica.save()
        a =PreRegistro.objects.create(
            nombre="Ale",
            correo="Notas",
            notas="Aqui va las notas",
            torneo=t1,
            codigo="abc",
            equipo=ea
        )
        a.save()
        d = Jugadora.objects.create(
            id = 1,
            Nombre = 'Nombre Def',
            Apellido = 'Apellido Def',
            Nacimiento = '1998-03-01',
            Numero = 4,
            Posicion = 1,
            Notas = 'Ejemplo Default Jugadora',
            activo = False
        );
        d.save();


    def test_validar_registro_jugadora(self):
        """
            Cambiar el estatus de una jugadora una vez que ha sido validada por el administrador.
            Se verifica que el estatus de la jugadora pase a activo, una vez que haya sido validada.
        """
        jugadora = Jugadora.objects.get(id=1)
        self.assertEqual(False, jugadora.activo)
        response = self.client.get(reverse('administrador:aceptar_jugadora',kwargs={'id_jugadora':jugadora.id}))
        self.assertEqual(response.status_code, 302)
        jugadora = Jugadora.objects.get(id=1)
        self.assertEqual(True, jugadora.activo)

    def test_eliminar_registro_jugadora(self):
        """
            Eliminar a la jugadora cuando el administrador rechaza la petición de registro.
            Se verifica que el registro ha sido eliminado si la jugadora fue rechazada.
        """
        jugadora = Jugadora.objects.get(id=1)
        equipo = Equipo.objects.get(id=1)
        self.assertEqual(1, Jugadora.objects.all().count())
        response = self.client.get(reverse('administrador:eliminar_jugadora',kwargs={'id_jugadora':jugadora.id,'id_equipo':equipo.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0, Jugadora.objects.all().count())
