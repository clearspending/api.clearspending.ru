# -*- coding: utf-8 -*-

APIdict = {}

from api.snippets import booleaniator, dbid, yearfilter, asIs, dateRange, floatRange, toListAnd, toListOr, toList, \
    is_guid, placingtype, mongo_id, unicode_whitespace, okdp_okpd, less_int

# используется для фильтрации входящих параметров
notUseParameterVal = {u'None', u'all', None, 'None', 'all', "", u""}
operatorsDontModify = {u"$all", u"$in", u"$or", u"$gte", u"$gt", u"$lte", u"$lt"}
share_parameters = {u"format", u"get_report"}

# словарь функций преобразования входящих из апи параметров
typeFunctions = {
    "mongo_id": mongo_id,
    "unicode": unicode,
    "unicode_whitespace": unicode_whitespace,
    "integer": int,
    "float": float,
    "string": str,
    "boolean": booleaniator,
    "dbid": dbid,
    "yearfilter": yearfilter,
    "asIs": asIs,
    "daterange": dateRange,
    "floatrange": floatRange,
    "listand": toListAnd,
    "listor": toListOr,
    "list": toList,
    "placingtype": placingtype,
    "guid": is_guid,
    "okdp_okpd": okdp_okpd,
    "less_int": less_int
}

from api.db_selectors import underConstruction, sphnxSelect, selectData, get_data, selectDict, select_budget_dict
from api.response_modifiers import modifier_select_rsp_dictionaries, modifier_select_rsp_suppliers, \
    modifier_select_rsp_customers, modifier_top_rsp_contracts, modifier_top_rsp_organizations, \
    modifier_get_rsp, modifier_select_rsp_contracts, modifier_select_rsp_invalidcontracts, \
    modifier_get_grants_rsp, modifier_select_rsp_grants, modifier_top_rsp_grants, modifier_top_rsp_farma, \
    modifier_get_notifications_rsp, modifier_select_rsp_notifications, modifier_top_rsp_notifications

APIdict[u"search"] = {
    u"contracts": {"function": underConstruction},
    u"suppliers": {"function": underConstruction},
    u"customers": {"function": underConstruction}
}

APIdict[u"request"] = {
    "stats": {"function": underConstruction}
}

