from collections import OrderedDict
from django.dispatch import receiver
from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import resolve
from django.template.loader import get_template

from pretix.base.signals import register_ticket_outputs, register_global_settings
from pretix.presale.signals import html_head as html_head_presale
from pretix.base.ticketoutput import BaseTicketOutput


@receiver(register_ticket_outputs, dispatch_uid="output_wallet")
def register_ticket_output(sender, **kwargs):
    from .ticketoutput import WalletTicketOutput
    return WalletTicketOutput


@receiver(register_global_settings, dispatch_uid="wallet_settings")
def register_global_settings(sender, **kwargs):
    return OrderedDict(
        [
            (
                "wallet_base_url",
                forms.CharField(
                    label=_("Google Wallet Base URL"),
                    initial='https://walletobjects.googleapis.com/walletobjects/v1',
                    required=False,
                )
            ),
            (
                "wallet_batch_url",
                forms.CharField(
                    label=_("Google Wallet Batch URL"),
                    initial='https://walletobjects.googleapis.com/batch',
                    required=False,
                )
            ),
            (
                "wallet_class_url",
                forms.CharField(
                    label=_("Google Wallet Class URL"),
                    initial='https://walletobjects.googleapis.com/walletobjects/v1/eventTicketClass',
                    required=False,
                )
            ),
            (
                "wallet_object_url",
                forms.CharField(
                    label=_("Google Wallet Object URL"),
                    initial='https://walletobjects.googleapis.com/walletobjects/v1/eventTicketObject',
                    required=False,
                )
            ),
            (
                "wallet_key_file",
                forms.CharField(
                    label=_("Google Wallet Keyfile"),
                    required=False,
                    widget=forms.Textarea,
                    help_text=_(
                        "To obtain a keyfile, please follow these instructions"
                        "https://developers.google.com/wallet/tickets/events/web/prerequisites"
                    ),

                )
            )
        ]
    )


@receiver(html_head_presale, dispatch_uid="wallet_html_head_presale")
def html_head_presale(sender, request=None, **kwargs):
    url = resolve(request.path_info)

    print(url.func.__name__)

    if url.namespace == 'presale' and url.func.__name__ in ['OrderDetails', 'OrderPositionDetails', 'view']:
        template = get_template('pretix_wallets/presale_head.html')
        return template.render({'event': sender})
    else:
        return ""
