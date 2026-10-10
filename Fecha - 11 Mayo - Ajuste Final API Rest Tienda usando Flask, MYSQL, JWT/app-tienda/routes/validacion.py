from flask import abort, request


def leer_json(campos, obligatorios):
    """Devuelve solo los campos conocidos del body; responde 400 si el body no es válido."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="El body debe ser un objeto JSON")
    faltan = [campo for campo in obligatorios if data.get(campo) in (None, "")]
    if faltan:
        abort(400, description="Faltan campos obligatorios: " + ", ".join(faltan))
    return {campo: data[campo] for campo in campos if campo in data}


def validar_numero(data, campo, minimo=0, entero=False):
    """Si el campo viene, exige que sea un número (entero si se pide) mayor o igual a minimo."""
    if campo not in data or data[campo] is None:
        return
    valor = data[campo]
    tipos = int if entero else (int, float)
    if isinstance(valor, bool) or not isinstance(valor, tipos) or valor < minimo:
        tipo = "un entero" if entero else "un número"
        abort(400, description=f"{campo} debe ser {tipo} mayor o igual a {minimo}")


def validar_opcion(data, campo, opciones):
    """Si el campo viene, exige que sea uno de los valores del ENUM de la tabla."""
    if campo in data and data[campo] is not None and data[campo] not in opciones:
        abort(400, description=f"{campo} debe ser uno de: " + ", ".join(opciones))
