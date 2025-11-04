from .models import CarMake, CarModel


def initiate():
    if CarMake.objects.exists() and CarModel.objects.exists():
        return  

    makes = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    make_objs = {}
    for m in makes:
        make_objs[m["name"]] = CarMake.objects.create(**m)

    models = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "make": make_objs["NISSAN"]},
        {"name": "Qashqai",    "type": "SUV", "year": 2023, "make": make_objs["NISSAN"]},
        {"name": "A-Class",    "type": "Sedan","year": 2023, "make": make_objs["Mercedes"]},
        {"name": "CLA",        "type": "Coupe","year": 2023, "make": make_objs["Mercedes"]},
        {"name": "Q7",         "type": "SUV", "year": 2023, "make": make_objs["Audi"]},
        {"name": "Sportage",   "type": "SUV", "year": 2023, "make": make_objs["Kia"]},
        {"name": "Sorento",    "type": "SUV", "year": 2023, "make": make_objs["Kia"]},
        {"name": "Camry",      "type": "Sedan","year": 2023, "make": make_objs["Toyota"]},
        {"name": "Corolla",    "type": "Sedan","year": 2023, "make": make_objs["Toyota"]},
    ]
    CarModel.objects.bulk_create([CarModel(**row) for row in models])
