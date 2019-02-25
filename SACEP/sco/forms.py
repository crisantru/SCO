from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,)
from sco.models import (
    User,
    Document,
    Authority,
    Type,
    Type_Pension,
    Type_InformeA,
    Process, )
from django.utils import timezone
from datetime import date
#from bootstrap_datepicker_plus import DatePickerInput
from django.conf import settings
from sco.validators import validate_len



class CustomAuthForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput(
    attrs={'class':'validate form-control col-sm-10 mx-auto',
    'placeholder': 'Introduce tu Correo'}))

    password = forms.CharField(widget=PasswordInput(
    attrs={'class':'validate form-control col-sm-10 mx-auto',
    'placeholder':'Introduce tu Contraseña'}))

class RegistrationForm(UserCreationForm):
    #print("entra a RegistrationForm")
    #email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=PasswordInput(attrs={'class':'validate form-control col-sm-4','placeholder':'Contraseña: Minimo 8 Caracteres'}))

    password2 = forms.CharField(widget=PasswordInput(attrs={'class':'validate form-control col-sm-4','placeholder':'Confirmar Contraseña'}))

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'lastNameP',
            'lastNameM',
            'email',
            'date_born',
            'type_account',
            'is_superuser',
        )

        labels = {
            'username': 'Usuario ',
            'name': 'Nombre ',
            'lastNameP': 'Apellido Paterno ',
            'lastNameM': 'Apellido Materno ',
            'email': 'Correo Electronico',
            'date_born': 'Fecha de Nacimiento: ',
            'type_account': 'Tipo de Cuenta',
            'is_superuser': 'Usuario Root'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'validate form-control col-sm-4',
            'placeholder': 'Introduce tu Nombre'}),
            'lastNameP': forms.TextInput(attrs={'class':'validate form-control col-sm-4',
            'placeholder': 'Apellido Paterno'}),
            'lastNameM': forms.TextInput(attrs={'class':'validate form-control col-sm-4',
            'placeholder': 'Apellido Materno'}),
            'email': forms.EmailInput(attrs={'class':'validate form-control col-sm-4',
            'placeholder':'Correo Ejemplo: alguien@example.com'}),
            'username': forms.TextInput(attrs={'class':'validate form-control col-sm-4',
            'placeholder':'Nombre de Usuario'}),
            'type_account': forms.Select(attrs={'class':'validate form-control col-sm-4'}),

        }

    def save(self, commit=True):
        #print("entra a save)
        user = super(RegistrationForm, self).save(commit=False)

        user.username = self.cleaned_data['username']
        user.name = self.cleaned_data['name']
        user.lastNameP = self.cleaned_data['lastNameP']
        user.lastNameM = self.cleaned_data['lastNameM']
        user.email = self.cleaned_data['email']
        user.type_account = self.cleaned_data['type_account']
        user.is_superuser = self.cleaned_data['is_superuser']
        user.is_active=True
        user.date_born = timezone.now()
        user.date_joined = timezone.now()

        if commit:
            user.save()

        return user;

class RegistrationFormDocument(forms.ModelForm):

    class Meta:
        model = Document
        fields = (
            'name_person',
            'num_folio',
            'consecutive',
            'num_folio_anwser',
            'register_date',
            'file_pdf',
            #'observations',
        )

        labels = {
			'num_folio': 'N° de Oficio de Solicitud:',
            'consecutive': 'Año',
            'num_folio_anwser': 'N° de Oficio de Respuesta:',
            'name_person': 'Nombre:',
            #'observations': 'Asunto:',
            'file_pdf': 'Archivo PDF',

		}

        widgets = {
            'name_person': forms.TextInput(attrs={'style': 'width:500',
            'class':'validate form-control'}),
            'num_folio': forms.TextInput(attrs={'style': 'width:100%',
            'class':'validate form-control', 'placeholder':'Número'}),
            'consecutive': forms.TextInput(attrs={'style': 'width:40%',
            'class':'validate form-control', 'placeholder':'Año'}),
            'num_folio_anwser': forms.NumberInput(attrs={'style': 'width:30%', 'class':'validate form-control'}),
            'file_pdf': forms.FileInput(attrs={'style': 'width:30%', 'class':'validate form-control'}),
            #'observations': forms.Textarea(attrs={'cols': 30, 'rows': 6, 'style': 'resize:none'}),

        }


    def save(self, commit=True):
        #create document inherit super class for access to attrs
        #save commit false for cleaned_data of elements from template
        document = super(RegistrationFormDocument, self).save(commit=False)
        #cleaned_data data from template for later save
        document.name_person = self.cleaned_data['name_person']
        document.num_folio = self.cleaned_data['num_folio']
        #document.description = self.cleaned_data['observations']
        document.register_date = date.today()


        if commit:
        	document.save()

        return document

