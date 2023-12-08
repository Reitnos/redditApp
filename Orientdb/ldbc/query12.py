
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

SELECT 
	friend.p_personid AS personId,
    friend.p_firstname AS personFirstName,
    friend.p_lastname AS personLastName,
    tag.t_name AS tagNames,
    count(distinct(comment)) AS replyCount
FROM(
  MATCH 
	{class:Person, as:person, where:(p_personid = 32985348834824)}-knows-{as: friend}<-has_m_creatorid-{as: comment}-has_m_c_replyof->{as:post}-message_tag->{as:tag}-has_t_tagclassid->{as:tagClass}
RETURN
    friend,tag,comment,post,tagClass)
WHERE tagClass.tc_name = 'OfficeHolder'
GROUP BY friend,tag
ORDER BY
    replyCount DESC,
    personId ASC
LIMIT 20


"""