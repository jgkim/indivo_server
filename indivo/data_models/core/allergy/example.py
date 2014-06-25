from indivo.models import Allergy
from indivo.lib.iso8601 import parse_iso8601_datetime as date

allergy_fact = Allergy(
    allergic_reaction_title="Anaphylaxis",
    allergic_reaction_code_title="Anaphylaxis",
    allergic_reaction_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    allergic_reaction_code_identifier="39579001",
    category_title="Drug allergy",
    category_code_title="Drug allergy",
    category_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    category_code_identifier="416098002",
    allergen_title="Sulfonamide Antibacterial",
    allergen_code_title="Sulfonamide Antibacterial",
    allergen_code_system="http://purl.bioontology.org/ontology/NDFRT/",
    allergen_code_identifier="N0000175503",
    severity_title="Severe",
    severity_code_title="Severe",
    severity_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    severity_code_identifier="24484000",
    start_date = date("2007-06-12"),
    )

allergy_exclusion = AllergyExclusion(
    name_title="No known allergies",
    name_code_title="No known allergies",
    name_code_identifier="160244002",
    name_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    date = date("2005-05-05T00-00-00Z"),
)
