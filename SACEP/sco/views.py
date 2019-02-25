#Importamos settings para poder tener a la mano la ruta de la carpeta media
import json
from django.utils import timezone
from django.conf import settings
#libs for Reportlab
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.views.generic import View
from django.http import HttpResponse
from django import forms
from django.shortcuts import render, redirect
from sco.forms import (
    RegistrationForm,
    RegistrationFormDocument,
    RegistrationFormAuthority,
    RegistrationFormType,
    RegistrationFormTypePension,
    RegistrationFormTypeInformesA,
    RegistrationFormProcess,
    )
from sco.render import Render
from sco.models import (
    Authority,
    Type,
    Type_Pension,
    Type_InformeA,
    Process,
    Document,
    User,
    )
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    )
from django.contrib import messages
from django.shortcuts import render_to_response
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime
#import pypandoc

def home(request):
    return render(request, 'sco/home.html')

#User
def register(request):
    print("entra a register")
    if request.method == 'POST':
        print("entra a request post")
        form = RegistrationForm(request.POST)
        response_data = {}
        print(str(form.is_valid()))
        if form.is_valid():
            print("formulario valido")
            user = form.save(commit=False)
            form.save()
            response_data['result'] = 'Usuario ' + user.username + ' se guardo Exitosamente!'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error": "Algo anda mal, no se pudo guardar"}),
            content_type="application/json")
    else:
        form = RegistrationForm()
        args = {'form': form}
    return render(request, 'sco/register_form.html', args)

class UserListView(ListView):
    model = User

class UserDelete(DeleteView):
    model = User
    success_url = '/sco/usuarios/'

#CRUD Authority
class AuthorityListView(ListView):
    model = Authority

class AuthorityDetailView(DetailView):
    model = Authority

    def authority_detail_view(request,pk):
        try:
            id_authority=Authority.objects.get(pk=id_authority)
        except Authority.DoesNotExist:
            raise Http404("Authority does not exist")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'sco/authority_detail.html',
            context={'authority':id_authority,}
        )

def register_authority(request):

    if request.method == 'POST':
        form = RegistrationFormAuthority(request.POST)
        response_data = {}
        if form.is_valid():
            authority = form.save(commit=False)
            form.save()
            response_data['result'] = 'Autoridad guardada Exitosamente!'
            response_data['authority'] = authority.name_authority

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error": "Algo anda mal, no se pudo guardar"}),
            content_type="application/json")
    else:
        form = RegistrationFormAuthority()
        args = {'form': form}
        return render(request, 'sco/register_authority.html', args)

class AuthorityUpdate(UpdateView):
    form_class = RegistrationFormAuthority
    model = Authority
    template_name = 'sco/register_authority.html'
    success_url = '/sco/autoridades/'

class AuthorityDelete(DeleteView):
    model = Authority
    success_url = '/sco/autoridades/'

#CRUD Type
class TypeListView(ListView):
    model = Type

def register_type(request):
    if request.method == 'POST':
        form = RegistrationFormType(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/sco/materias/')
    else:
        form = RegistrationFormType()
        args = {'form': form}
    return render(request, 'sco/register_type.html', args)

class TypeUpdate(UpdateView):
    form_class = RegistrationFormType
    model = Type
    template_name = 'sco/register_type.html'
    success_url = '/sco/materias/'

class TypeDelete(DeleteView):
    model = Type
    success_url = '/sco/materias/'

def type(request):
    return render(request, 'sco/type.html')

#CRUD Document
class DocumentListView(ListView):
    model = Document

class DocumentDetailView(DetailView):
    model = Document

    def document_detail_view(request,pk):
        try:
            id_document=Document.objects.get(pk=id_document)
        except Document.DoesNotExist:
            raise Http404("Document does not exist")

        #book_id=get_object_or_404(Book, pk=pk)
        file_path = "/sco/" + id_document.file_pdf
        a="hola"
        args = {'a': a}
        return render(
            request,
            'sco/document_detail.html',
            context={'document':id_document}
        )

def document_edit(request, pk):

    authorities = Authority.objects.all()
    document = Document.objects.get(pk=pk)

    if request.method == 'POST':
        print("entraste if a POST")
        print(request.POST['name_person'])
        print(request.POST['num_folio'])
        name_person = request.POST['name_person']
        num_folio = request.POST['num_folio']
        Document.objects.select_related().filter(id_document=pk).update(name_person=name_person, num_folio=num_folio)


        return redirect('/sco/oficios/')
    else:
        print("formulario entra a GET")
        form1 = RegistrationFormDocument()
        form2 = RegistrationFormType()
        form3 = RegistrationFormAuthority()
        form4 = RegistrationFormProcess()
        args = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4,
        'document': document, 'authorities': authorities}
    return render(request, 'sco/edit_document.html', args)

