#taken from https://github.com/laa/orientdb_ldbc_snb_implementation/tree/master

query3sql = """
SELECT *
FROM(
  MATCH
   {class:Person, as:p, where:(p_personid = 32985348834824)} -knows-> {as:person, maxdepth:2, where:($matched.p <> $currentMatch), pathAlias:pPath}
  RETURN 
    person.p_personid as personId, 
    person.p_firstname as personFirstName, 
    person.p_lastname as personLastName,   
    person.in("has_m_creatorid")[
      date(m_creationdate, 'yyyy-MM-dd HH:mm:ss') >= date('2012-08-31 10:11:18.875+02', 'yyyy-MM-dd HH:mm:ss')
      AND m_creationdate < m_creationdate + 1000*60*60*24 * 1
      AND out("has_m_locationid").pl_name CONTAINS 'China'
    ].size() as xCount,
 	 person.in("has_m_creatorid")[
      date(m_creationdate, 'yyyy-MM-dd HH:mm:ss') >= date('2012-08-31 10:11:18.875+02', 'yyyy-MM-dd HH:mm:ss')
      AND m_creationdate < m_creationdate + 1000*60*60*24 * 1
      AND out("has_m_locationid").pl_name CONTAINS 'Brazil'
    ].size() as yCount
    )
WHERE xCount > 0 AND yCount > 0
ORDER BY xCount DESC, personId ASC

"""
