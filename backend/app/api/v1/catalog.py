from collections import Counter

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.db.collections import Collections
from app.db.mongo import get_collection

router = APIRouter()

DEPARTMENT_NAMES = {
    "05": "Antioquia",
    "08": "Atlantico",
    "11": "Bogota",
    "13": "Bolivar",
    "15": "Boyaca",
    "17": "Caldas",
    "18": "Caqueta",
    "19": "Cauca",
    "20": "Cesar",
    "23": "Cordoba",
    "25": "Cundinamarca",
    "27": "Choco",
    "41": "Huila",
    "44": "La Guajira",
    "47": "Magdalena",
    "50": "Meta",
    "52": "Narino",
    "54": "Norte de Santander",
    "63": "Quindio",
    "66": "Risaralda",
    "68": "Santander",
    "70": "Sucre",
    "73": "Tolima",
    "76": "Valle del Cauca",
    "81": "Arauca",
    "85": "Casanare",
    "86": "Putumayo",
    "88": "San Andres y Providencia",
    "91": "Amazonas",
    "94": "Guainia",
    "95": "Guaviare",
    "97": "Vaupes",
    "99": "Vichada",
}


@router.get("/catalog/ciudades")
def list_cities(_: dict = Depends(get_current_user)) -> list[dict[str, str]]:
    collection = get_collection(Collections.CIUDADES)
    documents = list(collection.find({}, {"_id": 0, "nombre": 1, "codigo": 1, "coddep": 1}).sort("nombre", 1))
    counts = Counter((document.get("nombre") or "").strip() for document in documents)

    results: list[dict[str, str]] = []
    for document in documents:
        city_name = (document.get("nombre") or "").strip()
        department_name = DEPARTMENT_NAMES.get(document.get("coddep") or "", "")
        label = city_name
        if counts[city_name] > 1 and department_name:
            label = f"{city_name} - {department_name}"

        results.append(
            {
                "value": document.get("codigo") or city_name,
                "label": label,
            }
        )

    return results
