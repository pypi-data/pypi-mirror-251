from .abstract import ApiClientAbstract

class UsuarioClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def fetch_by_cliente_id(self, clienteId):
        data, ok = self.create_request_get(f'/usuarios/clientes/{clienteId}')
        if ok:
            return data

        return None