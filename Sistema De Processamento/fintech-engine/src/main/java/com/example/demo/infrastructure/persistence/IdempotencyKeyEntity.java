package com.example.demo.infrastructure.persistence;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import java.time.LocalDateTime;

@Entity
public class IdempotencyKeyEntity {
    @Id 
    private String keyName;
    private LocalDateTime createdAt;
    
    public IdempotencyKeyEntity() {}
    
    public String getKeyName() { return keyName; }
    public void setKeyName(String keyName) { this.keyName = keyName; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
