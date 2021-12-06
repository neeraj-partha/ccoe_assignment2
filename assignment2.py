import snap
import math
from terminaltables import SingleTable


SETTINGS = {
	'test_nodeIDs': [14, 35, 107, 200],
	'rec_num': 10,
}

# Recommend friends based on the Common Neighbours
def common_neighbours(graph: snap.TUNGraph, node_id, n_rec):
    scores = []
    for node in graph.Nodes():
        node = node.GetId()
        neighbours = snap.TIntV()
        # don't take into account itself and those it's already connected to
        if node != node_id and not graph.IsEdge(node,node_id):
            scores.append([node, snap.GetCmnNbrs(graph,node,node_id,neighbours)])

    # Sort the list based on the first item (the score) - Descending
    # Then sort by the nodeId - Ascending
    scores.sort(key=lambda x: x[0])
    scores.sort(key=lambda x: x[1], reverse=True)
    # And print the first n_rec ones - Defaults to 10
    # If the number of items is < n_rec it'll just print them all.
    return scores[:n_rec]

# Recommend friends based on the Adamic-Adar Score (AAS)
def adamic_adar(graph: snap.TUNGraph, node_id, n_rec):
    """ Adamic and Adar scoring similarity"""
    scores = []
    neighbours_b = graph.GetNI(node_id).GetOutDeg()
    for node in graph.Nodes():
        sum = 0
        # Get the number of neighbours for node and node_id
        node = node.GetId()
        neighbours = snap.TIntV()
        if node != node_id and not graph.IsEdge(node,node_id):
            snap.GetCmnNbrs(graph,node,node_id,neighbours)
            for c in neighbours:
                sum += 1 / math.log(graph.GetNI(c).GetOutDeg(),2)
            scores.append([node, sum])
    scores.sort(key=lambda x: x[0])
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:n_rec]

def _print_result_tables(node,method,recs):
	"""
		This function aims to do a fancy printing of the results into ascii tables.
		Don't get too excited though. We could also pipe this to a cowsay for the extra swag.
		Arguments:
		- node:	  node id for which we are recommending.
		- method: name of the method
		- recs:   actual recommendations of this method
	"""
	table_data = [['Rank','NodeID','Score']]
	for i in range(len(recs)):
		table_data.append([i+1,recs[i][0],recs[i][1]])

	table = SingleTable(table_data)
	table.justify_columns[0] = 'right'
	table.justify_columns[1] = 'right'
	table.justify_columns[2] = 'left'

	print ("\n{0} - Recommendations for Node: {1}".format(method,node))
	print (table.table)

G = snap.LoadEdgeList(snap.TUNGraph, "contact-high-school-proj-graph.txt", 0,1," ")


for node in SETTINGS["test_nodeIDs"]:
    print("Recommendations for Node: {0} ...".format(node))
    n_recs = SETTINGS["rec_num"]
	# Compute recommendations for Common Neighbour, Jaccard and Adamic & Adar
    rec_common = common_neighbours(G, node,n_recs)
    # Print the results using some fancy ascii art
    _print_result_tables(node,'Common Neighbors',rec_common)
    rec_common = adamic_adar(G, node,n_recs)
    _print_result_tables(node,'Adamic & Adar Score',rec_common)
