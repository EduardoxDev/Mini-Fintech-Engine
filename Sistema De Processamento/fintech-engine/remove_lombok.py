import os
import glob

base_dir = "c:/Users/Purple/Downloads/Sistema De Processamento/fintech-engine/src/main/java/com/example/demo"
test_dir = "c:/Users/Purple/Downloads/Sistema De Processamento/fintech-engine/src/test/java/com/example/demo"

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. pom.xml remove lombok
pom_file = "c:/Users/Purple/Downloads/Sistema De Processamento/fintech-engine/pom.xml"
with open(pom_file, "r", encoding="utf-8") as f:
    pom = f.read()

lombok_lines = """
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
			<optional>true</optional>
		</dependency>
"""
lombok_plugin_lines = """
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<configuration>
					<annotationProcessorPaths>
						<path>
							<groupId>org.projectlombok</groupId>
							<artifactId>lombok</artifactId>
							<version>1.18.30</version>
						</path>
					</annotationProcessorPaths>
				</configuration>
			</plugin>
"""
pom = pom.replace(lombok_lines, "")
pom = pom.replace(lombok_plugin_lines, "")
write_file(pom_file, pom)

# 2. Account.java
write_file(f"{base_dir}/core/domain/Account.java", """package com.example.demo.core.domain;
import jakarta.persistence.*;
import java.math.BigDecimal;
import com.example.demo.core.exception.BusinessException;

@Entity
public class Account {
    @Id
    private String id;
    private String name;
    private BigDecimal balance;
    
    @Version
    private Long version;

    public Account() {}
    public Account(String id, String name, BigDecimal balance, Long version) {
        this.id = id; this.name = name; this.balance = balance; this.version = version;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public BigDecimal getBalance() { return balance; }
    public void setBalance(BigDecimal balance) { this.balance = balance; }
    public Long getVersion() { return version; }
    public void setVersion(Long version) { this.version = version; }

    public void debit(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) throw new BusinessException("Amount must be positive");
        if (balance.compareTo(amount) < 0) throw new BusinessException("Insufficient funds");
        balance = balance.subtract(amount);
    }

    public void credit(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) throw new BusinessException("Amount must be positive");
        balance = balance.add(amount);
    }
}
""")

# 3. TransactionRecord.java
write_file(f"{base_dir}/core/domain/TransactionRecord.java", """package com.example.demo.core.domain;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
public class TransactionRecord {
    @Id
    private String id;
    private String sourceAccountId;
    private String targetAccountId;
    private BigDecimal amount;
    private String idempotencyKey;
    private LocalDateTime timestamp;
    @Enumerated(EnumType.STRING)
    private TransactionStatus status;

    public TransactionRecord() {}

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getSourceAccountId() { return sourceAccountId; }
    public void setSourceAccountId(String sourceAccountId) { this.sourceAccountId = sourceAccountId; }
    public String getTargetAccountId() { return targetAccountId; }
    public void setTargetAccountId(String targetAccountId) { this.targetAccountId = targetAccountId; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
    public String getIdempotencyKey() { return idempotencyKey; }
    public void setIdempotencyKey(String idempotencyKey) { this.idempotencyKey = idempotencyKey; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
    public TransactionStatus getStatus() { return status; }
    public void setStatus(TransactionStatus status) { this.status = status; }
}
""")

# 4. OutboxEvent.java
write_file(f"{base_dir}/infrastructure/outbox/OutboxEvent.java", """package com.example.demo.infrastructure.outbox;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class OutboxEvent {
    @Id
    private String id;
    private String aggregateType;
    private String aggregateId;
    private String type;
    @Column(columnDefinition = "TEXT")
    private String payload;
    private LocalDateTime createdAt;
    private boolean processed;

    public OutboxEvent() {}

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getAggregateType() { return aggregateType; }
    public void setAggregateType(String aggregateType) { this.aggregateType = aggregateType; }
    public String getAggregateId() { return aggregateId; }
    public void setAggregateId(String aggregateId) { this.aggregateId = aggregateId; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getPayload() { return payload; }
    public void setPayload(String payload) { this.payload = payload; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public boolean isProcessed() { return processed; }
    public void setProcessed(boolean processed) { this.processed = processed; }
}
""")

# 5. IdempotencyKeyRepository.java
write_file(f"{base_dir}/infrastructure/persistence/IdempotencyKeyRepository.java", """package com.example.demo.infrastructure.persistence;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import org.springframework.data.jpa.repository.JpaRepository;
import java.time.LocalDateTime;

@Entity
public class IdempotencyKeyEntity {
    @Id private String keyName;
    private LocalDateTime createdAt;
    
    public IdempotencyKeyEntity() {}
    public String getKeyName() { return keyName; }
    public void setKeyName(String keyName) { this.keyName = keyName; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}

public interface IdempotencyKeyRepository extends JpaRepository<IdempotencyKeyEntity, String> {}
""")

# 6. TransferRequest.java
write_file(f"{base_dir}/presentation/rest/dto/TransferRequest.java", """package com.example.demo.presentation.rest.dto;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public class TransferRequest {
    @NotBlank
    private String sourceId;
    @NotBlank
    private String targetId;
    @NotNull
    @DecimalMin("0.01")
    private BigDecimal amount;

    public String getSourceId() { return sourceId; }
    public void setSourceId(String sourceId) { this.sourceId = sourceId; }
    public String getTargetId() { return targetId; }
    public void setTargetId(String targetId) { this.targetId = targetId; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
}
""")

# 7. UseCase to remove builders
write_file(f"{base_dir}/core/usecase/TransferUseCase.java", """package com.example.demo.core.usecase;
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
        event.setPayload("{\\"id\\":\\""+record.getId()+"\\"}");
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
""")

# 8. TransferController and AccountController remove lombok
write_file(f"{base_dir}/presentation/rest/TransferController.java", """package com.example.demo.presentation.rest;
import com.example.demo.core.usecase.TransferUseCase;
import com.example.demo.presentation.rest.dto.TransferRequest;
import com.example.demo.core.domain.TransactionRecord;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/transfers")
public class TransferController {
    private final TransferUseCase transferUseCase;
    public TransferController(TransferUseCase tu) { this.transferUseCase = tu; }

    @PostMapping
    public ResponseEntity<TransactionRecord> transfer(
            @Valid @RequestBody TransferRequest request,
            @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey) {
        TransactionRecord record = transferUseCase.execute(request.getSourceId(), request.getTargetId(), request.getAmount(), idempotencyKey);
        return ResponseEntity.ok(record);
    }
}
""")

write_file(f"{base_dir}/presentation/rest/AccountController.java", """package com.example.demo.presentation.rest;
import com.example.demo.core.domain.Account;
import com.example.demo.infrastructure.persistence.AccountRepository;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/accounts")
public class AccountController {
    private final AccountRepository accountRepository;
    public AccountController(AccountRepository ar) { this.accountRepository = ar; }

    @PostMapping
    public Account create(@RequestBody Account account) {
        if (account.getId() == null) account.setId(UUID.randomUUID().toString());
        return accountRepository.save(account);
    }

    @GetMapping
    public List<Account> list() {
        return accountRepository.findAll();
    }
}
""")

print("Removed Lombok and injected Java standards.")
