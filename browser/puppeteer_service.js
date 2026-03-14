const express = require("express");
const puppeteer = require("puppeteer");

const app = express();
app.use(express.json());

let browser;
let page;

// Start browser
async function initBrowser() {
    browser = await puppeteer.launch({
        headless: true,
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });

    page = await browser.newPage();
    console.log("Browser started");
}

// Navigate to URL
app.post("/navigate", async (req, res) => {
    try {
        const { url } = req.body;

        await page.goto(url, { waitUntil: "networkidle2" });

        res.json({ status: "ok", message: "Page loaded" });
    } catch (err) {
        res.status(500).json({ error: err.toString() });
    }
});

// Click element
app.post("/click", async (req, res) => {
    try {
        const { selector } = req.body;

        await page.click(selector);

        res.json({ status: "ok", action: "clicked", selector });
    } catch (err) {
        res.status(500).json({ error: err.toString() });
    }
});

// Type text
app.post("/type", async (req, res) => {
    try {
        const { selector, value } = req.body;

        await page.type(selector, value);

        res.json({ status: "ok", action: "typed", selector });
    } catch (err) {
        res.status(500).json({ error: err.toString() });
    }
});

// Get HTML content
app.get("/html", async (req, res) => {
    try {
        const html = await page.content();

        res.json({ html });
    } catch (err) {
        res.status(500).json({ error: err.toString() });
    }
});

// Screenshot (optional useful tool)
app.get("/screenshot", async (req, res) => {
    try {
        const screenshot = await page.screenshot({ encoding: "base64" });

        res.json({ screenshot });
    } catch (err) {
        res.status(500).json({ error: err.toString() });
    }
});

// Start service
async function start() {
    await initBrowser();

    app.listen(3000, () => {
        console.log("Puppeteer service running on port 3000");
    });
}

start();
