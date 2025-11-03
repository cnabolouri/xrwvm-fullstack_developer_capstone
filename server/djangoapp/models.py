# from django.db import models
# from django.utils.timezone import now
# from django.core.validators import MaxValueValidator, MinValueValidator

# # Car manufacturer (e.g., Toyota, BMW)
# class CarMake(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     headquarters = models.CharField(max_length=120, blank=True)
#     founded = models.IntegerField(
#         null=True, blank=True,
#         help_text="Year the make was founded (optional)"
#     )
#     created_at = models.DateTimeField(default=now, editable=False)

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# # Specific model of a make (e.g., Corolla, 3-Series)
# class CarModel(models.Model):
#     # one make → many models
#     make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")

#     # basic fields
#     name = models.CharField(max_length=100)

#     # dealer id stored in Cloudant / external DB (as per lab)
#     dealer_id = models.IntegerField(
#         help_text="Dealer id of the model in Cloudant database"
#     )

#     # limited types
#     SEDAN = "SEDAN"
#     SUV = "SUV"
#     WAGON = "WAGON"
#     COUPE = "COUPE"
#     HATCH = "HATCH"
#     TRUCK = "TRUCK"

#     TYPE_CHOICES = [
#         (SEDAN, "Sedan"),
#         (SUV, "SUV"),
#         (WAGON, "Wagon"),
#         (COUPE, "Coupe"),
#         (HATCH, "Hatchback"),
#         (TRUCK, "Truck"),
#     ]
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SEDAN)

#     # year constrained to 2015–2023 per instructions
#     year = models.IntegerField(
#         validators=[MinValueValidator(2015), MaxValueValidator(2023)]
#     )

#     # optional extras
#     color = models.CharField(max_length=40, blank=True)
#     created_at = models.DateTimeField(default=now, editable=False)

#     class Meta:
#         unique_together = ("make", "name", "year")
#         ordering = ["make__name", "name", "-year"]

#     def __str__(self):
#         return f"{self.make.name} {self.name} ({self.year})"



from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    # headquarters = models.CharField(max_length=120, blank=True, null=True, default="")  
    def __str__(self):
        return self.name

class CarModel(models.Model):
    SEDAN = "SEDAN"
    SUV = "SUV"
    WAGON = "WAGON"
    COUPE = "COUPE"
    HATCH = "HATCH"
    TRUCK = "TRUCK"
    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (COUPE, "Coupe"),
        (HATCH, "Hatchback"),
        (TRUCK, "Truck"),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2023)])

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"
