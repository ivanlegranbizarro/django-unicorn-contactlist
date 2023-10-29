from django_unicorn.components import UnicornView
from core.models import User


class ContactPageView(UnicornView):
    contact_id = None
    contacts = User.objects.none()
    users = User.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_state()

    def add_contact(self):
        if self.contact_id:
            self.request.user.contacts.add(self.contact_id)
            self.refresh_state()

    def delete_contact(self, id):
        self.request.user.contacts.remove(id)
        self.refresh_state()

    def get_non_contacts(self):
        contact_ids = self.contacts.values_list("id")

        return User.objects.exclude(id__in=contact_ids).exclude(id=self.request.user.id)

    def refresh_state(self):
        self.contacts = self.request.user.contacts.all()
        self.users = self.get_non_contacts()

    class Meta:
        javascript_exclude = ("contacts", "users")
