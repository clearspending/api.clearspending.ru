# coding=utf-8
import json
from datetime import datetime

from api.snippets import dthandler, delete_item_in_list, lookahead
from common.settings import MONGO_LIMIT_REPORT


def pretty_data(cursor_db, data_set_name, total, per_page, page_n,
                response_format='json', keys=None, search_data=None):
    return preparation_response(cursor_db, data_set_name, total, per_page, page_n, response_format, search_data, keys)


def get_contract_id(contract):
    if contract.get('regNum', False):
        return {'regNum': contract.get('regNum', False)}
    elif contract.get('id', False):
        return {'id': contract.get('id', False)}
    else:
        return None


def get_report(data_cursor):
    """
    Для демонстрации масштабов исследуемого сегмента рынка должны выводиться в табличной форме:
        avg_price - Размер среднего контракта,
        max_price - Размер максимального контракта,
        min_price - Размер минимального контракта,
        sum_price - Сумма всех контрактов,
        total_contracts - Количество всех контрактов за указанный период,
        Максимальный годовой объём контрактов,
        Минимальный годовой объём контрактов,

        amount_suppliers - Количество поставщиков,
        amount_customers - Количество заказчиков в указанном периоде,

        Доля контрактов сектора в общем объёме госконтрактов сферы экономики и динамика этой доли,

        regions_contracts_stat - Топ 10 регионов по объёму заключённых в сегменте контрактов,
        Топ 10 муниципальных образований по объёму заключенных в сегменте контрактов,
        period_contracts - Сумма и количество контрактов по месяцам и доля по объёму и количеству за все месяцы указанного временного интервала для выявления сезонности закупок в секторе,
        period_economic_sectors - Сумма и количество контрактов в секторе по временам года, а также доля контрактов в секторе по объёму и количеству по временам года,
        top_contracts - Топ 30 крупнейших контрактов в выборке,
        top_customers - Топ 25 заказчиков в выборке,
        top_suppliers - Топ 25 поставщиков выборке,

        local_suppliers - Доля местных (когда заказчик и поставщик зарегистрированы в одном регионе) поставщиков (по объёму) по годам.
    """
    response = {
        'avg_price': 0,
        'total_contracts': data_cursor.count(),
        'top_contracts': [],
        'period_contracts': {},
        'period_economic_sectors': {},
        'local_suppliers': {
            'bad_suppliers': 0
        }
    }

    custom_contrac_index = 0

    regions_contracts_stat = dict()
    stat_suppliers = dict()
    stat_customers = dict()

    for contract, position in lookahead(data_cursor):
        custom_contrac_index += 1

        response['avg_price'] += contract.get('price', 0)
        if position == 1:
            response['max_price'] = contract.get('price', 0)
        elif position == -1:
            response['min_price'] = contract.get('price', 0)
        if len(response['top_contracts']) < 30:
            response['top_contracts'].append(
                {
                    'price': contract.get('price', 0),
                    'id': get_contract_id(contract),
                    'name': contract.get('name', '')
                }
            )

        customer_name = u'{}_{}'.format(contract.get('customer', {}).get('inn'), contract.get('customer', {}).get('kpp'))
        if not stat_customers.get(customer_name):
            stat_customers[customer_name] = {
                'fullName': contract.get('customer', {}).get('fullName'),
                'price': 0,
                'inn': contract.get('customer', {}).get('inn'),
                'kpp': contract.get('customer', {}).get('kpp'),
                'regNum': contract.get('customer', {}).get('regNum')
            }
        stat_customers[customer_name]['price'] += contract.get('price', 0)

        if contract.get('regionCode', False):
            regions_contracts_stat[contract['regionCode']] = regions_contracts_stat.get(contract['regionCode'], 0) + contract.get('price', 0)

        for supplier in contract.get('suppliers', {}):
            supplier_name = u'{}_{}'.format(supplier.get('inn'), supplier.get('kpp'))
            if not stat_suppliers.get(supplier_name):
                stat_suppliers[supplier_name] = {
                    'organizationName': supplier.get('organizationName'),
                    'price': 0,
                    'inn': supplier.get('inn'),
                    'kpp': supplier.get('kpp'),
                }
            stat_suppliers[supplier_name]['price'] += contract.get('price', 0)

            try:
                if customer_name[:2] == supplier_name[:2]:
                    date = datetime.strptime(contract.get('publishDate', '')[:19], "%Y-%m-%dT%H:%M:%S")
                    if not date.year in response['local_suppliers']:
                        response['local_suppliers'][date.year] = {}

                    response['local_suppliers'][date.year][date.month] = response['local_suppliers'][date.year].get(date.month, 0) + 1
            except (NameError, ValueError):
                response['local_suppliers']['bad_suppliers'] += 1

        if contract.get('publishDate'):
            try:
                date = datetime.strptime(contract.get('publishDate')[:19], "%Y-%m-%dT%H:%M:%S")
                if not response['period_contracts'].get(date.year):
                    response['period_contracts'][date.year] = {}
                response['period_contracts'][date.year][date.month] = \
                    response['period_contracts'][date.year].get(date.month, 0) + contract.get('price', 0)
                if contract.get('economic_sectors'):
                    try:
                        for sector in contract.get('economic_sectors'):
                            name = sector['name'] if 'name' in sector else sector['title']

                            if not name in response['period_economic_sectors']:
                                response['period_economic_sectors'][name] = {}
                            if not response['period_economic_sectors'][name].get(date.year):
                                response['period_economic_sectors'][name][date.year] = {}
                            if not response['period_economic_sectors'][name][date.year].get(date.month):
                                response['period_economic_sectors'][name][date.year][date.month] = {'price': 0, 'amount': 0}
                            response['period_economic_sectors'][name][date.year][date.month]['price'] += contract.get('price', 0)
                            response['period_economic_sectors'][name][date.year][date.month]['amount'] += 1
                    except KeyError as e:
                        pass

            except ValueError:
                pass

    response['regions_contracts_stat'] = sorted(regions_contracts_stat.items(), key=lambda x: x[1], reverse=True)[:10]

    response['top_customers'] = sorted(stat_customers.items(), key=lambda x: x[1], reverse=True)[:25]
    response['amount_customers'] = len(stat_customers)

    response['top_suppliers'] = sorted(stat_suppliers.items(), key=lambda x: x[1], reverse=True)[:25]
    response['amount_suppliers'] = len(stat_suppliers)

    response['sum_price'] = response['avg_price']
    response['avg_price'] /= custom_contrac_index

    response['limit'] = MONGO_LIMIT_REPORT
    return format_data(response, 'report')


