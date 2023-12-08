
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

SELECT 
	person.p_personid AS personId,
    person.p_firstname AS personFirstName,
    person.p_lastname AS personLastName,
    message.m_messageid AS commentOrPostId,
    message.m_content + message.m_ps_imagefile AS commentOrPostContent,
    message.m_creationdate AS commentOrPostCreationDate
FROM(
MATCH 
	{class:Person, as:p, where:(p_personid = 32985348834824)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath},
	{as:person}<-has_m_creatorid-{as: message}
return person,message)
WHERE date(message.m_creationdate,'yyyy-MM-dd HH:mm:ss') < date('2012-06-31 10:11:18.875+02', 'yyyy-MM-dd HH:mm:ss')
ORDER BY
    commentOrPostCreationDate DESC,
    message.m_messageid ASC
LIMIT 20
 

"""
