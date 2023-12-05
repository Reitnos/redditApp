
#:param [{ personId, maxDate }] 

query9cypher = """
MATCH (root:Person {id: $personId })-[:KNOWS*1..2]-(friend:Person)
WHERE NOT friend = root
WITH collect(distinct friend) as friends
UNWIND friends as friend
    MATCH (friend)<-[:HAS_CREATOR]-(message:Message)
    WHERE message.creationDate < $maxDate
RETURN
    friend.id AS personId,
    friend.firstName AS personFirstName,
    friend.lastName AS personLastName,
    message.id AS commentOrPostId,
    coalesce(message.content,message.imageFile) AS commentOrPostContent,
    message.creationDate AS commentOrPostCreationDate
ORDER BY
    commentOrPostCreationDate DESC,
    message.id ASC
LIMIT 20
"""

query9sql = """

MATCH 
	{class:Person, as:person, where:(id = :personId)}-knows-{as: otherPerson, where: ($matched.person != $currentMatch) while: ($depth < 2)},
	{as:otherPerson}<-hasCreator-{as: message, where: (message.creationDate < :maxDate)}
RETURN
	otherPerson.id AS personId,
    otherPerson.firstName AS personFirstName,
    otherPerson.lastName AS personLastName,
    message.id AS commentOrPostId,
    coalesce(message.content,message.imageFile) AS commentOrPostContent,
    message.creationDate AS commentOrPostCreationDate
ORDER BY
    commentOrPostCreationDate DESC,
    message.id ASC
LIMIT 20

"""
