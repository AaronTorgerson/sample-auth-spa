from django.http import JsonResponse

from api.access import requires_scope


@requires_scope('openid')
def get_stocks(request):
    stocks = [
        {"ticker": "UPST", "name": "Upstart Holdings, Inc."},
        {"ticker": "DOCN", "name": "DigitalOcean"},
        {"ticker": "SNOW", "name": "Snowflake"},
        {"ticker": "NET", "name": "Cloudflare, Inc."},
        {"ticker": "SHOP", "name": "Shopify"}
    ]

    return JsonResponse(stocks, safe=False)
