/**
 * Old API v1 Server
 * ABANDONED CODE - Contains numerous security vulnerabilities
 * Last maintained: 2019
 */
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const request = require('request');
const yaml = require('js-yaml');
const serialize = require('serialize-javascript');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();

// VULNERABILITY: Hardcoded credentials from 2019
const DB_URI = 'mongodb://admin:password123@localhost:27017/oldapi';
const JWT_SECRET = 'old-jwt-secret-from-2019-never-rotated';
const API_KEY = 'old-api-key-abc123-deprecated';

// VULNERABILITY: No helmet, no rate limiting
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// VULNERABILITY: Overly permissive CORS
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    next();
});

// VULNERABILITY: SQL Injection (NoSQL injection in MongoDB)
app.get('/api/v1/users', async (req, res) => {
    const query = req.query.filter;
    // Dangerous: directly using user input in query
    const users = await mongoose.connection.db.collection('users').find(JSON.parse(query));
    res.json(users);
});

// VULNERABILITY: Command injection
app.get('/api/v1/ping', (req, res) => {
    const host = req.query.host;
    // DANGEROUS: Unvalidated input in shell command
    exec(`ping -c 1 ${host}`, (error, stdout) => {
        res.send(stdout);
    });
});

// VULNERABILITY: Path traversal
app.get('/api/v1/files/:filename', (req, res) => {
    const filename = req.params.filename;
    // DANGEROUS: No path validation
    const filepath = path.join('/uploads', filename);
    res.sendFile(filepath);
});

// VULNERABILITY: Unsafe deserialization
app.post('/api/v1/config', (req, res) => {
    const configYaml = req.body.config;
    // DANGEROUS: yaml.load without safe loading
    const config = yaml.load(configYaml);
    res.json({ loaded: config });
});

// VULNERABILITY: XSS via template injection
app.get('/api/v1/greet', (req, res) => {
    const name = req.query.name;
    // DANGEROUS: Unescaped user input
    res.send(`<h1>Hello, ${name}!</h1>`);
});

// VULNERABILITY: Insecure JWT
app.post('/api/v1/login', async (req, res) => {
    const { username, password } = req.body;

    // VULNERABILITY: Weak password comparison
    if (password === 'admin') {
        const token = jwt.sign({ username, role: 'admin' }, JWT_SECRET);
        res.json({ token });
    } else {
        res.status(401).json({ error: 'Invalid' });
    }
});

// VULNERABILITY: MD5 for passwords (deprecated)
const crypto = require('crypto');
function hashPassword(password) {
    return crypto.createHash('md5').update(password).digest('hex');
}

// VULNERABILITY: Eval usage
app.post('/api/v1/calculate', (req, res) => {
    const expression = req.body.expression;
    // EXTREMELY DANGEROUS
    const result = eval(expression);
    res.json({ result });
});

// VULNERABILITY: SSRF
app.get('/api/v1/fetch', (req, res) => {
    const url = req.query.url;
    // DANGEROUS: Fetching arbitrary URLs
    request(url, (error, response, body) => {
        res.send(body);
    });
});

// VULNERABILITY: Information exposure
app.get('/api/v1/debug', (req, res) => {
    res.json({
        env: process.env,
        dbUri: DB_URI,
        jwtSecret: JWT_SECRET,
        apiKey: API_KEY
    });
});

mongoose.connect(DB_URI, { useNewUrlParser: true });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Old API v1 running on port ${PORT}`);
    console.log(`Using JWT secret: ${JWT_SECRET}`);
});
