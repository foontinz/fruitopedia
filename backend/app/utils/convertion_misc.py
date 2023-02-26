from app import models, schemas

def FruitModel_to_FruitResponseBody(fruit: models.Fruit) -> schemas.FruitResponseBody:
    return schemas.FruitResponseBody(
        id=fruit.id,
        name=fruit.name,
        description=fruit.description,
        varieties=[variety.id for variety in fruit.varieties]
    )

def VarietyModel_to_VarietyResponseBody(variety: models.Variety) -> schemas.VarietyResponseBody:
    return schemas.VarietyResponseBody(
        id=variety.id,
        name=variety.name,
        description=variety.description,
        fruit=variety.fruit.id
    )