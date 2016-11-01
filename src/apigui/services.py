from sandcage import SandCage

def initialize_sandcage(apikey):
    return SandCage(apikey)

def test_apikey_validity(apikey):
    sc = initialize_sandcage(apikey)
    payload = {}
    response = sc.list_files_service(payload)
    return not 'error_msg' in process_response(response)
    
def sc_schedule_files_service(apikey, payload):
    sc = initialize_sandcage(apikey)
    response = sc.schedule_files_service(payload)
    return process_response(response)

def sc_list_files_service(apikey, payload):
    sc = initialize_sandcage(apikey)
    response = sc.list_files_service(payload)
    return process_response(response)

def sc_get_info_service(apikey, payload):
    sc = initialize_sandcage(apikey)
    response = sc.get_info_service(payload)
    return process_response(response)

def sc_destroy_files_service(apikey, payload):
    sc = initialize_sandcage(apikey)
    response = sc.destroy_files_service(payload)
    return process_response(response)

def process_response(response):
    if response.status_code != 200:
        return {'error_msg':
                'Http error occured with status code {}.'.format(response.status_code)}
    else:
        return response.json()
