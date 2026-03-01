package com.example.demo.core.usecase;

import com.example.demo.core.domain.Account;
import com.example.demo.core.domain.TransactionRecord;
import com.example.demo.core.exception.BusinessException;
import com.example.demo.infrastructure.integration.AntiFraudService;
import com.example.demo.infrastructure.outbox.OutboxEventRepository;
import com.example.demo.infrastructure.persistence.AccountRepository;
import com.example.demo.infrastructure.persistence.IdempotencyKeyRepository;
import com.example.demo.infrastructure.persistence.TransactionRecordRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class TransferUseCaseTest {

    @Mock private AccountRepository accountRepository;
    @Mock private TransactionRecordRepository transactionRepository;
    @Mock private OutboxEventRepository outboxEventRepository;
    @Mock private IdempotencyKeyRepository idempotencyKeyRepository;
    @Mock private AntiFraudService antiFraudService;

    @InjectMocks
    private TransferUseCase transferUseCase;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void execute_successfulTransfer() {
        // Arrange
        Account src = new Account(); src.setId("acc-1"); src.setBalance(new BigDecimal("100"));
        Account tgt = new Account(); tgt.setId("acc-2"); tgt.setBalance(new BigDecimal("50"));
        
        when(idempotencyKeyRepository.existsById("key-123")).thenReturn(false);
        when(antiFraudService.isFraud(anyString(), anyString(), any())).thenReturn(false);
        when(accountRepository.findByIdForUpdate("acc-1")).thenReturn(Optional.of(src));
        when(accountRepository.findByIdForUpdate("acc-2")).thenReturn(Optional.of(tgt));

        // Act
        TransactionRecord result = transferUseCase.execute("acc-1", "acc-2", new BigDecimal("30"), "key-123");

        // Assert
        assertNotNull(result);
        assertEquals(new BigDecimal("70"), src.getBalance());
        assertEquals(new BigDecimal("80"), tgt.getBalance());
        verify(transactionRepository).save(any());
        verify(outboxEventRepository).save(any());
    }

    @Test
    void execute_fraudDetected_throwsBusinessException() {
        when(antiFraudService.isFraud(anyString(), anyString(), any())).thenReturn(true);
        assertThrows(BusinessException.class, () -> transferUseCase.execute("acc-1", "acc-2", new BigDecimal("10000"), null));
    }
}
