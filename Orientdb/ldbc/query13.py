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
SELECT  if(eval("shortestPathLength IS NULL"), -1 , shortestPathLength))
FROM(
SELECT sum(path.size()) as shortestPathLength FROM (
  SELECT shortestPath($from, $to, null, "knows") AS path 
  LET 
    $from = (SELECT FROM Person WHERE id = :person1Id), 
    $to = (SELECT FROM Person WHERE id = :person2Id)
  UNWIND path)
)
"""