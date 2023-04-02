from neo4j_conn import *


def connect_neo4j():
    """ Constructing our Neo4j connection string """
    return Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")


def prep_db():
    """ Here we can send queries to our Neo4j database: Or create a new DB if none exists first we make sure that
    there are no leftover data in our DB. """
    conn = connect_neo4j()
    conn.query("MATCH ()-[r]->() DELETE r")
    conn.query("MATCH (n) DETACH DELETE n")
    conn.query("CALL gds.graph.drop('PageRankProjection') YIELD graphName;")
    conn.query("CALL gds.graph.drop('KNN-Games') YIELD graphName;")
    conn.query("CALL gds.graph.drop('DegreeCentrality') YIELD graphName;")
    print('Neo4j database was successfully purged of data')


def csv_xD():
    """ Inorder to make the next step work we need to move a copy of the csv file named "games_stripped.csv" into the
    import folder of the Neo4j project. Vi kunne også bare ændre vores query så den tager den raw fil fra github nu,
    måske smartere og mindre opsætning for dem der skal review på peergrade. """
    print('smth')

def create_db():
    """ Then we populate the database with data using the following command. """
    conn = connect_neo4j()
    conn.query("LOAD CSV WITH HEADERS FROM 'file:///games_stripped.csv' as row MERGE (g: Game{title: row.Title, rating: toFloat(row.Rating), releaseDate: row.ReleaseDate, summary: row.Summary, publishers: split(row.Team, ','), genres: split(row.Genres, ','), numberOfReviews: toInteger(row.NumberOfReviews), reviews: split(row.Reviews, ',')}) WITH g MATCH (g) UNWIND g.publishers as pub MERGE (p: Publisher{name: pub}) MERGE (g)-[r1: RELEASED_BY]-> (p) WITH g MATCH (g) UNWIND g.genres as gen MERGE (ge: Genre{name: gen}) MERGE (g)-[r2: HAS_A]-> (ge) WITH g MATCH (g) UNWIND g.reviews as rev MERGE (re: Review{name: rev}) MERGE (g)-[r3: HAS_A]-> (re)")