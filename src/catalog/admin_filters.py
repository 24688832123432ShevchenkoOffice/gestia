"""Випадаючі фільтри зверху списку. Порожнє значення нічого не ховає."""

from collections.abc import Iterator

from django import forms
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet
from django.http import HttpRequest
from unfold.contrib.filters.admin.dropdown_filters import (
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
)
from unfold.contrib.filters.admin.mixins import DropdownMixin, ValueMixin
from unfold.widgets import UnfoldAdminSelectWidget

ALL = ("", "Усі")
_SUBMIT = "if (this.form.requestSubmit) { this.form.requestSubmit(); } else { this.form.submit(); }"


class NativeDropdownForm(forms.Form):
    def __init__(self, name, label, choices, multiple=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[name] = forms.ChoiceField(
            label=label,
            required=False,
            choices=choices,
            widget=UnfoldAdminSelectWidget(
                attrs={
                    "class": "admin-top-filter__select",
                    "onchange": _SUBMIT,
                }
            ),
        )


class _CleanLabelMixin:
    form_class = NativeDropdownForm

    def _selected(self) -> str:
        value = self.value()
        return "" if value in EMPTY_VALUES else str(value)

    def _form(self, name: str, choices: list) -> dict:
        return {
            "form": self.form_class(
                label=str(self.title),
                name=name,
                choices=choices,
                data={name: self._selected()},
            )
        }


class CatalogChoicesFilter(_CleanLabelMixin, ChoicesDropdownFilter):
    def choices(self, changelist: ChangeList) -> Iterator:
        yield self._form(self.lookup_kwarg, [ALL, *list(self.field.flatchoices)])


class CatalogRelatedFilter(_CleanLabelMixin, RelatedDropdownFilter):
    def choices(self, changelist: ChangeList) -> Iterator:
        yield self._form(self.lookup_kwarg, [ALL, *self.lookup_choices])


class CatalogBooleanFilter(
    _CleanLabelMixin,
    ValueMixin,
    DropdownMixin,
    admin.BooleanFieldListFilter,
):
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Iterator:
        # «Так» стоїть перед «Ні», але список відкривається на «Усі».
        yield self._form(self.lookup_kwarg, [ALL, ("1", "Так"), ("0", "Ні")])
