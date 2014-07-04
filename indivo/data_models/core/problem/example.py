from indivo.models import Problem
from indivo.lib.iso8601 import parse_iso8601_datetime as date

problem_fact = Problem(
    name_title="Backache (finding)",
    name_code_title="Backache (finding)",
    name_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    name_code_identifier="161891005",
    status_title="Active",
    status_code_title="Active",
    status_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    status_code_identifier="55561003",
    start_date=date("2009-05-16T12:00:00Z"),
    end_date=date("2009-05-16T16:00:00Z"),
    notes="also suggested some home exercises",
    )