class RegistrationFormAuthority(forms.ModelForm):

    class Meta:
        model = Authority
        fields = (
            'name_authority',
            'city',
            'category',
            'address',
            'observations',
        )

        labels = {
            'name_authority': 'Autoridad',
            'city': 'Ciudad',
            'category': 'Categoria',
            'address': 'Dirección',
            'observations': 'Observaciones',
        }

        widgets = {
            'name_authority': forms.TextInput(attrs={'style': 'width:100%',
            'id': 'authority_name', 'class':'validate form-control', 'name': 'authority_name'}),
            'category': forms.Select(attrs={'class':'validate form-control'}),
            'address': forms.TextInput(attrs={'style': 'width:80%', 'class':'validate form-control'}),
            'city': forms.Select(attrs={'class':'validate form-control'}),
            'observations': forms.TextInput(attrs={'style': 'width:80%', 'class':'validate form-control'})
        }

    def save(self, commit=True):
        authority = super(RegistrationFormAuthority, self).save(commit=False)

        authority.name_authority = self.cleaned_data['name_authority']
        authority.city = self.cleaned_data['city']
        authority.category = self.cleaned_data['category']
        authority.address = self.cleaned_data['address']
        authority.observations= self.cleaned_data['observations']

        if commit:
            authority.save()

        return authority

class RegistrationFormType(forms.ModelForm):

    date_answer = forms.DateField(widget=forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'termino', 'readonly': 'True', 'class':'validate form-control',
         'style': 'width:55%'}))

    class Meta:
        model = Type
        fields = (
            'name',
            'date_answer',
            'document_answer',
        )

        labels = {
            #'internal_control': 'N° de Control Interno de Oficio',
            'name': 'Tipo de Oficio',
            #'document_answer',
            #'date_answer': 'Fecha de Termino',
            #'subtype': 'Sub-Materia',
            #'end_days': 'Fecha de Termino',
            #'limit_answer': 'Limite Respuesta(Días) ',
        }

        widgets = {
            'name': forms.Select(attrs={'id': 'Materias', 'onclick': "insertItems()",
            'class':'validate form-control', 'style': 'width:100%'}),
            'document_answer': forms.Textarea(attrs={'style': ' rows:10; cols:90;', 'class':'validate form-control'}),
            #'subtype': forms.Select(attrs={'id':'subMaterias',
            #'disabled': 'true','onclick': "submaterias()", 'value': 'None',
            #'class':'validate form-control'}),
            #'limit_answer': forms.TextInput(attrs={'class':'validate form-control','id':'limite_respuesta',
            # 'style':'width:40%', 'readonly': 'True ' }),
            #'internal_control':forms.TextInput(attrs={'style': 'width:30%', 'class':'validate form-control'}),
            #'end_days': forms.DateInput(format=('%d/%m/%Y'), attrs={'id':'termino', 'readonly': 'True',
            #'class':'validate form-control', 'style': 'width:55%'})


        }

    def save(self, commit=True):

        document = super(RegistrationFormType, self).save(commit = False)

        #document.internal_control = 1
        document.name = self.cleaned_data['name']
        document.date_answer = self.cleaned_data['date_answer']
        document.document_answer = self.cleaned_data['document_answer']
        #document.subtype = self.cleaned_data['subtype']
        #document.limit_answer = self.cleaned_data['limit_answer']
        #document.end_days = self.cleaned_data['end_days']

        if commit:
            document.save()

        return document

