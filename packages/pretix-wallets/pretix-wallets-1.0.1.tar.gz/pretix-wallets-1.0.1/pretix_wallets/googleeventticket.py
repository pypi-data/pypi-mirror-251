import json

import pytz
from google.auth import jwt, crypt
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials

from pretix.base.models import OrderPosition
from pretix.multidomain.urlreverse import build_absolute_uri


class GoogleEventTickets:
    def __init__(self, service_account_info, object_url):
        self.service_account_info = service_account_info
        self.object_url = object_url
        self.auth()

    def auth(self):
        json_acct_info = json.loads(self.service_account_info)
        self.credentials = Credentials.from_service_account_info(
            json_acct_info,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
        )

        

        self.http_client = AuthorizedSession(self.credentials)

    
    
    def create_object(self, issuer_id: str, class_suffix: str,
                      object_suffix: str, order_position: OrderPosition) -> str:
        response = self.http_client.get(
            url=f'{self.object_url}/{issuer_id}.{object_suffix}')

        if response.status_code == 200:
            print(f'Object {issuer_id}.{object_suffix} already exists!')
            print(response.text)
            return f'{issuer_id}.{object_suffix}'
        elif response.status_code != 404:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{object_suffix}'

        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            'barcode': {
                'type': 'QR_CODE',
                'value': order_position.secret
            },
            'ticketNumber': order_position.order.code,
            'linksModuleData': {
                'uris': [{
                    'uri': '',
                    'description': 'Event Website',
                    'id': 'LINK_MODULE_URI_ID'
                }]
            },
            'dateTime': {}
        }

        if order_position.attendee_name:
            new_object['ticketHolderName'] = order_position.attendee_name
        
        if order_position.subevent:
            new_object['linksModuleData']['uris'][0]['uri'] = build_absolute_uri(
                    order_position.order.event,
                    "presale:event.index",
                    {"subevent": order_position.subevent.pk},
                )
        else:
            new_object['linksModuleData']['uris'][0]['uri'] = build_absolute_uri(order_position.order.event, "presale:event.index")

        tz = pytz.timezone(order_position.order.event.settings.timezone)
        ev = order_position.order.event
        

        if ev.date_admission:
            new_object['dateTime']['doorsOpen'] = ev.date_admission.astimezone(tz).isoformat()
        
        new_object['dateTime']['start'] = ev.date_from.astimezone(tz).isoformat()

        if ev.date_to:
            new_object['dateTime']['end'] = ev.date_to.astimezone(tz).isoformat()

        # Create the object
        response = self.http_client.post(url=self.object_url, json=new_object)

        print('Object insert response')
        print(response.text)

        return response.json().get('id')

    def create_jwt(self, object_id: str) -> str:
        
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'typ': 'savetowallet',
            'payload': {
                'eventTicketObjects': [
                    {
                        "id": object_id
                    }
                ]
            }
        }
        json_acct_info = json.loads(self.service_account_info)
        signer = crypt.RSASigner.from_service_account_info(json_acct_info)
        token = jwt.encode(signer, claims).decode('utf-8')


        return f'https://pay.google.com/gp/v/save/{token}'

