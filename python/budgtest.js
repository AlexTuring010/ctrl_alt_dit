const { exec } = require('child_process');

const customerId = 4009; // Replace with the actual customer ID

exec(`python3 /home/alexturing/Desktop/ctrl_alt_dit/python/budgtest.py ${customerId}`, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing Python script: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Python script error: ${stderr}`);
        return;
    }
    console.log(`Predicted weekly budget: ${stdout.trim()}`);
});