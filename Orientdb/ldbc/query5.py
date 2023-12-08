

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
SELECT forum.f_title as forumTitle, Count(*) as postCount
FROM(
MATCH
   {class:Person, as:p, where:(p_personid = 32985348834824)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath},
    {as:person}.(inE("forum_person"){where: (date(fp_joindate, 'yyyy-MM-dd HH:mm:ss') >= date('2012-06-31 10:11:18.875+02', 'yyyy-MM-dd HH:mm:ss'))}.bothV()){as:forum}-has_m_ps_forumid-{as:post}
  RETURN 
  	forum,post)
GROUP BY forum
ORDER BY
    postCount DESC,
    forum.f_forumid ASC
LIMIT 20
"""


##### notes!
#{where: (since > date('2012-07-02', 'yyyy-MM-dd'))}  maybe you need this date format in this and other queries as well
# maybe insted of bothV you need outV?
# maybe instead of inE you need bothE?
# creationDate can be joinDate?
# groupby might fail because of .title 

