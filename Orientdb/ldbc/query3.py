#taken from https://github.com/laa/orientdb_ldbc_snb_implementation/tree/master

query3sql = """
SELECT FROM (
  MATCH
   {class:Person, as:p, where:(id = :id)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath}
  RETURN 
    person.id as personId, 
    person.firstName as personFirstName, 
    person.lastName as personLastName,   
    person.in("hasCreator")[
      creationDate >= :creationDate 
      AND creationDate < creationDate + 1000*60*60*24 * :duration 
      AND out("messageIsLocatedId").name CONTAINS :countryXName
    ].size() as xCount,
    person.in("hasCreator")[
      creationDate >= :creationDate 
      AND creationDate < creationDate + 1000*60*60*24 * :duration 
      AND out("messageIsLocatedId").name CONTAINS :countryYName
    ].size() as yCount  
) WHERE xCount > 0 AND xCount > 0
ORDER BY xCount DESC, personId ASC

"""