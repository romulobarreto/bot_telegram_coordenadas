def gerador_coordenada(numero: str, dao) -> tuple[bool, str]:
    #  Recebe latitude e longitude da DAO
    sucesso, resultado = dao(numero)

    # Gera o link ou a mensagem de erro
    if sucesso:
        link = f"https://www.google.com/maps?q={resultado.latitude},{resultado.longitude}"
        return True, link
    else:
        return False, resultado