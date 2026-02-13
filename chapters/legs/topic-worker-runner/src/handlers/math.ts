import { StepHandler, StepContext } from '../executor/types';

export class MathHandler implements StepHandler {
    public type = 'math.add';

    public async handle(inputs: Record<string, unknown>, context: StepContext): Promise<Record<string, unknown>> {
        const a = inputs['a'];
        const b = inputs['b'];

        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error(`MathHandler requires inputs 'a' and 'b' to be numbers. Got: a=${typeof a}, b=${typeof b}`);
        }

        const result = a + b;
        console.log(`[MathHandler] ${a} + ${b} = ${result} (Step: ${context.step_id})`);

        return { result };
    }
}
