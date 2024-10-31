# Scripts
neo4j_export_labels_properties_relationships Script
<span style="color: green"> Some green text </span>

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
