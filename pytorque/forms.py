from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator

__author__ = 'rauch'

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


def validate_job_name(job_name):
    if job_name.find(" ") >= 0:
        raise ValidationError(
            u'The name specified may be up to and including 15 characters in length.  It must consist of  printable,  non  white space characters with the first character alphabetic.')


class SubmitScriptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SubmitScriptForm, self).__init__(*args, **kwargs)
        self.fields['stageInFrom'].widget.attrs['readonly'] = True
        self.fields['stageInTo'].widget.attrs['readonly'] = True
        self.fields['stageOutFrom'].widget.attrs['readonly'] = True
        self.fields['stageOutTo'].widget.attrs['readonly'] = True

    #    def __init__(self, queues_choices):
    #        self.queues_choices = queues_choices
    #        super(SubmitScriptForm, self).__init__()
    #
    #    def __init__(self, postData, queues_choices):
    #        self.queues_choices = queues_choices
    #        super(SubmitScriptForm, self).__init__(postData)

    #    hardcoded queues codes
    #    class Meta:
    #        model = SubmitScript


    QUEUES_CHOICES = (('1', 'batch'), ('2', 'custom'))

    #Job Name
    jobName = forms.CharField(validators=[RegexValidator, MaxLengthValidator, validate_job_name], initial='new_job',
        label='Job name',
        max_length=15, error_messages={
            'max_length': 'The name specified may be up to and including 15 characters in length.  It must consist of  printable,  non  white space characters with the first character alphabetic.'})


    #Job Options
    #todo: get it from Model
    queueToSubmitJobTo = forms.ChoiceField(label='Queue to submit job to:', choices=QUEUES_CHOICES, initial='1')

    cpuToUse = forms.IntegerField(label='Number of\n processors to use:', initial=1)
    maxTime = forms.TimeField(label='Maximum time\n(HH:MM:SS)', initial='01:00:00')
    sendMessageAbort = forms.BooleanField(label='Aborts', initial=False, required=False)
    sendMessageEnd = forms.BooleanField(label='Ends', initial=False, required=False)
    sendMessageStart = forms.BooleanField(label='Starts', initial=False, required=False)
    sendMessageTo = forms.EmailField(label='Address to send message to:', help_text='info@example.com', required=False,
        initial='info@example.com')

    #Execution Commands
    executionCommands = forms.CharField(label='Execution commands:', required=False, widget=forms.Textarea,
        initial='echo "Hello world"\npwd\ndate\necho "Done"')

    #File Staging
    stageInFrom = forms.URLField(label='From here:', required=False)
    stageInTo = forms.URLField(label='To there:', required=False)
    stageOutFrom = forms.URLField(label='From here:', required=False)
    stageOutTo = forms.URLField(label='To there:', required=False)
