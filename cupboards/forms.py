from django import forms
from .widgets import CustomClearableFileInput
from .models import Cupboard, Type, Material, Image

# Add a cupboard design
class DesignForm(forms.ModelForm):

    class Meta:
        model = Cupboard
        fields = '__all__'

    main_image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        types = Type.objects.all()
        friendly_names = [(t.id, t.get_friendly_name()) for t in types]
        self.fields['type'].choices = friendly_names
        
        materials = Material.objects.all()
        display_names = [(m.id, m.get_display_name()) for m in materials]
        self.fields['material'].choices = display_names

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    # Add a material
class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


