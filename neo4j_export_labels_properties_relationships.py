"""
This Python script connects to a Neo4j database to retrieve information about all node labels, their properties, and relationships. The data extracted from the database includes:
- Labels: All unique labels in the database.
- Properties: Distinct properties for each label.
- Relationships: Both incoming and outgoing relationships associated with each label, including the types of relationships and the labels of connected nodes.

The data is then written to a CSV file with the following columns:
- Label
- Properties
- Relationships
- Incoming Relationships
- Outgoing Relationships
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

# Function to retrieve all labels in the database
def get_all_labels():
    print("Fetching all labels...")
    try:
        with driver.session() as session:
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            print(f"Labels found: {labels}")
            return labels
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
            writer.writerow(["Label", "Properties", "Relationships", "Incoming Relationships", "Outgoing Relationships"])
            for row in data:
                print(f"Writing row: {row}")  # Debugging print statement
                writer.writerow(row)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Main function to process all labels and collect their properties/relationships
def main():
    print("Starting data extraction...")
    labels = get_all_labels()
    if not labels:
        print("No labels found in the database.")
        return

    data = []
    for label in labels:
        # Fetch properties for the current label
        properties = get_distinct_properties(label)
        # Fetch incoming and outgoing relationships for the current label
        incoming_relationships, outgoing_relationships = get_all_relationships(label)
        # Combine all relationships into a single field for the 'Relationships' column
        all_relationships = incoming_relationships + outgoing_relationships
        # Prepare the row data to write to CSV
        data.append([
            label,
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

