from neo4j_conn import *

conn = connect_neo4j()


def create_knn_projection():
    """ Creating Graph Projection. """
    conn.query("CALL gds.graph.project('KNN-Games',{Game: {properties: ['rating','numberOfReviews']}},'*');")


def knn_stream_mode():
    """ stream the knn Graph Projection. """
    conn.query("CALL gds.knn.stream('KNN-Games', { topK: 1, nodeProperties: ['rating'], randomSeed: 1337, "
               "concurrency: 1, sampleRate: 1.0, deltaThreshold: 0.0 }) YIELD node1, node2, similarity RETURN "
               "gds.util.asNode(node1).title AS Game1, gds.util.asNode(node2).title AS Game2, similarity ORDER BY "
               "similarity DESCENDING, Game1, Game2")


def knn_memory_estimation():
    """ KNN-Game Memory-Estimation. """
    conn.query("CALL gds.knn.write.estimate('KNN-Games', {nodeProperties: ['rating'],writeRelationshipType: "
               "'SIMILAR',writeProperty: 'score',topK: 1}) YIELD nodeCount, bytesMin, bytesMax, requiredMemory")


def knn_stat_mode():
    """ Creating Graph stats for knn. """
    conn.query("CALL gds.knn.stats('KNN-Games', {topK: 1, concurrency: 1, randomSeed: 42, nodeProperties: ["
               "'rating']}) YIELD nodesCompared, similarityPairs")


def knn_mutate_mode():
    """ mutate the knn Graph Projection. """
    conn.query("CALL gds.knn.mutate('KNN-Games', { mutateRelationshipType: 'SIMILAR', mutateProperty: 'score', "
               "topK: 1, randomSeed: 42, concurrency: 1, nodeProperties: ['rating'] }) YIELD nodesCompared, "
               "relationshipsWritten")


def write_knn_graph():
    """ writing our graph projecting to DB. """
    conn.query("CALL gds.knn.write('KNN-Games', { writeRelationshipType: 'SIMILAR', writeProperty: 'score', topK: 1, "
               "randomSeed: 42, concurrency: 1, nodeProperties: ['rating'] }) YIELD nodesCompared, "
               "relationshipsWritten")
