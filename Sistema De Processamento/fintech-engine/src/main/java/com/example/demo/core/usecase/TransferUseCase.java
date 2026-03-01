package com.example.demo.core.usecase;
import com.example.demo.core.domain.Account;
import com.example.demo.core.domain.TransactionRecord;
import com.example.demo.core.domain.TransactionStatus;
import com.example.demo.core.exception.BusinessException;
import com.example.demo.core.exception.IdempotencyException;
import com.example.demo.infrastructure.persistence.AccountRepository;
import com.example.demo.infrastructure.persistence.IdempotencyKeyRepository;
import com.example.demo.infrastructure.persistence.TransactionRecordRepository;
import com.example.demo.infrastructure.persistence.IdempotencyKeyEntity;
import com.example.demo.infrastructure.outbox.OutboxEvent;
import com.example.demo.infrastructure.outbox.OutboxEventRepository;
import com.example.demo.infrastructure.integration.AntiFraudService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class TransferUseCase {
    private static final Logger log = LoggerFactory.getLogger(TransferUseCase.class);
    private final AccountRepository accountRepository;
    private final TransactionRecordRepository transactionRepository;
    private final OutboxEventRepository outboxEventRepository;
    private final IdempotencyKeyRepository idempotencyKeyRepository;
    private final AntiFraudService antiFraudService;

    public TransferUseCase(AccountRepository ar, TransactionRecordRepository tr, OutboxEventRepository or, IdempotencyKeyRepository ir, AntiFraudService afs) {
        this.accountRepository = ar;
        this.transactionRepository = tr;
        this.outboxEventRepository = or;
        this.idempotencyKeyRepository = ir;
        this.antiFraudService = afs;
    }

    @Transactional
    public TransactionRecord execute(String sourceId, String targetId, BigDecimal amount, String idempotencyKey) {
        if (idempotencyKey != null && idempotencyKeyRepository.existsById(idempotencyKey)) {
            throw new IdempotencyException("Transaction already processed for key: " + idempotencyKey);
        }

        if (antiFraudService.isFraud(sourceId, targetId, amount)) {
            throw new BusinessException("Transaction rejected by anti-fraud policy");
        }

        Account source = accountRepository.findByIdForUpdate(sourceId).orElseThrow(() -> new BusinessException("Source acc not found"));
        Account target = accountRepository.findByIdForUpdate(targetId).orElseThrow(() -> new BusinessException("Target acc not found"));

        source.debit(amount);
        target.credit(amount);

        accountRepository.save(source);
        accountRepository.save(target);

        TransactionRecord record = new TransactionRecord();
        record.setId(UUID.randomUUID().toString());
        record.setSourceAccountId(sourceId);
        record.setTargetAccountId(targetId);
        record.setAmount(amount);
        record.setIdempotencyKey(idempotencyKey);
        record.setTimestamp(LocalDateTime.now());
        record.setStatus(TransactionStatus.SUCCESS);
        transactionRepository.save(record);

        OutboxEvent event = new OutboxEvent();
        event.setId(UUID.randomUUID().toString());
        event.setAggregateType("Transaction");
        event.setAggregateId(record.getId());
        event.setType("TransferCompleted");
        event.setPayload("{\"id\":\""+record.getId()+"\"}");
        event.setCreatedAt(LocalDateTime.now());
        event.setProcessed(false);
        outboxEventRepository.save(event);

        if (idempotencyKey != null) {
            IdempotencyKeyEntity entity = new IdempotencyKeyEntity();
            entity.setKeyName(idempotencyKey);
            entity.setCreatedAt(LocalDateTime.now());
            idempotencyKeyRepository.save(entity);
        }

        return record;
    }
}
