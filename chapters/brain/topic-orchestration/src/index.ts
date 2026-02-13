import { startServer } from './server';

async function main() {
    const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;

    const server = await startServer({ port });
    console.log(`topic-orchestration listening on ${port}`);

    // Handle shutdown signals
    process.on('SIGTERM', async () => {
        await server.close();
        process.exit(0);
    });
}

if (require.main === module) {
    main().catch(console.error);
}
