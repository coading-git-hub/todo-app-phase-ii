# Running the Next.js Frontend Application

## Development Mode

To run the frontend in development mode:

```bash
cd frontend
npm run dev
```

Or if using yarn:
```bash
cd frontend
yarn dev
```

This will start the development server on http://localhost:3000

## Production Mode

To run the frontend in production mode, you first need to build the application:

```bash
cd frontend
npm run build
```

Then start the production server:
```bash
npm start
```

## Troubleshooting

### Warning about Workspace Root
If you see a warning about Next.js inferring the workspace root, this has been resolved by adding the `outputFileTracingRoot` configuration to the `next.config.js` file.

### Missing Production Build Error
The error "Could not find a production build in the '.next' directory" occurs when trying to run `npm start` without first building the application. Always run `npm run build` before `npm start`.

## Available Scripts

In the frontend directory, you can run:

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run linting