def register_document(request):

    if request.method == 'POST':
        print("entraste if a POST")
        form1 = RegistrationFormDocument(request.POST)
        form2 = RegistrationFormType(request.POST)
        form4 = RegistrationFormProcess(request.POST)

        type_document = request.POST['name']
        print("tipo de oficio: " + type_document)

        #document_type = pensiones
        if(type_document == 'Pensiones_Alimenticias'):
            print("POST Pensiones Alimenticias")
            form5 = RegistrationFormTypePension(request.POST)

            if (((form1.is_valid() and form2.is_valid()) and form4.is_valid()) and form5.is_valid()):
                print("formulario valido de pensiones")
                name_authority = request.POST['name_authority']
                authority = Authority.objects.get(name_authority = name_authority)
                informeA = Type_InformeA.objects.get(pk=1)
                #data of pension
                pension = form5.save(commit=False)
                form5.save()
                #data of type
                type = form2.save(commit=False)
                type.pension = pension
                type.informeA = informeA
                form2.save()
                #data for process
                process = form4.save(commit=False)
                form4.save()
                document = form1.save(commit=False)
                #create relation one to many type, process and authority
                document.type = type
                document.process = process
                document.authority = authority
                print("relations save")
                #save Document
                document.save()
                print("document save")

                response_data = {}
                response_data['result'] = 'Oficio se Registro Exitosamente!'
                response_data['authority'] = 'Oficio No.' + document.num_folio + '/' + document.consecutive

                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"Error": "Algo anda mal, no se pudo guardar"}),
                content_type="application/json")
        #document_type = informeA
        elif(type_document == 'Informes_Autoridad'):
            print("POST Informes Autoridad")
            form5 = RegistrationFormTypeInformesA(request.POST)
            path_file = settings.MEDIA_ROOT + settings.FILE_NUM_INFORME

            if (((form1.is_valid() and form2.is_valid()) and form4.is_valid()) and form5.is_valid()):
                print("formulario valido informes autoridad")
                name_authority = request.POST['name_authority']
                authority = Authority.objects.get(name_authority = name_authority)
                pension = Type_Pension.objects.get(pk=1)
                #data of informeA
                informeA = form5.save(commit=False)
                #open file num_oficio_res.txt
                #save in the project
                file = open(path_file, 'r')
                internal_control = file.read()
                file.close()
                internal_control = int(internal_control)
                internal_control += 1
                #save internal control in database
                informeA.internal_control = internal_control
                #save new value internal control in file.txt
                internal_control = str(internal_control)
                file = open(path_file, 'w')
                file.write(internal_control)
                file.close()
                #save
                form5.save()
                #data of type
                type = form2.save(commit=False)
                type.pension = pension
                type.informeA = informeA
                form2.save()
                #data for process
                process = form4.save(commit=False)
                form4.save()
                document = form1.save(commit=False)
                #create relation one to many type, process and authority
                document.type = type
                document.process = process
                document.authority = authority
                print("relations save")
                #save Document
                document.save()
                print("document save")

                response_data = {}
                response_data['result'] = 'Oficio Registrado Exitosamente!'
                #response_data['document'] = 'Oficio No.' + document.num_folio + '/' + document.consecutive

                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"Error": "Algo anda mal, no se pudo guardar"}),
                content_type="application/json")
        #any other document type
        else:
            limit_answer = request.POST['limit_answer']
            #end_days = request.POST['end_days']
            print("limite de respuesta: " + limit_answer)
            #print("termino: " + end_days)
            print("form1: " + str(form1.is_valid()))
            print("form2: " + str(form2.is_valid()))
            #form2.is_valid()

            #print("form3: " + str(form3.is_valid()))
            print("form4: " + str(form4.is_valid()))

            if ((form1.is_valid() and form2.is_valid()) and form4.is_valid()):
                print("formulario valido")
                #data from template html

                #data for authority
                name_authority = request.POST['name_authority']
                #city_authority = request.POST['city']
                authority = Authority.objects.get(name_authority = name_authority)

                pension = Type_Pension.objects.get(pk=1)
                informeA = Type_InformeA.objects.get(pk=1)

                #data for type
                type = form2.save(commit=False)
                type.pension = pension
                type.informeA = informeA
                form2.save()
                #data for process
                process = form4.save(commit=False)
                form4.save()

                document = form1.save(commit=False)
                #create relation one to many type, process and authority
                document.type = type
                document.process = process
                document.authority = authority
                print("relations save")

                #save Document
                document.save()
                print("document save")

                response_data = {}
                response_data['result'] = 'Oficio se Registro Exitosamente!'
                response_data['authority'] = 'Oficio No.' + document.num_folio + '/' + document.consecutive

                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"Error": "Algo anda mal, no se pudo guardar"}),
                content_type="application/json")
    #request.method == GET
    else:
        messages.error(request, "Error")
        print("formulario in GET")
        authorities = Authority.objects.all()
        form1 = RegistrationFormDocument()
        form2 = RegistrationFormType()
        form3 = RegistrationFormAuthority()
        form4 = RegistrationFormProcess()
        form5 = RegistrationFormTypePension()
        args = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4,
            'form5': form5, 'authorities': authorities}
    return render(request, 'sco/register_document.html', args)

