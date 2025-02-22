// netlify/functions/call-python.js

const { exec } = require('child_process');

exports.handler = async (event, context) => {
  try {
    // Step 1: Parse the input from the request (it'll be JSON from the phone app)
    const { inputData } = JSON.parse(event.body);
    
    // Step 2: Run the Python script using Node.js child_process and pass inputData
    const command = `python3 python/modify_data.py '${inputData}'`;
    
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(error);
          reject({ statusCode: 500, body: JSON.stringify({ error: stderr }) });
        } else {
          // Step 3: Parse the result and send it back to the phone
          const result = JSON.parse(stdout);
          resolve({
            statusCode: 200,
            body: JSON.stringify({ modifiedData: result.modified_data }),
          });
        }
      });
    });
  } catch (error) {
    console.error("Error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'An error occurred during processing.' }),
    };
  }
};
