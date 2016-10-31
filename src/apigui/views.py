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
            if request.POST['directory']:
                payload['directory'] = request.POST['directory']
            if request.POST['page']:
                payload['page'] = request.POST['page']
            if request.POST['results_per_page']:
                payload['results_per_page'] = request.POST['results_per_page']

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

def scheduled_tasks(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():

            # Generate payload
            payload = {}

            # optional
            if request.POST['callback_url']:
                payload['callback_url'] = request.POST['callback_url']

            # Let's parse the task parameters
            task = {'overwrite_file': request.POST['overwrite']}

            # optional
            if request.POST['reference_id']:
                task['reference_id'] = request.POST['reference_id']

            # optional
            if request.POST['directory']:
                task['directory'] = request.POST['directory']

            # optional
            if request.POST['filename']:
                task['filename'] = request.POST['filename']

            # required
            action = request.POST['action']
            task['actions'] = action
            print ("action {}".format(action))

            # conditional
            if action == 'resize' or action == 'cover':
                if request.POST['resize'] and action != 'cover':
                    task['resize_percent'] = float(request.POST['resize'])
                else:
                    task['width'] = request.POST['width']
                    task['height'] = request.POST['height']

            # conditional and optional
            elif action == 'crop' and request.POST['coords']:
                task['coords'] = request.POST['coords']

            # conditional and optional
            elif action == 'rotate' and request.POST['rotation']:
                task['rotation'] = request.POST['rotation']
                
            # conditional and optional
            if action == 'cover':
                task['cover'] = ','.join(request.POST.getlist('cover'))

            # Add url and task to job, and job to the payload
            payload['jobs'] = [{'url': request.POST['url'],
                                'tasks':[task]}]
            
            # And save payload to session
            request.session['payload'] = payload
            return HttpResponseRedirect(reverse('apigui:tasks'))
        else:
            context = {'nbar': 'tasks',
                       'valid_apikey': get_apikey_validity(request),
                       'form': form}
    else:
        # GET (show results, or display the input form)
        context = {'nbar': 'tasks',
                   'valid_apikey': get_apikey_validity(request)}

        # Take payload from session
        if 'payload' in request.session:
            print(request.session['payload'])
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

            # Save apiky to session
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
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():

            # Generate payload
            payload = {}
            if request.POST['request_id']:
                payload['request_id'] = request.POST['request_id']
            if request.POST['file_token']:
                payload['files'] = [{'file_token': request.POST['file_token']}]

            # And save payload to session
            request.session['payload'] = payload
            return HttpResponseRedirect(reverse('apigui:info'))
    else:
        # GET (show results, or display form for input)
        context = {'nbar': 'info',
                   'valid_apikey': get_apikey_validity(request)}


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
    if request.method == 'POST':
        form = DestroyFilesForm(request.POST)
        if form.is_valid():

            # Generate payload
            payload = {}
            if request.POST['request_id']:
                payload['request_id'] = request.POST['request_id']
            if request.POST['file_token']:
                payload['files'] = [{'file_token': request.POST['file_token']}]
            if request.POST['callback_url']:
                payload['callback_url'] = request.POST['callback_url']

            # And save payload to session
            request.session['payload'] = payload
            return HttpResponseRedirect(reverse('apigui:destroy'))
    else:
        # GET (show results, or display form for input)
        context = {'nbar': 'destroy',
                   'valid_apikey': get_apikey_validity(request)}

        # Take payload from session
        if 'payload' in request.session:
            results = sc_destroy_files_service(get_apikey(request),
                                    request.session['payload'])
            context['results'] = results

            # Delete the already used payload from the session
            del request.session['payload']
        else:
            # Display the form for data
            form = DestroyFilesForm()
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
    
