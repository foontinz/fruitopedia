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
        fruit=variety.fruit.id,
        origin_countries=[country.id for country in variety.origin_countries]
    )

def CountryModel_to_CountryResponseBody(country: models.Country) -> schemas.CountryResponseBody:

    return schemas.CountryResponseBody(
        id=country.id,
        iso_code=country.iso_code,
        name=country.name,
        description=country.description,
        own_varieties=[variety.id for variety in country.own_varieties]
    )