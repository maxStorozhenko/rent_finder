import requests
from datetime import datetime, timedelta


class TelegramBotClient:
    '''Client for communicating with ria.com API'''
    def __init__(self, bot_token, chat_id) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = (
            'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id='
            '{chat_id}&text={message}'
        )

    def send_message(self, message):
        url = self.base_url.format(
            bot_token=self.bot_token,
            chat_id=self.chat_id,
            message=message,
            )
        response = requests.get(url)

        return response.json()


class DomRiaClient:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.base_url = (
            'https://developers.ria.com/dom/search?api_key={api_key}&category'
            '=1&realty_type=2&operation_type=3&state_id=11&city_id=11&distric'
            't_id=15661&district_id=17976&district_id=17988&district_id=15662'
            '&district_id=15660&district_id=17994&district_id=15650&district_'
            'id=15651&district_id=15659&district_id=15663&district_id=17391&d'
            'istrict_id=18033&district_id=18034&district_id=18035&district_id'
            '=18036&district_id=18037&district_id=17999&district_id=17968&dis'
            'trict_id=18000&district_id=15652&district_id=15655&district_id=1'
            '5171&district_id=17998&district_id=15169&district_id=18003&distr'
            'ict_id=15172&characteristic[209][from]=1&characteristic[209][to]'
            '=1&characteristic[235][from]=5000&characteristic[235][to]=10000&'
            'date_from={date}'
        )
        self.info_url = (
            'https://developers.ria.com/dom/info/{id}?api_key={api_key}'
            )
        self.ad_base_url = 'https://dom.ria.com/uk'

    @property
    def _url(self):
        date = datetime.today().date() - timedelta(days=3)
        url = self.base_url.format(
            api_key=self.api_key,
            date=date
        )
        return url

    def get_ids(self):
        url = self._url
        response = requests.get(url).json()
        ids = response.get('items')
        return ids

    def _get_info(self, id: str):
        url = self.info_url.format(id=id, api_key=self.api_key)
        response = requests.get(url)

        return response.json()

    def generate_message(self, id):
        response = self._get_info(id)
        path = response.get('beautiful_url')
        url = '/'.join([self.ad_base_url, path])
        price = response.get('price_total')

        message = f'{price}\n{url}'
        return message
