import logging
import re
from urllib.parse import urlparse

from pyframelessutils.token_utilities import token_parser


def tenant_extractor(origin: str, default_tenant: str = "public"):
    """
    Function to extract tenant from Origin/Header or assign default
    :param origin: origin value
    :param default_tenant: default tenant value
    :return:
    """

    subdomain = default_tenant

    request_hostname = urlparse(origin).hostname
    if (
        isinstance(origin, str)
        and request_hostname
        and len(request_hostname.split(".")) == 3
    ):
        logging.info("Origin: %s", request_hostname)
        # When origin is IP, it equals to 4 (e.g. 127.0.0.1).
        # It equals to 3 when origin is correct, (e.g. test.worksdone.io)
        subdomain = request_hostname.split(".")[0]
    logging.info("Tenant selected: %s", subdomain)
    return subdomain
