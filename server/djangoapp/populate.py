from .models import CarMake, CarModel

# (make, country, founded, description, [(model, type, year), ...])
CAR_DATA = [
    ("NISSAN", "Japan", 1933, "Japanese multinational automobile maker.",
     [("Pathfinder", "SUV", 2023), ("Qashqai", "SUV", 2023),
      ("XTRAIL", "SUV", 2023)]),
    ("Mercedes", "Germany", 1926, "German luxury automotive brand.",
     [("A-Class", "SUV", 2023), ("C-Class", "SUV", 2023),
      ("E-Class", "Sedan", 2023)]),
    ("Audi", "Germany", 1909, "German premium car manufacturer.",
     [("A4", "Sedan", 2023), ("A5", "Sedan", 2023), ("A6", "Sedan", 2023)]),
    ("Kia", "South Korea", 1944, "South Korean automaker.",
     [("Sorrento", "SUV", 2023), ("Carnival", "SUV", 2023),
      ("Cerato", "Sedan", 2023)]),
    ("Toyota", "Japan", 1937, "Japanese multinational automaker.",
     [("Camry", "Sedan", 2023), ("Corolla", "Sedan", 2023),
      ("RAV4", "SUV", 2023)]),
    ("Honda", "Japan", 1948, "Japanese maker of cars and motorcycles.",
     [("Civic", "Sedan", 2022), ("Accord", "Sedan", 2022),
      ("CR-V", "SUV", 2023)]),
    ("Ford", "United States", 1903, "American automobile manufacturer.",
     [("Fusion", "Sedan", 2019), ("Explorer", "SUV", 2022),
      ("Focus", "Wagon", 2018)]),
    ("Chevrolet", "United States", 1911, "American automobile division.",
     [("Malibu", "Sedan", 2021), ("Equinox", "SUV", 2022),
      ("Traverse", "SUV", 2023)]),
    ("BMW", "Germany", 1916, "German luxury vehicle manufacturer.",
     [("3 Series", "Sedan", 2023), ("X5", "SUV", 2023),
      ("5 Series", "Wagon", 2021)]),
    ("Volkswagen", "Germany", 1937, "German automotive brand.",
     [("Golf", "Wagon", 2020), ("Tiguan", "SUV", 2022),
      ("Passat", "Sedan", 2019)]),
    ("Subaru", "Japan", 1953, "Japanese automobile manufacturer.",
     [("Outback", "Wagon", 2022), ("Forester", "SUV", 2023),
      ("Impreza", "Sedan", 2021)]),
    ("Hyundai", "South Korea", 1967, "South Korean automaker.",
     [("Elantra", "Sedan", 2023), ("Tucson", "SUV", 2023),
      ("Santa Fe", "SUV", 2022)]),
]


def initiate():
    """Seed car makes and models. Safe to call repeatedly: it does nothing
    once data exists."""
    if CarMake.objects.exists():
        return
    for dealer_id, (name, country, founded, desc, models) in enumerate(
            CAR_DATA, start=1):
        make = CarMake.objects.create(
            name=name, country=country, founded_year=founded,
            description=desc)
        for model_name, car_type, year in models:
            CarModel.objects.create(
                car_make=make, name=model_name, type=car_type, year=year,
                dealer_id=dealer_id)
