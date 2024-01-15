from typing import List

from simple_ddl_parser.utils import remove_par


class Oracle:
    def p_alter_column_modify_oracle(self, p: List) -> None:
        """alter_column_modify_oracle : alt_table MODIFY defcolumn"""
        p[0] = p[1]
        p_list = list(p)
        p[0]["columns_to_modify"] = [p_list[-1]]

    def p_encrypt(self, p: List) -> None:
        """encrypt : ENCRYPT
        | encrypt NO SALT
        | encrypt SALT
        | encrypt USING STRING
        | encrypt STRING
        """
        p_list = list(p)
        if isinstance(p[1], dict):
            p[0] = p[1]
            if "NO" in p_list:
                p[0]["encrypt"]["salt"] = False
            elif "USING" in p_list:
                p[0]["encrypt"]["encryption_algorithm"] = p_list[-1]
            elif "SALT" not in p_list:
                p[0]["encrypt"]["integrity_algorithm"] = p_list[-1]

        else:
            p[0] = {
                "encrypt": {
                    "salt": True,
                    "encryption_algorithm": "'AES192'",
                    "integrity_algorithm": "SHA-1",
                }
            }

    def p_storage(self, p: List) -> None:
        """storage : STORAGE LP
        | storage id id
        | storage id id RP
        """
        # Initial 5m Next 5m Maxextents Unlimited
        p_list = remove_par(list(p))
        param = {}
        if len(p_list) == 4:
            param = {p_list[2].lower(): p_list[3]}
        if isinstance(p_list[1], dict):
            p[0] = p[1]
        else:
            p[0] = {}
        p[0].update(param)

    def p_expr_storage(self, p: List) -> None:
        """expr : expr storage"""
        p_list = list(p)
        p[0] = p[1]
        p[0]["storage"] = p_list[-1]

    def p_expr_index(self, p: List) -> None:
        """expr : expr ID INDEX"""
        p[0] = p[1]
        p[0][f"{p[2].lower()}_index"] = True
