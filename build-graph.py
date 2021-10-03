import pandas as pd
from IPython.core.display import display, HTML
from pyvis.network import Network

#define the graphobject
digmap_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# set the physics layout of the network
digmap_net.barnes_hut()

# LOAD THE NODES
nodes = pd.read_excel('data/data_nodes.xlsx')

# LOAD THE EDGES from project to organization
edges_p2o = pd.read_excel("data/data_edges_project_org.xlsx")

# LOAD THE EDGES from topic to project
edges_t2p = pd.read_excel("data/data_edges_topic_project.xlsx")

#Add NODES to graph
for i in range(len(nodes)):
    digmap_net.add_node(nodes["node"][i], nodes["node"][i], title=nodes["titel"][i])

#Add EDGES from project to organization to graph
for i in range(len(edges_p2o)):
    try:
        digmap_net.add_edge(edges_p2o["project"][i], edges_p2o["org"][i], value=1)
    except:
        print("Edge p2o FAIL -> "+str(edges_p2o["project"][i])+" and "+str(edges_p2o["org"][i]))

#Add EDGES from project to topic to graph
for i in range(len(edges_t2p)):
    try:
        digmap_net.add_edge(edges_t2p["project"][i], edges_t2p["topic"][i], value=1)
    except:
        print("Edge FAIL p2t -> "+str(edges_t2p["project"][i])+" and "+str(edges_t2p["topic"][i]))

#Customized Description in the NodesObjects
for node in digmap_net.nodes:
    titlestring = node["title"]
    if len(titlestring) > 50:
        listofstrings = titlestring.split(" ")
        node["title"] = "Beschreibung: <br>"
        i=0
        for word in listofstrings:
            i+=1
            if i % 9 == 0:
                node["title"] += word + "<br>"
            else:
                node["title"] += word + " "
    else:
        node["title"] = "Beschreibung: <br>" + titlestring
#set buttons to customized the graph
#digmap_net.show_buttons()

# OPTIONSET for the javascript graph
digmap_net.set_options("""
var options = {
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    },
    "color": {
      "inherit": true
    },
    "smooth": {
      "forceDirection": "none"
    }
  },
  "interaction": {
    "hover": true,
    "keyboard": {
      "enabled": true
    },
    "navigationButtons": true,
    "tooltipDelay": 375
  },
  "manipulation": {
    "enabled": true,
    "initiallyActive": true
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}
""")

digmap_net.show("graph.html")
#display(HTML('html/digimap-final.html'))



