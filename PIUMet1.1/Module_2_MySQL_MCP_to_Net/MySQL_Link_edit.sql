--this code will edit MySQL Link table
--
--By: Leila Pirhaji
----------------------------------


-- 1. removing rows with dru-drug and phenotype-phenotype links:
delete from MCP_Link where Interactor_1_type='Drug' and  Interactor_2_type='Drug' ;
delete from MCP_Link where Interactor_1_type='Clinical_Phenotype' and  Interactor_2_type='Clinical_Phenotype' ;


update MCP_Link set Confidence_Score='0' where Confidence_Score='<';