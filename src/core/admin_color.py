from django import forms

from src.content.colors import normalize_hex


class GestiaColorWidget(forms.TextInput):
    input_type = "color"
    template_name = "admin/widgets/gestia_color.html"

    def __init__(self, attrs=None, default="#241c16"):
        self.default_color = normalize_hex(default) or "#241c16"
        merged = {"class": "gestia-color__native"}
        merged.update(attrs or {})
        super().__init__(attrs=merged)

    def format_value(self, value):
        return normalize_hex(value) or self.default_color

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["default_color"] = self.default_color
        return context