def document_update(request, pk):

    document = Document.objects.get(pk=pk)
    path_file = settings.MEDIA_ROOT + settings.FILE_NUM_RESPUESTA

    """if request.method == 'POST':

        print("Entra a POST")
        status = request.POST['status']
        print(request.POST['status'])
        #print(request.POST['answer'])
        if status == 'Turnado/Area':
            #answer = request.POST['answer']
            #Process.objects.select_related().filter(id_process=pk).update(status=status,
            #answer=answer)
            Process.objects.select_related().filter(id_process=pk).update(status=status)
        elif status == 'Respuesta/Area':
            num_folio_anwser = request.POST['num_folio_anwser']
            internal_control = request.POST['internal_control']
            description = request.POST['description']
            #upload file
            file_pdf = request.FILES['file_pdf']
            fs = FileSystemStorage()
            filename = fs.save(file_pdf.name, file_pdf)
            uploaded_file_url = fs.url(filename)

            Document.objects.select_related().filter(id_document=pk).update(num_folio_anwser=num_folio_anwser, file_pdf=uploaded_file_url)
            Type.objects.select_related().filter(id_type=pk).update(internal_control=internal_control)
            Process.objects.select_related().filter(id_process=pk).update(status=status,description=description)
            return render(request, 'sco/document_update.html' , {'uploaded_file_url': uploaded_file_url})
        elif ((status == 'Turnado') or (status == 'En Juicio')) or (status == 'Concluido') :
            Process.objects.select_related().filter(id_process=pk).update(status=status, answer='')
        elif status == 'Enviado/Autoridad':
            #date_delivery = request.POST['date_delivery']
            if document.type.name == 'Pensiones_Alimenticias':
                observations = request.POST['observations']
                date_delivery = date.today()
                #upload file
                file_pdf = request.FILES['file_pdf']
                fs = FileSystemStorage()
                filename = fs.save(file_pdf.name, file_pdf)
                uploaded_file_url = fs.url(filename)
                #date_delivery = str(date_delivery)
                #date_delivery = date_delivery[0: 10]
                #print(date_delivery)
                Document.objects.select_related().filter(id_document=pk).update(file_pdf=uploaded_file_url)
                Process.objects.select_related().filter(id_process=pk).update(status=status,
                   date_delivery=date_delivery, observations=observations)
        else:
            return redirect('/sco/oficios/')
        return render(request, 'sco/document_update.html')"""

    if request.method == 'POST':
        status = request.POST['status']
        if document.type.name == 'Pensiones_Alimenticias':
            print("Entra server doc_type pensiones_alimenticias")
            if status == 'Turnado/Area':
                print("status turnado/area")
                #open file num_oficio_res.txt
                #save in the project
                file = open(path_file, 'r')
                num_folio_anwser = file.read()
                file.close()
                num_folio_anwser = int(num_folio_anwser)
                num_folio_anwser += 1
                Document.objects.select_related().filter(id_document=pk).update(num_folio_anwser=num_folio_anwser)
                #update status
                Process.objects.select_related().filter(id_process=pk).update(status=status)
                num_folio_anwser = str(num_folio_anwser)
                file = open(path_file, 'w')
                file.write(str(num_folio_anwser))
                file.close()
                return redirect('/sco/oficios')
            if status != 'Enviado/Autoridad' and status != 'Turnado/Area':
                print("status diferente a enviado/autoridad y turnado/area")
                Process.objects.select_related().filter(id_process=pk).update(status=status)
                return redirect('/sco/oficios')
            else:


                observations = request.POST['document_answer']
                date_delivery = date.today()
                #upload file
                file_pdf = request.FILES['file_pdf']
                fs = FileSystemStorage()
                filename = fs.save(file_pdf.name, file_pdf)
                uploaded_file_url = "/sco" + fs.url(filename)
                #date_delivery = str(date_delivery)
                #date_delivery = date_delivery[0: 10]
                #print(date_delivery)
                Document.objects.select_related().filter(id_document=pk).update(file_pdf=uploaded_file_url)
                Type.objects.select_related().filter(id_type=pk).update(document_answer=observations)
                print('type updated')
                Process.objects.select_related().filter(id_process=pk).update(status=status,
                   date_delivery=date_delivery)
                print("Doc Updated")
                return render(request, 'sco/document_list.html')
        else:
            print("entra")
            if status == 'Turnado/Area':
                print("entra a turnado area server")
                print("pk" + str(pk))
                status = request.POST['status']
                #open file num_oficio_res.txt
                #save in the project
                file = open(path_file, 'r')
                num_folio_anwser = file.read()
                file.close()
                num_folio_anwser = int(num_folio_anwser)
                num_folio_anwser += 1
                #update num_folio_anwser in database
                Document.objects.select_related().filter(id_document=pk).update(num_folio_anwser=num_folio_anwser)
                #update status
                Process.objects.select_related().filter(id_process=pk).update(status=status)
                print("status actualizado")
                #increment value of num_folio_anwser at file.txt
                num_folio_anwser = str(num_folio_anwser)
                file = open(path_file, 'w')
                file.write(num_folio_anwser)
                file.close()
                response_data ={}
                response_data['result'] = 'STATUS Actualizado!'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            elif status == 'Respuesta/Area':
                print("Entra a Respuesta/Area from server")
                #upload file
                file_pdf = request.FILES['file_pdf']
                fs = FileSystemStorage()
                filename = fs.save(file_pdf.name, file_pdf)
                uploaded_file_url = "/sco" + fs.url(filename)
                print("file uploaded")
                observations = request.POST['observations']
                Document.objects.select_related().filter(id_document=pk).update(file_pdf=uploaded_file_url)
                Process.objects.select_related().filter(id_process=pk).update(status=status, observations=observations)
            elif status == 'Enviado/Autoridad':
                date_delivery = date.today()
                #document_answer = request.POST['observations']
                #type = Type.objects.get(document__pk=pk)
                #id_informeA = type.informeA
                Process.objects.select_related().filter(id_process=pk).update(
                status= status,date_delivery=date_delivery)
            else:
                #save others status
                Process.objects.select_related().filter(id_process=pk).update(status=status)
        return redirect('/sco/oficios')


    else:
        document = Document.objects.get(pk=pk)
        process = Process.objects.get(pk=pk)
        form1 = RegistrationFormDocument()
        form2 = RegistrationFormType()
        form3 = RegistrationFormProcess()

        args = {'form1': form1, 'form2': form2,'form3': form3, 'document': document, 'process': process}
    return render(request, 'sco/document_update.html', args)

