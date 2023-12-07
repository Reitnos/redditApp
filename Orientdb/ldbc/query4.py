
# :param [{ personId, startDate, endDate }]}

query4sql_cypher = """
MATCH (person:Person {id: $personId })-[:KNOWS]-(friend:Person),
      (friend)<-[:HAS_CREATOR]-(post:Post)-[:HAS_TAG]->(tag)
WITH DISTINCT tag, post
WITH tag,
     CASE
       WHEN $startDate <= post.creationDate < $endDate THEN 1
       ELSE 0
     END AS valid,
     CASE
       WHEN post.creationDate < $startDate THEN 1
       ELSE 0
     END AS inValid
WITH tag, sum(valid) AS postCount, sum(inValid) AS inValidPostCount
WHERE postCount>0 AND inValidPostCount=0
RETURN tag.name AS tagName, postCount
ORDER BY postCount DESC, tagName ASC
LIMIT 10"""


query4sql = """
SELECT tag.name AS tagName, postCount
FROM (
SELECT  tag, sum(valid) AS postCount, sum(invalid) AS inValidPostCount
FROM (
SELECT if(eval(" post.creationDate <= :startDate "), 1 , 0)) as invalid, if(eval(" :startDate <= post.creationDate < :endDate "), 1 , 0)) as invalid
FROM(
MATCH {class:Person, as:p, where:(id = :personId)}-knows->{as:friend},
      {as:friend}<-hasCreator-{as:post}-hasTag->{as:tag}
RETURN post,tag)
)
)
WHERE postCount>0 AND inValidPostCount=0
ORDER BY postCount DESC, tagName ASC
LIMIT 10
"""

#you might have errors just beacuse of you are using as: inside where clause.
