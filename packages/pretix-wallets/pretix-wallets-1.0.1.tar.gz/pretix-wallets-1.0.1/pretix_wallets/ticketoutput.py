from pretix.base.ticketoutput import BaseTicketOutput
from django.utils.translation import gettext_lazy as _
from .googleeventticket import GoogleEventTickets
from collections import OrderedDict
from django import forms

class WalletTicketOutput(BaseTicketOutput):
    identifier = 'wallet'
    verbose_name = _('Wallet Android')
    download_button_text = _('Save to Google Wallet')
    download_button_icon = 'fa-brands fa-google'
    long_download_button_text = _('Save to Google Wallet')
    multi_download_enabled = False
    preview_allowed = False
    javascript_required = True


    def __init__(self, event):
        self.google_event_tickets = GoogleEventTickets(
            event.settings.get("wallet_key_file"),
            event.settings.get("wallet_object_url")
        )
        super().__init__(event)

    @property
    def settings_form_fields(self) -> dict:
         return OrderedDict(
            list(super().settings_form_fields.items())
            + [
                 (
                    "issuer_id",
                    forms.CharField(
                        label=_("Issuer ID"),
                        help_text=_(
                            "You can find your issuer id in the Google Pay & Wallet Console under 'Google Wallet API'."
                        ),
                        required=True,
                    ),
                ),
                (
                    "class_suffix",
                    forms.CharField(
                        label=_("Class ID"),
                        help_text=_(
                            "Please provide the class ID for the ticket class you created."
                        ),
                        required=True,
                    ),
                ),
            ]
         )

    def generate(self, op):
        order = op.order
        objectid = self.google_event_tickets.create_object(
            order.event.settings.get("ticketoutput_wallet_issuer_id"),
            order.event.settings.get("ticketoutput_wallet_class_suffix"),
            str(order.id) + "-" + str(op.positionid),
            op
        )
        url = self.google_event_tickets.create_jwt(objectid)
        return "", "text/uri-list", url
