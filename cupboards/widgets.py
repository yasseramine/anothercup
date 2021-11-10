from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image (click to open in a new tab)')
    input_text = _('')
    template_name = 'cupboards/custom_widget_templates/custom_clearable_file_input.html'