class RegistrationFormTypePension(forms.ModelForm):

    class Meta:
        model = Type_Pension
        fields = (
            'ordinary_judg',
        	'beneficiary',
        	'disposition_type',
        	'pension_type',
            'date_efect',
        )

        labels = {
            'ordinary_judg': 'Juicio Ordinario',
        	'beneficiary': 'Beneficiario',
        	'disposition_type': 'Tipo de Disposición',
        	'pension_type': 'Tipo de Pensión',
        }

        widgets = {
            'ordinary_judg': forms.TextInput(attrs={'style': 'width:100%',
            'class':'validate form-control'}),
            'beneficiary': forms.TextInput(attrs={'style': 'width:150%',
            'class':'validate form-control'}),
            'disposition_type': forms.Select(attrs={'style': 'width:100%',
            'class':'validate form-control'}),
            'pension_type': forms.TextInput(attrs={'style': 'width:100%;',
            'readonly': 'true', 'class':'validate form-control'}),
            'date_efect': forms.DateInput(format='%d/%m/%Y', attrs={'id': 'datepicker',
            'style': 'width:60%', 'class':'validate form-control'}),
        }

    def save(self, commit=True):
        pension = super(RegistrationFormTypePension, self).save(commit=False)

        pension.ordinary_judg = self.cleaned_data['ordinary_judg']
        pension.beneficiary = self.cleaned_data['beneficiary']
        pension.disposition_type = self.cleaned_data['disposition_type']
        pension.pension_type = self.cleaned_data['pension_type']
        pension.date_efect = self.cleaned_data['date_efect']

        if commit:
            pension.save()

        return pension

class RegistrationFormTypeInformesA(forms.ModelForm):

    class Meta:
        model = Type_InformeA
        fields = (
            'date_redaction',
            'document_answer',
        )

        widgets = {
            'date_redaction': forms.DateInput(format='%d/%m/%Y', attrs={'id': 'datepicker',
            'style': 'width:60%', 'class':'validate form-control'}),
            'document_answer': forms.Textarea(attrs={'style': 'resize:none; rows:10; cols:90;', 'class':'validate form-control'}),
        }

        def save(self, commit=True):
            informeA = super(RegistrationFormTypeInformesA, self).save(commit=False)

            informeA.date_redaction = self.cleaned_data['date_redaction']
            informeA.document_answer = self.cleaned_data['document_answer']

            if commit:
                informeA.save()

            return informeA

class RegistrationFormProcess(forms.ModelForm):
    class Meta:
        model = Process
        fields = (
            'manager_process',
            'derivate_area',
            #'answer',
            'status',
            'date_delivery',
            'observations'
        )

        labels = {
            'manager_process': 'Responsable',
            'derivate_area': 'Derivado a:',
            #'answer': 'Respuesta',  #al concluir documento
            'status': 'Status',
            'date_delivery': 'Fecha de entrega',    #al cocluir documento
            'observations': 'Observaciones'
        }

        widgets = {
            'manager_process': forms.Select(attrs={'class':'validate form-control'}),
            'status': forms.Select(attrs={'style': 'width:80%', 'class':'validate form-control'}),
            'derivate_area': forms.Select(attrs={'class':'validate form-control'}),
            'observations': forms.Textarea(attrs={'style': 'resize:none', 'class':'validate form-control'}),
            'date_delivery': forms.TextInput(attrs={'style': 'width:30%', 'class':'validate form-control'}),
        }

    def save(self, commit=True):
        process = super(RegistrationFormProcess, self).save(commit = False)

        process.manager_process = self.cleaned_data['manager_process']
        process.derivate_area = self.cleaned_data['derivate_area']
        #process.answer = self.cleaned_data['answer']
        process.status = self.cleaned_data['status']
        process.description = self.cleaned_data['observations']

        if commit:
            process.save()

        return process
