package com.example.demo.core.exception;
public class IdempotencyException extends RuntimeException {
    public IdempotencyException(String message) { super(message); }
}
