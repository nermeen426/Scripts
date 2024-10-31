# 📝 Neo4j Export Labels, Properties, and Relationships Script

This Python script connects to a Neo4j database and efficiently extracts information about all **node labels**, their **properties**, and **relationships**. This data is saved to a **CSV file** for easy access and further analysis.

---

## Overview

This script extracts the following details from a Neo4j database:

- **Labels**: All unique node labels in the database.
- **Properties**: Distinct properties associated with each label.
- **Relationships**: Both incoming and outgoing relationships for each label, including relationship types and connected node labels.

The data is then structured in a CSV file with the following columns:

| Column                 | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Label**              | The node label in Neo4j                                                    |
| **Properties**         | List of properties associated with each label                              |
| **Relationships**      | List of all relationships for each label                                   |
| **Incoming Relationships** | Types of incoming relationships, including labels of connected nodes |
| **Outgoing Relationships** | Types of outgoing relationships, including labels of connected nodes |

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
