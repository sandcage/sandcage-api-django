from django import forms

class TasksForm(forms.Form):
    url = forms.URLField(label='Source file URL', max_length=200,
                         required=True)
    reference_id = forms.CharField(label='Reference Id', max_length=100,
                                   required=False)
    overwrite_file = forms.ChoiceField(widget=forms.RadioSelect,
                                  choices=((False,'No'),
                                           (True,'Yes')), initial=False)
    directory = forms.CharField(label='Output directory', max_length=100,
                                required=False)
    filename = forms.CharField(label='Output filename', max_length=100,
                               required=False)
    actions = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=(('save', 'Save'),
                                        ('resize', 'Resize'),
                                        ('crop', 'Crop'),
                                        ('rotate', 'Rotate'),
                                        ('cover', 'Cover')), initial='save')
    width = forms.IntegerField(label='Width', min_value=0, max_value=10000,
                               required=False)
    height = forms.IntegerField(label='Height', min_value=0, max_value=10000,
                                required=False)
    resize_percent = forms.FloatField(label='Resize percent', min_value=0.01,
                              max_value=99.99, required=False)
    coords = forms.CharField(label='Coordinates (x1,y1,x2,y2)', max_length=30,
                             required=False)
    degrees = forms.ChoiceField(widget=forms.RadioSelect,
                                 choices=((90, '90'),
                                          (180, '180'),
                                          (270, '270')), initial=90)
    cover = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                              choices=(('top', 'Top'),
                                        ('bottom', 'Bottom'),
                                        ('middle', 'Middle'),
                                        ('left', 'Left'),
                                        ('right', 'Right'),
                                        ('center', 'Center')), required=False)
    callback_url = forms.URLField(label='Callback URL', max_length=200,
                                  required=False)

class InfoForm(forms.Form):
    request_id = forms.CharField(label='Request Id', max_length=100,
                                 required=False)
    file_token = forms.CharField(label='File token', max_length=100,
                                 required=False)

class DestroyFilesForm(forms.Form):
    reference_id = forms.CharField(label='Reference Id', max_length=100,
                                 required=False)
    file_token = forms.CharField(label='File token', max_length=100,
                                 required=False)
    callback_url = forms.URLField(label='Callback URL', max_length=200,
                                  required=False)

class ListFilesForm(forms.Form):
    directory = forms.CharField(label='Request Id', max_length=100,
                                required=False)
    page = forms.IntegerField(label='Page', min_value=1, required=False)
    results_per_page = forms.IntegerField(label='Results/page', min_value=1,
                                          required=False)

class ApiKeyForm(forms.Form):
    apikey = forms.CharField(label='SandCage API KEY', max_length=100)