def document_search(request):
    form3 = RegistrationFormProcess()
    args = {'form3': form3}

    return render(request, 'sco/document_search.html', args)

def search(request):

    if request.GET.get('num_folio'):
        print("busca por num_folio")
        num_folio =  request.GET.get('num_folio')#diccionarios
        document = Document.objects.get(num_folio=num_folio)
        document = document_serializer(document)
        return HttpResponse(json.dumps(document), content_type='application/json')

    if request.GET.get('name_person'):
        print("busca por name_person")
        name_person = request.GET.get('name_person')
        documents = Document.objects.filter(name_person__startswith=name_person)
        documents = [document_serializer(document) for document in documents]
        return HttpResponse(json.dumps(documents), content_type='application/json')

    """if request.GET.get('manager_process'):
        print("entra a get Search")
        manager_process = request.GET.get('manager_process')
        print(manager_process)
        documents = Document.objects.filter(process__manager_process__contains=manager_process)
        print(documents)
        documents = [document_serializer(document) for document in documents]
        return HttpResponse(json.dumps(documents), content_type='application/json')"""

    if request.GET.get('manager_process') or request.GET.get('status'):
        print("entra a get Search 2 args")
        manager_process = request.GET.get('manager_process')
        status = request.GET.get('status')
        if status == 'Seleccion':
            documents = Document.objects.filter(process__manager_process__contains=manager_process)
        else:
            documents = Document.objects.filter(process__manager_process__contains=manager_process,
            process__status__contains=status)
        documents = [document_serializer(document) for document in documents]
        return HttpResponse(json.dumps(documents), content_type='application/json')

