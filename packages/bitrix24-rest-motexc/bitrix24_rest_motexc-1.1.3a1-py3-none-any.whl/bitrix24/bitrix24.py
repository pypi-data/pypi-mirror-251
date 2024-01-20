# -*- coding: utf-8 -*-

"""
Bitrix24
~~~~~~~~~~~~

This module implements the Bitrix24 REST API.

:copyright: (c) 2019 by Akop Kesheshyan.

"""
import warnings

import requests
from time import sleep
from urllib.parse import urlparse
from .exceptions import BitrixError


class Bitrix24(object):
    """A user-created :class:`Bitrix24 <Bitrix24>` object.
    Used to sent to the server.

    :param domain: REST call domain, including account name, user ID and secret code.
    :param timeout: (Optional) waiting for a response after a given number of seconds.
    Usage::
      >>> from bitrix24 import Bitrix24
      >>> bx24 = Bitrix24('https://example.bitrix24.com/rest/1/33olqeits4avuyqu')
      >>> bx24.callMethod('crm.product.list')
    """

    def __init__(self, domain, timeout=60, safe=True):
        """Create Bitrix24 API object
        :param domain: str Bitrix24 webhook domain
        :param timeout: int Timeout for API request in seconds
        """
        self.domain = self._prepare_domain(domain)
        self.timeout = timeout
        self.safe = safe

    def _prepare_domain(self, domain):
        """Normalize user passed domain to a valid one."""
        if domain == '' or not isinstance(domain, str):
            raise Exception('Empty domain')

        o = urlparse(domain)
        user_id, code = o.path.split('/')[2:4]
        return "{0}://{1}/rest/{2}/{3}".format(o.scheme, o.netloc, user_id, code)

    def _prepare_params(self, params, prev=''):
        """Transforms list of params to a valid bitrix array."""
        ret = ''
        if isinstance(params, dict):
            for key, value in params.items():
                if isinstance(value, dict):
                    if prev:
                        key = "{0}[{1}]".format(prev, key)
                    ret += self._prepare_params(value, key)
                elif (isinstance(value, list) or isinstance(value, tuple)) and len(value) > 0:
                    for offset, val in enumerate(value):
                        if isinstance(val, dict):
                            ret += self._prepare_params(
                                val, "{0}[{1}][{2}]".format(prev, key, offset))
                        else:
                            if prev:
                                ret += "{0}[{1}][{2}]={3}&".format(
                                    prev, key, offset, val)
                            else:
                                ret += "{0}[{1}]={2}&".format(key, offset, val)
                else:
                    if prev:
                        ret += "{0}[{1}]={2}&".format(prev, key, value)
                    else:
                        ret += "{0}={1}&".format(key, value)
        return ret

    def callMethod(self, method, **params):
        """Calls a REST method with specified parameters.

       :param url: REST method name.
       :param \*\*params: Optional arguments which will be converted to a POST request string.
       :return: Returning the REST method response as an array, an object or a scalar
       """

        try:
            url = '{0}/{1}.json'.format(self.domain, method)

            param = self._prepare_params(params)
            answer = ''

            if method.rsplit('.', 1)[1] in ['add', 'update', 'delete', 'set', 'addfile']:
                request = requests.post(url, data=param, timeout=self.timeout, verify=self.safe).json()
            else:
                request = requests.get(url, params=param, timeout=self.timeout, verify=self.safe)
                try:
                    answer = request.json()
                except requests.exceptions.JSONDecodeError as e:
                    warnings.warn("bitrix24: JSON decode error...")
                    if answer.status_code == 403:
                        warnings.warn(f"bitrix24: Forbidden: {method}. Check your bitrix24 webhook settings. Returning None! ")
                        return None
                    elif answer.ok:
                        return answer.content



        except ValueError:
            if answer['error'] not in 'QUERY_LIMIT_EXCEEDED':
                raise BitrixError(answer)
            # Looks like we need to wait until expires limitation time by Bitrix24 API
            sleep(2)
            return self.callMethod(method, **params)

        if 'error' in answer:
            raise BitrixError(answer)
        if 'start' not in params:
            params['start'] = 0
        if 'next' in answer and answer['total'] > params['start']:
            params['start'] += 50
            data = self.callMethod(method, **params)
            if isinstance(answer['result'], dict):
                result = answer['result'].copy()
                result.update(data)
            else:
                result = answer['result'] + data
            return result
        return answer['result']
