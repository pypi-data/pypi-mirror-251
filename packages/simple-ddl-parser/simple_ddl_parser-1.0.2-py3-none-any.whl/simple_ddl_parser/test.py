from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE tablename (
  );

CONSTRAINT fk_order FOREIGN KEY (order_identifier) REFERENCES orders(order_id)
"""
result = DDLParser(ddl).run(group_by_type=True, 
                            output_mode="mysql")

import pprint

pprint.pprint(result)