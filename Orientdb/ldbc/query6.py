# :param [{ personId, tagName }]


query6sql_cypher = """
MATCH (knownTag:Tag { name: $tagName })
WITH knownTag.id as knownTagId

MATCH (person:Person { id: $personId })-[:KNOWS*1..2]-(friend)
WHERE NOT person=friend
WITH
    knownTagId,
    collect(distinct friend) as friends
UNWIND friends as f
    MATCH (f)<-[:HAS_CREATOR]-(post:Post),
          (post)-[:HAS_TAG]->(t:Tag{id: knownTagId}),
          (post)-[:HAS_TAG]->(tag:Tag)
    WHERE NOT t = tag
    WITH
        tag.name as tagName,
        count(post) as postCount
RETURN
    tagName,
    postCount
ORDER BY
    postCount DESC,
    tagName ASC
LIMIT 10
"""

query6sql = """
SELECT otherTag.name as tagName, COUNT(*) as postCount
FROM(
MATCH {class:Person, as:person, where:(id = :personId)}-knows-{as: otherPerson, where: ($matched.person != $currentMatch) while: ($depth < 2)},
      {as:otherPerson}<-hasCreator-{as:post},
      {as:post}-hasTag->{as:otherTag, where: (otherTag.name != :tagName)},
      {as:post}-hasTag->{as:tag, where: (otherTag.name = :tagName)}
      
RETURN post,otherTag)
GROUP BY otherTag
ORDER BY
    postCount DESC,
    tagName ASC
LIMIT 10
"""