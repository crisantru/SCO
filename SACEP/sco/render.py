import os
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

class Render:

    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access
        those resources
        """
        #use short variables names
        sUrl = settings.STATIC_URL      #Typically /static/
        sRoot = settings.STATIC_ROOT    #Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL       #Typically /static/media/
        mRoot = settings.MEDIA_ROOT     #Typically /home/userX/project_static/media/

        #convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        if uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
            print("path: " + path)
        else:
            return URIs     #handle absolute uri (ie: http//some.tID/foo.png)

        #make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must be start with %s or %s' % (sUrl, mUrl)
            )
        return path


    def render(path: str, args: dict):
        template = get_template(path)
        html = template.render(args)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback = Render.link_callback)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error durante el renderizado del PDF", status=400)
