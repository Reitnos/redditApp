
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


SELECT
		otherPerson.p_personid AS personId,
        otherPerson.p_firstname AS personFirstName,
        otherPerson.p_lastname AS personLastName,
        company.o_name AS organizationName,
        startYear
FROM(
SELECT person, country.pl_name, otherPerson, min(otherPerson.inE('person_company').pc_workfrom) as startYear
FROM(
MATCH 
	 {class:Person, as:person, where:(p_personid = 32985348834824)}-knows-{as:otherPerson, maxdepth:2, where:($matched.person <> $currentMatch), pathAlias:pPath},
     {as:otherPerson}-person_company-{as: company}-has_o_placeid->{as: country}
RETURN
       person, otherPerson,country)
       
WHERE country.pl_name = 'Brazil'
group by person,country,otherPerson)
WHERE startYear <= 2003

ORDER BY
        startYear ASC,
        personId ASC,
        organizationName DESC
LIMIT 10

""" 

