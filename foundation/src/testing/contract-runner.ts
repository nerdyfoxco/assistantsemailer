import * as fs from 'fs';
import * as path from 'path';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const SCHEMAS_DIR = path.resolve(__dirname, '../../contracts/pipes/schemas');

export class ContractRunner {
    private ajv: Ajv;

    constructor() {
        this.ajv = new Ajv({ strict: true });
        addFormats(this.ajv);
    }

    public getSchemaPath(pipeId: string): string {
        // Basic lookup assumption: pipeId + .schema.json
        // In a real runner we'd check registry, but for UMP-0003 simplicity:
        return path.join(SCHEMAS_DIR, `${pipeId}.schema.json`);
    }

    public validate(pipeId: string, payload: unknown): { valid: boolean; errors?: any[] } {
        const schemaPath = this.getSchemaPath(pipeId);
        if (!fs.existsSync(schemaPath)) {
            throw new Error(`Schema not found for ${pipeId} at ${schemaPath}`);
        }

        const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
        const validate = this.ajv.compile(schema);
        const valid = validate(payload);

        return {
            valid,
            errors: validate.errors || undefined,
        };
    }
}
