const http = require('http');
const url = require('url');
const predictBudgetHandler = require('./javascript/predict_budget');
const predictFlagHandler = require('./javascript/predict_flag');

const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    const query = parsedUrl.query;

    if (pathname === '/predict_budget' && req.method === 'GET') {
        const event = {
            queryStringParameters: {
                customer_id: query.customer_id,
                date: query.date
            }
        };

        const context = {};

        try {
            const response = await predictBudgetHandler.handler(event, context);
            res.writeHead(response.statusCode, { 'Content-Type': 'application/json' });
            res.end(response.body);
        } catch (error) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Internal Server Error' }));
        }
    } else if (pathname === '/predict_flag' && req.method === 'GET') {
        const event = {
            queryStringParameters: {
                customer_id: query.customer_id,
                date: query.date
            }
        };

        const context = {};

        try {
            const response = await predictFlagHandler.handler(event, context);
            res.writeHead(response.statusCode, { 'Content-Type': 'application/json' });
            res.end(response.body);
        } catch (error) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Internal Server Error' }));
        }
    } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not Found' }));
    }
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});