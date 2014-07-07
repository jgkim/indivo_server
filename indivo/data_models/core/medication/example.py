from indivo.models import Medication, Fill
from indivo.lib.iso8601 import parse_iso8601_datetime as date

med = Medication(
    name_title="AMITRIPTYLINE HCL 50 MG TAB",
    name_code_title="AMITRIPTYLINE HCL 50 MG TAB",
    name_code_system="http://purl.bioontology.org/ontology/RXNORM/",
    name_code_identifier="856845",
    start_date=date("2007-03-14"),
    end_date=date("2007-08-14"),
    frequency_value="2",
    frequency_unit="/d",
    quantity_value="2",
    quantity_unit="{tablet}",
    instructions="Take two tablets twice daily as needed for pain",
)

fill1 = Fill(
    date=date("2007-03-14T04:00:00Z"),
    dispenseDaysSupply=30,
    pbm="T00000000001011",
    pharmacy_ncpdpid="5235235",
    pharmacy_org="CVS #588",
    pharmacy_adr_country="Australia",
    pharmacy_adr_city="WonderCity",
    pharmacy_adr_postalcode="5555",
    pharmacy_adr_street="111 Lake Drive", 
    provider_dea_number="325555555",
    provider_npi_number="5235235",
    provider_email="joshua.mandel@fake.emailserver.com",
    provider_name_given="Josuha",
    provider_name_family="Mandel",
    provider_tel_1_type="w",
    provider_tel_1_number="1-235-947-3452",
    provider_tel_1_preferred_p=True,
    quantityDispensed_value="60",
    quantityDispensed_unit="{tablet}"
)

fill2 = Fill(
    date=date("2007-04-14T04:00:00Z"),
    dispenseDaysSupply=30,
    pbm="T00000000001011",
    pharmacy_ncpdpid="5235235",
    pharmacy_org="CVS #588",
    pharmacy_adr_country="Australia",
    pharmacy_adr_city="WonderCity",
    pharmacy_adr_postalcode="5555",
    pharmacy_adr_street="111 Lake Drive", 
    provider_dea_number="325555555",
    provider_npi_number="5235235",
    provider_email="joshua.mandel@fake.emailserver.com",
    provider_name_given="Josuha",
    provider_name_family="Mandel",
    provider_tel_1_type="w",
    provider_tel_1_number="1-235-947-3452",
    provider_tel_1_preferred_p=True,
    quantityDispensed_value="60",
    quantityDispensed_unit="{tablet}",
)

# save the medication so we can relate other objects to it
med.save()
med.fulfillments = [fill1, fill2]
med.save()
