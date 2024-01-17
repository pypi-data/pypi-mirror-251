from django.utils.translation import gettext_lazy as _

from reviewboard.admin import ModelAdmin, admin_site
from reviewboard.attachments.models import FileAttachment


class FileAttachmentAdmin(ModelAdmin):
    """Admin definitions for the FileAttachment model."""

    list_display = ('file', 'caption', 'mimetype',
                    'review_request_id')
    list_display_links = ('file', 'caption')
    search_fields = ('caption', 'mimetype')
    raw_id_fields = ('added_in_filediff', 'local_site', 'user')

    def review_request_id(self, obj):
        """Return the review request ID for this file attachment."""
        return obj.review_request.get().id

    review_request_id.short_description = _('Review request ID')


admin_site.register(FileAttachment, FileAttachmentAdmin)
