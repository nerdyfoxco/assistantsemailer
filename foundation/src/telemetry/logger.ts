export interface LogEntry {
    level: 'info' | 'warn' | 'error' | 'debug';
    message: string;
    context?: Record<string, unknown>;
    timestamp: string;
}

export interface Logger {
    info(message: string, context?: Record<string, unknown>): void;
    warn(message: string, context?: Record<string, unknown>): void;
    error(message: string, context?: Record<string, unknown>): void;
    debug(message: string, context?: Record<string, unknown>): void;
}

export class ConsoleLogger implements Logger {
    private log(level: LogEntry['level'], message: string, context?: Record<string, unknown>) {
        const entry: LogEntry = {
            level,
            message,
            context,
            timestamp: new Date().toISOString()
        };
        console.log(JSON.stringify(entry));
    }

    public info(message: string, context?: Record<string, unknown>) { this.log('info', message, context); }
    public warn(message: string, context?: Record<string, unknown>) { this.log('warn', message, context); }
    public error(message: string, context?: Record<string, unknown>) { this.log('error', message, context); }
    public debug(message: string, context?: Record<string, unknown>) { this.log('debug', message, context); }
}
