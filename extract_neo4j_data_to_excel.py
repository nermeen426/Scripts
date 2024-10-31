"""
This Python script connects to a Neo4j database to retrieve information about all node labels, their distinct properties, and relationships (incoming and outgoing) with other nodes. The data is structured to:
- Retrieve Labels: Get all unique labels (types of nodes) from the Neo4j database.
- Extract Properties: For each label, get a list of unique properties associated with nodes of that label.
- Get Relationships: Fetch all relationships (both incoming and outgoing) for each label, listing the type of relationship and the labels of connected nodes.

The data is then written to an Excel file, with each label's data on a separate sheet. The Excel file contains columns for:
- Label
- Property
- All Relationships (combined incoming and outgoing)
- Incoming Relationships
- Outgoing Relationships
"""

import openpyxl
from neo4j import GraphDatabase

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
    try:
        # Query for incoming relationships
        incoming_query = f"""
        MATCH (a:`{label_name}`)<-[r]-(b)
        RETURN DISTINCT type(r) AS relationship_name, labels(b) AS connected_labels
        """
        # Query for outgoing relationships
        outgoing_query = f"""
        MATCH (a:`{label_name}`)-[r]->(b)
        RETURN DISTINCT type(r) AS relationship_name, labels(b) AS connected_labels
        """
        
        with driver.session() as session:
            # Execute the incoming relationships query
            incoming_result = session.run(incoming_query)
            incoming_relationships = [
                f"{record['relationship_name']} ({', '.join(record['connected_labels'])})"
                for record in incoming_result
            ]

            # Execute the outgoing relationships query
            outgoing_result = session.run(outgoing_query)
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

# Function to write the results to an Excel file with multiple sheets, sorted alphabetically by label name
def write_to_excel(data, filename="F:/Etolv/Scripts/Excels/neo4j_data_labels_properties_relationships.xlsx"):
    print(f"Writing data to {filename}...")

    # Sort data alphabetically by label name
    data.sort(key=lambda x: x[0])

    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)  # Remove the default sheet

    for label, properties, all_relationships, incoming_relationships, outgoing_relationships in data:
        # Create a new sheet for each label in alphabetical order
        worksheet = workbook.create_sheet(title=label[:31])  # Limit sheet name to 31 characters

        # Write the header
        worksheet.append(["Label", "Property", "All Relationship", "Incoming Relationship", "Outgoing Relationship"])

        # Write properties, each in a separate row
        max_rows = max(len(properties), len(all_relationships), len(incoming_relationships), len(outgoing_relationships))
        
        for i in range(max_rows):
            row = [
                label if i == 0 else "",  # Only write the label name in the first row
                properties[i] if i < len(properties) else "",
                all_relationships[i] if i < len(all_relationships) else "",
                incoming_relationships[i] if i < len(incoming_relationships) else "",
                outgoing_relationships[i] if i < len(outgoing_relationships) else ""
            ]
            worksheet.append(row)

        print(f"Data written for sheet: {label}")

    workbook.save(filename)
    print(f"Data successfully written to {filename}")

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
        # Combine all relationships in one field for the 'All Relationships' column
        all_relationships = incoming_relationships + outgoing_relationships
        # Prepare the row data to write to Excel
        data.append([
            label,
            properties,
            all_relationships,
            incoming_relationships,
            outgoing_relationships
        ])
        print(f"Data for {label}: {data[-1]}")

    # Write collected data to Excel
    write_to_excel(data)
    print("Data extraction completed.")

# Run the main function
if __name__ == "__main__":
    main()
    # Close the Neo4j driver connection
    driver.close()
