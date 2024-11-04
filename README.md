# 📝 Neo4j Export Labels, Properties, and Relationships Script

This Python script connects to a Neo4j database and efficiently extracts information about all **node labels**, their **properties**, **relationships**, and **node counts**. The data is saved to a **CSV file** for easy access and further analysis.

---

## Overview

This script extracts the following details from a Neo4j database:

- **Labels**: All unique node labels in the database.
- **Node Count**: The number of nodes associated with each label, providing insight into the distribution of nodes.
- **Properties**: Distinct properties associated with each label.
- **Relationships**: Both incoming and outgoing relationships for each label, including relationship types and connected node labels.

The data is then structured in a CSV file with the following columns:

| Column                 | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Label**              | The node label in Neo4j                                                    |
| **Node Count**         | The total number of nodes with this label                                  |
| **Properties**         | List of properties associated with each label                              |
| **Relationships**      | List of all relationships for each label                                   |
| **Incoming Relationships** | Types of incoming relationships, including labels of connected nodes |
| **Outgoing Relationships** | Types of outgoing relationships, including labels of connected nodes | 

---

# 📊 Extract Neo4j Data to Excel Script

This Python script connects to a Neo4j database to retrieve information about all **node labels**, their **unique properties**, and **relationships** (incoming and outgoing). The extracted data is then saved into an organized **Excel file**, with each label’s data structured on separate sheets for easy analysis and documentation.

---

## Overview

This script performs the following tasks to capture the database structure:

- **Retrieve Labels**: Extracts all unique labels (types of nodes) from the Neo4j database.
- **Extract Properties**: Lists distinct properties associated with each label.
- **Get Relationships**: Captures all relationships (incoming and outgoing) for each label, including the type of relationship and the labels of connected nodes.

**The data is organized in an Excel file**, with each label’s data on a separate sheet containing the following columns:

| Column                  | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Label**               | The node label in Neo4j                                                    |
| **Property**            | Each unique property associated with the label                             |
| **All Relationships**   | Combined list of all incoming and outgoing relationships                   |
| **Incoming Relationships** | Types of incoming relationships, including connected node labels      |
| **Outgoing Relationships** | Types of outgoing relationships, including connected node labels      | 

---

# 🔍 Neo4j Data Extraction and Visualization

This project uses the Neo4j Python driver to connect to a Neo4j database, extract label, property, and relationship information, and visualize the data in directed network graphs.

## Features

### 1. Connect to a Neo4j Database
- Utilizes the Neo4j Python driver to establish a connection with a Neo4j database.
- Requires a URI, username, and password for authentication.

### 2. Retrieve Data from Neo4j
- **Label Extraction**: Collects information on each unique label (node type) in the Neo4j database.
- **Property Extraction**: For each label, retrieves all unique properties associated with that label.
- **Relationship Extraction**:
  - Fetches both incoming and outgoing relationships for each label.
  - Each relationship includes:
    - Type of relationship.
    - The label(s) of the connected node(s).

### 3. Organize and Structure the Data
- Data is organized into a structured list where each entry contains:
  - The label name.
  - A list of properties associated with the label.
  - A combined list of incoming and outgoing relationships.
  - Separate lists of incoming and outgoing relationships.
- This structured data is then transformed into a DataFrame to simulate the structure of a CSV file.

### 4. Visualize Relationships in Network Graphs
- For each label, a directed network graph is created using NetworkX.
- **Nodes**: Represent labels.
- **Edges**: Represent relationships between labels.
- **Directionality**: Relationships are displayed with directed arrows indicating the direction (incoming or outgoing) relative to the label.
- Each graph is saved as an image in a specified output directory.
