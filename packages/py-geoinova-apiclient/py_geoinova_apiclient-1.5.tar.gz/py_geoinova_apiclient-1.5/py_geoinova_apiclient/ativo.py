from .abstract import ApiClientAbstract

class AtivoClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def get_buckets(self, ativoId):
        data, ok = self.create_request_get(f'/ativos/buckets/{ativoId}')
        if ok:
            return data
        
        return []