
#:param [{ personId, tagClassName }] 


query12cypher = """

MATCH (tag:Tag)-[:HAS_TYPE|IS_SUBCLASS_OF*0..]->(baseTagClass:TagClass)
WHERE tag.name = $tagClassName OR baseTagClass.name = $tagClassName
WITH collect(tag.id) as tags
MATCH (:Person {id: $personId })-[:KNOWS]-(friend:Person)<-[:HAS_CREATOR]-(comment:Comment)-[:REPLY_OF]->(:Post)-[:HAS_TAG]->(tag:Tag)
WHERE tag.id in tags
RETURN
    friend.id AS personId,
    friend.firstName AS personFirstName,
    friend.lastName AS personLastName,
    collect(DISTINCT tag.name) AS tagNames,
    count(DISTINCT comment) AS replyCount
ORDER BY
    replyCount DESC,
    toInteger(personId) ASC
LIMIT 20

"""


query12sql = """

select 
    friend.id AS personId,
    friend.firstName AS personFirstName,
    friend.lastName AS personLastName,
    tag.name AS tagNames,
    count(DISTINCT comment) AS replyCount
from (
MATCH 
	{class:Person, as:person, where:(id = :personId)}-knows-{as: friend}<-hasCreator-{as: comment}-replyOf->{as:post}-hasTag->{as:tag}-hasType->{as:tagClass, where: (tagClass.name = :tagClassName)}
RETURN
    friend,tag,comment,post,tagClass
)
GROUP BY friend,tag
ORDER BY
    replyCount DESC,
    toInteger(personId) ASC
LIMIT 20


"""