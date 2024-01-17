from .abstract import ApiClientAbstract

class ImagemClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def add(self, imagem):
        data, ok = self.create_request_post('/imagens', imagem)
        if ok:
            return data

        return None
    
    def favoritar(self, imagem, usuario):
        imagem['usuarioId'] = usuario['id']
        data, ok = self.create_request_post('/imagens/favoritadas', imagem)
        if ok:
            return data

        return None