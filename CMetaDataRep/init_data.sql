-- Clear existing data
DELETE FROM attribute;
DELETE FROM business_term_owner;
DELETE FROM entity;
DELETE FROM glossary_of_business_terms;
DELETE FROM source_systems;

-- Insert sample data into attribute
INSERT INTO attribute (attribute_id, attribute_name, attribute_datatype, attribute_description, typical_values, validation_criteria) VALUES
(1, 'Customer ID', 'VARCHAR', 'Unique identifier for customers', 'CUS001, CUS002', 'Must start with CUS'),
(2, 'First Name', 'VARCHAR', 'Customer first name', 'John, Jane', 'Non-empty string'),
(3, 'Last Name', 'VARCHAR', 'Customer last name', 'Doe, Smith', 'Non-empty string'),
(4, 'Email', 'VARCHAR', 'Customer email address', 'example@email.com', 'Valid email format'),
(5, 'Phone Number', 'VARCHAR', 'Customer contact number', '+1-123-456-7890', 'Valid phone format');

-- Insert sample data into business_term_owner
INSERT INTO business_term_owner (term_owner_code, term_owner_description) VALUES
('CRM001', 'Customer Relations Manager'),
('SAL001', 'Sales Department Head'),
('MKT001', 'Marketing Team Lead'),
('SUP001', 'Support Team Manager'),
('FIN001', 'Finance Department Head');

-- Insert sample data into entity
INSERT INTO entity (entity_id, entity_name, entity_description) VALUES
(1, 'Customer', 'Core customer information'),
(2, 'Order', 'Customer order details'),
(3, 'Product', 'Product catalog information'),
(4, 'Invoice', 'Billing and payment information'),
(5, 'Support_Ticket', 'Customer support records');

-- Insert sample data into glossary_of_business_terms
INSERT INTO glossary_of_business_terms (business_term_short_name, date_term_defined) VALUES
('CUST', CURRENT_DATE),
('ORD', CURRENT_DATE),
('PROD', CURRENT_DATE),
('INV', CURRENT_DATE),
('SUPP', CURRENT_DATE);

-- Insert sample data into source_systems
INSERT INTO source_systems (src_system_id, src_system_name) VALUES
(1, 'CRM System'),
(2, 'Sales Portal'),
(3, 'Marketing Platform'),
(4, 'Support Desk'),
(5, 'Billing System'); 