import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import cookieParser from 'cookie-parser';
import session from 'express-session';
import { fileHandler } from './handlers/file';
import { previewHandler } from './handlers/preview';
import { proxyHandler } from './handlers/proxy';
import { templateHandler } from './handlers/template';
import { staticMiddleware } from './middleware/static';
import { authMiddleware } from './middleware/auth';

const app = express();

// VULNERABILITY: CORS allows all origins
app.use(cors({
    origin: '*',
    credentials: true
}));

app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

// VULNERABILITY: Weak session configuration
app.use(session({
    secret: 'keyboard-cat-weak-secret',
    resave: false,
    saveUninitialized: true,
    cookie: {
        secure: false, // VULNERABILITY: Not using secure cookies
        httpOnly: false, // VULNERABILITY: Not using httpOnly
        sameSite: 'none' as const // VULNERABILITY: SameSite none without secure
    }
}));

// Routes
app.use('/api/files', fileHandler);
app.use('/api/preview', previewHandler);
app.use('/api/proxy', proxyHandler);
app.use('/api/template', templateHandler);
app.use('/static', staticMiddleware);

// VULNERABILITY: Error handler exposes stack traces
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
    console.error(err.stack);
    res.status(500).json({
        error: err.message,
        stack: err.stack // VULNERABILITY: Stack trace exposure
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`API Gateway running on port ${PORT}`);
});

export default app;
