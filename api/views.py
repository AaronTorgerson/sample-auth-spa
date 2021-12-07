from django.http import JsonResponse

from api.access import requires_scope


# Using custom scopes takes some configuration in Auth0, so I'm using a built-in one for example's sake.
# All this does is check that 1) the token is valid and 2) it has the "openid" scope.
# Since Auth0 provides the "openid" scope in every token (if requested), all this does is ensure that the user is
#   authenticated. In practice, we would want to specify a scope that requires some additional authorization.
@requires_scope('openid')
def get_stocks(request, access_token):
    stocks = [
        {"ticker": "UPST", "name": "Upstart Holdings, Inc."},
        {"ticker": "DOCN", "name": "DigitalOcean"},
        {"ticker": "SNOW", "name": "Snowflake"},
        {"ticker": "NET", "name": "Cloudflare, Inc."},
        {"ticker": "SHOP", "name": "Shopify"}
    ]

    # we can also check if the member has SA!
    if 1081 in access_token.get('https://www.fool.com/accessible_services', []):
        stocks.append({"ticker": "NFLX", "name": "Netflix"})

    # we can also check if the member is level 3+!
    level = access_token.get('https://www.fool.com/highest_product_level', {}).get('ProductLevelId', 1)
    if level >= 3:
        stocks.append({"ticker": "AAPL", "name": "Apple"})

    return JsonResponse(stocks, safe=False)
