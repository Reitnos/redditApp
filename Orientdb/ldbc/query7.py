# :param personId: 4398046511268


query7cypher="""

MATCH (person:Person {id: $personId})<-[:HAS_CREATOR]-(message:Message)<-[like:LIKES]-(liker:Person)
    WITH liker, message, like.creationDate AS likeTime, person
    ORDER BY likeTime DESC, toInteger(message.id) ASC
    WITH liker, head(collect({msg: message, likeTime: likeTime})) AS latestLike, person
RETURN
    liker.id AS personId,
    liker.firstName AS personFirstName,
    liker.lastName AS personLastName,
    latestLike.likeTime AS likeCreationDate,
    latestLike.msg.id AS commentOrPostId,
    coalesce(latestLike.msg.content, latestLike.msg.imageFile) AS commentOrPostContent,
    toInteger(floor(toFloat(latestLike.likeTime - latestLike.msg.creationDate)/1000.0)/60.0) AS minutesLatency,
    not((liker)-[:KNOWS]-(person)) AS isNew
ORDER BY
    likeCreationDate DESC,
    toInteger(personId) ASC
LIMIT 20

"""

query7sql = """
SELECT
	liker.p_personid AS personId,
    liker.p_firstname AS personFirstName,
    liker.p_lastname AS personLastName,
    latestTime AS likeCreationDate,
    message.m_messageid AS commentOrPostId,
    message.m_content + message.m_ps_imagefile AS commentOrPostContent,
     (date(latestTime, 'yyyy-MM-dd HH:mm:ss') -
    date(message.m_creationdate, 'yyyy-MM-dd HH:mm:ss')) as Latency
FROM(
SELECT message,liker,person,min(likeTime) as latestTime, friend
FROM
(SELECT message, liker, person, message.oute('likes').l_creationdate AS likeTime, friend
FROM(
MATCH 
  {class:Person, as:person, where:(p_personid = 32985348834824)}<-has_m_creatorid-{as:message}.(outE("likes").inV()){as:liker},
  {as:person}-knows->{as:friend}
RETURN liker,person,message,friend)
)
GROUP BY message,liker,person
)
ORDER BY
    likeCreationDate DESC,
    personId ASC
LIMIT 20


"""

