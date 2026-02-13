import * as fs from 'fs';
import * as path from 'path';

// Assuming we run from project root
const registryPath = path.resolve(process.cwd(), 'foundation/contracts/pipes/pipe-registry.json');
console.log(`Checking registry at: ${registryPath}`);

try {
    if (!fs.existsSync(registryPath)) {
        throw new Error(`Registry not found at: ${registryPath}`);
    }

    const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
    console.log('Registry parsed successfully.');

    for (const pipe of registry.pipes) {
        // schema_path in registry is relative to project root (e.g. "foundation/contracts/...")
        const schemaPath = path.resolve(process.cwd(), pipe.schema_path);
        if (!fs.existsSync(schemaPath)) {
            throw new Error(`Schema not found: ${schemaPath}`);
        }
        const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
        console.log(`Verified schema: ${pipe.pipe_id} at ${schemaPath}`);
    }
    console.log('UMP-0002 Validation Passed: All pipes in registry have valid schemas.');
} catch (err) {
    console.error('Validation Failed:', err);
    process.exit(1);
}
