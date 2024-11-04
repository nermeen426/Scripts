"""
1. Connect to a Neo4j Database:
It uses the Neo4j Python driver to connect to a Neo4j database with the provided URI, username, and password.

2. Retrieve Data from Neo4j:
- It gathers information on each unique label (node type) in the Neo4j database.
- For each label:
It retrieves all unique properties associated with that label.
It fetches incoming and outgoing relationships for that label. Each relationship includes the type of relationship and the connected node’s label(s).

3.Organize and Structure the Data:
It structures the data into a list, where each entry includes:
- The label name.
- A list of properties for the label.
- A combined list of incoming and outgoing relationships.
- Separate lists of incoming and outgoing relationships.
- This data is then converted into a DataFrame to simulate reading it from a CSV file.

4.Visualize Relationships in Network Graphs:
- For each label, it creates a directed network graph using NetworkX.
- Nodes represent labels, and edges represent relationships between labels.
- Relationships are displayed with directed arrows showing the direction (incoming or outgoing) relative to the label.
- Each graph is saved as an image in a specified output directory.
"""

import csv
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
from io import StringIO

# Neo4j connection details
# Replace with actual Neo4j URI 
uri = "your_neo4j_uri_here"  
# Replace with actual username
username = "your_username_here"  
# Replace with actual password
password = "your_password_here"  

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to retrieve all labels in the database
def get_all_labels():
    # Opens a session with the Neo4j database and retrieves all unique labels
    with driver.session() as session:
        result = session.run("CALL db.labels()")
        labels = [record["label"] for record in result]
        return labels

# Function to get distinct properties for a label
def get_distinct_properties(label_name):
    # Query to get all distinct properties for a given label
    query = f"""
    MATCH (n:`{label_name}`)
    WITH collect(DISTINCT keys(n)) AS allKeys
    UNWIND allKeys AS keysList
    UNWIND keysList AS key
    RETURN DISTINCT key
    """
    with driver.session() as session:
        result = session.run(query)
        properties = [record["key"] for record in result]
        return properties

# Function to get all relationships with connected node labels for a label, separated by direction
def get_all_relationships(label_name):
    # Queries to get incoming and outgoing relationships for the label
    incoming_query = f"""
    MATCH (a:`{label_name}`)<-[r]-(b)
    RETURN DISTINCT type(r) AS relationship_name, labels(b) AS connected_labels
    """
    outgoing_query = f"""
    MATCH (a:`{label_name}`)-[r]->(b)
    RETURN DISTINCT type(r) AS relationship_name, labels(b) AS connected_labels
    """
    with driver.session() as session:
        incoming_result = session.run(incoming_query)
        outgoing_result = session.run(outgoing_query)
        
        # Format relationships to include type and connected labels
        incoming_relationships = [
            f"{record['relationship_name']} ({', '.join(record['connected_labels'])})"
            for record in incoming_result
        ]
        outgoing_relationships = [
            f"{record['relationship_name']} ({', '.join(record['connected_labels'])})"
            for record in outgoing_result
        ]
        
        return incoming_relationships, outgoing_relationships

# Collect data from Neo4j and prepare for visualization
data = []
labels = get_all_labels()

for label in labels:
    # Get properties and relationships for each label
    properties = get_distinct_properties(label)
    incoming_relationships, outgoing_relationships = get_all_relationships(label)
    all_relationships = incoming_relationships + outgoing_relationships
    # Append label data to list in a structured format
    data.append([
        label,
        ", ".join(properties),
        ", ".join(all_relationships),
        ", ".join(incoming_relationships),
        ", ".join(outgoing_relationships)
    ])

# Convert data into a DataFrame to simulate reading from CSV
csv_data = StringIO()
csv_writer = csv.writer(csv_data)
# Write CSV header and data rows
csv_writer.writerow(["Label", "Properties", "Relationships", "Incoming Relationships", "Outgoing Relationships"])
csv_writer.writerows(data)
csv_data.seek(0)  # Reset StringIO pointer to the start for reading
df = pd.read_csv(csv_data)

# Set the output directory for visualizations
output_dir = "path_to_your_output_directory"  # Replace with your desired output path
os.makedirs(output_dir, exist_ok=True)

# Loop over each unique label to create and save a network graph
unique_labels = df['Label'].unique()

for label in unique_labels:
    filtered_data = df[df['Label'] == label]

    # Initialize a directed graph for each label's relationships
    G = nx.DiGraph()

    # Add nodes and edges based on incoming and outgoing relationships
    for _, row in filtered_data.iterrows():
        incoming_relationships = row['Incoming Relationships'].split(", ") if pd.notna(row['Incoming Relationships']) else []
        outgoing_relationships = row['Outgoing Relationships'].split(", ") if pd.notna(row['Outgoing Relationships']) else []
        
        # Add edges for incoming relationships
        for relationship in incoming_relationships:
            if " (" in relationship:
                rel_type, source_label = relationship.split(" (")
                source_label = source_label.rstrip(")")
                G.add_edge(source_label, label, relationship=rel_type, direction="incoming")
        
        # Add edges for outgoing relationships
        for relationship in outgoing_relationships:
            if " (" in relationship:
                rel_type, target_label = relationship.split(" (")
                target_label = target_label.rstrip(")")
                G.add_edge(label, target_label, relationship=rel_type, direction="outgoing")

    # Draw the network graph for the current label
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=1)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=5000,
        node_color="lightcoral",
        font_size=12,
        font_weight="bold",
        arrows=True
    )
    plt.title(f"Network Graph of '{label}' Relationships")

    # Save the plot as an image in the output directory
    output_path = os.path.join(output_dir, f"{label}_network_graph.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved network graph for '{label}' at {output_path}")

# Close the Neo4j driver connection after the script is done
driver.close()