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
SELECT	
	  person.p_personid AS personId,
      person.p_firstname AS personFirstName,
      person.p_lastname AS personLastName,
      total AS commonInterestScore,
      person.p_gender AS personGender,
      city.pl_name AS personCityName
FROM(
SELECT person, post, city, Count(*) as total
FROM(
SELECT person, person.in('has_m_creatorid') as post , person.in('has_m_creatorid').out('message_tag').in('person_tag') as start, city
FROM(
SELECT p, person, city, birthday
FROM(
SELECT p, city, person, person.p_birthday as birthday
FROM(

MATCH 
	{class:Person, as:p, where:(p_personid = 32985348834824)} -knows-> {as:person, maxdepth:1, where:($matched.p <> $currentMatch), pathAlias:pPath},
    {as:person}-has_p_placeid->{as: city}
RETURN 
	p, person, city))
WHERE (birthday.format('MM') = '05' AND birthday.format('dd') >= '21' ) OR
		(birthday.format('MM') = '06' AND birthday.format('dd') < '22'))
)
GROUP BY person, post, city
)

GROUP BY friend
ORDER BY commonInterestScore DESC, personId ASC
LIMIT 10 
        
"""
