package com.example.demo.infrastructure.integration;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;

@Service

public class AntiFraudService {
    private static final Logger log = LoggerFactory.getLogger(AntiFraudService.class);

    @CircuitBreaker(name = "antiFraudService", fallbackMethod = "fallbackFraudCheck")
    public boolean isFraud(String sourceId, String targetId, BigDecimal amount) {
        // Simulating third-party call
        if (amount.compareTo(new BigDecimal("10000")) > 0) {
            log.warn("High amount detected, potential fraud");
            return true;
        }
        return false;
    }

    public boolean fallbackFraudCheck(String sourceId, String targetId, BigDecimal amount, Throwable t) {
        log.error("Anti-Fraud system is down. Applying fallback policies. Assume NOT fraud for amounts < 1000, else TRUE", t);
        return amount.compareTo(new BigDecimal("1000")) >= 0;
    }
}
