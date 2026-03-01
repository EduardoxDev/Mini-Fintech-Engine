package com.example.demo.core.domain;
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