APIdict[u"search"] = {
    u"notifications": {
        "function": sphnxSelect,
        "modifier": modifier_select_rsp_notifications,
        "description": {"DB_Name": "Notifications", "DB_collectionName": "Notifications"},
        "parameters": {
            "productsearch": {"field": u"sphnxsearch", "type": "unicode", "default": None,
                              "sphinx_field": "productsearch"},
            "placing": {"field": u"sphnxsearchlist", "type": "list", "default": None, "sphinx_field": "placingway"},

            "number": {"field": u"number", "type": "unicode", "default": None},
            "pricerange": {"field": u"lot.maxPrice", "type": "floatrange",
                           "default": None},
            "publish_daterange": {"field": u"publishDate", "type": "daterange", "default": None},
            "participate_daterange": {"field": u"collectingDate.procedureInfo.collecting.endDate", "type": "daterange",
                                      "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
        },
        "sort": {
            "lot.maxPrice": [1, -1],
            "publishDate": [1, -1],
            "collectingDate.procedureInfo.collecting.endDate": [1, -1]
        }
    },
    u"grants": {
        "function": sphnxSelect,
        "modifier": modifier_select_rsp_grants,
        "description": {"DB_Name": "Grants", "DB_collectionName": "grants"},
        "parameters": {
            "productsearch": {"field": u"sphnxsearch", "type": "unicode", "default": None,
                              "sphinx_field": "description"},
            "name_organization_search": {"field": u"sphnxsearch", "type": "unicode", "default": None,
                                         "sphinx_field": "name_organization_search"},
            "address_search": {"field": u"sphnxsearch", "type": "unicode", "default": None,
                               "sphinx_field": "address_search"},

            "operator": {"field": u"operator", "type": "unicode_whitespace", "default": None},
            "daterange": {"field": u"filing_date", "type": "daterange", "default": None},
            "OGRN": {"field": u"OGRN", "type": "unicode", "default": None},
            "price": {"field": u"price", "type": "floatrange", "default": None},
            "grant_status": {"field": u"grant_status", "type": "unicode", "default": None},
        },
    },

    u"customers": {
        "function": sphnxSelect,
        "modifier": modifier_select_rsp_customers,
        "description": {"DB_Name": "Organizations", "DB_collectionName": "Customers_v3"},
        "parameters": {
            "namesearch": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "names"},
            "address": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "address"},

            "namesearchlist": {"field": u"sphnxsearchlist", "type": "list", "default": None, "sphinx_field": "names"},

            "spzregnum": {"field": u"regNumber", "type": "unicode", "default": None},
            "okpo": {"field": u"OKPO", "type": "unicode", "default": None},
            "okved": {"field": u"OKVED", "type": "unicode", "default": None},
            "name": {"field": u"fullName", "type": "unicode", "default": None},
            "inn": {"field": u"inn", "type": "unicode", "default": None},
            "kpp": {"field": u"kpp", "type": "unicode", "default": None},
            "ogrn": {"field": u"ogrn", "type": "unicode", "default": None},
            "okogu": {"field": u"okogu.code", "type": "unicode", "default": None},
            "okato": {"field": u"factualAddress.OKATO", "type": "unicode", "default": None},
            "subordination": {"field": u"subordinationType.id", "type": "unicode", "default": None},
            "orgtype": {"field": u"organizationType.id", "type": "unicode", "default": None},
            "kladregion": {"field": u"region.kladrCode", "type": "unicode", "default": None},
            "fz": {"field": u"fz", "type": "unicode", "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
            "orgclass": {"field": u"_orgClass", "type": "unicode", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"suppliers": {
        "function": sphnxSelect,
        "modifier": modifier_select_rsp_suppliers,
        "description": {"DB_Name": "Organizations", "DB_collectionName": "Suppliers_v3"},
        "parameters": {
            "namesearch": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "names"},
            "address": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "address"},

            "inn": {"field": u"inn", "type": "unicode", "default": None},
            "kpp": {"field": u"kpp", "type": "unicode", "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
            "orgform": {"field": u"organizationForm", "type": "unicode", "default": None},
            "orgclass": {"field": u"_orgClass", "type": "unicode", "default": None},
            "inblacklist": {"field": u"xRNP.inRNP", "type": "boolean", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"contracts": {
        "function": sphnxSelect,
        "modifier": modifier_select_rsp_contracts,
        "description": {"DB_Name": "Contracts", "DB_collectionName": "Contracts4API_v3"},
        "parameters": {
            "productsearch": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "products"},
            "address": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "address"},
            "misuses": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "misuses"},

            "placing": {"field": u"sphnxsearchlist", "type": "list", "default": None, "sphinx_field": "placingway"},
            "productsearchlist": {"field": u"sphnxsearchlist", "type": "list", "default": None,
                                  "sphinx_field": "products"},

            "regnum": {"field": u"regNum", "type": "unicode", "default": None},
            "customerinn": {"field": u"customer.inn", "type": "unicode", "default": None},
            "customerkpp": {"field": u"customer.kpp", "type": "unicode", "default": None},
            "supplierinn": {"field": u"suppliers.inn", "type": "unicode", "default": None,
                            "sphinx_field": "supplierinn_list"},
            "supplierkpp": {"field": u"suppliers.kpp", "type": "unicode", "default": None,
                            "sphinx_field": "supplierkpp_list"},
            "okdp_okpd": {"field": u"okdp_okpd", "type": "okdp_okpd", "default": None,
                          "sphinx_field": "okdp_okpd_list"},
            "budgetlevel": {"field": u"finances.budgetLevel.code", "type": "unicode", "default": None},
            "grbs": {"field": u"finances.budgetary.KBK", "type": "unicode", "default": None},
            "fkr": {"field": u"finances.budgetary.KBK", "type": "unicode", "default": None},
            "sub-fkr": {"field": u"sub_fkr", "type": "unicode", "default": None},
            "csr": {"field": u"finances.budgetary.KBK", "type": "unicode", "default": None},
            "kvr": {"field": u"finances.budgetary.KBK", "type": "unicode", "default": None},
            "customerregion": {"field": u"regionCode", "type": "unicode", "default": None},
            "currentstage": {"field": u"currentContractStage", "type": "unicode", "default": None},
            "daterange": {"field": u"signDate", "type": "daterange", "default": None},
            "pricerange": {"field": u"price", "type": "floatrange", "default": None},
            "fz": {"field": u"fz", "type": "unicode", "default": None}
        },
        "sort": {
            "price": [1, -1],
            "signDate": [1, -1]
        }
    }
}

APIdict[u"top"] = {
    u"notifications": {
        "function": selectData,
        "modifier": modifier_top_rsp_notifications,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statName": {"field": u"statName", "type": "unicode", "default": u'topNotifications'},
            'fz': {'field': u'fz', "type": "unicode", "default": None}
        },
        "sort": {
            "price": [1, -1],
        }
    },

    u"grants": {
        "function": selectData,
        "modifier": modifier_top_rsp_grants,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        # TODO: нельзя не указывать параметр selectData отдаёт None
        "parameters": {
            "statName": {"field": u"statName", "type": "unicode", "default": u'topGrants'},
            'grant_status': {'field': u'grant_status', "type": "unicode", "default": None}
        },
        "sort": {
            "price": [1, -1],
        }
    },
    u"contracts": {
        "function": selectData,
        "modifier": modifier_top_rsp_contracts,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statname": {"field": u"statName", "type": "unicode", "default": u"topContracts"},
            "year": {"field": u"year", "type": "unicode", "default": None}
        },
        "sort": {
            "price": [1, -1],
            "signDate": [1, -1]
        }
    },
    u"suppliers": {
        "function": selectData,
        "modifier": modifier_top_rsp_organizations,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statname": {"field": u"statName", "type": "unicode", "default": u"topSuppliers"},
            "stattype": {"field": u"statType", "type": "unicode", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"customers": {
        "function": selectData,
        "modifier": modifier_top_rsp_organizations,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statname": {"field": u"statName", "type": "unicode", "default": u"topCustomers"},
            "stattype": {"field": u"statType", "type": "unicode", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"npo": {
        "function": selectData,
        "modifier": modifier_top_rsp_organizations,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statname": {"field": u"statName", "type": "unicode", "default": u"topNPO"},
            "stattype": {"field": u"statType", "type": "unicode", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"farma": {
        "function": selectData,
        "modifier": modifier_top_rsp_farma,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statname": {"field": u"statName", "type": "unicode", "default": u"topFarma"},
            "stattype": {"field": u"statType", "type": "unicode", "default": None}
        }
    },
    u"univers": {
        "function": selectData,
        "modifier": modifier_top_rsp_organizations,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "Statistics_v3"},
        "parameters": {
            "statname": {"field": u"statName", "type": "unicode", "default": u"topUniversities"},
            "stattype": {"field": u"statType", "type": "unicode", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    }
}

APIdict[u"get"] = {
    u"notifications": {
        "function": get_data,
        "modifier": modifier_get_notifications_rsp,
        "description": {"DB_Name": "Notifications", "DB_collectionName": "Notifications"},
        "parameters": {
            "number": {"field": u"number", "type": "unicode", "default": None},
            "id": {"field": u"id", "type": "unicode", "default": None}
        }
    },
    u"grants": {
        "function": get_data,
        "modifier": modifier_get_grants_rsp,
        "description": {"DB_Name": "Grants", "DB_collectionName": "grants"},
        "parameters": {
            "id": {"field": u"id", "type": "integer", "default": None}
        }
    },
    u"contracts": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Contracts", "DB_collectionName": "Contracts4API_v3"},
        "parameters": {
            # "newestver": {"field": u"_newestVersion", "type": "boolean", "default": True},
            "regnum": {"field": u"regNum", "type": "unicode", "default": None},
            "id": {"field": u"id", "type": "guid", "default": None}
        }
    },
    u"suppliers": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Organizations", "DB_collectionName": "Suppliers_v3"},
        "parameters": {
            "id": {"field": u"_id", "type": "dbid", "default": None},
            "inn": {"field": u"inn", "type": "unicode", "default": None},
            "kpp": {"field": u"kpp", "type": "unicode", "default": None}
        }
    },
    u"customers": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Organizations", "DB_collectionName": "Customers_v3"},
        "parameters": {
            "id": {"field": u"_id", "type": "dbid", "default": None},
            "spzregnum": {"field": u"regNumber", "type": "unicode", "default": None}
        }
    },
    u"dicts": {
        "function": underConstruction
    },
    u"regions": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "Regions"},
        "parameters": {
            "regioncode": {"field": u"subjectCode", "type": "integer", "default": None},
            "okato": {"field": u"codeOKATO", "type": "integer", "default": None},
            "kladr": {"field": u"codeKLADR", "type": "integer", "default": None}
        }
    },
    u"budgetlevels": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "BudgetLevels"},
        "parameters": {
            "level": {"field": u"budgetLevelCode", "type": "unicode", "default": None}
        }
    },
    u"opf": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "OPF"},
        "parameters": {
            "opf": {"field": u"opf", "type": "unicode", "default": None}
        }
    },
    u"kbk": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "kbk"},
        "parameters": {
            "actual": {"field": u"actual", "type": "unucode", "default": u"true"},
            "kbk": {"field": u"kbk", "type": "unicode", "default": None},
            "budget": {"field": u"budget", "type": "unicode", "default": None}
        }
    },
    u"kosgu": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "kosgu"},
        "parameters": {
            "actual": {"field": u"actual", "type": "unucode", "default": u"true"},
            "kosgu": {"field": u"kbk", "type": "unicode", "default": None}
        }
    },
    u"invalidreasons": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "InvalidReasons"},
        "parameters": {
            "code": {"field": u"code", "type": "unicode", "default": None}
        }
    },
    u"placing": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "Placing"},
        "parameters": {
            "code": {"field": u"code", "type": "unicode", "default": None}
        }
    },
    u"okato": {
        "function": get_data,
        "modifier": modifier_get_rsp,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "okato"},
        "parameters": {
            "code": {"field": u"code", "type": "unicode", "default": None},
        }
    }
}

