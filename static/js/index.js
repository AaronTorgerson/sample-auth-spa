new Vue({
    el: '#app',
    delimiters: ['{', '}'],
    data: {
        stocks: [],
        status: "ready",
        auth0: null
    },
    created: async function () {
        this.status = "authenticating...";

        this.auth0 = await createAuth0Client({
            domain: 'development.auth.fool.com',
            client_id: '0CJYkY4FfNva9Cyaz6wxZrdivAUWuol3',
            audience: 'https://www.fool.com/membership',
            scope: 'email profile openid accessible_services'
        });

        this.status = "ready";
    },
    methods: {
        getStocks: async function (event) {
            this.stocks = [];

            const accessToken = await this.auth0.getTokenSilently();

            this.status = "fetching stocks...";

            const response = await fetch('/api/stocks', {
                method: 'GET',
                headers: {
                    Authorization: 'Bearer ' + accessToken
                }
            });

            const result = await response.json();
            this.stocks = result;

            this.status = "done";
        }
    }
});

