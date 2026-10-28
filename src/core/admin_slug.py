class SlugAdminMixin:
    """Новий запис: слаг можна лишити порожнім. Існуючий слаг лише для перегляду."""

    auto_slug = True
    slug_source_field = "name_uk"

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and getattr(obj, "pk", None) and _has_slug(obj) and "slug" not in readonly:
            readonly.append("slug")
        return readonly

    def get_prepopulated_fields(self, request, obj=None):
        return {}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if self.auto_slug and db_field.name == "slug" and formfield is not None:
            formfield.required = False
            if not formfield.help_text:
                formfield.help_text = "Якщо порожньо — створиться з назви."
        return formfield

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)
        if not self.auto_slug:
            return form_class
        source_field = self.slug_source_field

        class AutoSlugForm(form_class):
            def clean_slug(self):
                slug = (self.cleaned_data.get("slug") or "").strip()
                if slug or self.instance.pk:
                    return slug or self.instance.slug
                source = (self.data.get(source_field) or "").strip()
                if not source:
                    return slug
                from src.core.slug import unique_slug

                group = self.data.get("group")
                extra = {"group_id": group} if group else None
                return unique_slug(
                    self._meta.model,
                    source,
                    instance=self.instance,
                    extra_filter=extra,
                )

        return AutoSlugForm


def _has_slug(obj) -> bool:
    return any(field.name == "slug" for field in obj._meta.concrete_fields)
