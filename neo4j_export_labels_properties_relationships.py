"""
This Python script connects to a Neo4j database to retrieve detailed information about all node labels, their properties, relationships, and the count of nodes for each label. The extracted data provides a comprehensive view of the database structure, including:

- **Labels**: All unique node labels within the database.
- **Node Count**: The number of nodes present for each label, helping to understand the distribution of nodes.
- **Properties**: Distinct properties associated with each label, providing insight into the attributes available across different types of nodes.
- **Relationships**: Incoming and outgoing relationships for each label, including the type of each relationship and the labels of connected nodes. This allows us to see how nodes of a certain label connect to others within the graph.

After extracting the data, it is written to a CSV file with the following columns:

- **Label**: The unique label for the nodes.
- **Node Count**: The total count of nodes with this label.
- **Properties**: A list of unique properties for nodes with this label.
- **Relationships**: A combined list of incoming and outgoing relationships.
- **Incoming Relationships**: Relationships where nodes of this label are the target of the relationship.
- **Outgoing Relationships**: Relationships where nodes of this label are the source of the relationship.
"""

import csv
from neo4j import GraphDatabase

# Neo4j connection details

# Replace with actual Neo4j URI
uri = "your_neo4j_uri_here"  
# Replace with actual Neo4j username
username = "your_username_here"  
# Replace with actual Neo4j password
password = "your_password_here"  

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to retrieve all labels in the database along with node count
def get_all_labels_with_count():
    print("Fetching all labels with node counts...")
    labels_with_counts = []
    try:
        with driver.session() as session:
            # First, get all labels
            result = session.run("CALL db.labels() YIELD label")
            labels = [record["label"] for record in result]
            
            # For each label, count the nodes
            for label in labels:
                count_result = session.run(f"MATCH (n:`{label}`) RETURN count(n) AS count")
                node_count = count_result.single()["count"]
                labels_with_counts.append({"label": label, "count": node_count})
            
            print(f"Labels with counts: {labels_with_counts}")
            return labels_with_counts
    except Exception as e:
        print(f"Error retrieving labels: {e}")
        return []

# Function to get distinct properties for a label
def get_distinct_properties(label_name):
    print(f"Fetching properties for label: {label_name}")
    query = f"""
    MATCH (n:`{label_name}`)
    WITH collect(DISTINCT keys(n)) AS allKeys
    UNWIND allKeys AS keysList
    UNWIND keysList AS key
    RETURN DISTINCT key
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            properties = [record["key"] for record in result]
            print(f"Properties for {label_name}: {properties}")
            return properties
    except Exception as e:
        print(f"Error retrieving properties for {label_name}: {e}")
        return []

# Function to get all relationships with connected node labels for a label, separated by direction
def get_all_relationships(label_name):
    print(f"Fetching relationships for label: {label_name}")
    incoming_query = f"""
    MATCH (a:`{label_name}`)<-[r]-(b)
    RETURN DISTINCT type(r) AS relationship_name, labels(b) AS connected_labels
    """
    outgoing_query = f"""
    MATCH (a:`{label_name}`)-[r]->(b)
    RETURN DISTINCT type(r) AS relationship_name, labels(b) AS connected_labels
    """
    try:
        with driver.session() as session:
            incoming_result = session.run(incoming_query)
            outgoing_result = session.run(outgoing_query)
            
            # Format incoming and outgoing relationships
            incoming_relationships = [
                f"{record['relationship_name']} ({', '.join(record['connected_labels'])})"
                for record in incoming_result
            ]
            outgoing_relationships = [
                f"{record['relationship_name']} ({', '.join(record['connected_labels'])})"
                for record in outgoing_result
            ]
            
            print(f"Incoming relationships for {label_name}: {incoming_relationships}")
            print(f"Outgoing relationships for {label_name}: {outgoing_relationships}")
            
            return incoming_relationships, outgoing_relationships
    except Exception as e:
        print(f"Error retrieving relationships for {label_name}: {e}")
        return [], []

# Function to write the results to a CSV file
def write_to_csv(data, filename="F:/Etolv/Scripts/database.csv"):
    print(f"Writing data to {filename}...")
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Updated header with new columns
            writer.writerow(["Label", "Node Count", "Properties", "Relationships", "Incoming Relationships", "Outgoing Relationships"])
            for row in data:
                print(f"Writing row: {row}")  # Debugging print statement
                writer.writerow(row)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Main function to process all labels and collect their properties/relationships
def main():
    print("Starting data extraction...")
    labels_with_counts = get_all_labels_with_count()
    if not labels_with_counts:
        print("No labels found in the database.")
        return

    data = []
    for label_info in labels_with_counts:
        label = label_info["label"]
        node_count = label_info["count"]
        # Fetch properties for the current label
        properties = get_distinct_properties(label)
        # Fetch incoming and outgoing relationships for the current label
        incoming_relationships, outgoing_relationships = get_all_relationships(label)
        # Combine all relationships into a single field for the 'Relationships' column
        all_relationships = incoming_relationships + outgoing_relationships
        # Prepare the row data to write to CSV
        data.append([
            label,
            node_count,
            ", ".join(properties),
            ", ".join(all_relationships),
            ", ".join(incoming_relationships),
            ", ".join(outgoing_relationships)
        ])
        print(f"Data for {label}: {data[-1]}")
    # Write collected data to CSV
    write_to_csv(data)
    print("Data extraction completed.")

# Run the main function
if __name__ == "__main__":
    main()
    # Close the Neo4j driver connection
    driver.close()
