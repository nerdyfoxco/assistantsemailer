export enum ErrorCode {
    INTERNAL_ERROR = 'INTERNAL_ERROR',
    VALIDATION_ERROR = 'VALIDATION_ERROR',
    NOT_FOUND = 'NOT_FOUND',
    UNAUTHORIZED = 'UNAUTHORIZED',
    DEPENDENCY_FAILURE = 'DEPENDENCY_FAILURE'
}

export interface ErrorDetails {
    message: string;
    code: ErrorCode;
    correlationId?: string;
    cause?: unknown;
}

export class BaseError extends Error {
    public readonly code: ErrorCode;
    public readonly correlationId?: string;

    constructor(details: ErrorDetails) {
        super(details.message);
        this.name = this.constructor.name;
        this.code = details.code;
        this.correlationId = details.correlationId;

        // Maintain prototype chain
        Object.setPrototypeOf(this, new.target.prototype);
    }

    public toJSON() {
        return {
            name: this.name,
            message: this.message,
            code: this.code,
            correlationId: this.correlationId
        };
    }
}
