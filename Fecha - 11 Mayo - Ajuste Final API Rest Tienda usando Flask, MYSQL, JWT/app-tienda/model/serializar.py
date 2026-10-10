from datetime import date
from decimal import Decimal


def valor_json(valor):
    """Convierte los tipos que devuelve MySQL (DECIMAL, DATETIME) a valores JSON."""
    if isinstance(valor, Decimal):
        return float(valor)
    if isinstance(valor, date):  # date y datetime
        return valor.isoformat()
    return valor
