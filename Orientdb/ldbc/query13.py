#:param [{ person1Id, person2Id }]

query13cypher = """
MATCH
    (person1:Person {id: $person1Id}),
    (person2:Person {id: $person2Id}),
    path = shortestPath((person1)-[:KNOWS*]-(person2))
RETURN
    CASE path IS NULL
        WHEN true THEN -1
        ELSE length(path)
    END AS shortestPathLength
""" 

query13sql = """
SELECT  if(eval("shortestPathLength >= 0 "),shortestPathLength,-1) as shortestPathLength
FROM(
SELECT sum(path.size()) as shortestPathLength FROM (
  SELECT shortestPath($from, $to, null, "knows") AS path 
  LET 
    $from = (SELECT FROM Person WHERE p_personid = 6597069767242), 
    $to = (SELECT FROM Person WHERE p_personid = 10995116278973)
  UNWIND path))
"""