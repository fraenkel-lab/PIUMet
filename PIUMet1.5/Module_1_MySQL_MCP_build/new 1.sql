Alter table MCP_Metabolites ADD COLUMN drugbank_metabolite_id TEXT, ADD COLUMN cellular_location TEXT, ADD COLUMN tissue TEXT, ADD COLUMN biofluid TEXT, ADD COLUMN biofunctions TEXT after Charge;

alter table HMDB_3_6_Metabolites_info modify column monisotopic_moleculate_weight double;


Alter table MCP_Metabolites ADD COLUMN kegg_map_id TEXT;

alter table MCP_Metabolites change Synonyms synonym text; 
alter table MCP_Metabolites change 	monisotopic_moleclar_weight monisotopic_moleculate_weight double(16,8); 