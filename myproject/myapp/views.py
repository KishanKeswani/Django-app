from django.shortcuts import render, render_to_response,get_object_or_404

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from myapp.models import Document
from myapp.forms import DocumentForm
import pandas as pd

def process_file():
    # 1st operation
    df=pd.read_excel('mass_spec_data_assgnmnt.xlsx')
    PC_df=df[df['Accepted Compound ID'].str.endswith('PC')==True  ]
    LPC_df=df[df['Accepted Compound ID'].str.endswith('LPC')==True ]
    plasma_df=df[df['Accepted Compound ID'].str.endswith('plasmalogen')==True ]
    PC_df=PC_df[~PC_df.isin(LPC_df.to_dict('l')).all(1)]
    PC_df.to_csv('1.csv')
    LPC_df.to_csv('2.csv')
    plasma_df.to_csv('2.csv')
    
    # 2nd operation
    df['Retention Time Roundoff (in mins)']=round(df['Retention time (min)'])

    # 3rd operation
    df.groupby('Retention Time Roundoff (in mins)').mean()


from django.http import HttpResponse
from django.template import Context, loader

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('my_template_name.txt')
    c = Context({
        'data': csv_data,
    })
    response.write(t.render(c))
    return response



def list(request):
    # Handle file upload
    # check=1
    o1=''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            


            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    
    df=pd.read_excel('mass_spec_data_assgnmnt.xlsx')
    # Render list page with the documents and the form
    return render(request, 'list.html', {'documents': documents, 'form': form,'o1':df})#