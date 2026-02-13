import { StepHandler, StepContext } from './types';

export class WorkerDispatcher {
    private handlers = new Map<string, StepHandler>();

    public register(handler: StepHandler): void {
        if (this.handlers.has(handler.type)) {
            console.warn(`[Dispatcher] Overwriting handler for type: ${handler.type}`);
        }
        this.handlers.set(handler.type, handler);
    }

    public async dispatch(
        stepType: string,
        inputs: Record<string, unknown>,
        context: StepContext
    ): Promise<Record<string, unknown>> {
        const handler = this.handlers.get(stepType);
        if (!handler) {
            throw new Error(`No handler registered for step type: ${stepType}`);
        }

        try {
            console.log(`[Dispatcher] Executing ${stepType} for step ${context.step_id}`);
            return await handler.handle(inputs, context);
        } catch (err: any) {
            console.error(`[Dispatcher] Error executing ${stepType}:`, err);
            throw err;
        }
    }
}
