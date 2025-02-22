const express = require('express');
const predictBudgetHandler = require('./javascript/predict_budget');

const app = express();

app.get('/predict_budget', async (req, res) => {
    const event = {
        queryStringParameters: {
            customer_id: req.query.customer_id
        }
    };

    const context = {};

    const response = await predictBudgetHandler.handler(event, context);

    res.status(response.statusCode).json(JSON.parse(response.body));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});