def preparation_response(data_cursor, data_set_name, total, per_page, page_n,
                         response_format, search_data=None, keys=None):
    """
    Makes JSON-data from MongoDB usable for REST API
    Преобразует JSON-ответ из MongoDb в формат ответа API
    """
    d = {data_set_name: {'total': total, 'perpage': per_page, 'page': page_n + 1, 'data': []}}

    if not search_data:
        for doc in data_cursor:
                try:
                    doc["mongo_id"] = str(doc.pop(u"_id"))
                except:
                    pass
                d[data_set_name]['data'].append(doc)
    else:
        doc_list = list()
        ordered_by_relevance = list()
        for doc in data_cursor:
            try:
                doc["mongo_id"] = str(doc.pop(u"_id"))
            except:
                pass
            doc[u"searchRank"] = search_data[doc["mongo_id"]]
            doc_list.append(doc)
        if doc and not keys: keys = doc.keys()
        ordered_by_relevance = sorted(doc_list, key=lambda doc: doc[u"searchRank"])
        d[data_set_name]['data'].extend(ordered_by_relevance)
    return format_data(d, data_set_name, response_format=response_format, keys=keys)


def format_data(data, data_set_name, response_format='json', keys=None, params = {}):
    """
    Returns data using specific format CSV or JSON
    Преобразует данные в указанный формат JSON или CSV
    """
    if not response_format: response_format = ''

    if u'csv' in response_format:
        response = u''
        if keys:
            delete_item_in_list(keys, 'mongo_id')
            delete_item_in_list(keys, 'searchRank')

            response += u'total:{total};perpage:{perpage};page:{page}\n'.format(**data.get(data_set_name, {}))
            response += u"{}\n".format(u";".join(keys))

            for item in data.get(data_set_name, {}).get('data', []):
                response += u"{} \n".format(u';'.join([unicode(item.get(key, u'')) for key in keys]))
            return response
        else:
            raise StandardError
    elif u'xls' in response_format:
        pass
    elif response_format == 'json':
        s = json.dumps(data, indent=4, default=dthandler)
        value = u'\n'.join([l.rstrip() for l in s.splitlines()])
        return value
    else:   # by default - return JSON data
        s = json.dumps(data, indent=4, default=dthandler)
        value = u'\n'.join([l.rstrip() for l in s.splitlines()])
        return value
