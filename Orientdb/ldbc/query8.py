
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
  {class:Person, as:person, where:(p_personid = 32985348834824)}<-has_m_creatorid-{as:message}<-has_m_c_replyof-{as:comment}-has_m_creatorid->{as:commentAuthor}
RETURN
	commentAuthor.p_personid AS personId,
    commentAuthor.p_firstname AS personFirstName,
    commentAuthor.p_lastname AS personLastName,
    comment.m_creationdate AS commentCreationDate,
    comment.m_messageid AS commentId,
    comment.m_content AS commentContent
ORDER BY
    commentCreationDate DESC,
    commentId ASC
LIMIT 20


"""