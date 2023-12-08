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

SELECT tagName, COUNT(*) as postCount
FROM(
MATCH  
		{class:Person, as:p, where:(p_personid = 32985348834824)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath},
      {as:person}<-has_m_creatorid-{as:post},
      {as:post}-message_tag->{as:otherTag}
RETURN post,otherTag.t_name as tagName)
WHERE tagName <> 'Saddam_Hussein'
GROUP BY tagName
ORDER BY
    postCount DESC,
    tagName ASC
LIMIT 10
"""

