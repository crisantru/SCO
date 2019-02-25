from django import forms
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sco.validators import validate_len

class CustomUserManager(BaseUserManager):
	def _create_user(self, email, password, is_staff, is_superuser, **extra_fileds):

		now = timezone.now()

		if not email:
			raise ValueError('Debes introducir un email')

		email = self.normaliza_email(email)
		user = self.model(email,
				is_staff=is_staff, is_active=True,
				is_superuser=is_superuser, last_login=now,
				date_joined=now, **extra_fileds)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fileds):
		return self._create_user(email, password, False, False, **extra_fileds)

	def create_superuser(self, email, password=None, **extra_fileds):
		return self._create_user(email, password, False, False, **extra_fileds)

class User(AbstractBaseUser):

	ACCOUNTS = (
		("Seleccion", "Seleccione Tipo de Cuenta"),
		("Captura", "Captura"),
		("Operativo", "Operativo"),
		("Administrador", "Administrador")
	)

	username = models.CharField(max_length=50, unique=True)
	name = models.CharField(max_length=25, blank=True)
	lastNameP = models.CharField(max_length=25, blank=True)
	lastNameM = models.CharField(max_length=25, blank=True)
	email = models.EmailField(max_length=35, unique=True)
	password = models.CharField(max_length=128, blank=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	type_account = models.CharField(max_length=13, choices=ACCOUNTS, default='Seleccion')
	is_active = models.BooleanField(default=False)
	date_joined = models.DateField(max_length=6, blank=True)
	date_born = models.DateField(max_length=6, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['usename', 'name', 'lastNameP', 'lastNameM', 'is_superuser', 'date_born']

	objects = CustomUserManager()

	class Meta:
		verbose_name = ('user')
		verbose_name_plural = ('users')
		db_table = ('user')

class Authority(models.Model):
    CATEGORIES = (
        ("Seleccion", "Seleccione un elemento"),
        ("PRIMERA INSTANCIA Y MENORES", "Primera Instancia y Menores"),
		("SEPTIMO CIRCUITO", "Septimo Circuito"),
        ("OTROS...", "Otros..."),
    )

    AUTHORITY_CITIES = (
        ("Seleccion", "Selecciona un elemento"),
        ("XALAPA", "Xalapa"),
        ("VERACRUZ", "Veracruz"),
        ("POZA RICA", "Poza Rica"),
        ("OTROS...", "Otros..."),
    )


    id_authority = models.AutoField(primary_key=True)
    name_authority = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORIES, default='Seleccion')
    city = models.CharField(max_length=50, choices=AUTHORITY_CITIES, default='Seleccion')
    address = models.CharField(max_length=255, blank=False)
    observations = models.CharField(max_length=255, blank=True, null=True)

    REQUIRED_FIELDS = ['id_authority', 'name_authority','category', 'city', 'address', 'observations']

    class Meta:
        verbose_name = ('autoridad')
        verbose_name_plural = ('autoridades')
        db_table = ('authority')

    #representation String of Object Unicode
    def __str__(self):
        return 'ID: %s Nombre: %s' % (self.id_authority, self.name_authority)

    def get_absolute_url(self):
        return reverse("authority-detail", kwargs={'pk': self.id_authority})

class Process(models.Model):

    STATUS_DOCUMENT = (
        ("Seleccion", "Seleccione un elemento"),
        ("Turnado", "Turnado"),
        ("Turnado/Area", "Turnado/Area"),
        ("Respuesta/Area", "Respuesta/Area"),
        ("Enviado/Autoridad", "Enviado/Autoridad")
    )

    MANAGER_PROCESS = (
        ("Seleccion", "Seleccione un elemento"),
        ("Lic. Olivia", "Lic. Olivia"),
        ("Lic. Yair", "Lic. Yair"),
        ("Lic. Abad", "Lic. Abad")
    )

    DERIVATE_AREA = (
        ("Seleccion", "Seleccione un elemento"),
		("Area Afiliacón","Area Afiliación"),
        ("Area Personal","Area Personal"),
		("Area Prestaciones Economicas","Area Prestaciones Economicas"),
		("Area Retiro Laboral","Area Retiro Laboral"),
        ("Area Medica","Area Medica"),
        ("Otros","Otros"),
		("Archivar","Archivar")
    )

    id_process = models.AutoField(primary_key=True)
    manager_process = models.CharField(max_length=100, blank=False,
    choices=MANAGER_PROCESS, default='Seleccion')
    derivate_area =  models.CharField(max_length=100, blank=False,
    choices=DERIVATE_AREA, default='Seleccion')
    #derivate_city =  models.CharField(max_length=100, blank=True, null=True)
    #answer = models.CharField(max_length=200, blank=True, null=True)#Informes_Autoridad
    status = models.CharField(max_length=100, blank = False,
    choices=STATUS_DOCUMENT, default='Seleccion')
    date_delivery = models.DateField(max_length=6, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = ['id_process', 'manager_process', 'derivate_area',
     'status', 'date_delivery', 'observations']

    class Meta:
        verbose_name = ('proceso')
        verbose_name_plural = ('procesos')
        db_table = ('process')

    def __str__(self):
        return self.manager_process

class Type_Pension(models.Model):

	PENSION_TYPES = (
        ("Seleccion", "Seleccione un elemento"),
		("Inclusión", "Inclusión"),
		("Modificación", "Modificación"),
		("Cancelación", "Cancelación"),
    )

	DISPOSITION_TYPES = (
        ("Seleccion", "Seleccione un elemento"),
		("PROVISIONAL", "Provisional"),
		("DEFINITIVO", "Definitivo"),
    )

	id_pension = models.AutoField(primary_key=True)
	ordinary_judg = models.CharField(max_length=14, blank=False)
	beneficiary = models.CharField(max_length=80, blank=False)
	disposition_type = models.CharField(max_length=30, choices=DISPOSITION_TYPES, default='Seleccion')
	date_efect = models.DateField(max_length=10, blank=True, null=True)
	pension_type = models.CharField(max_length=30, blank=False)
	observations = models.TextField(blank=True, null=True)

	REQUIRED_FIELDS = ['id_pension', 'ordinary_judg', 'beneficiary', 'disposition_type',
	'date_efect', 'pension_type', 'observations']

	class Meta:
		verbose_name = ('tipo_pension')
		verbose_name_plural = ('tipo_pensiones')
		db_table = ('type_pension')

	def __str__(self):
		return str(self.id_pension)

class Type_InformeA(models.Model):

	id_type_informe = models.AutoField(primary_key=True)

	date_redaction = models.DateTimeField(max_length=6, blank=True, null=True)
	document_answer = models.CharField(max_length=255, blank=True, null=True)
	internal_control = models.IntegerField(unique=True, blank=True, null=True)

	REQUIRED_FIELDS =['id_informeA', 'internal_control', 'date_redaction',
	'document_answer']

	class Meta:
		verbose_name = ('informe_autoridad')
		verbose_name_plural = ('informes_autoridad')
		db_table = ('type_informe_a')

	def __str__(self):
		return str(self.id_type_informe)

class Type(models.Model):

    DOCUMENT_TYPES = (
        ("Seleccion", "Seleccione un elemento"),
		("Asuntos_Administrativos", "Asuntos Administrativos"),
		("Asuntos_Civiles", "Asuntos Civiles"),
        ("Asuntos_Penales", "Asuntos Penales"),
        ("Depositaria_Infiel", "Depositaria Infiel"),
		("Expedientes_Penales", "Expedientes Penales"),
        ("Informes_Autoridad", "Informes Autoridad"),
        ("Juicios_Amparo", "Juicios Amparo"),
		("Juicios_Civiles", "Juicios Civiles"),
        ("Negativa_Peritos", "Negativa Peritos"),
        ("Oficios_Varios", "Oficios Varios"),
        ("Pensiones_Alimenticias", "Pensiones Alimenticias"),
        ("Recuperacion_Fianzas", "Recuperación Fianzas"),
    )

    id_type = models.AutoField(primary_key=True)
    #internal_control = models.IntegerField(blank=True, null=True)#Informes_Autoridad
    name = models.CharField(max_length=30, choices=DOCUMENT_TYPES, default='Seleccion')
    date_answer = models.DateField(blank=True, null=True)
    document_answer = models.TextField(blank=True, null=True)
    #subtype = models.CharField(max_length=30, blank=True, null=True )
    #limit_answer = models.IntegerField(blank=False)#ERASE ONLY FRONTED

    pension = models.ForeignKey(Type_Pension, on_delete=models.CASCADE)
    informeA = models.ForeignKey(Type_InformeA, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['id_type', 'name']

    class Meta:
        verbose_name = ('tipo')
        verbose_name_plural = ('tipos')
        db_table = ('type')

    def __str__(self):
        return self.id_type

class Document(models.Model):
    id_document = models.AutoField(primary_key=True)
    name_person = models.CharField(max_length=100, blank=False)
    num_folio = models.CharField(max_length=8, blank=False)
    consecutive = models.CharField(max_length=4, blank=False)
    num_folio_anwser = models.IntegerField(unique=True, blank=True, null=True)
    register_date = models.DateField(blank=True, null=True)
    file_pdf = models.FileField(upload_to='documents/', blank=True, null=True)
    #observations = models.CharField(max_length=255, blank=True, null=True)

    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete = models.CASCADE)
    type = models.ForeignKey(Type, on_delete = models.CASCADE)

    REQUIRED_FIELDS = ['id_document', 'name_person', 'num_folio',
	'consecutive', 'num_folio_anwser', 'register_date', 'file_pdf']

    class Meta:
        verbose_name = _('documento')
        verbose_name_plural = _('documentos')
        db_table = ('document')

    def __str__(self):
        return self.name_person
