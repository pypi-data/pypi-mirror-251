from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from rps_milea import settings as milea
from rps_milea.models import MileaChoices

# Default Naming
admin.site.site_header = admin.site.site_title = '%s Verwaltung' % getattr(milea, 'FW_NAME', "Django")
admin.site.index_title = 'Dashboard'


# Default Admin
class MileaAdmin(admin.ModelAdmin):

    show_sysdata = True  # Zeigt die Systemfelder an (created, updated, ...)

    list_display = ('verbose_id',)
    list_display_links = ('verbose_id',)
    readonly_fields = ['created_at', '_created_by', 'updated_at', '_updated_by',]
    search_fields = ['id',]
    list_per_page = 10
    admin_fieldsets = ()

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 9})},
    }

    def _created_by(self, obj=None):
        if obj and obj.created_by is not None:
            return str(obj.created_by)
        elif obj and obj.created_by is None:
            return "Systemuser"
        return None
    _created_by.short_description = _("Created by")

    def _updated_by(self, obj=None):
        if obj and obj.updated_by is not None:
            return str(obj.updated_by)
        elif obj and obj.updated_by is None:
            return "Systemuser"
        return None
    _updated_by.short_description = _("Updated by")

    def is_active_badge(self, obj):
        return format_html(
            '<span class="badge bg-{} me-1"></span> {}', 'success' if obj.is_active else 'secondary', '',
        )
    is_active_badge.short_description = _("Active")

    def get_progressbar(self, obj):
        # Gibt eine Progressbar in HTML zurück.
        # Dafür muss das Model aber eine spalte "progress" besitzen
        # und mit einem Wert zwischen 0 und 100 befüllt sein.
        if not hasattr(self.model, 'progress'):
            return None
        value = 100 if obj.progress > 100 else obj.progress
        return format_html(
            f'''<div class="progress">
                <div class="progress-bar" style="width: {value}%" role="progressbar" aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="100" aria-label="{value}% Complete">
                <span class="visually-hidden">{value}% Complete</span>
                </div>
            </div>'''
        )
    get_progressbar.short_description = _("Progress")

    def get_fieldsets(self, request, obj=None):
        # Hole die standardmäßigen Felder, die von Django automatisch generiert werden
        fieldsets = super().get_fieldsets(request, obj=obj)

        # Füge Adminfieldset hinzu
        if request.user.is_superuser:
            fieldsets += self.admin_fieldsets

        # Füge das benutzerdefinierte Feldset hinzu
        if self.show_sysdata:
            fieldsets += (
                (_("System data"), {
                    'classes': ('milea-system-data mt-3 col-lg-12',),
                    'fields': (('created_at', '_created_by', 'updated_at', '_updated_by'),),
                }),
            )

        return fieldsets

    def get_fields(self, request, obj=None):
        # Hole alle Felder, die von Django automatisch generiert werden
        fields = super().get_fields(request, obj=obj)

        # Entferne die Felder, die bereits im benutzerdefinierten Feldset enthalten sind
        fields = [field for field in fields if field not in ('is_active', 'created_at', '_created_by', 'updated_at', '_updated_by')]

        return fields

    # Allow search with verbose_id
    def get_search_results(self, request, queryset, search_term):
        # Hole den Verbose Id Tag aus dem Model und modifiziere den suchstring
        if self.model.OBJ_VERB_TAG and search_term.startswith('%s.' % self.model.OBJ_VERB_TAG):
            search_term = search_term.split('.')
            search_term = int(search_term[1])
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        return queryset, use_distinct

    # Modify MileaChoices Queryset, this is maybe not the best place, but done is better than perfect
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.__class__.__name__ == "MileaChoicesField":
            model = ContentType.objects.get_for_model(self.model)
            kwargs["queryset"] = MileaChoices.objects.filter(model=model)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Ridiculous override just to get rid of the "Hold down" text
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        msg = _("Hold down “Control”, or “Command” on a Mac, to select more than one.")
        form_field.help_text = form_field.help_text.replace(str(msg), '').strip()
        return form_field
