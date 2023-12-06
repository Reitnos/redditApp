# :param [{ personId, month }]

query10cypher = """
    MATCH (person:Person {id: $personId})-[:KNOWS*2..2]-(friend),
        (friend)-[:IS_LOCATED_IN]->(city:City)
    WHERE NOT friend=person AND
        NOT (friend)-[:KNOWS]-(person)
    WITH person, city, friend, datetime({epochMillis: friend.birthday}) as birthday
    WHERE  (birthday.month=$month AND birthday.day>=21) OR
            (birthday.month=($month%12)+1 AND birthday.day<22)
    WITH DISTINCT friend, city, person
    OPTIONAL MATCH (friend)<-[:HAS_CREATOR]-(post:Post)
    WITH friend, city, collect(post) AS posts, person
    WITH friend,
        city,
        size(posts) AS postCount,
        size([p IN posts WHERE (p)-[:HAS_TAG]->()<-[:HAS_INTEREST]-(person)]) AS commonPostCount
    RETURN friend.id AS personId,
        friend.firstName AS personFirstName,
        friend.lastName AS personLastName,
        commonPostCount - (postCount - commonPostCount) AS commonInterestScore,
        friend.gender AS personGender,
        city.name AS personCityName
    ORDER BY commonInterestScore DESC, personId ASC
    LIMIT 10
"""

query10sql = """
WITH tmp as (SELECT DISTINCT otherPerson, city, person
FROM(
SELECT person, city, otherPerson, datetime(otherPerson.birthday) as birthday
FROM(
MATCH 
	{class:Person, as:person, where:(id = :personId)}-knows-{as: otherPerson, where: ($matched.person != $currentMatch) while: ($depth = 1)},
	{as:otherPerson}<-isLocatedIn-{as: city}
RETURN person, city, otherPerson))
WHERE  (birthday.month=:month AND birthday.day>=21) OR
        (birthday.month=(:month%12)+1 AND birthday.day<22)
SELECT
   	  friend.id AS personId,
      friend.firstName AS personFirstName,
      friend.lastName AS personLastName,
      total AS commonInterestScore,
      friend.gender AS personGender,
      city.name AS personCityName
FROM(
SELECT friend,post, Count(*) as total
FROM(
MATCH
     {class: Person, as:friend, where: (friend.id = tmp.otherPerson.id))<-hasCreator-(as: post)},
     {as:post}-hasTag->()<-hasInterest-{as:strt, where strt = person}]
RETURN     
    	friend,post)
)
GROUP BY friend
ORDER BY commonInterestScore DESC, personId ASC
LIMIT 10 
"""

