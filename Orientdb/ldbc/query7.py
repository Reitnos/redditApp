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
	liker.id AS personId,
    liker.firstName AS personFirstName,
    liker.lastName AS personLastName,
    latestTime AS likeCreationDate,
    message.id AS commentOrPostId,
    coalesce(message.content, message.imageFile) AS commentOrPostContent,
    toInteger(floor(toFloat(latestTime - message.creationDate)/1000.0)/60.0) AS minutesLatency,
    if(eval("friend IS NULL"), true , false))
FROM(
SELECT message,liker,person,min(likeTime) as latestTime, friend
FROM(
SELECT liker, message, like.creationDate AS likeTime, person, friend
FROM(
MATCH 
  {class:Person, as:person, where:(id = :personId)}<-hasCreator-{as:message}.(inE("likes"){as:like}.bothV()){as:liker},
  {as:person}-knows-{as:friend, where ($matched.person = liker)}
RETURN post,otherTag,friend)
)
GROUP BY message,liker,person
)
ORDER BY
    likeCreationDate DESC,
    toInteger(personId) ASC
LIMIT 20

"""
