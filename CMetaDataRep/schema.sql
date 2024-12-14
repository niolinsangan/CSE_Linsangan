-- Drop tables if they exist
DROP TABLE IF EXISTS attribute;
DROP TABLE IF EXISTS business_term_owner;
DROP TABLE IF EXISTS entity;
DROP TABLE IF EXISTS glossary_of_business_terms;
DROP TABLE IF EXISTS source_systems;
DROP TABLE IF EXISTS business_term_type;

-- Create attribute table
CREATE TABLE attribute (
    attribute_id INT PRIMARY KEY,
    attribute_name VARCHAR(255) NOT NULL,
    attribute_datatype VARCHAR(50) NOT NULL,
    attribute_description TEXT,
    typical_values TEXT,
    validation_criteria TEXT
);

-- Create business_term_owner table
CREATE TABLE business_term_owner (
    term_owner_code VARCHAR(50) PRIMARY KEY,
    term_owner_description TEXT NOT NULL
);

-- Create entity table
CREATE TABLE entity (
    entity_id INT PRIMARY KEY,
    entity_name VARCHAR(255) NOT NULL,
    entity_description TEXT
);

-- Create glossary_of_business_terms table
CREATE TABLE glossary_of_business_terms (
    business_term_short_name VARCHAR(50) PRIMARY KEY,
    date_term_defined DATE NOT NULL
);

-- Create source_systems table
CREATE TABLE source_systems (
    src_system_id INT PRIMARY KEY,
    src_system_name VARCHAR(255) NOT NULL
);

-- Create business_term_type table
CREATE TABLE business_term_type (
    term_type_code VARCHAR(50) PRIMARY KEY,
    term_type_description TEXT NOT NULL
); 