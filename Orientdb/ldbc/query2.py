#taken from https://github.com/laa/orientdb_ldbc_snb_implementation/tree/master

query2sql = """
MATCH
 {class:Person, as:p, where:(id = :id)} -knows-> {as:person},
 {as:person} <-hasCreator- {as:message, where:(creationDate <= :creationDate)}
RETURN 
  person.id as personId,
  person.firstName as personFirstName,
  person.lastName as personLastName,  
  message.id as postOrCommentId,
  message.content + message.imageFile as postOrCommentContent,
  message.creationDate as postOrCommentCreationDate
ORDER BY message.creationDate DESC, postOrCommentId ASC
"""
