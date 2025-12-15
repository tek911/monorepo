/**
 * Mobile BFF Service
 * Contains vulnerabilities for security scanner testing.
 */
import express from 'express';
import { ApolloServer, gql } from 'apollo-server-express';
import jwt from 'jsonwebtoken';
import axios from 'axios';
import { merge } from 'lodash';

const app = express();
app.use(express.json());

// VULNERABILITY: Hardcoded secrets
const JWT_SECRET = 'mobile-bff-jwt-secret-12345';
const API_KEY = 'mobile-api-key-abc123';
const DATABASE_URL = 'mongodb://admin:password123@localhost:27017/mobile';

// VULNERABILITY: Weak JWT configuration
const jwtOptions = {
  expiresIn: '365d',  // VULNERABILITY: Token never expires effectively
  algorithm: 'HS256' as const
};

// VULNERABILITY: GraphQL schema with introspection enabled
const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    password: String!  # VULNERABILITY: Password exposed in schema
    ssn: String        # VULNERABILITY: Sensitive data exposed
    creditCard: String # VULNERABILITY: PCI data exposed
    apiKey: String     # VULNERABILITY: API key exposed
  }

  type Query {
    user(id: ID!): User
    users: [User!]!
    # VULNERABILITY: Debug query exposed
    debug: DebugInfo
  }

  type DebugInfo {
    jwtSecret: String
    databaseUrl: String
    env: String
  }

  type Mutation {
    # VULNERABILITY: No rate limiting on auth
    login(email: String!, password: String!): AuthPayload
    # VULNERABILITY: IDOR possible
    updateUser(id: ID!, data: UserInput!): User
  }

  input UserInput {
    email: String
    password: String
  }

  type AuthPayload {
    token: String!
    user: User!
  }
`;

// VULNERABILITY: Resolvers with security issues
const resolvers = {
  Query: {
    user: async (_: any, { id }: { id: string }, context: any) => {
      // VULNERABILITY: No authorization check, IDOR possible
      const user = await fetchUser(id);
      return user;
    },
    users: async () => {
      // VULNERABILITY: Returns all users including sensitive data
      return await fetchAllUsers();
    },
    debug: () => ({
      // VULNERABILITY: Exposing secrets via GraphQL
      jwtSecret: JWT_SECRET,
      databaseUrl: DATABASE_URL,
      env: JSON.stringify(process.env)
    })
  },
  Mutation: {
    login: async (_: any, { email, password }: { email: string; password: string }) => {
      // VULNERABILITY: SQL/NoSQL injection possible
      const user = await findUserByCredentials(email, password);

      // VULNERABILITY: Logging sensitive data
      console.log(`Login attempt: ${email}:${password}`);

      if (user) {
        const token = jwt.sign({ userId: user.id, email }, JWT_SECRET, jwtOptions);
        // VULNERABILITY: Token logged
        console.log(`Generated token: ${token}`);
        return { token, user };
      }
      throw new Error('Invalid credentials');
    },
    updateUser: async (_: any, { id, data }: { id: string; data: any }) => {
      // VULNERABILITY: No authorization, any user can update any other user
      // VULNERABILITY: Prototype pollution via merge
      const user = await fetchUser(id);
      const updated = merge({}, user, data);
      return updated;
    }
  }
};

// VULNERABILITY: SSRF via proxy endpoint
app.post('/api/proxy', async (req, res) => {
  const { url } = req.body;
  // VULNERABILITY: Fetching arbitrary URLs
  const response = await axios.get(url);
  res.json(response.data);
});

// VULNERABILITY: Command injection
app.get('/api/health/:service', (req, res) => {
  const { service } = req.params;
  const { exec } = require('child_process');
  // VULNERABILITY: Unvalidated input in shell command
  exec(`curl http://${service}/health`, (error: any, stdout: string) => {
    res.send(stdout);
  });
});

// VULNERABILITY: Path traversal
app.get('/api/config/:filename', (req, res) => {
  const { filename } = req.params;
  const fs = require('fs');
  // VULNERABILITY: No path validation
  const content = fs.readFileSync(`/config/${filename}`, 'utf8');
  res.send(content);
});

// VULNERABILITY: Information disclosure in errors
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  // VULNERABILITY: Full error details exposed
  res.status(500).json({
    error: err.message,
    stack: err.stack,
    env: process.env,
    secrets: { JWT_SECRET, DATABASE_URL, API_KEY }
  });
});

// Mock functions (would connect to real DB in production)
async function fetchUser(id: string) {
  return { id, email: 'user@example.com', password: 'hashed', ssn: '123-45-6789' };
}
async function fetchAllUsers() {
  return [{ id: '1', email: 'user@example.com', password: 'hashed', creditCard: '4111111111111111' }];
}
async function findUserByCredentials(email: string, password: string) {
  return { id: '1', email };
}

async function startServer() {
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    // VULNERABILITY: Introspection enabled in production
    introspection: true,
    // VULNERABILITY: Playground enabled in production
    playground: true
  });

  await server.start();
  server.applyMiddleware({ app });

  app.listen(4000, () => {
    console.log(`Mobile BFF running on port 4000`);
    console.log(`JWT Secret: ${JWT_SECRET}`);  // VULNERABILITY: Logging secret
  });
}

startServer();
