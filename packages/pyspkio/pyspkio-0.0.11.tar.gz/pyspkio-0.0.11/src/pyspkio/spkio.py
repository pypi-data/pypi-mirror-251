import requests

class Spkio:

    def __init__(self, host, token) -> None:
        self.URL_SPKIO_SERVICE = f'{host}'
        self.req = requests.Session()
        self.req.headers.update({'Authorization': f'Bearer {token}'})

    def createSource(self, p):
        out = {
            'name': p['name'],
            'source': p['source'],
            'date': {
                   'year': p['dt_data'].year,
                   'month': p['dt_data'].month,
                   'day': p['dt_data'].day
            }
        }
        res = self.req.post(f'{self.URL_SPKIO_SERVICE}/source', json = out)
        return self.catchCreatedResponse(res)

    def createLink(self, idFrom, idKey, el, idSource, idKeyBind=None):
        return self.bindLink(idFrom, idKeyBind, self.createNode(el, idKey, idSource), idSource)

    def bindLink(self, idFrom, idKey, idTo, idSource):
        out = {
            'idFrom': idFrom,
            'idTo': idTo
        }
        if idKey != None: out['idKey'] = idKey
        res = self.req.post(f'{self.URL_SPKIO_SERVICE}/link/{idSource}', json = out)
        return self.catchCreatedResponse(res)

    def createGlossary(self, el, idSource):
        res = self.req.post(f'{self.URL_SPKIO_SERVICE}/glossary/{idSource}', json = {'id': el['tx_text']})
        return self.catchCreatedResponse(res)

    def createNode(self, el, idKey=None, idSource=None):
        out = {
            'idFrom': el['id_from'] if 'id_from' in el else None,
            'idTo': el['id_to'] if 'id_to' in el else None,
            'idKey': el['id_key'] if 'id_key' in el else idKey if idKey != None else None,
            'idContent': el['id_content'] if 'id_content' in el else None,

            'text': el['tx_text'] if 'tx_text' in el else None,
            'integer': el['nr_integer'] if 'nr_integer' in el else None,
            'decimal': el['vr_decimal'] if 'vr_decimal' in el else None,
            'datetime': {
                'year': el['nr_year'] if 'nr_year' in el else None,
                'month': el['nr_month'] if 'nr_month' in el else None,
                'day': el['nr_day'] if 'nr_day' in el else None,
                'hour': el['nr_hour'] if 'nr_hour' in el else None,
                'minute': el['nr_minute'] if 'nr_minute' in el else None,
                'second': el['nr_second'] if 'nr_second' in el else None,
                'timezone': el['nr_timezone'] if 'nr_timezone' in el else None,
                'about': el['nr_about'] if 'nr_about' in el else None
            }
        }
        res = self.req.post(f'{self.URL_SPKIO_SERVICE}/node/{idSource}', json = out)
        return self.catchCreatedResponse(res)

    def catchCreatedResponse(self, res):
        if res.status_code != 202: raise Exception(res.text)
        return res.headers['Location'].split('/')[-1]