#ajax search authorities
def get_authorities(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    authorities = Authority.objects.filter(name_authority__startswith=q)
    results = []
    for field in authorities:
      authority_json = {}
      authority_json = field.name_authority
      results.append(authority_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def document_generate_pdf(request, pk):

    document = Document.objects.get(pk=pk)

    if request.method == 'POST':
        if document.type.name == 'Pensiones_Alimenticias':
            observations = request.POST['observaciones']
            pension = request.POST['tipo_pension']
            informe = request.POST['informe']
            #found id_pension from relation document and type
            type = Type.objects.get(document__pk=pk)
            id_pension = type.pension_id
            date_efect = request.POST['date_efect']
            date_efect = str(date_efect[0: 10])
            print(date_efect)
            format = '%Y-%d-%m'
            date_efect = datetime.strptime(date_efect, format)
            print(date_efect)
            #update fields of type_pension restants
            Type_Pension.objects.select_related().filter(id_pension=id_pension).update(
            date_efect= date_efect, observations=observations)
            args = {'document': document, 'request': request, 'date_today': date_efect,
             'pension': pension, 'informe': informe}
            return Render.render('pdf/pdf_pensionesA.html', args)

        if document.type.name == 'Informes_Autoridad':
            date_redaction = request.POST['date_redaction']
            date_redaction = str(date_redaction[0: 10])
            print(date_redaction)
            format = '%Y-%d-%m'
            date_redaction = datetime.strptime(date_redaction, format)
            print(date_redaction)

            judge_type = request.POST['judge_type']
            info_answer = request.POST['info_answer']
            #args = {'document': document, 'date_redaction': date_redaction, 'observations': observations}
            #output = pypandoc.convert('/home/crisantru/Documentos/servicio_social/contencioso/sco/templates/pdf/pdf_pensionesA.html',
            #format='html', to='docx', outputfile='/home/crisantru/Documentos/output.docx', extra_args=['-RTS'])
            if info_answer == '1':
                args = {'document': document, 'date_redaction': date_redaction,
                'judge_type': judge_type}
                return Render.render('pdf/pdf_informesA_1.html', args)
            elif info_answer == '2':
                observations = request.POST['document_answer']
                args = {'document': document, 'date_redaction': date_redaction,
                'judge_type': judge_type, 'observations': observations}
                return Render.render('pdf/pdf_informesA_2.html', args)
            elif info_answer == '3':
                observations = request.POST['document_answer']
                #observations2 = request.POST['observaciones2']
                args = {'document': document, 'date_redaction': date_redaction,
                'judge_type': judge_type, 'observations': observations}
                return Render.render('pdf/pdf_informesA_3.html', args)
            elif info_answer == '4':
                args = {'document': document, 'date_redaction': date_redaction,
                'judge_type': judge_type}
                return Render.render('pdf/pdf_informesA_4.html', args)



    else:
        if document.type.name == 'Pensiones_Alimenticias':
            args = {'pk': pk, 'document': document}
            return render(request, 'pdf/generate_pdf_pensionesA.html', args)
        elif document.type.name == 'Informes_Autoridad':
            form = RegistrationFormTypeInformesA()
            print("pdf informeA")
            args = {'pk': pk, 'document': document, 'form': form}
            return render(request, 'pdf/generate_pdf_informesA.html', args)
    #elif document.type.name == 'Informes_Autoridad':
    #    if request.method == 'POST':
    #        args = {}
    #        return Render.render('pdf/generate_pdf_informesA.html', args)
    #    else:
    #        print(document)
    #        args = {'pk': pk, 'document': document}
    #        return render(request, 'pdf/generate_pdf_informesA.html', args)
    #else:
    #    args = {'document': document}
    #    return render(request, 'sco/document_generate_pdf.html', args)

def document_generate_xml(request):
    form2 = RegistrationFormType()
    args = {'form2': form2}

    return render(request, 'sco/document_filter.html', args)

def filter_document_type(request):
    print("entra a filter_document_type")
    if request.method == 'GET':
        print("entra a get")
        type_name = request.GET.get('name')
        document_status = request.GET.get('document_status')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        print(type_name)
        #busqueda por pensiones_alimenticias 2 args
        if type_name == 'Pensiones_Alimenticias':
            subtype = request.GET.get('subtype')
            if document_status == 'Turnado':
                documents = Document.objects.filter(type__name__contains=type_name, type__pension__pension_type=subtype)
            else:
                documents = Document.objects.filter(type__name__contains=type_name, type__pension__pension_type=subtype, process__status=document_status, register_date__range=[start_date, end_date])
            documents = [document_serializer(document) for document in documents]
            return HttpResponse(json.dumps(documents), content_type='application/json')
        else:
            #(type_name == 'Expedientes_Penales' or type_name == 'Juicios_Amparo') or type_name == 'Juicios_Civiles':

            print(document_status)
            documents = Document.objects.filter(type__name__contains=type_name, process__status__contains=document_status)
            documents = [document_serializer(document) for document in documents]
            return HttpResponse(json.dumps(documents), content_type='application/json')
        #else:
        #    documents = Document.objects.filter(type__name__contains=type_name)
        #    documents = [document_serializer(document) for document in documents]
        #    return HttpResponse(json.dumps(documents), content_type='application/json')

def document_assigned(request):
    print("entra a document_assigned")
    return render(request, 'sco/document_assigned.html')

def document_serializer(document):
    return {
        'id_document': document.id_document,
        'num_folio': document.num_folio,
        'name_person': document.name_person,
        'process_manager': document.process.manager_process,
        'derivate_area': document.process.derivate_area,
        'document_type': document.type.name,
        #'type_end_days': str(document.type.end_days),
        'process_status': document.process.status,
        'register_date': str(document.register_date),
        'date_delivery': str(document.process.date_delivery)}
        #'register_date': document.register_date}
