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

def get_common_context(request, label):
    return {'nbar': label,
               'valid_apikey': get_apikey_validity(request)}

def index(request):
    context = get_common_context(request, 'home')
    return render(request, 'apigui/index.html', context)

def invalid_form(request, form, label, template):
    context = get_common_context(request, 'files')
    context['form'] = form
    return render(request, 'apigui/files.html', context)
    
def files(request):
    if request.method == 'GET':
        return general_get_routines(request, 'files',
                                    ListFilesForm(),
                                    sc_list_files_service,
                                    'apigui/files.html')

    # Request is POST
    form = ListFilesForm(request.POST)
    if not form.is_valid():
        return invalid_form(request, form, 'files', 'apigui/files.html')
            
    # Generate payload
    keys = ['directory', 'page', 'results_per_page']
    payload = generate_payload_with_optional_post_keys(request, keys)

    return save_payload_and_redirect(request, payload, 'apigui:files')

def check_for_action(request, task, action_key, key):
    if task['actions'] == action_key:
        add_optional_post_key(request, task, key)

def check_resize(request, task):
    if task['actions'] == 'resize':
        if request.POST['resize_percent']:
            task['resize_percent'] = float(request.POST['resize_percent'])
        else:
            task['width'] = request.POST['width']
            task['height'] = request.POST['height']

def check_cover(request, task):
    if  task['actions'] == 'cover':
        task['cover'] = ','.join(request.POST.getlist('cover'))
        add_optional_post_key(request, task, 'width')
        add_optional_post_key(request, task, 'height')
        
def parse_task_data(request):
    # Let's parse the task parameters
    task = {'overwrite_file': request.POST['overwrite_file']}

    # Add these post variables to task
    keys = ['reference_id', 'directory', 'filename', 'actions']
    for key in keys:
        add_optional_post_key(request, task, key)

    # Add options to task
    check_resize(request, task)
    check_for_action(request, task, 'crop', 'coords')
    check_for_action(request, task, 'rotate', 'degrees')
    check_cover(request, task)
    return task

def generate_payload_with_optional_post_keys(request, keys):
    payload = {}
    for key in keys:
        add_optional_post_key(request, payload, key)
    return payload
    
def scheduled_tasks_post(request):
    form = TasksForm(request.POST)
    if not form.is_valid():
        # The form is not valid, so show it again to the user
        return invalid_form(request, form, 'tasks', 'apigui/tasks.html')
    
    # The form is valid    
    # Generate payload
    payload = generate_payload_with_optional_post_keys(request, ['callback_url'])

    # parse task data
    task = parse_task_data(request)

    # Add url and task to job, and job to the payload
    payload['jobs'] = [{'url': request.POST['url'],
                        'tasks':[task]}]
            
    return save_payload_and_redirect(request, payload, 'apigui:tasks')

    
def scheduled_tasks(request):
    if request.method == 'POST':
        return scheduled_tasks_post(request)
    
    else:
        # GET (show results, or display the input form)
        context = get_common_context(request, 'tasks')

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
    return invalid_form(request, form, 'apikey', 'apigui/apikey.html')
    
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

    # GET, show form
    form = ApiKeyForm()
    context = get_common_context(request, 'apikey')
    context['form'] = form
    if 'apikey' in request.session:
        context.update({'apikey': request.session['apikey']})
        
    return render(request, 'apigui/apikey.html', context)

def info_post(request):
    form = InfoForm(request.POST)
    if not form.is_valid():
        return invalid_form(request, form, 'info', 'apigui/info.html')
        
    return special_routine(request,
                           ['request_id'],
                           ['file_token'],
                           'apigui:info')
    
def info(request):
    if request.method == 'GET':
        return general_get_routines(request, 'info',
                                    InfoForm(),
                                    sc_get_info_service,
                                    'apigui/info.html')
    
    else:
        return info_post(request)

def destroy(request):
    if request.method == 'GET':
        return general_get_routines(request, 'destroy',
                                    DestroyFilesForm(),
                                    sc_destroy_files_service,
                                    'apigui/destroy.html')

    # Request is POST
    form = DestroyFilesForm(request.POST)
    if not form.is_valid():
        return invalid_form(request, form, 'destroy', 'apigui/destroy.html')
            
    return special_routine(request,
                           ['callback_url'],
                           ['reference_id','file_token'],
                           'apigui:destroy')
    
def special_routine(request, optional_keys, file_keys, address):
    payload = generate_payload_with_optional_post_keys(request, optional_keys)
    add_files_to_payload(request, payload, file_keys)
    return save_payload_and_redirect(request, payload, address)
    
def add_files_to_payload(request, payload, keys):
    for key in keys:
        # Take the first and use it
        if request.POST[key]:
            payload['files'] = [{key: request.POST[key]}]
            return
        
def save_payload_and_redirect(request, payload, address):
    request.session['payload'] = payload
    return HttpResponseRedirect(reverse(address))
    
def general_get_routines(request, label, form, service_function, template):
    """ General routines to handle GET request
    - If session contains 'payload' key, the 
      SandCage service should be called.
    - Otherwise a form is displayed for the user.
    """
    
    context = get_common_context(request, label)

    # Check whether the payload is in session
    if 'payload' in request.session:
        # Make the service call
        results = service_function(get_apikey(request),
                                   request.session['payload'])
        context['results'] = results

        # Delete the already used payload from the session
        del request.session['payload']
    else:
        # Display the form for user input
        context['form'] = form
    return render(request, template, context)
    
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
