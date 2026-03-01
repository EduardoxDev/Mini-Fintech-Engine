package com.example.demo.presentation.rest;
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
