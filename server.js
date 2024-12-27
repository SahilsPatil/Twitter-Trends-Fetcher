const express = require('express');
const mongoose = require('mongoose');
const { spawn } = require('child_process');

const app = express();
app.use(express.json());
app.use(express.static('public'));

// MongoDB Connection
const MONGO_URI = 'mongodb://localhost:27017/twitter_trends';
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });

const trendSchema = new mongoose.Schema({
    _id: String,
    trends: [String],
    timestamp: String,
    ip_address: String,
});

const Trend = mongoose.model('Trend', trendSchema);

// API to Run Selenium Script
app.post('/run-script', async (req, res) => {
    const seleniumProcess = spawn('python', ['python/main.py']);
    seleniumProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    seleniumProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    seleniumProcess.on('error', (error) => {
        console.error(`Error spawning Selenium script: ${error.message}`);
        res.status(500).json({ success: false, message: 'Failed to start Selenium script' });
    });

    seleniumProcess.on('close', async (code) => {
        if (code === 0) {
            const latestTrend = await Trend.findOne().sort({ timestamp: -1 });
            res.json({ success: true, data: latestTrend });
        } else {
            res.status(500).json({ success: false, message: 'Failed to execute Selenium script' });
        }
    });
});
app.get('/get-latest-data', async (req, res) => {
    try {
        const latestTrend = await Trend.findOne().sort({ timestamp: -1 });
        if (latestTrend) {
            res.json(latestTrend);
        } else {
            res.status(404).json({ success: false, message: 'No data found' });
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        res.status(500).json({ success: false, message: 'Internal Server Error' });
    }
});



const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