APIdict[u"select"] = {
    u"notifications": {
        "function": sphnxSelect,
        "modifier": modifier_select_rsp_notifications,
        "description": {"DB_Name": "Notifications", "DB_collectionName": "Notifications"},
        "parameters": {
            "productsearch": {"field": u"sphnxsearch", "type": "unicode", "default": None, "sphinx_field": "product"},
            "placing": {"field": u"sphnxsearchlist", "type": "list", "default": None, "sphinx_field": "placingway"},

            "number": {"field": u"number", "type": "unicode", "default": None},
            "pricerange": {"field": u"lots.lot.customerRequirements.customerRequirement.maxPrice", "type": "floatrange",
                           "default": None},
            "publish_daterange": {"field": u"publishDate", "type": "daterange", "default": None},
            "participate_daterange": {"field": u"notificationCommission.p1Date", "type": "daterange", "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
            "fz": {"field": u"fz", "type": "unicode", "default": None},

        },
        "sort": {
            "publish_daterange": [1, -1]
        }
    },

    u"grants": {
        "function": selectData,
        "modifier": modifier_select_rsp_grants,
        "description": {"DB_Name": "Grants", "DB_collectionName": "grants"},
        "parameters": {
            "year": {"field": u"year", "type": "unicode", "default": None},
            "status": {"field": u"grant_status", "type": "unicode", "default": None},
            "grant": {"field": u"grant", "type": "unicode", "default": None},
            "price": {"field": u"price", "type": "floatrange", "default": None},
            "daterange": {"field": u"filing_date", "type": "daterange", "default": None},

        },
    },
    u"contracts": {
        "function": selectData,
        "modifier": modifier_select_rsp_contracts,
        "description": {"DB_Name": "Contracts", "DB_collectionName": "Contracts4API_v3"},
        "parameters": {
            "regnum": {"field": u"regNum", "type": "unicode", "default": None},
            "customerinn": {"field": u"customer.inn", "type": "unicode", "default": None},
            "customerkpp": {"field": u"customer.kpp", "type": "unicode", "default": None},
            "supplierinn": {"field": u"suppliers.inn", "type": "unicode", "default": None},
            "supplierkpp": {"field": u"suppliers.kpp", "type": "unicode", "default": None},
            "okpd": {"field": u"products.OKPD.code", "type": "unicode", "default": None},
            "okdp": {"field": u"products.OKDP.code", "type": "unicode", "default": None},
            "budgetlevel": {"field": u"finances.budgetLevel.code", "type": "unicode", "default": None},
            "customerregion": {"field": u"regionCode", "type": "unicode", "default": None},
            "industrial": {"field": u"economic_sectors.code", "type": "unicode", "default": None},
            "currentstage": {"field": u"currentContractStage", "type": "unicode", "default": None},
            "daterange": {"field": u"signDate", "type": "daterange", "default": None},

            "placing": {"field": u"placingWayCode", "type": "placingtype", "default": None},
            "pricerange": {"field": u"price", "type": "floatrange", "default": None},
            "fz": {"field": u"fz", "type": "unicode", "default": None},
        },
        "sort": {
            "price": [1, -1],
            "signDate": [1, -1]
        }
    },
    u"invalidcontracts": {
        "function": selectData,
        "modifier": modifier_select_rsp_invalidcontracts,
        "description": {"DB_Name": "Contracts", "DB_collectionName": "ContractsInnKppAnalytics_v3"},
        "parameters": {
            "valid": {"field": u"_valid", "type": "boolean", "default": False},
            "regnum": {"field": u"regNum", "type": "unicode", "default": None},
            "customerinn": {"field": u"customer.inn", "type": "unicode", "default": None},
            "customerkpp": {"field": u"customer.kpp", "type": "unicode", "default": None},
            "supplierinn": {"field": u"suppliers.inn", "type": "unicode", "default": None},
            "supplierkpp": {"field": u"suppliers.kpp", "type": "unicode", "default": None},
            "customerregion": {"field": u"regionCode", "type": "unicode", "default": None},
            "reasonslistand": {"field": u"_invalidReasonList", "type": "listand", "default": None},
            "reasonslistor": {"field": u"_invalidReasonList", "type": "listor", "default": None}
        },
        "sort": {
            "price": [1, -1],
            "signDate": [1, -1]
        }
    },
    u"suppliers": {
        "function": selectData,
        "modifier": modifier_select_rsp_suppliers,
        "description": {"DB_Name": "Organizations", "DB_collectionName": "Suppliers_v3"},
        "parameters": {
            "inn": {"field": u"inn", "type": "unicode", "default": None},
            "kpp": {"field": u"kpp", "type": "unicode", "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
            "orgform": {"field": u"organizationForm", "type": "unicode", "default": None},
            "orgclass": {"field": u"_orgClass", "type": "unicode", "default": None},
            "inblacklist": {"field": u"xRNP.inRNP", "type": "boolean", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"customers": {
        "function": selectData,
        "modifier": modifier_select_rsp_customers,
        "description": {"DB_Name": "Organizations", "DB_collectionName": "Customers_v3"},
        "parameters": {
            "spzregnum": {"field": u"regNumber", "type": "unicode", "default": None},
            "okpo": {"field": u"OKPO", "type": "unicode", "default": None},
            "okved": {"field": u"OKVED", "type": "unicode", "default": None},
            "name": {"field": u"fullName", "type": "unicode", "default": None},
            "inn": {"field": u"inn", "type": "unicode", "default": None},
            "kpp": {"field": u"kpp", "type": "unicode", "default": None},
            "ogrn": {"field": u"ogrn", "type": "unicode", "default": None},
            "okogu": {"field": u"okogu.code", "type": "unicode", "default": None},
            "okato": {"field": u"factualAddress.OKATO", "type": "unicode", "default": None},
            "subordination": {"field": u"subordinationType.id", "type": "unicode", "default": None},
            "orgtype": {"field": u"organizationType.id", "type": "unicode", "default": None},
            "kladregion": {"field": u"factualAddress.region.kladrCode", "type": "unicode", "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
            "orgclass": {"field": u"_orgClass", "type": "unicode", "default": None}
        },
        "sort": {
            "contractsCount": [1, -1],
            "contractsSum": [1, -1]
        }
    },
    u"dicts": {"function": underConstruction},
    u"regions": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "Regions"},
        "parameters": {
            # "name": {"field": u"name", "type": "unicode", "default": None},
            "regioncode": {"field": u"subjectCode", "type": "integer", "default": None},
            "okato": {"field": u"codeOKATO", "type": "integer", "default": None},
            "kladr": {"field": u"codeKLADR", "type": "integer", "default": None}
        }
    },
    u"budgetlevels": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "BudgetLevels"},
        "parameters": {
            "level": {"field": u"budgetLevelCode", "type": "unicode", "default": None}
        }
    },
    u"opf": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "OPF"},
        "parameters": {
            "opf": {"field": u"opf", "type": "unicode", "default": None}
        }
    },
    u"kbk": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "kbk"},
        "parameters": {
            "actual": {"field": u"actual", "type": "unucode", "default": u"true"},
            "kbk": {"field": u"kbk", "type": "unicode", "default": None},
            "budget": {"field": u"budget", "type": "unicode", "default": None}
        }
    },
    u"kosgu": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "kosgu"},
        "parameters": {
            "actual": {"field": u"actual", "type": "unucode", "default": u"true"},
            "kosgu": {"field": u"code", "type": "unicode", "default": None}
        }
    },
    u"invalidreasons": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "InvalidReasons"},
        "parameters": {
            "code": {"field": u"code", "type": "unicode", "default": None}
        }
    },
    u"orgtype": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "OrgType"},
        "parameters": {
            "code": {"field": u"code", "type": "unicode", "default": None}
        }
    },
    u"okato": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "okato"},
        "parameters": {
            "code": {"field": u"code", "type": "unicode", "default": None},
            "parentcode": {"field": u"parent", "type": "unicode", "default": None},
            "level": {"field": u"level", "type": "integer", "default": None}
        }
    }
}

