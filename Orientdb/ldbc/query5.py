

#:param [{ personId, minDate }] 

query5sql_cypher = """

MATCH (person:Person { id: $personId })-[:KNOWS*1..2]-(friend)
WHERE
    NOT person=friend
WITH DISTINCT friend
MATCH (friend)<-[membership:HAS_MEMBER]-(forum)
WHERE
    membership.joinDate > $minDate
WITH
    forum,
    collect(friend) AS friends
OPTIONAL MATCH (friend)<-[:HAS_CREATOR]-(post)<-[:CONTAINER_OF]-(forum)
WHERE
    friend IN friends
WITH
    forum,
    count(post) AS postCount
RETURN
    forum.title AS forumName,
    postCount
ORDER BY
    postCount DESC,
    forum.id ASC
LIMIT 20
"""


query5sql = """
SELECT forum.title as forumTitle, Count(*) as postCount
FROM(
MATCH {class:Person, as:person, where:(id = :personId)}-knows-{as: otherPerson, where: ($matched.person != $currentMatch) while: ($depth < 2)},
      {as:otherPerson}.(inE("hasMember"){where: (creationDate > :minDate)}.bothV()){as:forum}-containerOf->{as:post}
RETURN forum,post)
GROUP BY forum
ORDER BY
    postCount DESC,
    forum.id ASC
LIMIT 2O
"""


##### notes!
#{where: (since > date('2012-07-02', 'yyyy-MM-dd'))}  maybe you need this date format in this and other queries as well
# maybe insted of bothV you need outV?
# maybe instead of inE you need bothE?
# creationDate can be joinDate?
# groupby might fail because of .title 

