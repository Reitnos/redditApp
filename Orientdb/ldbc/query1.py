#taken from https://github.com/laa/orientdb_ldbc_snb_implementation/tree/master

query1sql = """
MATCH 
 {class:Person, as:p, where:(id = :id)} -knows-> {as:person, maxdepth:3, where:(firstName = :firstName AND $matched.p <> $currentMatch), pathAlias:pPath},
 {as:p} -personIsLocatedIn-> {as:place},
 {as:p} -studyAt-> {as:university, optional:true}
RETURN 
  person.id as friendId,
  person.lastName as frientLastName,
  pPath.size() as distanceFromPerson,
  person.birthDate as friendBirthDay,
  person.creationDate as friendCreationDate,
  person.gender as friendGender,
  person.browserUsed as friendBrowserUsed,
  person.locationIP as friendLocationIp,
  person.email as friendEmails,
  person.speaks as friendLanguages,
  place.name as friendCityName,
  p.out("studyAt"):{
    name, classYear, out("organisationIsLocatedIn").name as city
  } as friendUniversities,
  p.out("workAt"):{
    name, workFrom, out("organisationIsLocatedIn").name as city
  } as friendCompanies
ORDER BY distanceFromPerson, frientLastName, friendId """ 