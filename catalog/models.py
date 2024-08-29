from django.template.defaultfilters import truncatechars
from django.db import models


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SearchTerm(BaseModel):
    class Meta:
        db_table = "search_terms"

    term = models.CharField(max_length=2000, blank=False)


class Domain(BaseModel):
    """Domain objects.  All are technically sub-domains to the 1 root domain."""

    class Meta:
        db_table = "domains"

    name = models.CharField(
        max_length=250, unique=True, null=False, help_text="Domain name (required)"
    )

    description = models.CharField(
        max_length=500,
        unique=False,
        null=True,
        help_text="Domain name description (optional)",
    )

    root_domain = models.CharField(
        unique=False,
        null=False,
        blank=False,
        default="usfs",
        choices=[["usfs", "United States Forest Service"]],
    )

    host_system_name = models.CharField(
        max_length=500,
        unique=False,
        null=True,
        blank=True,
        help_text="System name currently hosting the data (i.e. Redshift,  Oracle)",
    )

    host_system_type = models.CharField(
        max_length=500,
        unique=False,
        null=True,
        blank=True,
        help_text="System type currently hosting the data",
    )

    DATA_FORMAT_CHOICES = (
        ("TABULAR", "Tabular"),
        ("TABULAR_AND_GEOSPATIAL", "Tabular and Geospatial"),
        ("GEOSPATIAL", "Geospatial"),
        ("N/A", "N/A"),
    )

    format = models.CharField(
        max_length=125,
        unique=False,
        null=True,
        help_text="The data format",
        choices=DATA_FORMAT_CHOICES,
    )

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def short_descr(self):
        return truncatechars(self.description, 50)


class Asset(BaseModel):
    class Meta:
        db_table = "assets"

    metadata_url = models.CharField(
        max_length=1500,
        unique=True,
        null=True,
        blank=True,
        help_text="The url used to access/retrieve the metadata.",
    )

    title = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text="Name describing the asset",
    )

    description = models.CharField(
        max_length=3000,
        unique=False,
        null=True,
        blank=True,
        help_text="The description of the metadata document.",
    )

    domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)

    modified = models.DateTimeField(
        null=True, blank=True, help_text="Date metadata was last modified."
    )

    @property
    def short_descr(self):
        return truncatechars(self.description, 75)

    @property
    def short_url(self):
        return truncatechars(self.metadata_url, 50)

    def __str__(self) -> str:
        return f"{self.title}"


class Keyword(BaseModel):
    class Meta:
        db_table = "keywords"

    word = models.CharField(max_length=250)
    assets = models.ManyToManyField(Asset)

    def __str__(self) -> str:
        return f"{self.word}"
