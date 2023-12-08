
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
SELECT 
  (SELECT tag, COUNT(*) as invalid
   FROM (
     MATCH 
       {class:person, as:p, where:(p_personid = 32985348834824)}-knows->{as:friend},
       {as:friend}<-forum_person-{as:post}-forum_tag->{as:tag}
     RETURN post,tag
   )
   WHERE date(post.f_creationdate, 'yyyy-MM-dd HH:mm:ss') <= date('2010-08-31 10:11:18.875+02', 'yyyy-MM-dd HH:mm:ss')
   GROUP BY tag
   LIMIT 10) AS invalid,

  (SELECT tag, COUNT(*) as valid
   FROM (
     MATCH 
       {class:person, as:p, where:(p_personid = 32985348834824)}-knows->{as:friend},
       {as:friend}<-forum_person-{as:post}-forum_tag->{as:tag}
     RETURN post,tag
   )
   WHERE date('2010-08-31 10:11:18.875+02', 'yyyy-MM-dd HH:mm:ss') <= date(post.f_creationdate, 'yyyy-MM-dd HH:mm:ss') AND date(post.f_creationdate, 'yyyy-MM-dd HH:mm:ss') < date('2011-08-31 10:11:18.875+02' +  1000*60*60*24 * 1,'yyyy-MM-dd HH:mm:ss')
   GROUP BY tag
   LIMIT 10) AS valid;
"""

#you might have errors just beacuse of you are using as: inside where clause.

