from django.db import models

from db_email.fields import EmailField, MultiEmailField


class Email(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    from_email = EmailField()
    to = MultiEmailField()
    cc = MultiEmailField(blank=True)
    bcc = MultiEmailField(blank=True)

    def __str__(self):
        return self.subject

    @property
    def html(self):
        alternatives = self.alternatives.filter(mimetype='text/html').all()
        return alternatives[0].content if alternatives else ''


class EmailAlternative(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='alternatives')
    content = models.TextField(blank=True)
    mimetype = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return '{}: alternative {}'.format(self.email, self.mimetype)


class EmailAttachment(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='attachments')
    mimetype = models.CharField(max_length=254, blank=True)
    file = models.FileField(upload_to='db_email', blank=True)

    def __str__(self):
        return '{}: attachment {}'.format(self.email, self.file.name)