APIdict[u"dictionaries"] = {
    u"budget": {
        "function": select_budget_dict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Dictionaries", "DB_collectionName": "Budget"},
        "parameters": {
            "grbs": {"field": u"chief_steward", "type": "unicode", "default": None},
            "fkr": {"field": u"section", "type": "unicode", "default": None},
            "sub-fkr": {"field": u"subsection", "type": "unicode", "default": None},
            "csr": {"field": u"target_article", "type": "unicode", "default": None},
            "kvr": {"field": u"type_expenditure", "type": "unicode", "default": None},
            "level": {"field": u"level", "type": "less_int", "default": None}
        }
    },
}

APIdict[u"statistics"] = {
    u"regionspending": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "RegionSpending_v3"},
        "parameters": {
            # "name": {"field": u"name", "type": "unicode", "default": None},
            "regioncode": {"field": u"regionCode", "type": "unicode", "default": None},
            "year": {"field": u"year", "type": "unicode", "default": None}
        }
    },
    u"db_info": {
        "function": selectDict,
        "modifier": modifier_select_rsp_dictionaries,
        "description": {"DB_Name": "Statistics", "DB_collectionName": "db_statistics"},
        "parameters": {
            "info": {"field": u"info", "type": "unicode", "default": None},
        }
    }
}

try:
    from common.local_query_settings import *
except ImportError:
    pass
