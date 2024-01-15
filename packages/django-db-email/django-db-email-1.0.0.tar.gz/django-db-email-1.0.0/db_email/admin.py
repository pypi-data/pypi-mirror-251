from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from db_email.models import Email


class EmailAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "from_address", "to_address", "cc_address", "bcc_address", "subject", "message", "html_message",
                    "attachments"
                ],
            },
        )
    ]

    readonly_fields = (
        "from_address", "to_address", "cc_address", "bcc_address", "subject", "message", "html_message", "attachments"
    )

    search_fields = ('subject', 'body')

    @admin.display(description=_('From'))
    def from_address(self, obj):
        return obj.from_email

    @admin.display(description=_('To'))
    def to_address(self, obj):
        return obj.to.as_string

    @admin.display(description=_('Cc'))
    def cc_address(self, obj):
        return obj.cc.as_string or self.get_empty_value_display()

    @admin.display(description=_('Bcc'))
    def bcc_address(self, obj):
        return obj.bcc.as_string or self.get_empty_value_display()

    @admin.display(description=_('Message'))
    def message(self, obj):
        return obj.body

    @staticmethod
    def format_links(links, separator='<br>'):
        html = []
        args = []
        for url, text in links:
            html.append('<a href="{}" target="_blank">{}</a>')
            args += [url, text]
        return format_html(
            separator.join(html),
            *args
        )

    @admin.display(description=_('HTML message'))
    def html_message(self, obj):
        return self.format_links([
            (reverse('db_email:html_message', args=[obj.pk]), _('View html message'))
        ]) if obj.html else self.get_empty_value_display()

    @admin.display(description=_('Attachments'))
    def attachments(self, obj):
        attachments = obj.attachments.all()
        if not attachments:
            return self.get_empty_value_display()

        return self.format_links([
            (attachment.file.url, attachment.file.name)
            for attachment in attachments
        ])

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Email, EmailAdmin)
