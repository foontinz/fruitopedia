from app import models, schemas

#TODO converter generic class
def FruitModel_to_FruitResponseBody(fruit: models.Fruit, detailed: bool = False) -> schemas.FruitResponseBody:
    if detailed:
        return schemas.FruitResponseBody(
            id=fruit.id,
            name=fruit.name,
            description=fruit.description,
            varieties=[VarietyModel_to_VarietyResponseBody(variety) for variety in fruit.varieties]
        )
    return schemas.FruitResponseBody(
        id=fruit.id,
        name=fruit.name
    )

def VarietyModel_to_VarietyResponseBody(variety: models.Variety, detailed: bool = False) -> schemas.VarietyResponseBody:
    if detailed:
        return schemas.VarietyResponseBody(
        id=variety.id,
        name=variety.name,
        description=variety.description,
        fruit=variety.fruit.id,
        origin_countries=[country.id for country in variety.origin_countries]
    )
    return schemas.VarietyResponseBody(
        id=variety.id,
        name=variety.name,
        fruit=variety.fruit.id
    )

def CountryModel_to_CountryResponseBody(country: models.Country, detailed: bool = False) -> schemas.CountryResponseBody:
    if detailed:
        return schemas.CountryResponseBody(
        id=country.id,
        iso_code=country.iso_code,
        name=country.name,
        description=country.description,
        own_varieties=[variety.id for variety in country.own_varieties]
    )
    return schemas.CountryResponseBody(
        id=country.id,
        name=country.name,
        iso_code=country.iso_code,
    )