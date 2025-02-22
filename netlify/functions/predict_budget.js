const { exec } = require('child_process');
const path = require('path');

exports.handler = async (event, context) => {
    const customerId = event.queryStringParameters.customer_id;

    if (!customerId) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'customer_id query parameter is required' }),
        };
    }

    const scriptPath = path.resolve(__dirname, '../../python/budgtest.py');

    return new Promise((resolve, reject) => {
        exec(`python3 ${scriptPath} ${customerId}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing Python script: ${error.message}`);
                resolve({
                    statusCode: 500,
                    body: JSON.stringify({ error: 'Error executing Python script' }),
                });
                return;
            }
            if (stderr) {
                console.error(`Python script error: ${stderr}`);
                resolve({
                    statusCode: 500,
                    body: JSON.stringify({ error: 'Python script error' }),
                });
                return;
            }
            resolve({
                statusCode: 200,
                body: JSON.stringify({ predicted_budget: stdout.trim() }),
            });
        });
    });
};