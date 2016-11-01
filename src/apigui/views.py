from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse


from .forms import ApiKeyForm
from .forms import InfoForm
from .forms import DestroyFilesForm
from .forms import ListFilesForm
from .forms import TasksForm
from .services import test_apikey_validity
from .services import sc_get_info_service
from .services import sc_list_files_service
from .services import sc_destroy_files_service
from .services import sc_schedule_files_service

def index(request):
    context = {'nbar': 'home',
               'valid_apikey': get_apikey_validity(request)}
    return render(request, 'apigui/index.html', context)

def files(request):
    if request.method == 'POST':
        form = ListFilesForm(request.POST)
        if form.is_valid():

            # Generate payload
            payload = {}
            keys = ['directory', 'page', 'results_per_page']
            for key in keys:
                add_optional_post_key(request, payload, key)

            # And save payload to session
            request.session['payload'] = payload
            return HttpResponseRedirect(reverse('apigui:files'))
    else:
        # GET (show results, or display the input form)
        context = {'nbar': 'files',
                   'valid_apikey': get_apikey_validity(request)}
        

        # Take payload from session
        if 'payload' in request.session:
            results = sc_list_files_service(get_apikey(request),
                                    request.session['payload'])
            context['results'] = results

            # Delete the already used payload from the session
            del request.session['payload']
        else:
            # Display the form for data
            form = ListFilesForm()
            context['form'] = form
            
    return render(request, 'apigui/files.html', context)

def scheduled_tasks_post(request):
    form = TasksForm(request.POST)
    if not form.is_valid():
        # The form is not valid
        context = {'nbar': 'tasks',
                   'valid_apikey': get_apikey_validity(request),
                   'form': form}
        return render(request, 'apigui/tasks.html', context)
    
    # The form is valid    
    # Generate payload
    payload = {}

    # optional
    add_optional_post_key(request, payload, 'callback_url')

    # Let's parse the task parameters
    task = {'overwrite_file': request.POST['overwrite']}

    # Add these post variables to task
    keys = ['reference_id', 'directory', 'filename', 'actions']
    for key in keys:
        add_optional_post_key(request, task, key)

    actions = task['actions']
    # conditional
    if actions == 'resize':
        if request.POST['resize']:
            task['resize_percent'] = float(request.POST['resize'])
        else:
            task['width'] = request.POST['width']
            task['height'] = request.POST['height']

    # conditional and optional
    if actions == 'crop' and request.POST['coords']:
        task['coords'] = request.POST['coords']

    # conditional and optional
    if actions == 'rotate' and request.POST['rotation']:
        task['rotation'] = request.POST['rotation']
                
    # conditional and optional
    if actions == 'cover':
        task['cover'] = ','.join(request.POST.getlist('cover'))
        add_optional_post_key(request, task, 'width')
        add_optional_post_key(request, task, 'height')


    # Add url and task to job, and job to the payload
    payload['jobs'] = [{'url': request.POST['url'],
                        'tasks':[task]}]
            
    # And save payload to session
    request.session['payload'] = payload
    return HttpResponseRedirect(reverse('apigui:tasks'))
    
def scheduled_tasks(request):
    if request.method == 'POST':
        scheduled_tasks_post(request)

    else:
        # GET (show results, or display the input form)
        context = {'nbar': 'tasks',
                   'valid_apikey': get_apikey_validity(request)}

        # Take payload from session
        if 'payload' in request.session:
            results = sc_schedule_files_service(get_apikey(request),
                                    request.session['payload'])
            context['results'] = results

            # Delete the already used payload from the session
            del request.session['payload']
        else:
            # Display the form for data
            form = TasksForm()
            context['form'] = form
    return render(request, 'apigui/tasks.html', context)

def edit_apikey(request):
    form = ApiKeyForm(initial={'apikey': request.session['apikey']})
    context = {'nbar': 'apikey',
               'valid_apikey': get_apikey_validity(request),
               'form': form}
    return render(request, 'apigui/apikey.html', context)
    
def apikey(request):
    if request.method == 'POST':
        form = ApiKeyForm(request.POST)
        if form.is_valid():
            apikey = request.POST['apikey']

            # Test the validity and save to session
            request.session['apikey_validity'] = test_apikey_validity(apikey)
            # Save apikey to session
            request.session['apikey'] = apikey

        return HttpResponseRedirect(reverse('apigui:apikey'))
    
    form = ApiKeyForm()
    context = {'nbar': 'apikey',
               'valid_apikey': get_apikey_validity(request),
               'form': form}
    if 'apikey' in request.session:
        context.update({'apikey': request.session['apikey']})
        
    return render(request, 'apigui/apikey.html', context)

def info(request): 
    context = {'nbar': 'info',
               'valid_apikey': get_apikey_validity(request)}
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():

            # Generate payload
            payload = {}
            add_optional_post_key(request, payload, 'request_id')

            if request.POST['file_token']:
                payload['files'] = [{'file_token': request.POST['file_token']}]

            # And save payload to session
            request.session['payload'] = payload
            return HttpResponseRedirect(reverse('apigui:info'))
        else:
            context['form'] = form
            
    else:
        # GET (show results, or display form for input)
        # Take payload from session
        if 'payload' in request.session:
            results = sc_get_info_service(get_apikey(request),
                                    request.session['payload'])
            context['results'] = results

            # Delete the already used payload from the session
            del request.session['payload']
        else:
            # Display the form for data
            form = InfoForm()
            context['form'] = form
            
    return render(request, 'apigui/info.html', context)

def destroy(request):
    context = {'nbar': 'destroy',
               'valid_apikey': get_apikey_validity(request)}
    if request.method == 'GET':
        # GET (show request response, or display form for input)

        # Take payload from session
        if 'payload' in request.session:
            results = sc_destroy_files_service(get_apikey(request),
                                    request.session['payload'])
            context['results'] = results

            # Delete the already used payload from the session
            del request.session['payload']
        else:
            # Display the form for user input
            form = DestroyFilesForm()
            context['form'] = form

    else:
        # Request is POST
        form = DestroyFilesForm(request.POST)
        if form.is_valid():
            # Generate payload
            payload = {}
            add_optional_post_key(request, payload, 'callback_url')
            add_optional_post_key(request, payload, 'request_id')
            
            if request.POST['file_token']:
                payload['files'] = [{'file_token': request.POST['file_token']}]

            # Save payload to session
            request.session['payload'] = payload
            return HttpResponseRedirect(reverse('apigui:destroy'))
        else:
            # If the form is not valid, display it again
            context['form'] = form
    return render(request, 'apigui/destroy.html', context)

def tasks(request):
    pass
    
def get_apikey(request):
    if 'apikey' in request.session:
        return request.session['apikey']
    else:
        return None

def get_apikey_validity(request):
    if 'apikey_validity' in request.session:
        return request.session['apikey_validity']
    else:
        request.session['apikey_validity'] = False
        return False
    
def add_optional_post_key(request, dictionary, key):
    if request.POST[key]:
        dictionary[key] = request.POST[key]
