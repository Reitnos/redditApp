
#:param personId: 143


query8cypher = """
MATCH (start:Person {id: $personId})<-[:HAS_CREATOR]-(:Message)<-[:REPLY_OF]-(comment:Comment)-[:HAS_CREATOR]->(person:Person)
RETURN
    person.id AS personId,
    person.firstName AS personFirstName,
    person.lastName AS personLastName,
    comment.creationDate AS commentCreationDate,
    comment.id AS commentId,
    comment.content AS commentContent
ORDER BY
    commentCreationDate DESC,
    commentId ASC
LIMIT 20
"""


query8sql = """
MATCH 
  {class:Person, as:person, where:(id = :personId)}<-hasCreator-{as:message}<-replyOf-{as:comment}-hasCreator->{as:commentAuthor}
RETURN 
 	commentAuthor.id AS personId,
    commentAuthor.firstName AS personFirstName,
    commentAuthor.lastName AS personLastName,
    comment.creationDate AS commentCreationDate,
    comment.id AS commentId,
    comment.content AS commentContent
ORDER BY
    commentCreationDate DESC,
    commentId ASC
LIMIT 20


"""