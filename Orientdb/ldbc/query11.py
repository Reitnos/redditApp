
#:param [{ personId, countryName, workFromYear }]


query11cypher = """
MATCH (person:Person {id: $personId })-[:KNOWS*1..2]-(friend:Person)
WHERE not(person=friend)
WITH DISTINCT friend
MATCH (friend)-[workAt:WORK_AT]->(company:Company)-[:IS_LOCATED_IN]->(:Country {name: $countryName })
WHERE workAt.workFrom < $workFromYear
RETURN
        friend.id AS personId,
        friend.firstName AS personFirstName,
        friend.lastName AS personLastName,
        company.name AS organizationName,
        workAt.workFrom AS organizationWorkFromYear
ORDER BY
        organizationWorkFromYear ASC,
        toInteger(personId) ASC,
        organizationName DESC
LIMIT 10

"""


query11sql = """


MATCH 
	{class:Person, as:person, where:(id = :personId)}-knows-{as: otherPerson, where: ($matched.person != $currentMatch) while: ($depth < 2)},
	{as:otherPerson}.(outE("workAt"){as:wat, where:  wat.workFrom < :workFromYear }.bothV()){as: company}-isLocatedIn->{class:Country, as: country, where: (country.name = :countryName)},
RETURN
        otherPerson.id AS personId,
        otherPerson.firstName AS personFirstName,
        otherPerson.lastName AS personLastName,
        company.name AS organizationName,
        wat.workFrom AS organizationWorkFromYear
ORDER BY
        organizationWorkFromYear ASC,
        toInteger(personId) ASC,
        organizationName DESC
LIMIT 10

""" 