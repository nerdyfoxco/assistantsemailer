import { startServer } from './server';

async function main() {
    const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3001; // Default to 3001 for legs

    const server = await startServer({ port });
    console.log(`legs-worker-runner listening on ${port}`);

    process.on('SIGTERM', async () => {
        await server.close();
        process.exit(0);
    });
}

if (require.main === module) {
    main().catch(console.error);
}
