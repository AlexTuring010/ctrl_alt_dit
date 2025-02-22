// netlify/functions/call-python.js

exports.handler = async (event, context) => {
    try {
      // Step 1: Parse the input from the request (it'll be JSON from the phone app)
      const { inputData } = JSON.parse(event.body);
      
      // Step 2: Return a simple mock response without calling Python
      const responseData = {
        originalData: inputData,
        modifiedData: `${inputData} has been modified!` // Just a simple transformation for testing
      };
  
      return {
        statusCode: 200,
        body: JSON.stringify(responseData),
      };
    } catch (error) {
      console.error("Error:", error);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'An error occurred during processing.' }),
      };
    }
  };
  