package com.example.demo.infrastructure.persistence;
import com.example.demo.core.domain.TransactionRecord;
import org.springframework.data.jpa.repository.JpaRepository;
public interface TransactionRecordRepository extends JpaRepository<TransactionRecord, String> {}
